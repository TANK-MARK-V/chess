import pygame
from ..const import WIDTH, CELL


class Again:
    def __init__(self):

        self.image = pygame.font.Font(None, CELL).render("Играть снова", True, pygame.Color('black'))
        self.coord_x = (WIDTH - self.image.get_width()) // 2
        self.coord_y = CELL * 6

    def check_coords(self, coords):
        return self.coord_x <= coords[0] <= self.coord_x + self.image.get_width() and \
            self.coord_y <= coords[1] <= self.coord_y + self.image.get_height()
