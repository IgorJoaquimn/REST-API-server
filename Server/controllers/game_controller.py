from flask import Blueprint, jsonify, request

game_controller = Blueprint('game_controller', __name__)

@game_controller.route('/api/game/<int:id>', methods=['GET'])
def get_game(id):
    return jsonify({"message": "Game not found"}), 404
