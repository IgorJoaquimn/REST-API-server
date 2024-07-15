from flask import Blueprint, jsonify, request
from services.dataloader import Dataloader


dataloader = Dataloader("db/scores.jsonl")

game_controller = Blueprint('game_controller', __name__)

# MUST FORMAT THE RESPONSE
@game_controller.route('/api/game/<int:id>', methods=['GET'])
def get_game(id):
    try:
        return jsonify(dataloader.get_id(id)), 200
    except ValueError as e:
        return jsonify([]), 404
