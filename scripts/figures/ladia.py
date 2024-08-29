from .. import const
from . import void


class Ladia:
    def __init__(self, place, color):
        self.name = 'ладья'
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

        """Проверка ходов по горизонтали"""
        for i in range(self.place[1] - 1, -1, -1):  # Влево от фигуры
            place = board[self.place[0]][i]
            if const.DEBUG and info:
                print(f'{place} - влево')
            if type(place) is void.Void:
                ways.add((self.place[0], i))
            elif place.color != self.color:
                kills.add((self.place[0], i))
                break
            else:
                friends.add((self.place[0], i))
                break

        for i in range(self.place[1] + 1, 8):  # Направо от фигуры
            place = board[self.place[0]][i]
            if const.DEBUG and info:
                print(f'{place} - вправо')
            if type(place) is void.Void:
                ways.add((self.place[0], i))
            elif place.color != self.color:
                kills.add((self.place[0], i))
                break
            else:
                friends.add((self.place[0], i))
                break

        for i in range(self.place[0] - 1, -1, -1):  # Вверх от фиугры
            place = board[i][self.place[1]]
            if const.DEBUG and info:
                print(f'{place} - вверх')
            if type(place) is void.Void:
                ways.add((i, self.place[1]))
            elif place.color != self.color:
                kills.add((i, self.place[1]))
                break
            else:
                friends.add((i, self.place[1]))
                break

        for i in range(self.place[0] + 1, 8):  # Вниз от фигуры
            place = board[i][self.place[1]]
            if const.DEBUG and info:
                print(f'{place} - вниз')
            if type(place) is void.Void:
                ways.add((i, self.place[1]))
            elif place.color != self.color:
                kills.add((i, self.place[1]))
                break
            else:
                friends.add((i, self.place[1]))
                break

        if const.DEBUG and info:
            print(*self.information())
            print(f'Ходит - {const.make_normal(ways)}\n'
                  f'Убивает - {const.make_normal(kills)}\n'
                  f'Прикрывает - {const.make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
        self.first = False if not checking else self.first
