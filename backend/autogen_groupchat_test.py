import os
os.environ["AUTOGEN_USE_DOCKER"] = "0"
import autogen
from autogen import AssistantAgent, UserProxyAgent, Agent, GroupChat
from autogen.coding import LocalCommandLineCodeExecutor
from pathlib import Path
from typing import Union, Literal

# Put your api key in the environment variable 
config_list = [{
        # Let's choose the llama 3.1 70b model
        "model": "llama3-70b-8192",
        # Put your Groq API key here or put it into the GROQ_API_KEY environment variable.
        "api_key": "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",
        # We specify the API Type as 'groq' so it uses the Groq client class
        "api_type": "groq",
    }]

llm_config = {
    "config_list": config_list,
    "cache_seed": 42  # Optional: for reproducibility
}


def custom_speaker_selection_func(
    last_speaker: Agent, 
    groupchat: GroupChat
) -> Union[Agent, Literal['auto', 'manual', 'random' 'round_robin'], None]:

    """Define a customized speaker selection function.
    A recommended way is to define a transition for each speaker in the groupchat.

    Parameters:
        - last_speaker: Agent
            The last speaker in the group chat.
        - groupchat: GroupChat
            The GroupChat object
    Return:
        Return one of the following:
        1. an `Agent` class, it must be one of the agents in the group chat.
        2. a string from ['auto', 'manual', 'random', 'round_robin'] to select a default method to use.
        3. None, which indicates the chat should be terminated.

    """
    return 'auto'


initializer = autogen.UserProxyAgent(
    name="Init",
)

boozman = autogen.AssistantAgent(
    name="boozman",
    llm_config=llm_config,
    system_message="""you are boozman, a stupid 10 year old school student, talk about how you went to school today""",
)
# executor = autogen.UserProxyAgent(
#     name="Retrieve_Action_2",
#     system_message="Executor. Execute the code written by the boozman and report the result.",
#     human_input_mode="NEVER",
#     code_execution_config={
#         "last_n_messages": 3,
#         "work_dir": "paper",
#         "use_docker": False,
#     },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
# )
stabenow = autogen.AssistantAgent(
    name="stabenow",
    llm_config=llm_config,
    system_message="""You are the stabenow. Please describe your day as a software engineer and respond to how boozmans day went, go through specifics of what boozman did today""",
)

def state_transition(last_speaker, groupchat):
    if last_speaker is initializer:
        return boozman
    elif last_speaker is boozman:
        return stabenow
    elif last_speaker is stabenow:
        return None
    else:
        return 'auto'

groupchat = autogen.GroupChat(
    agents=[initializer, boozman, stabenow],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
initializer.initiate_chat(
    manager, message="discuss how your days went today"
)