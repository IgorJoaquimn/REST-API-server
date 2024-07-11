from utils.Client import Client

c = Client()

def get_game(game_id):
    response = c.send_request("GET", f"/api/game/{game_id}")
    print("Response from server:")
    print(response)

def rank_sunk(limit=10, start=0):
    response = c.send_request("GET", f"/api/rank/sunk?limit={limit}&start={start}")
    print("Response from server:")
    print(response)

def rank_escaped(limit=10, start=0):
    response = c.send_request("GET", f"/api/rank/escaped?limit={limit}&start={start}")
    print("Response from server:")
    print(response)

if __name__ == "__main__":
    get_game(1)
    rank_sunk(5, 0)
    rank_escaped(5, 0)