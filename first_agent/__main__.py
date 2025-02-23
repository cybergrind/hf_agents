import logging
from pathlib import Path

import yaml
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, OpenAIServerModel, load_tool

from first_agent.context_tools import (
    get_context_size,
    get_from_persistent_memory,
    get_step,
    list_steps,
    log_global_memory,
    modify_step,
    persist_in_memory,
    remove_step,
    set_context_agent,
)
from first_agent.Gradio_UI import GradioUI
from first_agent.tools.final_answer import FinalAnswerTool
from first_agent.tools.visit_webpage import VisitWebpageTool
from tools.editor import get_file_contents, list_directory_contents, write_content_to_file
from tools.testing import run_tests

PROMPTS_FILE = Path(__file__).parent / 'prompts.yaml'
MODEL_ID = 'Qwen/Qwen2.5-Coder-32B-Instruct'
# MODEL_ID = 'google/gemma-2-2b-it'

log = logging.getLogger('first_agent')

FULL_CONTEXT_LOG = Path('full_context_log.txt')


final_answer = FinalAnswerTool()
visit_webpage = VisitWebpageTool()
model = HfApiModel(
    max_tokens=2096,
    temperature=0.5,
    model_id=MODEL_ID,
    custom_role_conversions=None,
)

model = OpenAIServerModel(model_id='gpt-3.5-turbo', api_base='http://localhost:5000/v1', api_key='local_key')


# Import tool from Hub
image_generation_tool = load_tool('agents-course/text-to-image', trust_remote_code=True)

with PROMPTS_FILE.open('r') as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[
        final_answer,
        visit_webpage,
        DuckDuckGoSearchTool(),
        list_steps,
        get_step,
        modify_step,
        remove_step,
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
        'tools',
        'yaml',
    ],
)
set_context_agent(agent)


GradioUI(agent).launch()
