import re
import asyncio
from groq import Groq
from senator import Senator
import numpy as np

import websockets

from senator_debate import SenatorDebate

# class SenatorDebate:
#     def __init__(self, agent1: str, agent2: str, agent_data, websocket, clause, clause_id):
#         pass
# 
#     async def start_debate(self):
#         await asyncio.sleep(1)
#         print("hiiiiiii")
# 
def open_bill():
    """
    Opens the bill and returns the clauses in a list.
    """

    # Open the bill
    with open('agriculture_bill.txt', 'r') as bill:
        bill_lines = bill.readlines()

        clauses = []
        clauses_html = []

        current_clause_html = ""
        current_clause = ""


        for i in range(len(bill_lines)):
            parsed_line = parse_line(bill_lines[i])
            if "SECTION" in parsed_line:
                if current_clause:
                    clauses_html.append(current_clause_html)
                    clauses.append(current_clause)
                    current_clause = ""
                current_clause_html = parsed_line
                current_clause += bill_lines[i]
            else:
                current_clause_html += parsed_line
                current_clause += bill_lines[i]

        clauses.append(current_clause)
        clauses_html.append(current_clause_html)

        for i in range(len(clauses)):
            print(clauses[i])

    return clauses_html, clauses

def parse_line(line):
    """
    Parses a line of the bill into HTML with <p> tags and correct indenting.
    """

    line = line.replace("\n", "")

    u_alpha_re = re.compile(r'\([A-Z]\)')
    num_re = re.compile(r'\([0-9]\)')

    if u_alpha_re.match(line):
        return f'<p style="padding-left: 2em" class="clause-text">{line}</p>'
    elif num_re.match(line):
        return f'<p style="padding-left: 1em" class="clause-text">{line}</p>'
    else:
        return f'<p class="clause-text">{line}</p>'

class Simulation():

    def __init__(self, clauses, websocket):
        self.client = Groq()
        self.clauses = clauses
        self.senators = []
        self.senator_names = ["boozman", "stabenow", "mcconnell", "klobuchar", "braun", "booker"]
        self.websocket = websocket

        for i, name in enumerate(self.senator_names):
            senator = Senator(i, name)
            self.senators.append(senator)

    def create_vector_query(self, clause):
        """
        Creates a vector query for a given clause.
        """

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"You will be provided a clause in a bill. Please output a string that contains relevant keywords that I can use to analyze relevant traits for the Senators' personas. Here is the clause: {clause}",
                }
            ],
            model="llama3-8b-8192",
        )

        search_str = chat_completion.choices[0].message.content

        return search_str

    def get_data(self, clause: str, senator: Senator):
        """
        Get past relevant data for a given clause and given senator.
        
        Returns:
            List for each senator's data, a 3x3 array, of 3 tweets, 3 web things, 3 voted bills.
        """

        query = self.create_vector_query(clause)

        data = [[], [], []]

        for i, label in enumerate(senator.data_labels):
            data[i] = senator.query([query], n_results=3, label=label)

        tweets, websites, votes = data

        return { "tweets": tweets, "website": websites, "voting": votes }

    def get_all_senator_data(self, clause: str) -> dict[str, dict[str, list[str]]]:
        """
        Get all senator data for a given clause.

        Returns:
            {
                "senator1_name": {
                                    "tweets": list[str],
                                    "website": list[str],
                                    "voting": list[str]
                                 }
            }
        """

        senator_data = {}

        for senator in self.senators:
            senator_data[senator.name] = self.get_data(clause, senator)

        return senator_data

    def get_senator_alignment(self, clause: str, senator_data: dict[str, list[str]]):
        """Gets a senator's alignment for a clause."""

        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"You will be provided a clause in a bill, a senator's past tweets, websites, and voted bills. Please output ONE integer from 0 to 1 that represents how aligned the senator is with the clause. Here are the senator's past tweets: {senator_data['tweets']} Here are the senator's past websites: {senator_data['website']} Here are the senator's past voted bills: {senator_data['voting']}. Here is the clause: {clause}. Output NOTHING ELSE other than the single integer representing alignment.",
                }
            ],
            model="llama3-8b-8192",
        )

        try:
            alignment = int(chat_completion.choices[0].message.content)
        except:
            alignment = 0.5
        
        return alignment

    def choose_senators(self, clause: str, senator_data: dict[str, [dict[str, list[str]]]]) -> (Senator, Senator):
        """Choose senators based on a probability distribution of most/least aligned with a clause."""

        distribution = [0.35, 0.1, 0.05, 0.05, 0.1, 0.35]

        alignments = []
        for i, senator in enumerate(self.senators):
            alignment = self.get_senator_alignment(clause, senator_data[senator.name])
            alignments.append([i, alignment])

        alignments = sorted(alignments, key=lambda x: x[1])
        ids_only = [x[0] for x in alignments]

        chosen_first = np.random.choice(ids_only, p=distribution)
        print("chosen first:", chosen_first)
        ids_only.pop(chosen_first)
        removed_probability = distribution.pop(chosen_first)
        distribution[-1] += removed_probability

        chosen_second = np.random.choice(ids_only, p=distribution)

        first_senator = self.senators[chosen_first]
        second_senator = self.senators[chosen_second]

        return first_senator, second_senator

    async def start_simulation(self):
        """Creates a simulation of the bill passing through the Senate for all clauses in an async manner."""
        

        tasks = []
        for i, clause in enumerate(self.clauses):
            all_senator_data: dict[str, dict[str, list[str]]] = self.get_all_senator_data(clause)
            first_senator, second_senator = self.choose_senators(clause, all_senator_data)

            debate_data = {
                            first_senator.name: all_senator_data[first_senator.name],
                            second_senator.name: all_senator_data[second_senator.name]
                          }

            debate = SenatorDebate(first_senator.name, second_senator.name, debate_data, self.websocket, clause, i)

            print(debate.start_debate())

            tasks.append(asyncio.create_task(debate.start_debate()))

        for i in range(len(self.senators)):
            await tasks[i]

async def main(websocket):
    clauses = open_bill()[1]

    simulation = Simulation(clauses, websocket)

    await simulation.start_simulation()

async def create_websocket():
    async with websockets.serve(main, "localhost", 8765):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(create_websocket())
