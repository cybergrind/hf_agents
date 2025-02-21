import datetime
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytz
import yaml
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool
from smolagents.memory import MemoryStep, Message
from smolagents.models import MessageRole

from first_agent.Gradio_UI import GradioUI
from first_agent.tools.final_answer import FinalAnswerTool
from first_agent.tools.visit_webpage import VisitWebpageTool
from tools.editor import get_file_contents, list_directory_contents, write_content_to_file
from tools.testing import run_tests

PROMPTS_FILE = Path(__file__).parent / 'prompts.yaml'
GLOBAL_AGENT = None
MODEL_ID = 'Qwen/Qwen2.5-Coder-32B-Instruct'
# MODEL_ID = 'google/gemma-2-2b-it'


class Fake:
    def get(self):
        return GLOBAL_AGENT


AGENT = Fake()
log = logging.getLogger('first_agent')


# Below is an example of a tool that does nothing. Amaze us with your creativity!
@tool
def list_steps() -> dict[int, str]:  # it's important to specify the return type
    # Keep this format for the tool description / args description but feel free to modify the tool
    """Tool that returns a list of previous steps.
    Ouptut:
        step_number: step_metadata
    """
    output = {}
    agent = AGENT.get()
    if agent is None:
        raise ValueError('Agent not initialized')
    for idx, memory_step in enumerate(agent.memory.steps):
        output[idx] = getattr(memory_step, 'metadata', None)
    return output


@tool
def get_step(num: int) -> (str, dict):
    """Tool for context size calculation.
    Args:
        num: A number representing the step to return.

    Output:
        str: step repsentation as string
        dict: step metadata if exists
    """
    agent = AGENT.get()
    if agent is None:
        raise ValueError('Agent not initialized')
    return str(agent.memory.steps[num]), getattr(agent.memory.steps[num], 'metadata', None)


@dataclass
class SummarizedStep(MemoryStep):
    summarized: str

    def to_messages(self, **kwargs) -> list[Message]:
        return [
            Message(
                role=MessageRole.SYSTEM,
                content=[{'type': 'text', 'text': f'[STEP_SUMMARY]:\n{self.summarized}'}],
            )
        ]


@tool
def modify_step(step_num: int, summarized: str) -> None:
    """Tool that allows to reduce context size

    Args:
        step_num: The index of the step to replace.
        summarized: A summarized version of the step
    """
    agent = AGENT.get()
    if agent is None:
        raise ValueError('Agent not initialized')
    agent.memory.steps[step_num] = SummarizedStep(summarized=summarized)


@tool
def remove_step(step_num: int) -> None:
    """Tool that allows to reduce context size by removing a step.

    Args:
        step_num: The index of the step to remove.
    """
    agent = AGENT.get()
    if agent is None:
        raise ValueError('Agent not initialized')
    agent.memory.steps.pop(step_num)


@tool
def get_context_size() -> int:
    """Tool for monitoring context size."""
    agent = AGENT.get()
    if agent is None:
        raise ValueError('Agent not initialized')
    context_as_text = ''.join([str(step.to_messages()) for step in agent.memory.steps])
    return len(context_as_text)


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        return f'The current local time in {timezone} is: {local_time}'
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {e!s}"


GLOBAL_MEMORY = {}


@tool
def persist_in_memory(key: str, value: Any) -> None:
    """Tool that stores a value in memory with a given key.

    Args:
        key: The key to store the value under.
        value: The value to store.
    """
    global GLOBAL_MEMORY
    GLOBAL_MEMORY[key] = value
    modify_step(0, f'PERSISTENT MEMORY:\n{GLOBAL_MEMORY}')


@tool
def get_from_persistent_memory(key: str) -> Any:
    """Tool that retrieves a value from memory with a given key.

    Args:
        key: The key to retrieve the value for.
    """
    global GLOBAL_MEMORY
    return GLOBAL_MEMORY.get(key, None)


FULL_CONTEXT_LOG = Path('full_context_log.txt')


@tool
def log_global_memory() -> None:
    """Tool that logs the current global memory."""
    log.info(f'GLOBAL MEMORY: {GLOBAL_MEMORY}')
    print(f'GLOBAL MEMORY: {GLOBAL_MEMORY}')
    agent = AGENT.get()
    context_as_string = ''.join([str(step.to_messages()) for step in agent.memory.steps])
    FULL_CONTEXT_LOG.write_text(context_as_string)


final_answer = FinalAnswerTool()
visit_webpage = VisitWebpageTool()
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id=MODEL_ID,
    custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool('agents-course/text-to-image', trust_remote_code=True)

with PROMPTS_FILE.open('r') as stream:
    prompt_templates = yaml.safe_load(stream)

# agent = ToolCallingAgent(
#     model=model,
#     tools=[
#         final_answer,
#         visit_webpage,
#         DuckDuckGoSearchTool(),
#         list_steps,
#         get_step,
#         modify_step,
#         # remove_step,
#         get_context_size,
#         persist_in_memory,
#         get_from_persistent_memory,
#         log_global_memory,
#     ],  # add your tools here (don't remove final_answer)
#     max_steps=20,
#     verbosity_level=1,
#     grammar=None,
#     planning_interval=None,
#     name=None,
#     description=None,
#     prompt_templates=prompt_templates,
#     # additional_authorized_imports=['requests', 're', 'json', 'bs4'],
# )
agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        visit_webpage,
        DuckDuckGoSearchTool(),
        list_steps,
        get_step,
        modify_step,
        # remove_step,
        get_context_size,
        persist_in_memory,
        get_from_persistent_memory,
        log_global_memory,
        list_directory_contents,
        get_file_contents,
        write_content_to_file,
        run_tests,
    ],  # add your tools here (don't remove final_answer)
    max_steps=20,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
    use_e2b_executor=False,
    additional_authorized_imports=[
        'requests',
        're',
        'json',
        'bs4',
        'pathlib',
        'os',
        'typing',
        'itertools',
        'pytest',
        'tools'
    ],
)
GLOBAL_AGENT = agent


GradioUI(agent).launch()
