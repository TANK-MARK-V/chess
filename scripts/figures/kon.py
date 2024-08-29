from .. import const
from . import void


class Kon:
    def __init__(self, place, color):
        self.name = 'конь'
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = const.COLORS[self.color]
        self.figure = const.FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, const.COLORS[self.color]

    def __str__(self):
        return self.figure

    def can_move(self, board, info=False):
        ways = set()  # Множество с ходами на пустые клетки
        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета

        one, two = (-1, 1), (-2, 2)  # Конь ходит либо вертикально (+-2, +-1) и горизонтально (+-1, +-2)
        """Вертикальные буквы Г"""
        for vert in two:
            for hor in one:
                coords = (self.place[0] + vert, self.place[1] + hor)
                if 0 <= coords[0] <= 7 and 0 <= coords[1] <= 7:
                    place = board[coords[0]][coords[1]]
                    if type(place) is void.Void:
                        ways.add(coords)
                    elif place.color != self.color:
                        kills.add(coords)
                    else:
                        friends.add(coords)

        """Горизонтальные буквы Г"""
        for vert in one:
            for hor in two:
                coords = (self.place[0] + vert, self.place[1] + hor)
                if 0 <= coords[0] <= 7 and 0 <= coords[1] <= 7:
                    place = board[coords[0]][coords[1]]
                    if type(place) is void.Void:
                        ways.add(coords)
                    elif place.color != self.color:
                        kills.add(coords)
                    else:
                        friends.add(coords)

        if const.DEBUG and info:
            print(*self.information())
            print(f'Ходит - {const.make_normal(ways)}\n'
                  f'Убивает - {const.make_normal(kills)}\n'
                  f'Прикрывает - {const.make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
