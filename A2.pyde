COLS = 7
ROWS = 6
CELL_SIZE = 80
HEADER_HEIGHT = 80
board = []
current_player = 1
game_over = False
winner = 0

def create_1d_array(length):
    if length <= 0:
        return []
    return [0] + create_1d_array(length - 1)

def create_2d_array(cols, rows):
    if rows <= 0:
        return []
    return [create_1d_array(cols)] + create_2d_array(cols, rows - 1)

def init_board():
    global board, current_player, game_over, winner
    board = create_2d_array(COLS, ROWS)
    current_player = 1
    game_over = False
    winner = 0

def setup():
    size(COLS * CELL_SIZE, ROWS * CELL_SIZE + HEADER_HEIGHT)
    init_board()

def draw():
    background(255)
    draw_ui()
    draw_grid_2d(0, 0)

def draw_ui():
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(20)

    if not game_over:
        if current_player == 1:
            text("Turn: Player 1 (Black Disc)", width / 2, HEADER_HEIGHT / 2)
        else:
            text("Turn: Player 2 (White Disc)", width / 2, HEADER_HEIGHT / 2)
    else:
        if winner == 1:
            text("PLAYER 1 (BLACK) WINS! (Click to restart)", width / 2, HEADER_HEIGHT / 2)
        elif winner == 2:
            text("PLAYER 2 (WHITE) WINS! (Click to restart)", width / 2, HEADER_HEIGHT / 2)
        else:
            text("DRAW GAME! (Click to restart)", width / 2, HEADER_HEIGHT / 2)

    stroke(0)
    strokeWeight(2)
    line(0, HEADER_HEIGHT, width, HEADER_HEIGHT)

def draw_grid_2d(c, r):
    if r >= ROWS:
        return
    if c >= COLS:
        draw_grid_2d(0, r + 1)
        return

    x = c * CELL_SIZE
    y = r * CELL_SIZE + HEADER_HEIGHT

    stroke(0)
    strokeWeight(2)
    line(x, y, x + CELL_SIZE, y)
    line(x, y + CELL_SIZE, x + CELL_SIZE, y + CELL_SIZE)
    line(x, y, x, y + CELL_SIZE)
    line(x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE)

    cx = x + CELL_SIZE / 2
    cy = y + CELL_SIZE / 2
    disc_size = CELL_SIZE * 0.75

    val = board[r][c]
    if val == 0:
        stroke(200)
        strokeWeight(1)
        fill(255)
        ellipse(cx, cy, disc_size, disc_size)
    elif val == 1:
        stroke(0)
        strokeWeight(2)
        fill(0)
        ellipse(cx, cy, disc_size, disc_size)
    elif val == 2:
        stroke(0)
        strokeWeight(3)
        fill(255)
        ellipse(cx, cy, disc_size, disc_size)

    draw_grid_2d(c + 1, r)
