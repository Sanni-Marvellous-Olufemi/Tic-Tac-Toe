from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

def create_board():
    return [""] * 9

@app.route("/")
def index():
    return render_template("HTML")

@app.route("/init", methods=["GET"])
def initialize_game():
    session["board"] = create_board()
    session["current_player"] = "X"
    session["game_over"] = False
    session["players"] = {"X": "Player X", "O": "Player O"}
    session["wins"] = {"X": 0, "O": 0}
    return jsonify({
        "success": True,
        "board": session["board"],
        "current_player": session["current_player"],
        "game_over": session["game_over"],
        "players": session["players"],
        "wins": session["wins"],
        "message": f"{session['players']['X']}'s Turn (X)"  # Initial turn message
    })

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
    return jsonify({
        "success": True,
        "board": session["board"],
        "current_player": session["current_player"],
        "game_over": session["game_over"],
        "players": session["players"],
        "wins": session["wins"],
        "message": f"{player_x}'s Turn (X)"
    })

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    index = data.get("index")

    board = session.get("board", create_board())
    current_player = session.get("current_player", "X")
    game_over = session.get("game_over", False)
    players = session.get("players", {"X": "Player X", "O": "Player O"})
    wins = session.get("wins", {"X": 0, "O": 0})

    if game_over or board[index] != "":
        return jsonify({
            "success": False,
            "message": "Invalid move.",
            "board": board,
            "current_player": current_player,
            "game_over": game_over,
            "wins": wins
        })

    board[index] = current_player

    if check_winner(board, current_player):
        session["game_over"] = True
        wins[current_player] += 1
        session["wins"] = wins
        message = f"{players[current_player]} Wins!"
    elif is_tie(board):
        session["game_over"] = True
        message = "It's a Tie!"
    else:
        current_player = "O" if current_player == "X" else "X"
        session["current_player"] = current_player
        message = f"{players[current_player]}'s Turn ({current_player})"

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
    players = session.get("players", {"X": "Player X", "O": "Player O"})
    return jsonify({
        "success": True,
        "board": session["board"],
        "message": f"{players['X']}'s Turn (X)",
        "current_player": "X",
        "game_over": False,
        "wins": session.get("wins", {"X": 0, "O": 0}),
        "players": players
    })

def check_winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in win_conditions)

def is_tie(board):
    return all(cell != "" for cell in board)

if __name__ == "__main__":
    app.run(debug=True)