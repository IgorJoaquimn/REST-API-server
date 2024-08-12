from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from services.dataloader import Dataloader, build_pagination_response

import json
# Create a namespace for rank operations
api = Namespace('rank', description='Rank operations')

# This object is responsible for reading the db and processing the queries
dataloader = Dataloader("Server/db/scores.jsonl")

# Define a model for the game data with full stats
game_model = api.model('Game', {
    'game_id': fields.Integer(description='The game ID'),
    'game_stats': fields.Raw(description='Filtered game statistics'),
})

# Update the pagination model to use the new game_model
pagination_model = api.model('Pagination', {
    'ranking': fields.String(description='Type of ranking'),
    'limit': fields.Integer(description='Limit of items per page'),
    'start': fields.Integer(description='Start index for pagination'),
    'games': fields.List(fields.Nested(game_model), description='List of games with detailed stats'),
    'prev': fields.String(description='URL for the previous page'),
    'next': fields.String(description='URL for the next page')
})


# Route for ranking sunk ships
@api.route('/sunk')
@api.response(400, 'Bad Request')
class RankSunk(Resource):
    @api.doc('rank_sunk')
    @api.marshal_with(pagination_model)
    def get(self):
        '''Get ranking based on sunk ships'''
        limit = int(request.args.get('limit', 10))
        start = int(request.args.get('start', 1))

        # Requests with limit larger than 50 should return a 400 error
        if limit > 50 or start <= 0:
            api.abort(400, 'Limit must be <= 50 and start must be > 0')

        try:
            data = dataloader.get_max_sunk_games()
            # Build the response with full game data
            response = build_pagination_response(data, start, limit, ranking="sunk", url="/api/rank/sunk")
            return response, 200
        except ValueError:
            return {'message': 'Bad request'}, 400

# Route for ranking escaped ships
@api.route('/escaped')
@api.response(400, 'Bad Request')
class RankEscaped(Resource):
    @api.doc('rank_escaped')
    @api.marshal_with(pagination_model)
    def get(self):
        '''Get ranking based on escaped ships'''
        limit = int(request.args.get('limit', 10))
        start = int(request.args.get('start', 1))

        # Requests with limit larger than 50 should return a 400 error
        if limit > 50 or start <= 0:
            api.abort(400, 'Limit must be <= 50 and start must be > 0')

        try:
            data = dataloader.get_min_escaped_games()
            # Build the response with full game data
            response = build_pagination_response(data, start, limit, ranking="escaped", url="/api/rank/escaped")
            return response, 200
        except ValueError:
            return {'message': 'Not found'}, 404

