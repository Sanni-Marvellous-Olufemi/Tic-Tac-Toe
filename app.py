from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

def create_board():
    return [["" for _ in range(3)] for _ in range(3)]

@app.route("/")
def index():
    return render_template("Frontend1")  # Only ever load the static UI here

"""
@app.route("/init", methods=["GET"])
def initialize_game():
    # Called once when frontend loads to initialize state
    session["board"] = create_board()
    session["current_player"] = "X"
    session["game_over"] = False
    session["players"] = {"X": "", "O": ""}
    session["wins"] = {"X": 0, "O": 0}
    return jsonify(success=True)

@app.route("/set_players", methods=["POST"])
def set_players():
    data = request.json
    player_x = data.get("playerX", "Player X")
    player_o = data.get("playerO", "Player O")
    session["players"] = {"X": player_x, "O": player_o}
    session["wins"] = {"X": 0, "O": 0}
    session["board"] = create_board()
    session["current_player"] = "X"
    session["game_over"] = False
    return jsonify(success=True, players=session["players"])

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    row = data.get("row")
    col = data.get("col")

    board = session.get("board", create_board())
    current_player = session.get("current_player", "X")
    game_over = session.get("game_over", False)
    players = session.get("players", {"X": "Player X", "O": "Player O"})
    wins = session.get("wins", {"X": 0, "O": 0})

    if game_over or board[row][col] != "":
        return jsonify({
            "success": False,
            "message": "Invalid move.",
            "board": board,
            "current_player": current_player,
            "game_over": game_over,
            "wins": wins
        })

    board[row][col] = current_player

    if check_winner(board, current_player):
        session["game_over"] = True
        wins[current_player] += 1
        session["wins"] = wins
        message = f"{players[current_player]} ({current_player}) wins!"
    elif is_tie(board):
        session["game_over"] = True
        message = "It's a tie!"
    else:
        current_player = "O" if current_player == "X" else "X"
        session["current_player"] = current_player
        message = f"{players[current_player]}'s ({current_player}) turn"

    session["board"] = board

    return jsonify({
        "success": True,
        "board": board,
        "message": message,
        "current_player": current_player,
        "game_over": session["game_over"],
        "wins": wins
    })

@app.route("/reset", methods=["POST"])
def reset():
    session["board"] = create_board()
    session["current_player"] = "X"
    session["game_over"] = False
    return jsonify({
        "board": session["board"],
        "message": "Game reset.",
        "current_player": "X",
        "game_over": False,
        "wins": session.get("wins", {"X": 0, "O": 0}),
        "players": session.get("players", {"X": "", "O": ""})
    })

def check_winner(board, player):
    for i in range(3):
        if all(cell == player for cell in board[i]):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
       all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_tie(board):
    return all(cell != "" for row in board for cell in row)
    """

if __name__ == "__main__":
    app.run(debug=True)
