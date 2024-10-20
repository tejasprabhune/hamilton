import os
import autogen
import json
from groq import Groq

os.environ["AUTOGEN_USE_DOCKER"] = "0"
os.environ["GROQ_API_KEY"] = "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"

client = Groq()


class SenatorDebate:

    def __init__(self, agent1, agent2, agent_data, socket, clause, clause_id):
        self.clause_id = clause_id
        self.clause = clause
        self.agent_data = agent_data
        senator_names = {
            "boozman": "John Boozman",
            "mcconnell": "Mitch McConnell",
            "stabenow": "Debbie Stabenow",
        }

        # Put your api key in the environment variable
        self.config_list = [
            {
                # Let's choose the llama 3.1 70b model
                "model": "llama3-8b-8192",
                # Put your Groq API key here or put it into the GROQ_API_KEY environment variable.
                "api_key": "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",
                # We specify the API Type as 'groq' so it uses the Groq client class
                "api_type": "groq",
            }
        ]

        self.llm_config = {
            "config_list": self.config_list,
            "cache_seed": 42,  # Optional: for reproducibility
            "max_tokens": 2048,
        }

        self.initializer = autogen.UserProxyAgent(
            name="Init",
        )

        # self.socket = socket

        self.agent1 = autogen.AssistantAgent(
            name=senator_names[agent1],
            llm_config=self.llm_config,
            system_message=f"""You are now {senator_names[agent1]}. The following information will help you embody his persona:
        Website Information: This includes details about your political platform, key initiatives, and any personal background that shapes your views. The structure is a plain string of relevant information: {'\n'.join(self.agent_data[agent1]['website'])}.
        Recent Tweets: Here are your last 50 tweets, which reflect your current thoughts, reactions to events, and engagement with constituents. The structure is a comma-separated string: tweet1, tweet2, tweet3, … Here is the string: {'\n'.join(self.agent_data[agent1]['tweets'])}.
        Past Bill Decisions: You have voted on the following bills, demonstrating your legislative priorities and positions. The structure is a comma-separated string formatted as follows: bill name: yes/no, bill name: yes/no, bill name: yes/no. here is the string/dictionary: {'\n'.join(self.agent_data[agent1]['voting'])}
        The chat manager has introduced a new bill for discussion. Your task is to engage in a thoughtful dialogue about this bill and provide suggestions for improvement. Follow these guidelines:
        Section 1: Dialogue
        Share your perspective on this bill. Do you support or oppose it? Use insights from your previous voting record, recent tweets, and website content. Respond to their arguments—agreeing or disagreeing—while staying true to the persona you've adopted.
        Section 2: Concrete Suggestions
        Identify specific parts of the clause that you believe should be revised.
        Provide detailed recommendations for changes, explaining how these adjustments would enhance the bill.
        Ensure that your responses reflect {senator_names[agent1]}'s values, priorities, and communication style as derived from the information provided.
        """,
        )

        self.agent2 = autogen.AssistantAgent(
            name=senator_names[agent2],
            llm_config=self.llm_config,
            system_message=f"""You are now {senator_names[agent2]}. The following information will help you embody his persona:
        Website Information: This includes details about your political platform, key initiatives, and any personal background that shapes your views. The structure is a plain string of relevant information: {'\n'.join(self.agent_data[agent2]['website'])}.
        Recent Tweets: Here are your last 50 tweets, which reflect your current thoughts, reactions to events, and engagement with constituents. The structure is a comma-separated string: tweet1, tweet2, tweet3, … Here is the string: {'\n'.join(self.agent_data[agent2]['tweets'])}.
        Past Bill Decisions: You have voted on the following bills, demonstrating your legislative priorities and positions. The structure is a comma-separated string formatted as follows: bill name: yes/no, bill name: yes/no, bill name: yes/no. here is the string/dictionary: {'\n'.join(self.agent_data[agent2]['voting'])}
        The chat manager has introduced a new bill for discussion. Your task is to engage in a thoughtful dialogue about this bill and provide suggestions for improvement. Follow these guidelines:
        Section 1: Dialogue
        Share your perspective on this bill. Do you support or oppose it? Use insights from your previous voting record, recent tweets, and website content. Respond to their arguments—agreeing or disagreeing—while staying true to the persona you've adopted.
        Section 2: Concrete Suggestions
        Identify specific parts of the clause that you believe should be revised.
        Provide detailed recommendations for changes, explaining how these adjustments would enhance the bill.
        Ensure that your responses reflect {senator_names[agent2]}'s values, priorities, and communication style as derived from the information provided.
        """,
        )

        self.rounds = 0

    def start_debate(self):
        def state_transition(self, last_speaker):
            if self.rounds == 6:
                return None

            self.rounds += 1
            if last_speaker is self.initializer:
                return self.agent1
            elif last_speaker is self.agent1.name:
                x = self.agent1.chat_messages
                content = list(x.values())[0][-1]["content"]

                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are tasked with revising a bill clause based on a senator's feedback. You will receive two inputs: Senator's Opinion/Changes: This includes specific opinions or suggestions for changes the senator wishes to make regarding the original clause. The structure will be a clear statement of the desired changes: {content}. Original Clause: This is the text of the original bill clause that needs to be revised: {clause}. Your output must strictly be the revised/changed clause based on the senators feedback. Do not include any additional explanations, comments, or context. Just provide the updated clause.""",
                        }
                    ],
                    model="llama3-8b-8192",
                )
                clause = chat_completion.choices[0].message.content
                print(clause)
                return self.agent2
            elif last_speaker is self.agent2.name:
                y = self.agent2.chat_messages
                contenty = list(y.values())[0][-1]["content"]
                chat_completiony = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": f"""You are tasked with revising a bill clause based on a senator's feedback. You will receive two inputs: Senator's Opinion/Changes: This includes specific opinions or suggestions for changes the senator wishes to make regarding the original clause. The structure will be a clear statement of the desired changes: {contenty}. Original Clause: This is the text of the original bill clause that needs to be revised: {clause}. Your output must strictly be the revised/changed clause based on the senators feedback. Do not include any additional explanations, comments, or context. Just provide the updated clause.""",
                        }
                    ],
                    model="llama3-8b-8192",
                )
                clause = chat_completiony.choices[0].message.content
                print(clause)
                return None
            else:
                return "auto"

        groupchat = autogen.GroupChat(
            agents=[self.initializer, self.agent1, self.agent2],
            messages=[],
            max_round=20,
            speaker_selection_method=state_transition,
        )
        manager = autogen.GroupChatManager(
            groupchat=groupchat, llm_config=self.llm_config
        )
        self.initializer.initiate_chat(
            manager,
            message=f"""this is the new bill that is to be discussed by both agents: {self.clause}""",
        )


debate = SenatorDebate(
    "boozman",
    "stabenow",
    {
        "boozman": {
            "tweets": ["example"],
            "website": ["example"],
            "voting": ["example"],
        },
        "stabenow": {
            "tweets": ["example"],
            "website": ["example"],
            "voting": ["example"],
        },
    },
    "bob",
    "Here is a sample clause about climate change. Climate change sucks.",
    3,
)
