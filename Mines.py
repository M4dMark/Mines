import pygame
import sys
import random
from Mine import Mine

pygame.init()
window = pygame.display.set_mode((800, 800))
flags = 35
board = [[Mine(window, col * 50, row * 50, True) if random.randint(1, 10) == 1 else Mine(window, col * 50, row * 50, False) for col in range(16)] for row in range(16)]
font = pygame.font.SysFont('monospace', 32)

def render_mines():
    for x in board:
        for mine in x:
            mine.render()

def number_of_mines():
    number_of_mines = 0
    for row in board:
        for mine in row:
            if mine.is_a_mine:
                number_of_mines += 1
            else:
                pass
    return number_of_mines

def render_lines():
    for x in range(800 // 50):
        pygame.draw.line(window, (0, 0, 0), (x * 50, 0), (x * 50, 800))
    for y in range(800 // 50):
        pygame.draw.line(window, (0, 0, 0), (0, y * 50), (800, y * 50))

def assign_mine_indexes():
    for row in board:
        for mine in row:
            if mine.is_a_mine:
                pygame.draw.rect(window, (255, 0 , 0), mine.rect)
            else:
                pygame.draw.rect(window, (255, 255, 255), mine.rect)

def first_click(mouse):
    for row in board:
        for mine in row:
            if mine.is_hovering(mouse) and check_if_mine(mine):
                replace_if_mine(mine) 
                undercover()
    calculate_mine_probabilities()
    display_text()

def replace_if_mine(mine):
    mine.is_a_mine = False
    new_mine = [random.randint(0, 15), random.randint(0, 15)]
    board[new_mine[0]][new_mine[1]].is_a_mine = True
    assign_mine_indexes()

def calculate_mine_probabilities():
    for row in range(len(board)):
        for col in range(len(board[row])):
            mines_around = 0
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    if row + x > -1 and row + x < len(board):
                        if col + y > -1 and col + y < len(board[0]):
                            if board[row + x][col + y].is_a_mine:
                                mines_around += 1
            board[row][col].status = mines_around

def display_text():
    for x in board:
        for mine in x:
            text = font.render(str(mine.status), True, (0, 0, 0))
            window.blit(text, mine.rect.center)

def check_if_mine(mine):
    if mine.is_a_mine:
        return True
    else:
        return False

def assign_flag(mouse):
    global flags
    flags -= 1
    for row in board:
        for mine in row:
            if mine.is_marked and mine.is_hovering(mouse):
                print('Already marked this tile.')
            elif mine.is_marked is False and mine.is_hovering(mouse):
                pygame.draw.rect(window, (255, 0, 0), mine.rect)
                mine.is_marked = True

def undercover():
    pass

def check_over(mouse):
    for row in board:
        for mine in row:
            if mine.is_a_mine and mine.is_hovering(mouse):
                print('Youve clicked on a mine. Games Over!')
                pygame.quit()
                sys.exit()
            else:
                continue

def check_win():
    number_of_marked = 0
    for row in board:
        for mine in row:
            if mine.is_a_mine and mine.is_marked:
                number_of_marked += 1
                if number_of_marked == number_of_mines():
                    print('Youve won!')
    #jestli je pocet oznacenych min roven poctu celkovych min

def main():
    done = False
    click = 0
    render_mines()
    assign_mine_indexes()
    render_lines()
    while done is False:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and click < 1:
                    first_click(mouse)
                    click += 1
                elif pygame.mouse.get_pressed()[0] and click >= 1:
                    undercover()
                    check_over(mouse)
                elif pygame.mouse.get_pressed()[2]:
                    assign_flag(mouse)
                    check_win()
            pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()