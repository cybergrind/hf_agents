import datetime
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytz
from smolagents import tool
from smolagents.memory import MemoryStep, Message, MessageRole

AGENT = None
GLOBAL_MEMORY = {}
FULL_CONTEXT_LOG = Path('full_context_log.txt')
log = logging.getLogger('context_tools')


def set_context_agent(agent):
    global AGENT
    AGENT = agent


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
def list_steps() -> dict[int, str]:
    """Tool that returns a list of previous steps.
    Ouptut:
        step_number: step_metadata
    """
    output = {}
    for idx, memory_step in enumerate(AGENT.memory.steps):
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
    return str(AGENT.memory.steps[num]), getattr(AGENT.memory.steps[num], 'metadata', None)


@tool
def modify_step(step_num: int, summarized: str) -> None:
    """Tool that allows to reduce context size

    Args:
        step_num: The index of the step to replace.
        summarized: A summarized version of the step
    """
    AGENT.memory.steps[step_num] = SummarizedStep(summarized=summarized)


@tool
def remove_step(step_num: int) -> None:
    """Tool that allows to reduce context size by removing a step.

    Args:
        step_num: The index of the step to remove.
    """
    AGENT.memory.steps.pop(step_num)


@tool
def get_context_size() -> int:
    """Tool for monitoring context size."""
    context_as_text = ''.join([str(step.to_messages()) for step in AGENT.memory.steps])
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


@tool
def log_global_memory() -> None:
    """Tool that logs the current global memory."""
    log.info(f'GLOBAL MEMORY: {GLOBAL_MEMORY}')
    print(f'GLOBAL MEMORY: {GLOBAL_MEMORY}')
    context_as_string = ''.join([str(step.to_messages()) for step in AGENT.memory.steps])
    FULL_CONTEXT_LOG.write_text(context_as_string)
