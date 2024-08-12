import sys
import csv
from collections import defaultdict
from utils.Client import Client

def get_game(c, game_id):
    response = c.send_request("GET", f"/api/game/{game_id}")
    return response

def process_performance(games):
    games_stats = defaultdict(lambda: {'count': 0, 'total_sunk_ships': 0})

    for game in games:
        auth = game['game_stats']['auth']
        sunk_ships = game['game_stats']['sunk_ships']
        games_stats[auth]['count'] += 1
        games_stats[auth]['total_sunk_ships'] += sunk_ships
    
    for auth, stats in games_stats.items():
        games_stats[auth]['average'] = stats['total_sunk_ships'] / stats['count']

    return games_stats

def get_normalized_cannons(cannons):
    count = [0] * 8
    cannons_stats = [0] * 8

    for cannon in cannons:
        row = cannon[1]
        count[row] += 1

    for i in count:
        cannons_stats[i] += 1

    normalized = ''.join(map(str, cannons_stats))

    return normalized

def process_cannons(games):
    games_stats = defaultdict(lambda: {'count': 0, 'total_escaped_ships': 0})

    for game in games:
        cannon = get_normalized_cannons(game['game_stats']['cannons'])
        escaped_ships = game['game_stats']['escaped_ships']
        games_stats[cannon]['count'] += 1
        games_stats[cannon]['total_escaped_ships'] += escaped_ships

    for cannon, stats in games_stats.items():
        games_stats[cannon]['average'] = stats['total_escaped_ships'] / stats['count']

    return games_stats

def best_performance(c, limit, analysis, path):
    games = []       
    url = f"/api/rank/{path}?limit={50}&start={1}"

    while url and (len(games) < limit):
        response = c.send_request("GET", url)
        games += response["games"]
      
        url = response["next"]
        
    games_stats = analysis(games)
    return games_stats

def write_to_csv(data, filename, type):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)

        if type == 1:
            sorted_data = sorted(data.items(), key=lambda item: item[1]['count'], reverse=True)
            for auth, metrics in sorted_data:
                writer.writerow([auth, metrics['count'], metrics['average']])
        else:
            sorted_data = sorted(data.items(), key=lambda item: item[1]['average'])
            for auth, metrics in sorted_data:
                writer.writerow([auth, metrics['average']])

def analysis(c, type, output_filename):
    if type == 1:
        result = best_performance(c, 100, process_performance, 'sunk')
        write_to_csv(result, output_filename, type)
    else:
        result = best_performance(c, 100, process_cannons, 'escaped')
        write_to_csv(result, output_filename, type)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: ./client <IP> <port> <analysis> <output>")
        sys.exit(1)

    ip = sys.argv[1]
    port = sys.argv[2]
    analysis_type = int(sys.argv[3])
    output_filename = sys.argv[4]

    c = Client(ip, port)  # Initialize Client with IP and port

    analysis(c, analysis_type, output_filename)
