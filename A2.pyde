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

def save_game():
    global board, current_player, game_over, show_load_menu
    if game_over or show_load_menu:
        return

    board_string = ""
    for row in board:
        for cell in row:
            board_string += str(cell)
            
    save_data = board_string + "|" + str(current_player)
    
    with open("c4_save.txt", "w") as f:
        f.write(save_data)
        
    print("[ระบบ]: บันทึกเกมลงในไฟล์ c4_save.txt สำเร็จแล้ว!")

def load_game():
    global board, current_player, game_over, winner, show_load_menu
    
    if not os.path.exists("c4_save.txt"):
        print("[ระบบ]: ไม่พบไฟล์เซฟเก่า เริ่มต้นเกมใหม่")
        show_load_menu = False
        return
        
    try:
        with open("c4_save.txt", "r") as f:
            save_data = f.read()
            
        board_part, turn_part = save_data.split("|")
        current_player = int(turn_part)
        game_over = False
        winner = 0
        
        new_board = []
        idx = 0
        for r in range(ROWS):
            row = []
            for c in range(COLS):
                row.append(int(board_part[idx]))
                idx += 1
            new_board.append(row)
            
        board = new_board
        print("[ระบบ]: โหลดเกมสำเร็จแล้ว!")
        
    except Exception as e:
        print("[ข้อผิดพลาด]: ไฟล์เซฟเสียหาย กำลังเริ่มเกมใหม่:", e)
        if os.path.exists("c4_save.txt"):
            os.remove("c4_save.txt")
    
    show_load_menu = False

def keyPressed():
    if key == 's' or key == 'S':
        save_game()
    elif key == 'l' or key == 'L':
        load_game()

def draw_load_menu():
    fill(0, 0, 0, 200) 
    rect(0, 0, width, height)
    
    fill(255)
    rect(width/2 - 180, height/2 - 100, 360, 200, 10)
    
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(18)
    text("Old save file found!\nDo you want to continue?", width / 2, height / 2 - 40)
    
    fill(46, 204, 113)
    rect(width/2 - 130, height/2 + 20, 100, 40, 5)
    fill(255)
    text("YES", width/2 - 80, height/2 + 40)
    
    fill(231, 76, 60)
    rect(width/2 + 30, height/2 + 20, 100, 40, 5)
    fill(255)
    text("NO", width/2 + 80, height/2 + 40)

def create_1d_array(length):
    if length <= 0:
        return []
    return [0] + create_1d_array(length - 1)

def create_2d_array(cols, rows):
    if rows <= 0:
        return []
    return [create_1d_array(cols)] + create_2d_array(cols, rows - 1)

def init_board():
    global board, current_player, game_over, winner, show_load_menu
    board = create_2d_array(COLS, ROWS)
    current_player = 1
    game_over = False
    winner = 0
    
    if os.path.exists("c4_save.txt"):
        show_load_menu = True
    else:
        show_load_menu = False

def setup():
    size(COLS * CELL_SIZE, ROWS * CELL_SIZE + HEADER_HEIGHT)
    init_board()

def draw():
    background(255)
    draw_ui()
    draw_grid_2d(0, 0)
    
    if show_load_menu:
        draw_load_menu()

def draw_ui():
    fill(0)
    textAlign(CENTER, CENTER)
    textSize(20)

    if not game_over:
        if current_player == 1:
            text("Turn: Player 1 (Black Disc)", width / 2.0, HEADER_HEIGHT / 2.0)
        else:
            text("Turn: Player 2 (White Disc)", width / 2.0, HEADER_HEIGHT / 2.0)
    else:
        if winner == 1:
            text("PLAYER 1 (BLACK) WINS! (Click to restart)", width / 2.0, HEADER_HEIGHT / 2.0)
        elif winner == 2:
            text("PLAYER 2 (WHITE) WINS! (Click to restart)", width / 2.0, HEADER_HEIGHT / 2.0)
        else:
            text("DRAW GAME! (Click to restart)", width / 2.0, HEADER_HEIGHT / 2.0)

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
