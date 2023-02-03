import pygame
import sys
import random
from Mine import Mine

pygame.init()
window = pygame.display.set_mode((800, 800))
board = [[None for y in range(800 // 50)] for x in range(800 // 50)]

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
print(mines)

def assign_mine_indexes():
    for mine in mines:
        pygame.draw.rect(window, (255, 0 , 0), board[mine[0]][mine[1]].rect)

def main():
    done = False
    create_board()
    render_mines()
    render_lines()
    assign_mine_indexes()
    while done is False:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass     
            pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()