# controllers/rank_controller.py
from flask import Blueprint, jsonify, request

rank_controller = Blueprint('rank_controller', __name__)

@rank_controller.route('/api/rank/sunk', methods=['GET'])
def rank_sunk():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 0))
    return jsonify([]), 404

@rank_controller.route('/api/rank/escaped', methods=['GET'])
def rank_escaped():
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 0))
    return jsonify([]), 404
