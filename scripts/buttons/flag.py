from ..const import WIDTH, HEIGHT, MESSAGES, load_image


class Flag:
    def __init__(self):
        self.image = load_image(another='flag')
        self.coord_x = WIDTH - MESSAGES + 10
        self.coord_y = HEIGHT - 10 - self.image.get_height()

    def check_coords(self, coords):
        return self.coord_x <= coords[0] <= self.coord_x + self.image.get_width() and \
            self.coord_y <= coords[1] <= self.coord_y + self.image.get_height()
