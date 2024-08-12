import json

class Dataloader:
    '''
    This class is responsible for:
        * dealing with the IO in the file that the data is stored
        * processing the querys created by the controllers
            * get_id()
            * get_max_sunk_games()
            * get_min_escaped_games()
    
    At the bottom of this file there is the pagination code
    '''
    def __init__(self,file_path='Server/db/scores.jsonl'):
        self.file_path = file_path
        self.data = self.read_jsonl(file_path)
    

    def clean_game(self,game):
        # This function is responsible by take only the desired information to display in the api
        # For instance, the data tstamp_auth_start is not a important column for the client
        # But the game id is, so this function filters it 
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
                            'auth',
                            'cannons'
                        ]
        

        # Selecting only the stats_columns from the game and putting them in another dict
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

    def order_by(self,data,f):
        # This second order function expects a list and a function to work
        # The function can be, Min, Max, etc
        # After that, the corresponding value is filtered in the data list
        # For instance, if f = max(), the code will filter all games that also are the max in that stat
        if not data: raise ValueError("Data not loaded.")

        data.sort(key=f)
        data = [self.clean_game(i) for i in data]
        return data

    def get_max_sunk_games(self):
        if not self.data: raise ValueError("Data not loaded.")

        f = lambda x: -1*x["sunk_ships"]
        return self.order_by(self.data,f)
    
    def get_min_escaped_games(self):
        if not self.data: raise ValueError("Data not loaded.")

        f = lambda x: x["escaped_ships"]
        return self.order_by(self.data,f)


def pagination(data,start,limit):
    '''
        Pagination is necessary whenever the amount of data to send in a response grows very large. 
        The idea is that the server will respond with a "page" of results. 
        A response should contain (up to) limit entries starting by the entry number given in start. 

        For example, a request may ask for the top 10 games with the highest number of sunk ships
          The response should contain: 
            (1) a ranking entry with the value sunnk to specify the type of response, 
            (2) the limit used in the request, 
            (3) the start index, 
            (4) the list of games, and URLs for the previous and next page of results in the ranking:
    '''
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