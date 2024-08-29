from ..const import WIDTH, HEIGHT, load_image


class Bug:
    def __init__(self):
        self.image = load_image(another='bug')
        self.coord_x = WIDTH - 10 - self.image.get_width()
        self.coord_y = HEIGHT - 10 - self.image.get_height()

    def check_coords(self, coords):
        return self.coord_x <= coords[0] <= self.coord_x + self.image.get_width() and \
            self.coord_y <= coords[1] <= self.coord_y + self.image.get_height()
