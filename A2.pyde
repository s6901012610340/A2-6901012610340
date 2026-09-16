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
