from pathlib import Path

class Senator:
    def __init__(self, id, name):
        self.id = id
        self.name = name

        self.data_root = Path("../senator_data/")

        data_labels = ["tweet", "website", "voting"]
        data = [[], [], []]

        for i, label in enumerate(data_labels[:2]):
            with open(self.data_root / f"{label}_data" / f"{self.name}.txt", "r") as f:
                for line in f:
                    if line != "\n":
                        data[i].append(line)

        with open(self.data_root / "voting_data" / f"{self.name}.json", "r") as f:
            data[2] = f.read()

        self.tweets, self.websites, self.votes = data
        
        print(self.tweets)

    def __str__(self):
        return f"Senator {self.name} (ID: {self.id})"
    
if __name__ == "__main__":
    senator = Senator(0, "boozman")
    print(senator)
