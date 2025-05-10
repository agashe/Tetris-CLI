import os
import time
import random
from util import *
from input import *

ROWS       = 40
COLS       = 20
FRAME_RATE = 300/1000

CH_V_WALL = '|'
CH_H_WALL = '-'
CH_CORNER = '+'
CH_PLAYER = '*'
CH_BLOCK  = '#'
CH_SPACE  = ' '

map    = []
player = Tetromino(4, int(COLS / 2))
score  = 0
level  = 0

tetrominos = {
    'I': [Block(0, 0), Block(1, 0), Block(2, 0), Block(3, 0)],
    'O': [Block(0, 0), Block(0, 1), Block(1, 0), Block(1, 1)],
    'S': [Block(0, 0), Block(0, 1), Block(1, 0), Block(1, -1)],
    'Z': [Block(0, 0), Block(0, -1), Block(1, 0), Block(1, 1)],
    'T': [Block(0, 0), Block(0, 1), Block(0, -1), Block(1, 0)],
    'L': [Block(0, 0), Block(1, 0), Block(2, 0), Block(2, 1)],
    'J': [Block(0, 0), Block(1, 0), Block(2, 0), Block(2, -1)],
}

def generate_tetromino():
    player.id = random.choice('IOSZTLJ')
    player.update(tetrominos[player.id])
    player.rotation = 0
    draw_player(CH_PLAYER)

def is_safe(y, x):
    return not (x < 0 or x > COLS - 2 or y > ROWS - 2 or 
        map[y][x] in [CH_BLOCK, CH_V_WALL, CH_H_WALL])

def init():
    for i in range(ROWS):
        map.append([' ' for j in range(COLS)])
    
    for i in range(ROWS):
        for j in range(COLS):
            if i == 0 or i == ROWS - 1:
                map[i][j] = CH_H_WALL
            elif j == 0 or j == COLS - 1:
                map[i][j] = CH_V_WALL

    # corners
    map[0][0] = CH_CORNER
    map[0][COLS - 1] = CH_CORNER
    map[ROWS - 1][0] = CH_CORNER
    map[ROWS - 1][COLS - 1] = CH_CORNER

def clear():
    os.system('clear')       

def sleep():
    time.sleep(FRAME_RATE)

def draw():
    for i in range(ROWS):
        for j in range(COLS):
            print(map[i][j], end='')
        print()

def draw_player(char):
    for i in range(4):
        map[player.blocks[i].y][player.blocks[i].x] = char

def update():
    collision = False

    draw_player(CH_SPACE)
    player.update([Block(1, 0) for i in range(4)])

    for i in range(4):
        if not is_safe(player.blocks[i].y, player.blocks[i].x):
            collision = True
            break

    if collision:
        player.update([Block(-1, 0) for i in range(4)])

        draw_player(CH_BLOCK)
        check_lines()

        if not check_lose():
            player.reset(1, int(COLS / 2))
            generate_tetromino()
    else:
        draw_player(CH_PLAYER)

def move(direction):
    collision = False
    step = 1 if direction == 'right' else -1

    draw_player(CH_SPACE)
    player.update([Block(0, step) for i in range(4)])

    for i in range(4):
        if not is_safe(player.blocks[i].y, player.blocks[i].x):
            collision = True
            break

    if collision:
        player.update([Block(0, step * -1) for i in range(4)])
        draw_player(CH_PLAYER)

def rotate():
    collision = False

    if player.blocks[0].y < 3:
        return
    
    draw_player(CH_SPACE)

    player.rotate()

    for i in range(4):
        if not is_safe(player.blocks[i].y, player.blocks[i].x):
            collision = True
            break

    if collision:
        draw_player(CH_BLOCK)
        check_lines()

        if not check_lose():
            player.reset(1, int(COLS / 2))
            generate_tetromino()

    draw_player(CH_PLAYER)

def speed():
    # this function implement soft-lock feature
    # by increasing the move down speed from 1 to ROWS - 2
    collision = False
    step = 5

    draw_player(CH_SPACE)
    player.update([Block(step, 0) for i in range(4)])

    for i in range(4):
        if not is_safe(player.blocks[i].y, player.blocks[i].x):
            collision = True
            break

    if collision:
        player.update([Block(step * -1, 0) for i in range(4)])
        draw_player(CH_PLAYER)

def check_lose():
    return True if CH_BLOCK in map[1] else False

def check_lines():
    cleared_lines = 0

    for i in range(1, ROWS - 1):
        count = 0

        for j in range(1, COLS - 1):
            if map[i][j] == CH_BLOCK:
                count += 1

        if count == COLS - 2:
            clear_line(i)    
            move_lines(i)
            cleared_lines += 1
    
    update_score(cleared_lines)
    
def clear_line(l):
    for j in range(1, COLS - 1):
        map[l][j] = CH_SPACE

def move_lines(l):
    for line in range(l, 1, -1):
        for j in range(1, COLS - 1):
            map[line][j] = map[line - 1][j]

def update_score(cleared_lines):
    global score
    
    # scoring system is based on 2 elements :
    # 1- the current level starting from lvl 0 (which in our case is always 0)
    # 2- the number of cleared lines
    #
    # So if `n` is the level then :
    #   
    # 1 x line --> 40 * (n + 1) 	
    # 2 x line --> 100 * (n + 1) 
    # 3 x line --> 300 * (n + 1)
    # 4 x line --> 1200 * (n + 1) 
    match cleared_lines:
        case 1:
            score += 40
        case 2:
            score += 100
        case 3:
            score += 300
        case _ if cleared_lines >= 4:
            score += 1200
    

# ================ [Init Game] ================ #

init()
generate_tetromino()
input_reader = InputReader()

# ================ [Game Loop] ================ #

while True:    
    clear()
    update()
    draw()
    print(f"score: {score} \n")

    if check_lose():
        break

    draw_player(CH_PLAYER)
    sleep()

    if input_reader.check():
        key = input_reader.get()

        if key == 'q':
            break
        elif key == input_reader.ARROW_RIGHT:
            move('right')
        elif key == input_reader.ARROW_LEFT:
            move('left')
        elif key == input_reader.ARROW_UP:
            rotate()
        elif key == input_reader.ARROW_DOWN:
            speed()

# ================ [Game Over] ================ #

input_reader.stop()
print("\nYou Lose :( \n")
