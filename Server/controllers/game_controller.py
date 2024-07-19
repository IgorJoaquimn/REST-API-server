from flask import Blueprint, jsonify, request
from services.dataloader import Dataloader


#This object is responsible for readind the db and processing the querys
dataloader = Dataloader("db/scores.jsonl")

game_controller = Blueprint('game_controller', __name__)

@game_controller.route('/api/game/<int:id>', methods=['GET'])
def get_game(id):
    try:
        return jsonify(dataloader.get_id(id)), 200
    except ValueError as e:

        #This error can occur if the desired id isn't present in the db
        return jsonify([]), 404
