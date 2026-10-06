import os

COLS = 7
ROWS = 6
CELL_SIZE = 80
HEADER_HEIGHT = 80

board = []
current_player = 1
game_over = False
winner = 0
show_load_menu = False
p1_wins = 0
p2_wins = 0

# Save current game state and scores to sketch folder
def save_game():
    global board, current_player, game_over, show_load_menu, p1_wins, p2_wins
    if game_over or show_load_menu:
        return
    board_string = ""
    for row in board:
        for cell in row:
            board_string += str(cell)
    save_data = board_string + "|" + str(current_player) + "|" + str(p1_wins) + "|" + str(p2_wins)

    save_path = sketchPath("c4_save.txt")
    with open(save_path, "w") as f:
        f.write(save_data)
    print("[System]: Game saved successfully to c4_save.txt!")

# Load saved game state and scores safely from sketch folder
def load_game():
    global board, current_player, game_over, winner, show_load_menu, p1_wins, p2_wins
    save_path = sketchPath("c4_save.txt")
    if not os.path.exists(save_path):
        show_load_menu = False
        return
    try:
        with open(save_path, "r") as f:
            save_data = f.read()
        parts = save_data.split("|")
        board_part = parts[0]
        current_player = int(parts[1])
        if len(parts) >= 4:
            p1_wins = int(parts[2])
            p2_wins = int(parts[3])
        new_board = []
        idx = 0
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                row.append(int(board_part[idx]))
                idx += 1
            new_board.append(row)
        board = new_board
        game_over = False
        winner = 0
        print("[System]: Game loaded successfully!")
    except Exception as e:
        print("[Load Error]:", e)
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
            except:
                pass
        show_load_menu = False

# Open load menu on 'L' or save on 'S' key press
def keyPressed():
    global show_load_menu
    if key == 's' or key == 'S':
        save_game()
    elif key == 'l' or key == 'L':
        if os.path.exists(sketchPath("c4_save.txt")):
            show_load_menu = True
        else:
            print("[System]: No save file found in Sketch folder.")

# Render load menu popup overlay
def draw_load_menu():
    fill(0, 0, 0, 200)
    rect(0, 0, width, height)
    fill(255)
    rect(width / 2 - 180, height / 2 - 100, 360, 200, 10)
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(18)
    text("Old save file found!\nDo you want to continue?", width / 2, height / 2 - 40)
    fill(46, 204, 113)
    rect(width / 2 - 130, height / 2 + 20, 100, 40, 5)
    fill(255)
    text("YES", width / 2 - 80, height / 2 + 40)
    fill(231, 76, 60)
    rect(width / 2 + 30, height / 2 + 20, 100, 40, 5)
    fill(255)
    text("NO", width / 2 + 80, height / 2 + 40)

# Create 1D array using recursion
def create_1d_array(length):
    if length <= 0:
        return []
    return [0] + create_1d_array(length - 1)

# Create 2D array using recursion
def create_2d_array(cols, rows):
    if rows <= 0:
        return []
    return [create_1d_array(cols)] + create_2d_array(cols, rows - 1)

# Reset board state and check for save file
def init_board():
    global board, current_player, game_over, winner, show_load_menu
    board = create_2d_array(COLS, ROWS)
    current_player = 1
    game_over = False
    winner = 0
    if os.path.exists(sketchPath("c4_save.txt")):
        show_load_menu = True
    else:
        show_load_menu = False

# Window setup
def setup():
    size(COLS * CELL_SIZE, ROWS * CELL_SIZE + HEADER_HEIGHT)
    init_board()

# Main draw loop
def draw():
    background(255)
    draw_ui()
    draw_grid_2d(0, 0)
    if show_load_menu:
        draw_load_menu()

