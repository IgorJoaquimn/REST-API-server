import json

class Dataloader:
    def __init__(self,file_path='../db/scores.jsonl'):
        self.file_path = file_path
        self.data = self.read_jsonl(file_path)
    

    def clean_game(self,game):
        new_game = {}
        new_game["game_id"] = game["id"]


        stats_columns = [
                            'escaped_ships', 
                            'last_turn', 
                            'remaining_life_on_escaped_ships', 
                            'ship_moves', 
                            'shot_received', 
                            'sunk_ships', 
                            'valid_shots', 
                        ]
        
        stats = {col: game[col] for col in stats_columns if col in game}

        new_game["game_stats"] = stats

        return new_game

    def read_jsonl(self,file_path):
        data = []
        with open(file_path, 'r') as file:
            data = [json.loads(line.strip()) for line in file]
        return data
    
    def get_id(self,id):
        if not self.data: raise ValueError("Data not loaded.")

        games = [d for d in self.data if d["id"] == id]

        if not games: raise ValueError("Invalid Id")
        return self.clean_game(games[0])

    def filter_list(self,data,f):
        if not self.data: raise ValueError("Data not loaded.")

        target = f(data)
        data = [self.data[i] for (i,stat) in enumerate(data) if stat == target ]
        data = [self.clean_game(i) for i in data]
        return data

    def get_max_sunk_games(self):
        if not self.data: raise ValueError("Data not loaded.")

        sunks = [d["sunk_ships"] for d in self.data if "sunk_ships" in d]
        return self.filter_list(sunks,max)
    
    def get_min_escaped_games(self):
        if not self.data: raise ValueError("Data not loaded.")

        escapeds = [d["escaped_ships"] for d in self.data if "escaped_ships" in d]
        return self.filter_list(escapeds,min)


def pagination(data,start,limit):
    if(limit > 50): raise ValueError("limit greater then 50")

    available_data  = data[start-1:start+limit-1]
    there_is_prev   = data[:start-1]
    there_is_next   = data[start+limit-1:]

    prev_start = None
    prev_limit = None

    next_start = None
    next_limit = None

    if(there_is_next):
        next_start = start + limit
        next_limit = min(limit, len(there_is_next)) # Confirmar com prof e giro
    
    if(there_is_prev):
        prev_start = max(1,start-limit)
        prev_limit = limit

    return available_data,(prev_start,prev_limit),(next_start,next_limit)    

def build_pagination_response(data,start,limit,ranking="sunk",url="/api/rank/sunk"):
    available_data,(prev_start,prev_limit),(next_start,next_limit)   = pagination(data,start,limit)
    response = {}
    response["ranking"] = ranking
    response["limit"] = limit
    response["start"] = start
    response["games"] = available_data

    prev_u = None
    next_u = None

    if(prev_start): prev_u = url + f"?limit={prev_limit}&start={prev_start}"
    if(next_start): next_u = url + f"?limit={next_limit}&start={next_start}"

    response["prev"] = prev_u
    response["next"] = next_u

    return response