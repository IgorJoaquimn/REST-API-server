from flask import jsonify
from flask_restx import Namespace, Resource, fields
from services.dataloader import Dataloader

# Create a namespace for game operations
api = Namespace('game', description='Game operations')

# This object is responsible for reading the db and processing the queries
dataloader = Dataloader("Server/db/scores.jsonl")

# Define a model for game data
game_model = api.model('Game', {
    'game_id': fields.Integer(description='The game ID'),
    'game_stats': fields.Raw(description='Filtered game statistics'),
})

# Route for getting a game by ID
@api.route('/<int:id>')
@api.response(404, 'Game not found')
@api.param('id', 'The game identifier')
class Game(Resource):
    @api.doc('get_game')
    @api.marshal_with(game_model)
    def get(self, id):
        '''Fetch a game given its identifier'''
        try:
            game_data = dataloader.get_id(id)
            return game_data, 200
        except ValueError:
            # This error can occur if the desired ID isn't present in the db
            return [], 404
