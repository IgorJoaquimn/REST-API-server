from flask import Flask
from flask_cors import CORS
from flask_restx import Api

# Import the namespaces from controllers
from controllers.game_controller import api as game_ns
from controllers.rank_controller import api as rank_ns

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# Initialize the Flask-RESTX API
api = Api(
    app,
    version='1.0',
    title='Game and Rank API',
    description='An API for managing games and rankings',
)

# Add namespaces to the API
api.add_namespace(game_ns, path='/api/game')
api.add_namespace(rank_ns, path='/api/rank')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
