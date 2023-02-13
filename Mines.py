import pygame
import sys
import random
from Mine import Mine

pygame.init()
window = pygame.display.set_mode((800, 800))
board = [[None for y in range(800 // 50)] for x in range(800 // 50)]
font = pygame.font.SysFont('monospace', 32)

def create_board():
    for x in range(len(board)):
        for y in range(len(board[x])):
            board[x][y] = Mine(window, x * 50, y * 50)

def render_mines():
    for x in board:
        for mine in x:
            mine.render()

def render_lines():
    for x in range(800 // 50):
        pygame.draw.line(window, (0, 0, 0), (x * 50, 0), (x * 50, 800))
    for y in range(800 // 50):
        pygame.draw.line(window, (0, 0, 0), (0, y * 50), (800, y * 50))

def calculate_mine_indexes():
    mine_indexes = []
    for x in range(50):
        index = calculate_index()
        mine_indexes.append(check_index(index, mine_indexes))
    return mine_indexes

def calculate_index():
    mine_index = [random.randint(0, 15), random.randint(0, 15)]
    return mine_index

def check_index(index, mines):
    while index in mines:
        index = calculate_index()
    return index

mines = calculate_mine_indexes()

def assign_mine_indexes():
    for x in board:
        for rect in x:
            if [rect.position_x // 50, rect.position_y // 50] in mines:
                pygame.draw.rect(window, (255, 0 , 0), rect.rect)
                rect.is_a_bomb = True
            else:
                pygame.draw.rect(window, (255, 255, 255), rect.rect)

def search_clicked_rect(mouse):
    for x in board:
        for mine in x:
            if mine.is_hovering(mouse) == True and check_if_mine(mine):
                replace_if_mine(mine) 
                calculate_mine_probability(mine)
    display_text()

def replace_if_mine(mine):
    mines.remove([mine.position_x // 50, mine.position_y // 50])
    new_mine = calculate_index()
    new_mine = check_index(new_mine, mines)
    mines.append(new_mine)
    assign_mine_indexes()
    render_lines()

def calculate_mine_probability(mine):
    mine_position_x = mine.position_x // 50
    mine_position_y = mine.position_y // 50
    board[mine_position_x + 1][mine_position_y].status += 1
    board[mine_position_x][mine_position_y + 1].status += 1
    board[mine_position_x - 1][mine_position_y].status += 1
    board[mine_position_x][mine_position_y - 1].status += 1 

def display_text():
    for x in board:
        for mine in x:
            text = font.render(str(mine.status), True, (0, 0, 0))
            window.blit(text, mine.rect.center)

def check_if_mine(mine):
    if mine.is_a_bomb == True:
        return True
    else:
        return False


def main():
    done = False
    create_board()
    render_mines()
    assign_mine_indexes()
    render_lines()
    while done is False:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                search_clicked_rect(mouse)
            pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()