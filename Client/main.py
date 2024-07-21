from utils.Client import Client
from collections import defaultdict

c = Client()

def get_game(game_id):
    response = c.send_request("GET", f"/api/game/{game_id}")
    print("Response from server:")
    print(response)
    return response

def rank_sunk(limit=10, start=0):
    response = c.send_request("GET", f"/api/rank/sunk?limit={limit}&start={start}")
    # print("Response from server:")
    # print(response)
    return response

def rank_escaped(limit=10, start=0):
    response = c.send_request("GET", f"/api/rank/escaped?limit={limit}&start={start}")
    # print("Response from server:")
    # print(response)
    return response

def proccess_performance(games):
    games_stats = defaultdict(lambda: {'count': 0, 'total_sunk_ships': 0})

    for game in games:
        auth = game['game_stats']['auth']
        sunk_ships = game['game_stats']['sunk_ships']
        games_stats[auth]['count'] += 1
        games_stats[auth]['total_sunk_ships'] += sunk_ships
    
    for auth, stats in games_stats.items():
        games_stats[auth]['average'] = stats['total_sunk_ships']/stats['count']
        # print(f"Auth: {auth}, Average Sunk Ships: {games_stats[auth]['average']:.2f}")

    return games_stats

def get_normalized_cannons(cannons):
    count = [0] * 8
    cannons_stats = [0] * 8

    for cannon in cannons:
        row = cannon[1]
        count[row] +=1

    for i in count:
        cannons_stats[i] +=1

    normalized = ''.join(map(str, cannons_stats))

    return normalized


def proccess_cannons(games):
    games_stats = defaultdict(lambda: {'count': 0})

    for game in games:
        cannon = get_normalized_cannons(game['game_stats']['cannons'])
        games_stats[cannon]['count']+=1

    # for auth, stats in games_stats.items():
    #     print(f"Auth: {auth}, Average Sunk Ships: {games_stats[auth]['count']:.2f}")

    return games_stats
        

def best_performance(limit):
    games = []       
    start = 1
    while(limit > 0): 
        response = rank_sunk(min(limit, 50), start)
        start +=50
        limit-=50
        games += response["games"]   

    games_stats = proccess_performance(games)
    return games_stats

def best_cannon(limit):
    games = []       
    start = 1
    while(limit > 0): 
        response = rank_escaped(min(limit, 50), start)
        start +=50
        limit-=50
        games += response["games"]   

    games_stats = proccess_cannons(games)
    return games_stats
    


if __name__ == "__main__":

    best_cannon(50)