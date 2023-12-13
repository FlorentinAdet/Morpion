from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Plateau de jeu initial
board = [['', '', ''], ['', '', ''], ['', '', '']]

@app.route('/')
def index():
    return render_template('index.html', board=board)

@app.route('/make_move', methods=['POST'])
def make_move():
    global board

    # Récupérer les données du mouvement depuis la requête AJAX
    row = int(request.form['row'])
    col = int(request.form['col'])
    player = request.form['player']

    # Vérifier si la case est libre
    if board[row][col] == '':
        board[row][col] = player

    # Vérifier s'il y a un gagnant
    winner = check_winner()
    if winner:
        return jsonify({'status': 'win', 'winner': winner})
    
    # Vérifier s'il y a un match nul
    if check_draw():
        return jsonify({'status': 'draw'})

    return jsonify({'status': 'ok', 'board': board})

def check_winner():
    # Vérifier les lignes, colonnes et diagonales
    for i in range(3):
        # Vérifier les lignes
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]

        # Vérifier les colonnes
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]

    # Vérifier les diagonales
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]

    return None

def check_draw():
    # Vérifier s'il y a une case vide
    for row in board:
        if '' in row:
            return False
    return True

if __name__ == '__main__':
    app.run(debug=True)
