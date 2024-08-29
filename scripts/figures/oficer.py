from .. import const
from . import void


class Oficer:
    def __init__(self, place, color):
        self.name = 'офицер'
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

        moves = ((1, 1), (-1, 1), (-1, -1), (1, -1))
        for x, y in moves:
            for i in range(1, 8):
                if self.place[0] + y * i in range(8) and self.place[1] + x * i in range(8):
                    place = board[self.place[0] + y * i][self.place[1] + x * i]
                    if const.DEBUG and info:
                        print(f'{place} x:{x} y:{y} i:{i}')
                    if type(place) is void.Void:
                        ways.add((self.place[0] + y * i, self.place[1] + x * i))
                    elif place.color != self.color:
                        kills.add((self.place[0] + y * i, self.place[1] + x * i))
                        break
                    else:
                        friends.add((self.place[0] + y * i, self.place[1] + x * i))
                        break
                else:
                    break

        if const.DEBUG and info:
            print(*self.information())
            print(f'Ходит - {const.make_normal(ways)}\n'
                  f'Убивает - {const.make_normal(kills)}\n'
                  f'Прикрывает - {const.make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
