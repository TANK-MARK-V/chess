from .. import const
from . import void


class Peshka:
    def __init__(self, place, color):
        self.name = 'пешка'
        self.first = True
        self.danger = True
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = const.COLORS[self.color]
        self.figure = const.FIGURES[self.name][self.color]
        self.walk = 1 if self.color else -1

    def information(self):
        return self.name.capitalize(), self.figure, self.place, const.COLORS[self.color], self.walk, self.first

    def __str__(self):
        return self.figure

    def can_move(self, board, info=False):
        ways = set()  # Множество с ходами на пустые клетки
        if self.place[0] not in (0, 7) and type(board[self.place[0] + self.walk][self.place[1]]) is void.Void:
            ways.add((self.place[0] + self.walk, self.place[1]))
            if self.first and type(board[self.place[0] + self.walk * 2][self.place[1]]) is void.Void:
                ways.add((self.place[0] + self.walk * 2, self.place[1]))

        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета
        if self.place[1] and self.place[0] not in (0, 7):
            place = board[self.place[0] + self.walk][self.place[1] - 1]
            if type(place) is not void.Void:
                if self.color != place.color:
                    kills.add((self.place[0] + self.walk, self.place[1] - 1))
                else:
                    friends.add((self.place[0] + self.walk, self.place[1] - 1))
        if self.place[1] - 7 and self.place[0] not in (0, 7):
            place = board[self.place[0] + self.walk][self.place[1] + 1]
            if type(place) is not void.Void:
                if self.color != place.color:
                    kills.add((self.place[0] + self.walk, self.place[1] + 1))
                else:
                    friends.add((self.place[0] + self.walk, self.place[1] + 1))

        if const.DEBUG and info:
            print(*self.information())
            print(f'Ходит - {const.make_normal(ways)}\n'
                  f'Убивает - {const.make_normal(kills)}\n'
                  f'Прикрывает - {const.make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
        self.danger = False if not checking and not self.first else self.danger
        self.first = False if not checking else self.first

