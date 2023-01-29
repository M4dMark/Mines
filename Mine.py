import pygame

class Mine:
    def __init__(self, screen, position_x, position_y) -> None:
        self.screen = screen
        self.position_x = position_x
        self.position_y = position_y
        self.size = 50
        self.is_a_bomb = False
        self.status = 0
        self.rect = pygame.Rect(self.position_x, self.position_y, self.size, self.size)

    def render(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

    def is_hovering(self, mouse):
        if [self.position_x, self.position_y] in mouse:
            return True
        else:
            return False