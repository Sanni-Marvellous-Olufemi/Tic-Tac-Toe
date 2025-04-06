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
    if "board" not in session:
        session["board"] = create_board()
        session["current_player"] = "X"
        session["game_over"] = False
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    row = data.get("row")
    col = data.get("col")
    
    board = session.get("board", create_board())
    current_player = session.get("current_player", "X")
    game_over = session.get("game_over", False)

    if game_over or board[row][col] != "":
        return jsonify({
            "success": False,
            "message": "Invalid move.",
            "board": board,
            "current_player": current_player,
            "game_over": game_over
        })

    board[row][col] = current_player

    if check_winner(board, current_player):
        session["game_over"] = True
        message = f"Player {current_player} wins!"
    elif is_tie(board):
        session["game_over"] = True
        message = "It's a tie!"
    else:
        current_player = "O" if current_player == "X" else "X"
        message = f"Player {current_player}'s turn"
    
    session["board"] = board
    session["current_player"] = current_player

    return jsonify({
        "success": True,
        "board": board,
        "message": message,
        "game_over": session["game_over"]
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
        "game_over": False
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
    

if __name__ == "__main__":
    app.run(debug=True)
