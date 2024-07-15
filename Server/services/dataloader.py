import json

class Dataloader:
    def __init__(self,file_path='../db/scores.jsonl'):
        self.file_path = file_path
        self.data = self.read_jsonl(file_path)

    def read_jsonl(self,file_path):
        data = []
        with open(file_path, 'r') as file:
            data = [json.loads(line.strip()) for line in file]
        return data
    
    def get_id(self,id):
        if not self.data: raise ValueError("Data not loaded.")

        games = [d for d in self.data if d["id"] == id]

        if not games: raise ValueError("Invalid Id")
        return games[0]

    def filter_list(self,data,f):
        if not self.data: raise ValueError("Data not loaded.")

        target = f(data)
        data = [self.data[i] for (i,sunk) in enumerate(data) if sunk == target ]
        return data

    def get_max_sunk_games(self):
        if not self.data: raise ValueError("Data not loaded.")

        sunks = [d["sunk_ships"] for d in self.data if "sunk_ships" in d]
        return self.filter_list(sunks,max)
    
    def get_min_escaped_games(self):
        if not self.data: raise ValueError("Data not loaded.")

        escapeds = [d["escaped_ships"] for d in self.data if "escaped_ships" in d]
        return self.filter_list(escapeds,min)