# Draw UI header, player turn, and score
def draw_ui():
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(18)
    if not game_over:
        if current_player == 1:
            msg = "Turn: Player 1 (Black Disc)"
        else:
            msg = "Turn: Player 2 (White Disc)"
    else:
        if winner == 1:
            msg = "PLAYER 1 (BLACK) WINS! (Click to restart)"
        elif winner == 2:
            msg = "PLAYER 2 (WHITE) WINS! (Click to restart)"
        else:
            msg = "DRAW GAME! (Click to restart)"
    text(msg, width / 2.0, HEADER_HEIGHT / 2.0 - 12)
    textSize(14)
    fill(80)
    text("Score | P1 (Black): " + str(p1_wins) + " P2 (White): " + str(p2_wins), width / 2.0, HEADER_HEIGHT / 2.0 + 16)
    stroke(0)
    strokeWeight(2)
    line(0, HEADER_HEIGHT, width, HEADER_HEIGHT)

# Draw grid and discs using recursion
def draw_grid_2d(c, r):
    if r >= ROWS:
        return
    if c >= COLS:
        draw_grid_2d(0, r + 1)
        return

    x = c * CELL_SIZE
    y = r * CELL_SIZE + HEADER_HEIGHT

    noFill()
    stroke(0)
    strokeWeight(2)
    rect(x, y, CELL_SIZE, CELL_SIZE)

    cx = x + CELL_SIZE / 2.0
    cy = y + CELL_SIZE / 2.0
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

# Find lowest empty row using recursion
def find_lowest_row(col, r):
    if r < 0:
        return False
    if board[r][col] == 0:
        board[r][col] = current_player
        return True
    return find_lowest_row(col, r - 1)

# Drop disc into column
def drop_disc(col):
    if col < 0 or col >= COLS:
        return False
    return find_lowest_row(col, ROWS - 1)

# Check line of 4 discs using recursion
def check_direction(c, r, dc, dr, player, count):
    if count == 4:
        return True
    if c < 0 or c >= COLS or r < 0 or r >= ROWS:
        return False
    if board[r][c] != player:
        return False
    return check_direction(c + dc, r + dr, dc, dr, player, count + 1)

# Check win across board using recursion
def check_board_win(c, r):
    if r >= ROWS:
        return False
    if c >= COLS:
        return check_board_win(0, r + 1)
    p = board[r][c]
    if p != 0:
        if (check_direction(c, r, 1, 0, p, 0) or
            check_direction(c, r, 0, 1, p, 0) or
            check_direction(c, r, 1, 1, p, 0) or
            check_direction(c, r, 1, -1, p, 0)):
            return True
    return check_board_win(c + 1, r)

# Check if board is full using recursion
def check_full_board(c):
    if c >= COLS:
        return True
    if board[0][c] == 0:
        return False
    return check_full_board(c + 1)

# Check game over state, update scores, and remove save file
def check_game_over():
    global game_over, winner, p1_wins, p2_wins
    if check_board_win(0, 0):
        game_over = True
        winner = current_player
        if winner == 1:
            p1_wins += 1
        elif winner == 2:
            p2_wins += 1
    elif check_full_board(0):
        game_over = True
        winner = 3

    # Clean up save file when match finishes so starting new match won't prompt popup
    if game_over:
        save_path = sketchPath("c4_save.txt")
        if os.path.exists(save_path):
            try:
                os.remove(save_path)
            except:
                pass

# Handle mouse presses for popup buttons and gameplay
def mousePressed():
    global current_player, show_load_menu
    if show_load_menu:
        # Click YES
        if (width / 2 - 130 <= mouseX <= width / 2 - 30) and (height / 2 + 20 <= mouseY <= height / 2 + 60):
            show_load_menu = False
            load_game()
            return
        # Click NO
        elif (width / 2 + 30 <= mouseX <= width / 2 + 130) and (height / 2 + 20 <= mouseY <= height / 2 + 60):
            show_load_menu = False
            save_path = sketchPath("c4_save.txt")
            if os.path.exists(save_path):
                try:
                    os.remove(save_path)
                except:
                    pass
            print("[System]: Loading canceled. Old save deleted, starting a new game.")
            return
        return
    if game_over:
        init_board()
        return
    if mouseY > HEADER_HEIGHT:
        col = mouseX // CELL_SIZE
        if drop_disc(col):
            check_game_over()
            if not game_over:
                if current_player == 1:
                    current_player = 2
                else:
                    current_player = 1
