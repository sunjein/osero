import pygame
from pygame.locals import *
from pygame import gfxdraw
import sys
import copy


# 0: なし
# 1: 白
# 2: 黒

MASS_SIZE = 50
PADDING = 20

# 判定用進む道 [x,y]
DIRECTIONS = [
    [0,-1],
    [1,-1],
    [1,0],
    [1,1],
    [0,1],
    [-1,1],
    [-1,0],
    [-1,-1],
]


def bot(field, turn):
    if turn == 1:
        enemy = 2
    if turn == 2:
        enemy = 1
    best_cnt = 0
    best_pos = [0,0]
    for y in range(8):
        for x in range(8):
            clone_field = put(field, turn, x, y)
            if clone_field == False:
                continue
            color_count = 0
            for y2 in range(8):
                for x2 in range(8):
                    clone_clone_field = put(clone_field, enemy, x2, y2)
                    if clone_clone_field == False:
                        continue
                    for cnty in range(8):
                        for cntx in range(8):
                            if clone_clone_field[cnty][cntx] == turn:
                                color_count += 1

            if best_cnt < color_count:
                best_cnt = color_count
                best_pos= [x,y]
    
    return best_pos
    
                


def can_put_check(field, my_color, mouse_field_x, mouse_field_y):
    # 自分
    mouse_field_x_mass, mouse_field_y_mass = int(mouse_field_x), int(mouse_field_y)

    if not (0 <= mouse_field_x_mass <= 7):
        return False
    if not (0 <= mouse_field_y_mass <= 7):
        return False
    if field[int(mouse_field_y)][int(mouse_field_x)] != 0:
        return False

    available_directions = []

    for direction in DIRECTIONS:
        direction_x = direction[0]
        direction_y = direction[1]
        # 範囲内か確認
        if not (0 <= mouse_field_x_mass+direction_x <= 7):
            continue
        if not (0 <= mouse_field_y_mass+direction_y <= 7):
            continue
        if field[mouse_field_y_mass+direction_y][mouse_field_x_mass+direction_x] in [0,my_color]:
            continue
        available_directions.append(direction)
    
    if not available_directions:
        return False
    
    can_put_directions = []
    for direction in available_directions:
        direction_x = direction[0]
        direction_y = direction[1]
        test_x = mouse_field_x_mass+direction_x
        test_y = mouse_field_y_mass+direction_y
        finished = False
        while not finished:
            test_x += direction_x
            test_y += direction_y
            if not (0 <= test_x <= 7): #壁なら
                finished = True
            elif not (0 <= test_y <= 7): #壁なら
                finished = True
            elif field[test_y][test_x] == 0:
                finished = True
            elif field[test_y][test_x] == my_color:
                can_put_directions.append(direction)
                finished = True
    
    if not can_put_directions:
        return False
    
    return can_put_directions



