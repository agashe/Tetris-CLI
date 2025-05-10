def old_check_l():
    count = 0

    for i in range(1, ROWS - 1):
        for j in range(1, COLS - 1):
            if map[i][j] in [CH_BLOCK, CH_PLAYER]:
                count += 1
                break
        
        if count == ROWS - 2:
            return True

    return False


def rotate():
    if player.blocks[0].y < 4:
        return
    
    if player.id == 'O':
        return
    
    draw_player(CH_SPACE)

    if player.blocks[0].y == 0:
        for i in range(4):
            move('left')

    sin_90 = math.sin(1.5708)
    cos_90 = math.cos(1.5708)

    for i in range(1, 4):
        point_y = player.blocks[i].y - player.blocks[0].y
        point_x = player.blocks[i].x - player.blocks[0].x

        new_point_y = (point_x * sin_90) + (point_y * cos_90)
        new_point_x = (point_x * cos_90) - (point_y * sin_90)

        player.blocks[i].y = int(player.blocks[0].y + new_point_y)
        player.blocks[i].x = int(player.blocks[0].x + new_point_x)

    draw_player(CH_PLAYER)


def rotate2():
    if player.blocks[0].y < 4:
        return
    
    if player.id == 'O':
        return
    
    draw_player(CH_SPACE)

    if player.blocks[0].y == 0:
        for i in range(4):
            move('left')

    sin_90 = math.sin(1.5708)
    cos_90 = math.cos(1.5708)

    for i in range(4):
        point_y = player.blocks[i].y
        point_x = player.blocks[i].x

        player.blocks[i].y = point_x
        player.blocks[i].x = point_y

    draw_player(CH_PLAYER)