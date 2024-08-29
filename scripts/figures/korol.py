from .. import const
from . import void


class Korol:
    def __init__(self, place, color):
        self.name = 'король'
        self.first = True
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = const.COLORS[self.color]
        self.figure = const.FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, const.COLORS[self.color], self.first

    def __str__(self):
        return self.figure

    def can_move(self, board, info=False):
        ways = set()  # Множество с ходами на пустые клетки
        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0 or not (self.place[0] + i in range(8) and self.place[1] + j in range(8)):
                    continue
                place = board[self.place[0] + i][self.place[1] + j]
                if const.DEBUG and info:
                    print(f'{place} - y:{i} x:{j}')
                if type(place) is void.Void:
                    ways.add((self.place[0] + i, self.place[1] + j))
                elif place.color != self.color:
                    kills.add((self.place[0] + i, self.place[1] + j))
                else:
                    friends.add((self.place[0] + i, self.place[1] + j))

        if const.DEBUG and info:
            print(*self.information())
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
        self.first = False if not checking else self.first
