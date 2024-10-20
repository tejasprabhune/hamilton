from pathlib import Path
import json

from chromadb.utils.embedding_functions.onnx_mini_lm_l6_v2 import ONNXMiniLM_L6_V2

import chromadb

class Senator:
    def __init__(self, id, name):
        self.ef = ONNXMiniLM_L6_V2(preferred_providers=["CPUExecutionProvider"])

        self.id = id
        self.name = name

        self.data_root = Path("../senator_data/")

        self.data_labels = ["tweet", "website", "voting"]
        self.data = [[], [], []]

        for i, label in enumerate(self.data_labels[:2]):
            with open(self.data_root / f"{label}_data" / f"{self.name}.txt", "r") as f:
                for line in f:
                    if line != "\n":
                        self.data[i].append(line)

        with open(self.data_root / "voting_data" / f"{self.name}.json", "r") as f:
            self.data[2] = json.load(f)

        self.tweets, self.websites, self.votes = self.data

    def __str__(self):
        return f"Senator {self.name} (ID: {self.id})"

    def create_db(self):
        self.collections = []
        client = chromadb.PersistentClient(path=f"db/{self.name}")

        for i, label in enumerate(self.data_labels[:2]):
            print(f"Creating collection for {label} data...")
            collection = client.get_or_create_collection(label, embedding_function=self.ef)
            collection.add(documents=self.data[i], ids=[str(i) for i in range(len(self.data[i]))])

            self.collections.append(collection)

        print("Creating collection for voting data...")
        voting_collection = client.get_or_create_collection("voting", embedding_function=self.ef)
        voting_collection.add(documents=list(self.votes.keys()),
                              metadatas=[{"key": vote} for vote in list(self.votes.values())], 
                              ids=[str(i) for i in range(len(self.votes))])
        self.collections.append(voting_collection)

        self.tweet_collection, self.website_collection, self.vote_collection = self.collections

        print(f"Database for {self.name} created.")
    
if __name__ == "__main__":
    
    senator_names = ["boozman", "stabenow"]
    senators = []

    for i, senator_name in enumerate(senator_names):
        senator = Senator(i, senator_name)
        senators.append(senator)
        senator.create_db()

    print("Testing query \"Israel\":")
    result = senators[0].tweet_collection.query(query_texts=["Israel"], n_results=3)
    
    print(result)