def put(field, my_color, mouse_field_x, mouse_field_y):
    clone_field = copy.deepcopy(field)
    mouse_field_x_mass, mouse_field_y_mass = int(mouse_field_x), int(mouse_field_y)
    result = can_put_check(field, my_color, mouse_field_x, mouse_field_y)
    if result == False:
        return False
    can_put_directions = result
    clone_field[mouse_field_y_mass][mouse_field_x_mass] = my_color
    for direction in can_put_directions:
        direction_x = direction[0]
        direction_y = direction[1]
        put_x = mouse_field_x_mass+direction_x
        put_y = mouse_field_y_mass+direction_y
        clone_field[put_y][put_x] = my_color
        finished = False
        while not finished:
            put_x += direction_x
            put_y += direction_y
            if clone_field[put_y][put_x] == my_color:
                finished = True
            else:
                clone_field[put_y][put_x] = my_color
    
    return clone_field
 
 


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("オセロ")
    clock = pygame.time.Clock()

    click = False # 一度のみクリック判定用
    turn = 2
    cant_put_count = 0

    field = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,1,2,0,0,0],
        [0,0,0,2,1,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
    ]



    font = pygame.font.SysFont(None, 50)

    while True:
        screen.fill((255,255,255))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_field_x = (mouse_x-PADDING)/MASS_SIZE
        mouse_field_y = (mouse_y-PADDING)/MASS_SIZE

        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0]:
            if click == False:
                click = True
                # クリック時、一度だけ行われる処理
                if PADDING <= mouse_x and PADDING <= mouse_y:
                    field_data = put(field, turn, mouse_field_x, mouse_field_y)
                    if field_data != False:
                        field = copy.deepcopy(field_data)
                        if turn == 1:
                            turn = 2
                        elif turn == 2:
                            pos = bot(field, 1)
                            result2 = put(field, 1, pos[0], pos[1])
                            print(pos)
                            if result2 != False:
                                field = copy.deepcopy(result2)
                            turn = 2
        else:
            click = False
        
        cant_put = True
        cnt_black = 0
        cnt_white = 0

        for y in range(8):
            for x in range(8):
                color = (0,200,0)
                result = can_put_check(field, turn, x, y) # TODO:mouse field x渡すんじゃないからなんとかする
                if result != False:
                    cant_put = False
                    color = (0,240,0)
                if PADDING <= mouse_x and PADDING <= mouse_y:
                    if int(mouse_field_x) == x and int(mouse_field_y) == y:
                        color = (0,250,0)
                pygame.draw.rect(screen,color,Rect(PADDING+MASS_SIZE*x,PADDING+MASS_SIZE*y,MASS_SIZE,MASS_SIZE))
                pygame.draw.rect(screen,(0,0,0),Rect(PADDING+MASS_SIZE*x-2,PADDING+MASS_SIZE*y-2,MASS_SIZE+2,MASS_SIZE+2),2)

                if field[y][x] == 0:
                    pass

                elif field[y][x] == 1:
                    cnt_white += 1
                    # 2つでアンチエイリアスされた円の描画
                    color = (255,255,255)
                    gfxdraw.filled_circle(screen, int(PADDING+MASS_SIZE*x+MASS_SIZE*0.5-1), int(PADDING+MASS_SIZE*y+MASS_SIZE*0.5-1), int(MASS_SIZE*0.4), color)
                    gfxdraw.aacircle(screen, int(PADDING+MASS_SIZE*x+MASS_SIZE*0.5-1), int(PADDING+MASS_SIZE*y+MASS_SIZE*0.5-1), int(MASS_SIZE*0.4), color)

                elif field[y][x] == 2:
                    cnt_black += 1
                    color = (0,0,0)
                    gfxdraw.filled_circle(screen, int(PADDING+MASS_SIZE*x+MASS_SIZE*0.5-1), int(PADDING+MASS_SIZE*y+MASS_SIZE*0.5-1), int(MASS_SIZE*0.4), color)
                    gfxdraw.aacircle(screen, int(PADDING+MASS_SIZE*x+MASS_SIZE*0.5-1), int(PADDING+MASS_SIZE*y+MASS_SIZE*0.5-1), int(MASS_SIZE*0.4), color)
        
        if turn == 1:
            turn_text = font.render("Turn: White", True, (0,0,0))
            color = (255,255,255)
        if turn == 2:
            turn_text = font.render("Turn: Black", True, (0,0,0))
            color = (0,0,0)

        # 座標は相対的なのじゃなくて適当
        gfxdraw.filled_circle(screen, 40, 455, int(MASS_SIZE*0.4), color)
        gfxdraw.aacircle(screen, 40, 455, int(MASS_SIZE*0.4), (0,0,0))
        screen.blit(turn_text, (PADDING+MASS_SIZE,PADDING+MASS_SIZE*8+20))

        cnt_text = font.render(f"Black:{cnt_black} / White:{cnt_white}", True, (0,0,0))
        screen.blit(cnt_text, (PADDING+MASS_SIZE,PADDING+MASS_SIZE*8+70))

        if cant_put == True:
            cant_put_count += 1
            if turn == 1:
                turn = 2
            elif turn == 2:
                turn = 1
        else:
            cant_put_count = 0
        
        if 1 < cant_put_count:
            print("ゲーム終了!")
            break

        pygame.display.update()
        clock.tick(60)

        # イベント処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
 


if __name__ == "__main__":
    main()