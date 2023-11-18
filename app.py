import autogen
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")


config_list = [
    {
        'model': 'gpt-4-1106-preview',
        'api_key': OPENAI_KEY
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="Expert webscraper and data analyst for retail product information"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=15,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task = """
Find me a good deal on a GPU capable of running local large langauge models (LLms) with atleast 30b parameters and no quantization. Give me a graph of the price of the gpu over time from atleast 3 sources and dating back atleast 6 months.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)
