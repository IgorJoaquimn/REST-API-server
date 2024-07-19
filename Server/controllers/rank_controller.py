# controllers/rank_controller.py
from flask import Blueprint, jsonify, request
from services.dataloader import Dataloader, build_pagination_response

dataloader = Dataloader("db/scores.jsonl")

rank_controller = Blueprint('rank_controller', __name__)

@rank_controller.route('/api/rank/sunk', methods=['GET'])
def rank_sunk():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 1))

    #Requests with limit larger than 50 should be answered with an HTTP 400 (Bad Request) error code.
    if(limit > 50): return jsonify([]), 400
    if(start <= 0): return jsonify([]), 400

    try:
        data = dataloader.get_max_sunk_games()
        response = build_pagination_response(data,start,limit,ranking="sunk",url="/api/rank/sunk")
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify([]), 400

@rank_controller.route('/api/rank/escaped', methods=['GET'])
def rank_escaped():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 1))

    #Requests with limit larger than 50 should be answered with an HTTP 400 (Bad Request) error code.
    if(limit > 50): return jsonify([]), 400
    if(start <= 0): return jsonify([]), 400

    try:
        data = dataloader.get_min_escaped_games()
        response = build_pagination_response(data,start,limit,ranking="sunk",url="/api/rank/escaped")
        return jsonify(response), 200
    
    except ValueError as e:
        return jsonify([]), 404
