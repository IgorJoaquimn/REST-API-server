# controllers/rank_controller.py
from flask import Blueprint, jsonify, request
from services.dataloader import Dataloader

dataloader = Dataloader("db/scores.jsonl")

rank_controller = Blueprint('rank_controller', __name__)


# MUST IMPLEMENT PAGINATION
# MUST FORMAT THE RESPONSE
@rank_controller.route('/api/rank/sunk', methods=['GET'])
def rank_sunk():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 0))
    try:
        return jsonify(dataloader.get_max_sunk_games()), 200
    except ValueError as e:
        return jsonify([]), 404

# MUST IMPLEMENT PAGINATION
# MUST FORMAT THE RESPONSE
@rank_controller.route('/api/rank/escaped', methods=['GET'])
def rank_escaped():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 0))
    try:
        return jsonify(dataloader.get_min_escaped_games()), 200
    except ValueError as e:
        return jsonify([]), 404
