from .. import const
from . import void


class Ferz:
    def __init__(self, place, color):
        self.name = 'ферзь'
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = const.COLORS[self.color]
        self.figure = const.FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, const.COLORS[self.color]


    def __str__(self):
        return self.figure

    def move_lad(self, board, info):
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

        return ways, kills, friends

    def move_ofi(self, board, info):
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

        return ways, kills, friends

    def move_kor(self, board, info):
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

        return ways, kills, friends

    def can_move(self, board, info=False):
        ways = set()  # Множество с ходами на пустые клетки
        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета

        """Ферзь может ходить как ладья, офицер и король"""
        if const.DEBUG and info:
            print('Ладья')
        an_ways, an_kills, an_friends = self.move_lad(board=board, info=info)  # Ходы ладьи
        ways = ways | an_ways
        kills = kills | an_kills
        friends = friends | an_friends

        if const.DEBUG and info:
            print('Офицер')
        an_ways, an_kills, an_friends = self.move_ofi(board=board, info=info)  # Ходы офицера
        ways = ways | an_ways
        kills = kills | an_kills
        friends = friends | an_friends

        if const.DEBUG and info:
            print('Король')
        an_ways, an_kills, an_friends = self.move_kor(board=board, info=info)  # Ходы короля
        ways = ways | an_ways
        kills = kills | an_kills
        friends = friends | an_friends

        if const.DEBUG and info:
            print(*self.information())
            print(f'Ходит - {const.make_normal(ways)}\n'
                  f'Убивает - {const.make_normal(kills)}\n'
                  f'Прикрывает - {const.make_normal(friends)}')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
