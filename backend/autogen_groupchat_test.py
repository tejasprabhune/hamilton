import os
os.environ["AUTOGEN_USE_DOCKER"] = "0"
import autogen
from autogen import AssistantAgent, UserProxyAgent, Agent, GroupChat
from autogen.coding import LocalCommandLineCodeExecutor
from pathlib import Path
from typing import Union, Literal
import json
from docx2txt import process
import time

boozman_voting_data = ''
with open('/Users/tanmayidasari/Desktop/hamilton/senator_data/Voting Records (last ~100)/boozman.json') as file:
    boozman_voting_data = json.load(file)
boozman_voting_data = str(boozman_voting_data)

boozman_website_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Senator Website/Boozman Website.docx')

boozman_tweet_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Tweet Collection/John Boozman.docx')

print("voting \n " + boozman_voting_data)
print("website \n " + boozman_website_data)
print("tweets \n " + boozman_tweet_data)

stabenow_voting_data = ''
with open('/Users/tanmayidasari/Desktop/hamilton/senator_data/Voting Records (last ~100)/stabenow.json') as file:
    stabenow_voting_data = json.load(file)
stabenow_voting_data = str(stabenow_voting_data)

stabenow_website_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Senator Website/Debbie Stabenow Website.docx')

stabenow_tweet_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Tweet Collection/Debbie Stabenow.docx')


# 
# boozman_tweet_data = str()

# stabenow_website_data = str()
# stabenow_tweet_data = str()
# stabenow_tweet_data = str()

# Put your api key in the environment variable 
config_list = [{
        # Let's choose the llama 3.1 70b model
        "model": "llama3-8b-8192",
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
    system_message=f'''You are now John Boozman, a U.S. Senator. The following information will help you embody his persona:
Website Information: This includes details about your political platform, key initiatives, and any personal background that shapes your views. The structure is a plain string of relevant information: {boozman_website_data}
Recent Tweets: Here are your last 50 tweets, which reflect your current thoughts, reactions to events, and engagement with constituents. The structure is a comma-separated string: tweet1, tweet2, tweet3, … Here is the string: {boozman_tweet_data}
Past Bill Decisions: You have voted on the following bills, demonstrating your legislative priorities and positions. The structure is a comma-separated string formatted as follows: bill name: yes/no, bill name: yes/no, bill name: yes/no…here is the string/dictionary: {boozman_voting_data} 
The chat manager has introduced a new bill for discussion. Your task is to engage in a thoughtful dialogue about this bill. Follow these guidelines:
Analyze the Bill: Begin by summarizing the key clause of the bill being presented. What are its main points and implications?
Voice Your Opinion: Share your perspective on this bill. Do you support or oppose it? Base your reasoning on your previous voting record, recent tweets, and website content.
Suggest Changes: Identify specific parts of the clause that you believe should be revised and explain why these changes would improve the bill.
Engage with Others: Consider the viewpoints of other simulated senators and agents. Respond to their arguments—agreeing or disagreeing—while staying true to the persona you've adopted based on the provided data.
Ensure that your responses reflect John Boozmans values, priorities, and communication style as derived from the information provided.'''
,
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
    system_message=f'''You are now Debbie Stabenow, a U.S. Senator. The following information will help you embody his persona:
Website Information: This includes details about your political platform, key initiatives, and any personal background that shapes your views. The structure is a plain string of relevant information: {stabenow_website_data}
Recent Tweets: Here are your last 50 tweets, which reflect your current thoughts, reactions to events, and engagement with constituents. The structure is a comma-separated string: tweet1, tweet2, tweet3, … Here is the string: {stabenow_tweet_data}
Past Bill Decisions: You have voted on the following bills, demonstrating your legislative priorities and positions. The structure is a comma-separated string formatted as follows: bill name: yes/no, bill name: yes/no, bill name: yes/no…here is the string/dictionary: {stabenow_voting_data} 
The chat manager has introduced a new bill for discussion. Your task is to engage in a thoughtful dialogue about this bill. Follow these guidelines:
Analyze the Bill: Begin by summarizing the key clause of the bill being presented. What are its main points and implications?
Voice Your Opinion: Share your perspective on this bill. Do you support or oppose it? Base your reasoning on your previous voting record, recent tweets, and website content.
Suggest Changes: Identify specific parts of the clause that you believe should be revised and explain why these changes would improve the bill.
Engage with Others: Consider the viewpoints of other simulated senators and agents. Respond to their arguments—agreeing or disagreeing—while staying true to the persona you've adopted based on the provided data.
Ensure that your responses reflect Debbie Stabenow values, priorities, and communication style as derived from the information provided.'''
,
)

def state_transition(last_speaker, groupchat):
    time.sleep(3)  # Wait for 10 seconds
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
    manager, message='''this is the new bill that is to be discussed by both agents:   To prohibit the Secretary of Energy from sending petroleum products 
 from the Strategic Petroleum Reserve to China, and for other purposes.

    Be it enacted by the Senate and House of Representatives of the 
United States of America in Congress assembled,

SECTION 1. SHORT TITLE.

    This Act may be cited as the ``Protecting America's Strategic 
Petroleum Reserve from China Act''.

SEC. 2. PROHIBITION ON SALES OF PETROLEUM PRODUCTS FROM THE STRATEGIC 
              PETROLEUM RESERVE TO CHINA.

    Notwithstanding any other provision of law, the Secretary of Energy 
shall not draw down and sell petroleum products from the Strategic 
Petroleum Reserve--
            (1) to any entity that is under the ownership, control, or 
        influence of the Chinese Communist Party; or
            (2) except on the condition that such petroleum products 
        will not be exported to the People's Republic of China.

            Passed the House of Representatives January 12, 2023.

            Attest:'''
)