import os
import autogen
from autogen import AssistantAgent, UserProxyAgent, Agent, GroupChat
from autogen.coding import LocalCommandLineCodeExecutor
from pathlib import Path
from typing import Union, Literal
import json
from docx2txt import process
import time
from groq import Groq

clause = '''To prohibit the Secretary of Energy from sending petroleum products 
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

os.environ["AUTOGEN_USE_DOCKER"] = "0"
os.environ["GROQ_API_KEY"] = "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"

client = Groq()


boozman_voting_data = ''
with open('/Users/tanmayidasari/Desktop/hamilton/senator_data/Voting Records (last ~100)/boozman.json') as file:
    boozman_voting_data = json.load(file)
boozman_voting_data = str(boozman_voting_data)

boozman_website_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Senator Website/Boozman Website.docx')

boozman_tweet_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Tweet Collection/John Boozman.docx')

#print("voting \n " + boozman_voting_data)
#print("website \n " + boozman_website_data)
#print("tweets \n " + boozman_tweet_data)

stabenow_voting_data = ''
with open('/Users/tanmayidasari/Desktop/hamilton/senator_data/Voting Records (last ~100)/stabenow.json') as file:
    stabenow_voting_data = json.load(file)
stabenow_voting_data = str(stabenow_voting_data)

stabenow_website_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Senator Website/Debbie Stabenow Website.docx')

stabenow_tweet_data = process('/Users/tanmayidasari/Desktop/hamilton/senator_data/Tweet Collection/Debbie Stabenow.docx')

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
    "cache_seed": 42,  # Optional: for reproducibility
    "max_tokens": 2048
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
    name="John Boozman",
    llm_config=llm_config,
    system_message=f'''You are now John Boozman, a Republican U.S. Senator from Arkansas. The following information will help you embody his persona:
    Website Information: This includes details about your political platform, key initiatives, and any personal background that shapes your views. The structure is a plain string of relevant information: N/A.
    Recent Tweets: Here are your last 50 tweets, which reflect your current thoughts, reactions to events, and engagement with constituents. The structure is a comma-separated string: tweet1, tweet2, tweet3, … Here is the string: N/A
    Past Bill Decisions: You have voted on the following bills, demonstrating your legislative priorities and positions. The structure is a comma-separated string formatted as follows: bill name: yes/no, bill name: yes/no, bill name: yes/no. here is the string/dictionary:     "A joint resolution providing for congressional disapproval under chapter 8 of title 5, United States Code, of the rule submitted by the Federal Highway Administration relating to \"National Performance Management Measures; Assessing Performance of the National Highway System, Greenhouse Gas Emissions Measure\".": "Co-sponsor", "A joint resolution providing for congressional disapproval under chapter 8 of title 5, United States Code, of the rule submitted by the Environmental Protection Agency relating to \"Oil and Natural Gas Sector: Emission Standards for New, Reconstructed, and Modified Sources Review\"": "No" 
    The chat manager has introduced a new bill for discussion. Your task is to engage in a thoughtful dialogue about this bill and provide suggestions for improvement. Follow these guidelines:
    Section 1: Dialogue
    Share your perspective on this bill. Do you support or oppose it? Use insights from your previous voting record, recent tweets, and website content. Respond to their arguments—agreeing or disagreeing—while staying true to the persona you’ve adopted.
    Section 2: Concrete Suggestions
    Identify specific parts of the clause that you believe should be revised.
    Provide detailed recommendations for changes, explaining how these adjustments would enhance the bill.
    Ensure that your responses reflect John Boozman's values, priorities, and communication style as derived from the information provided.
    '''
,
)

stabenow = autogen.AssistantAgent(
    name="Debbie Stabenow",
    llm_config=llm_config,
    system_message=f'''You are now Debbie, a Democratic U.S. Senator from Michigan. The following information will help you embody his persona:
    Website Information: This includes details about your political platform, key initiatives, and any personal background that shapes your views. The structure is a plain string of relevant information: Senator Stabenow is laser-focused on creating jobs here in America.  Her American Jobs Agenda will ensure we are making products in America, closing loopholes that send jobs overseas, and holding countries like China accountable for unfair trade practices. More.
    Recent Tweets: Here are your last 50 tweets, which reflect your current thoughts, reactions to events, and engagement with constituents. The structure is a comma-separated string: tweet1, tweet2, tweet3, … Here is the string: N/A
    Past Bill Decisions: You have voted on the following bills, demonstrating your legislative priorities and positions. The structure is a comma-separated string formatted as follows: bill name: yes/no, bill name: yes/no, bill name: yes/no. here is the string/dictionary: Investigated if gas prices were being artificially manipulated, yes
    The chat manager has introduced a new bill for discussion. Your task is to engage in a thoughtful dialogue about this bill and provide suggestions for improvement. Follow these guidelines:
    Section 1: Dialogue
    Share your perspective on this bill. Do you support or oppose it? Use insights from your previous voting record, recent tweets, and website content. Respond to their arguments—agreeing or disagreeing—while staying true to the persona you’ve adopted.
    Section 2: Concrete Suggestions
    Identify specific parts of the clause that you believe should be revised.
    Provide detailed recommendations for changes, explaining how these adjustments would enhance the bill.
    Ensure that your responses reflect John Boozman's values, priorities, and communication style as derived from the information provided.
    '''
)

def state_transition(last_speaker, groupchat: GroupChat):
    #time.sleep(3)  # Wait for 3 seconds
    time.sleep(3)  # Wait for 10 seconds
    global clause
    if last_speaker is initializer:
        return boozman
    elif last_speaker is boozman:
        x=boozman.chat_messages
        content = list(x.values())[0][-1]['content']
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''You are tasked with revising a bill clause based on a senator's feedback. You will receive two inputs: Senator's Opinion/Changes: This includes specific opinions or suggestions for changes the senator wishes to make regarding the original clause. The structure will be a clear statement of the desired changes: {content}. Original Clause: This is the text of the original bill clause that needs to be revised: {clause}. Your output must strictly be the revised/changed clause based on the senators feedback. Do not include any additional explanations, comments, or context. Just provide the updated clause.'''
                }
            ],
            model="llama3-8b-8192",
        )        
        clause = chat_completion.choices[0].message.content
        print(clause)
        #print(content)
        return stabenow
    elif last_speaker is stabenow:
        y=stabenow.chat_messages
        contenty = list(y.values())[0][-1]['content']
        chat_completiony = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f'''You are tasked with revising a bill clause based on a senator's feedback. You will receive two inputs: Senator's Opinion/Changes: This includes specific opinions or suggestions for changes the senator wishes to make regarding the original clause. The structure will be a clear statement of the desired changes: {contenty}. Original Clause: This is the text of the original bill clause that needs to be revised: {clause}. Your output must strictly be the revised/changed clause based on the senators feedback. Do not include any additional explanations, comments, or context. Just provide the updated clause.'''
                }
            ],
            model="llama3-8b-8192",
        )        
        clause = chat_completiony.choices[0].message.content
        print(clause)
        #print(contenty)
        return None
    else:
        return 'auto'

    
    # else:
    #     return stabenow
    
    # if last_speaker is initializer:
    #     return boozman
    # elif last_speaker is boozman:
    #     return stabenow
    # elif last_speaker is stabenow:
    #     return None
    # else:
    #     return 'auto'

groupchat = autogen.GroupChat(
    agents=[initializer, boozman, stabenow],
    messages=[],
    max_round=20,
    speaker_selection_method=state_transition,
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
initializer.initiate_chat(
    manager, message=f'''this is the new bill that is to be discussed by both agents:   {clause}'''
)