# server.py
from flask import Flask

# Each one of the routes is managed by a specific controller
from controllers.game_controller import game_controller # /api/game/
from controllers.rank_controller import rank_controller # /api/rank/

app = Flask(__name__)

app.register_blueprint(game_controller)
app.register_blueprint(rank_controller)

if __name__ == '__main__':
    app.run(debug=True)
