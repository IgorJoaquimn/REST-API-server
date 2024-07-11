# server.py
from flask import Flask
from controllers.game_controller import game_controller
from controllers.rank_controller import rank_controller

app = Flask(__name__)

app.register_blueprint(game_controller)
app.register_blueprint(rank_controller)

if __name__ == '__main__':
    app.run(debug=True)
