import pygame
import pygame.image

import os


"""                                                                            const.py"""
DEBUG, CONSOLE, FPS = 0, 0, 60  # Режим дебагга, режим консоли, фпс
try:
    with open('params.txt', 'r', encoding='utf-8') as params:
        dct = {
            'debug': 0,
            'console': 0,
            'FPS': 60
        }
        for param in params.readlines():
            if '\n' in param:
                readed = param[:-1].split(' = ')
            else:
                readed = param.split(' = ')
            try:
                dct[readed[0]] = int(readed[1])
            except Exception:
                pass
        DEBUG, CONSOLE, FPS = dct['debug'], dct['console'], dct['FPS']
except Exception:
    pass

CELL = 70  # Размер клеток
MESSAGES = 200  # Размер информационного поля справа
SIZE = WIDTH, HEIGHT = CELL * 9 + 9 + MESSAGES, CELL * 9 + 9  # Размер окна

SURE = False  # Подтверждение хода

FIGURES = {
    'ладья': ('♖', '♜'),
    'конь': ('♘', '♞'),
    'офицер': ('♗', '♝'),
    'король': ('♔', '♚'),
    'ферзь': ('♕', '♛'),
    'пешка': ('♙', '♟')
}

COLORS = {
    0: 'черные',
    1: 'белые',
    'черные': 0,
    'белые': 1
}

WHITE = ('♚', '♛', '♜', '♝', '♞', '♟')
BLACK = ('♔', '♕', '♖', '♗', '♘', '♙')


def make_index(take, put) -> tuple:
    """
    Переводит ход из удобного для игрока в читаемый для программы вид
    (С какой клетки взять фигуру, в какую клетку поставить)
    """
    new_take = (int(take[1]) - 1, 'ABCDEFGH'.index(take[0].upper()))
    new_put = (int(put[1]) - 1, 'ABCDEFGH'.index(put[0].upper()))
    return new_take, new_put


def make_normal(moves) -> str:
    """
    Переводит ход из удобного для программы в читаемый для игрока вид
    """
    leest = []
    for move in moves:
        leest.append('ABCDEFGH'[move[1]] + str(move[0] + 1))
    return ', '.join(leest)


def load_image(figure=None, another=''):  # Загрузка картинки
    if another:
        return pygame.image.load(os.path.join('pictures', another + '.png'))
    color = 'white' if str(figure) in WHITE else 'black'
    name = figure.name.capitalize()
    fullname = os.path.join('pictures', color, name + '.png')
    image = pygame.image.load(fullname)
    image.set_colorkey(image.get_at((0, 0)))
    return image


"""                                                                            again.py"""
class Again:
    def __init__(self):

        self.image = pygame.font.Font(None, CELL).render("Играть снова", True, pygame.Color('black'))
        self.coord_x = (WIDTH - self.image.get_width()) // 2
        self.coord_y = CELL * 6

    def check_coords(self, coords):
        return self.coord_x <= coords[0] <= self.coord_x + self.image.get_width() and \
            self.coord_y <= coords[1] <= self.coord_y + self.image.get_height()


"""                                                                            bug.py"""
class Bug:
    def __init__(self):
        self.image = load_image(another='bug')
        self.coord_x = WIDTH - 10 - self.image.get_width()
        self.coord_y = HEIGHT - 10 - self.image.get_height()

    def check_coords(self, coords):
        return self.coord_x <= coords[0] <= self.coord_x + self.image.get_width() and \
            self.coord_y <= coords[1] <= self.coord_y + self.image.get_height()


"""                                                                            flag.py"""
class Flag:
    def __init__(self):
        self.image = load_image(another='flag')
        self.coord_x = WIDTH - MESSAGES + 10
        self.coord_y = HEIGHT - 10 - self.image.get_height()

    def check_coords(self, coords):
        return self.coord_x <= coords[0] <= self.coord_x + self.image.get_width() and \
            self.coord_y <= coords[1] <= self.coord_y + self.image.get_height()
    

"""                                                                            void.py"""
class Void:
    def __init__(self, *args, **nargs):
        pass

    def __str__(self):
        return '_'

    def information(self):
        return ('_', )


"""                                                                            ferz.py"""
class Ferz:
    def __init__(self, place, color):
        self.name = 'ферзь'
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = COLORS[self.color]
        self.figure = FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, COLORS[self.color]


    def __str__(self):
        return self.figure

    def move_lad(self, board, info):
        ways = set()  # Множество с ходами на пустые клетки
        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета

        """Проверка ходов по горизонтали"""
        for i in range(self.place[1] - 1, -1, -1):  # Влево от фигуры
            place = board[self.place[0]][i]
            if DEBUG and info:
                print(f'{place} - влево')
            if type(place) is Void:
                ways.add((self.place[0], i))
            elif place.color != self.color:
                kills.add((self.place[0], i))
                break
            else:
                friends.add((self.place[0], i))
                break

        for i in range(self.place[1] + 1, 8):  # Направо от фигуры
            place = board[self.place[0]][i]
            if DEBUG and info:
                print(f'{place} - вправо')
            if type(place) is Void:
                ways.add((self.place[0], i))
            elif place.color != self.color:
                kills.add((self.place[0], i))
                break
            else:
                friends.add((self.place[0], i))
                break

        for i in range(self.place[0] - 1, -1, -1):  # Вверх от фиугры
            place = board[i][self.place[1]]
            if DEBUG and info:
                print(f'{place} - вверх')
            if type(place) is Void:
                ways.add((i, self.place[1]))
            elif place.color != self.color:
                kills.add((i, self.place[1]))
                break
            else:
                friends.add((i, self.place[1]))
                break

        for i in range(self.place[0] + 1, 8):  # Вниз от фигуры
            place = board[i][self.place[1]]
            if DEBUG and info:
                print(f'{place} - вниз')
            if type(place) is Void:
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
                    if DEBUG and info:
                        print(f'{place} x:{x} y:{y} i:{i}')
                    if type(place) is Void:
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
                if DEBUG and info:
                    print(f'{place} - y:{i} x:{j}')
                if type(place) is Void:
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
        if DEBUG and info:
            print('Ладья')
        an_ways, an_kills, an_friends = self.move_lad(board=board, info=info)  # Ходы ладьи
        ways = ways | an_ways
        kills = kills | an_kills
        friends = friends | an_friends

        if DEBUG and info:
            print('Офицер')
        an_ways, an_kills, an_friends = self.move_ofi(board=board, info=info)  # Ходы офицера
        ways = ways | an_ways
        kills = kills | an_kills
        friends = friends | an_friends

        if DEBUG and info:
            print('Король')
        an_ways, an_kills, an_friends = self.move_kor(board=board, info=info)  # Ходы короля
        ways = ways | an_ways
        kills = kills | an_kills
        friends = friends | an_friends

        if DEBUG and info:
            print(*self.information())
            print(f'Ходит - {make_normal(ways)}\n'
                  f'Убивает - {make_normal(kills)}\n'
                  f'Прикрывает - {make_normal(friends)}')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]


"""                                                                            kon.py"""
class Kon:
    def __init__(self, place, color):
        self.name = 'конь'
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = COLORS[self.color]
        self.figure = FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, COLORS[self.color]

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
                    if type(place) is Void:
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
                    if type(place) is Void:
                        ways.add(coords)
                    elif place.color != self.color:
                        kills.add(coords)
                    else:
                        friends.add(coords)

        if DEBUG and info:
            print(*self.information())
            print(f'Ходит - {make_normal(ways)}\n'
                  f'Убивает - {make_normal(kills)}\n'
                  f'Прикрывает - {make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]


"""                                                                            korol.py"""
class Korol:
    def __init__(self, place, color):
        self.name = 'король'
        self.first = True
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = COLORS[self.color]
        self.figure = FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, COLORS[self.color], self.first

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
                if DEBUG and info:
                    print(f'{place} - y:{i} x:{j}')
                if type(place) is Void:
                    ways.add((self.place[0] + i, self.place[1] + j))
                elif place.color != self.color:
                    kills.add((self.place[0] + i, self.place[1] + j))
                else:
                    friends.add((self.place[0] + i, self.place[1] + j))

        if DEBUG and info:
            print(*self.information())
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
        self.first = False if not checking else self.first


"""                                                                            ladia.py"""
class Ladia:
    def __init__(self, place, color):
        self.name = 'ладья'
        self.first = True
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = COLORS[self.color]
        self.figure = FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, COLORS[self.color], self.first

    def __str__(self):
        return self.figure

    def can_move(self, board, info=False):
        ways = set()  # Множество с ходами на пустые клетки
        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета

        """Проверка ходов по горизонтали"""
        for i in range(self.place[1] - 1, -1, -1):  # Влево от фигуры
            place = board[self.place[0]][i]
            if DEBUG and info:
                print(f'{place} - влево')
            if type(place) is Void:
                ways.add((self.place[0], i))
            elif place.color != self.color:
                kills.add((self.place[0], i))
                break
            else:
                friends.add((self.place[0], i))
                break

        for i in range(self.place[1] + 1, 8):  # Направо от фигуры
            place = board[self.place[0]][i]
            if DEBUG and info:
                print(f'{place} - вправо')
            if type(place) is Void:
                ways.add((self.place[0], i))
            elif place.color != self.color:
                kills.add((self.place[0], i))
                break
            else:
                friends.add((self.place[0], i))
                break

        for i in range(self.place[0] - 1, -1, -1):  # Вверх от фиугры
            place = board[i][self.place[1]]
            if DEBUG and info:
                print(f'{place} - вверх')
            if type(place) is Void:
                ways.add((i, self.place[1]))
            elif place.color != self.color:
                kills.add((i, self.place[1]))
                break
            else:
                friends.add((i, self.place[1]))
                break

        for i in range(self.place[0] + 1, 8):  # Вниз от фигуры
            place = board[i][self.place[1]]
            if DEBUG and info:
                print(f'{place} - вниз')
            if type(place) is Void:
                ways.add((i, self.place[1]))
            elif place.color != self.color:
                kills.add((i, self.place[1]))
                break
            else:
                friends.add((i, self.place[1]))
                break

        if DEBUG and info:
            print(*self.information())
            print(f'Ходит - {make_normal(ways)}\n'
                  f'Убивает - {make_normal(kills)}\n'
                  f'Прикрывает - {make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
        self.first = False if not checking else self.first


"""                                                                            oficer.py"""
class Oficer:
    def __init__(self, place, color):
        self.name = 'офицер'
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = COLORS[self.color]
        self.figure = FIGURES[self.name][self.color]

    def information(self):
        return self.name.capitalize(), self.figure, self.place, COLORS[self.color]

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
                    if DEBUG and info:
                        print(f'{place} x:{x} y:{y} i:{i}')
                    if type(place) is Void:
                        ways.add((self.place[0] + y * i, self.place[1] + x * i))
                    elif place.color != self.color:
                        kills.add((self.place[0] + y * i, self.place[1] + x * i))
                        break
                    else:
                        friends.add((self.place[0] + y * i, self.place[1] + x * i))
                        break
                else:
                    break

        if DEBUG and info:
            print(*self.information())
            print(f'Ходит - {make_normal(ways)}\n'
                  f'Убивает - {make_normal(kills)}\n'
                  f'Прикрывает - {make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]


"""                                                                            pechka.py"""
class Peshka:
    def __init__(self, place, color):
        self.name = 'пешка'
        self.first = True
        self.danger = True
        self.place = place
        self.color = color
        if type(self.color) is str:
            self.color = COLORS[self.color]
        self.figure = FIGURES[self.name][self.color]
        self.walk = 1 if self.color else -1

    def information(self):
        return self.name.capitalize(), self.figure, self.place, COLORS[self.color], self.walk, self.first

    def __str__(self):
        return self.figure

    def can_move(self, board, info=False):
        ways = set()  # Множество с ходами на пустые клетки
        if self.place[0] not in (0, 7) and type(board[self.place[0] + self.walk][self.place[1]]) is Void:
            ways.add((self.place[0] + self.walk, self.place[1]))
            if self.first and type(board[self.place[0] + self.walk * 2][self.place[1]]) is Void:
                ways.add((self.place[0] + self.walk * 2, self.place[1]))

        kills = set()  # Множество с ходами на фигуры другого цвета
        friends = set()  # Множество с ходами на фигуры своего цвета
        if self.place[1] and self.place[0] not in (0, 7):
            place = board[self.place[0] + self.walk][self.place[1] - 1]
            if type(place) is not Void:
                if self.color != place.color:
                    kills.add((self.place[0] + self.walk, self.place[1] - 1))
                else:
                    friends.add((self.place[0] + self.walk, self.place[1] - 1))
        if self.place[1] - 7 and self.place[0] not in (0, 7):
            place = board[self.place[0] + self.walk][self.place[1] + 1]
            if type(place) is not Void:
                if self.color != place.color:
                    kills.add((self.place[0] + self.walk, self.place[1] + 1))
                else:
                    friends.add((self.place[0] + self.walk, self.place[1] + 1))

        if DEBUG and info:
            print(*self.information())
            print(f'Ходит - {make_normal(ways)}\n'
                  f'Убивает - {make_normal(kills)}\n'
                  f'Прикрывает - {make_normal(friends)}\n')
        return ways, kills, friends

    def move(self, place, checking=False):
        self.place = place[:]
        self.danger = False if not checking and not self.first else self.danger
        self.first = False if not checking else self.first


"""                                                                            chess.py"""
class Chess:
    def __init__(self):
        self.board = []  # Доска

        self.kings = {  # Расположение королей
            1: (0, 4),
            0: (7, 4)
        }
        self.shah = ''  # Кому стоит шах
        self.over = ''  # Как именно кончилась игра

        self.turn = 1  # Счётчик ходов
        self.history = []  # История ходов

        self.moves = []  # Выбранные для хода клетки
        self.text = ''  # Сообщение для вывода

        self.make_prep()

    def make_prep(self):  # "Создание" фигур на доске
        placement = [
        (Void, Void, Void, Void, Void, Void, Void, Void),
        (Void, Void, Void, Void, Void, Void, Void, Void),
        (Peshka, Peshka, Peshka, Peshka, Peshka, Peshka, Peshka, Peshka),
        (Ladia, Kon, Oficer, Ferz, Korol, Oficer, Kon, Ladia)]
        placement = placement[::-1] + placement  # Стандартное расположение шахмат
        for i in range(len(placement)):
            row = placement[i]
            leest = list()
            color = int(i in range(4))  # Первые 4 ряда - белый цвет
            for j in range(len(row)):
                place = row[j]
                leest.append(place(place=(i, j), color=color))
            self.board.append(leest)

    def draw_board(self, screen, buttons, clock):
        if CONSOLE:  # Вывод доски в консоль
            print("\t" + "\t".join(tuple('ABCDEFGH')))
            for row in range(len(self.board)):
                print('12345678'[row], end='|\t')
                for place in self.board[row]:
                    print(place, end='\t')
                print()
        else:  # Отрисовка доски на экране
            screen.fill(pygame.Color('white'))  # Фон
            pygame.draw.line(screen, pygame.Color('darkgrey'),  # Правый конец доски
                             (CELL * 9 + 9, 0), (CELL * 9 + 9, CELL * 9 + 9))

            """Линии между клетками"""
            for i in range(CELL + 1, CELL * 9, CELL + 1):
                pygame.draw.line(screen, pygame.Color('darkgrey'), (i, 0), (i, CELL * 9 + 9))
            for i in range(CELL + 1, CELL * 9, CELL + 1):
                pygame.draw.line(screen, pygame.Color('darkgrey'), (0, i), (CELL * 9 + 9, i))

            """Клеточки разных цветов"""
            for i in range(8):
                dark = 0 if i % 2 else CELL + 1
                for j in range(CELL + dark + 2, CELL * 9, CELL * 2 + 2):
                    pygame.draw.rect(screen, pygame.Color('darkgrey'), ((j, (CELL + 1) * (i + 1) + 1), (CELL, CELL)), 0)

            "Буквы, цифры и фигуры"
            font = pygame.font.Font(None, 125)
            for i in range(CELL + 1, CELL * 9, CELL + 1):
                num = ' 12345678'[i // (CELL + 1)]
                text = font.render(num, True, pygame.Color('black'))
                screen.blit(text, (0, i))

            for i in range(CELL + 1, CELL * 9, CELL + 1):
                letter = ' ABCDEFGH'[i // (CELL + 1)]
                text = font.render(letter, True, pygame.Color('black'))
                screen.blit(text, (i, 0))

            for i in range(len(self.board)):
                row = self.board[i]
                for j in range(len(row)):
                    figure = row[j]
                    if type(figure) is Void:
                        continue
                    image = load_image(figure=figure)
                    screen.blit(image, ((j + 1) * (CELL + 1), (i + 1) * (CELL + 1)))
            if len(self.moves) == 1:  # Выбранная клетка
                place = make_index(self.moves[0], 'A1')[0]
                pygame.draw.rect(screen, pygame.Color('red'),
                                 (((place[1] + 1) * (CELL + 1), (place[0] + 1) * (CELL + 1)), ((CELL + 1), (CELL + 1))),
                                 1)

            """Сообщения справа"""
            big = 40
            font = pygame.font.Font(None, big)
            screen.blit(font.render(f'Ходят {COLORS[self.turn % 2]}', True, pygame.Color('black')), (CELL * 9 + 15, 10))
            if self.shah:
                screen.blit(font.render('Шах ' + self.shah, True, pygame.Color('black')), (CELL * 9 + 15, big + 10))
            if self.text:
                pygame.draw.line(screen, pygame.Color('red'), (CELL * 9 + 10, big * 2 + 10), (WIDTH, big * 2 + 10))
                for i in range(len(self.text.split())):
                    word = self.text.split()[i]
                    screen.blit(font.render(word, True, pygame.Color('black')), (CELL * 9 + 15, big * 2.5 + big * i))
            for button in buttons:  # Кнопки
                screen.blit(button.image, (button.coord_x, button.coord_y))
            pygame.display.flip()
            clock.tick(FPS)


    def check_over(self):
        for i in range(len(self.board)):  # Простой перебор всех клеток
            row = self.board[i]
            for j in range(len(row)):
                place = row[j]
                if type(place) is Void or place.color != self.turn % 2:
                    continue
                ways, kills, friends = place.can_move(self.board)
                for move in ways | kills:  # Перебор всех ходов
                    if self.check_move(self.turn % 2, ((i, j), move), checking=True):  # Фигура может походить
                        return False
        if self.shah[:-1] == COLORS[self.turn % 2][:-1]:
            self.over = 'Мат'
        else:
            self.over = 'Пат'
        return True
                        

    def get_move(self):  # Игрок вводит свой ход
        color = self.turn % 2
        print(f'Ходят {COLORS[color]}')
        while True:

            take = input('Какая фигура ходит: ').upper()
            if len(take) >= 3 and take in "SURRENDERСДАЮСЬ":
                self.over = 'Сдались'
                return True
            if len(take) != 2 or take[0] not in 'ABCDEFGH' or take[1] not in '12345678':
                print('Введите клетку на поле')
                continue
            if "DEBUG" in take and DEBUG:
                place = make_index(take=take[-2:], put='A1')[0]
                self.board[place[0]][place[1]].information()
                continue

            put = input('Куда ходит: ').upper()
            if len(put) != 2 or put[0] not in 'ABCDEFGH' or put[1] not in '12345678':
                print('Введите клетку на поле')
                continue
            if len(take) >= 3 and take in "BACKAGAINОБРАТНОНАЗАДЗАНОГОСНОВА":
                continue

            if SURE and input(f"Ваш ход: {take} - {put}, чтобы подтвердить нажмите 'Enter'") != '':
                continue

            if self.check_move(color=color, info=make_index(take, put)):  # Проверка хода
                self.turn += 1
                self.history.append((COLORS[color], take, put))
                return None

    def check_move(self, color, info, checking=False):
        killed = False  # Убитая фигура (пока её нет)

        take, put = info
        figure = self.board[take[0]][take[1]]

        if type(figure) is Void:
            text = 'Выбрана пустая клетка'
            if CONSOLE:
                print(text)
            else:
                self.text = text
                self.moves.clear()
            return False

        if figure.color != color:
            text = 'Вы не можете брать чужие фигуры'
            if CONSOLE:
                print(text)
            else:
                self.text = text
                self.moves.clear()
            return False
        ways, kills, friends = figure.can_move(self.board, info=True)  # Все возможные ходы выбранной фигуры

        is_king = type(self.board[take[0]][take[1]]) is Korol
        if is_king:  # Король не может ходить на клетку, доступную для врага
            danger = self.danger_zones()  # Получение опасных для хода клеток
            ways = set(ways) - danger[figure.color]['ways']
            kills = set(kills) - danger[figure.color]['friends']

        if is_king and DEBUG:
            print(f'Ходит - {ways}\n'
                  f'Убивает - {kills}\n'
                  f'Прикрывает - {friends}\n')

        """Выбранный ход является возможным"""

        if is_king and type(self.board[put[0]][put[1]]) is Ladia:  # Рокировка
            if not(figure.first == self.board[put[0]][put[1]].first == True):
                if not checking:
                    text = 'Фигура уже ходила'
                    if CONSOLE:
                        print(text)
                    else:
                        self.text = text
                        self.moves.clear()
                return False
            if take[1] > put[1]:  # Справа
                if type(self.board[take[0]][1]) is Void and type(self.board[take[0]][2]) is Void and type(self.board[take[0]][3]) is Void:
                    if len(danger[figure.color]['ways'] & {(take[0], 1), (take[0], 2), (take[0], 3)}) == 0:

                        self.board[take[0]][take[1]].move((take[0], 2), checking=checking)
                        self.board[take[0]][take[1]], self.board[take[0]][2] = self.board[take[0]][2], self.board[take[0]][take[1]]

                        self.board[put[0]][put[1]].move((put[0], 3), checking=checking)
                        self.board[put[0]][put[1]], self.board[put[0]][3] = self.board[put[0]][3], self.board[put[0]][put[1]]
                    else:
                        if not checking:
                            text = 'Рокировка невозможна'
                            if CONSOLE:
                                print(text)
                            else:
                                self.text = text
                                self.moves.clear()
                        return False
                else:
                    if not checking:
                        text = 'Нет места для рокировки'
                        if CONSOLE:
                            print(text)
                        else:
                            self.text = text
                            self.moves.clear()
                    return False
            elif take[1] < put[1]:  # Слева
                if type(self.board[take[0]][5]) is Void and type(self.board[take[0]][6]) is Void:
                    if len(danger[figure.color]['ways'] & {(take[0], 5), (take[0], 6)}) == 0:
                        
                        self.board[take[0]][take[1]].move((take[0], 6), checking=checking)
                        self.board[take[0]][take[1]], self.board[put[0]][6] = self.board[put[0]][6], self.board[take[0]][take[1]]

                        self.board[put[0]][put[1]].move((put[0], 5), checking=checking)
                        self.board[put[0]][put[1]], self.board[put[0]][5] = self.board[put[0]][5], self.board[put[0]][put[1]]
                    else:
                        if not checking:
                            text = 'Рокировка невозможна'
                            if CONSOLE:
                                print(text)
                            else:
                                self.text = text
                                self.moves.clear()
                        return False
                else:
                    if not checking:
                        text = 'Нет места для рокировка'
                        if CONSOLE:
                            print(text)
                        else:
                            self.text = text
                            self.moves.clear()
                    return False

        elif type(figure) is Peshka and take[0] == figure.color + 3 and type(self.board[put[0] + -1 ** figure.color][put[1]]) is Peshka and\
            self.board[put[0] + -1 ** figure.color][put[1]].color != figure.color and self.board[put[0] + -1 ** figure.color][put[1]].danger:
            killed = self.board[put[0] + -1 ** figure.color][put[1]]
            self.board[put[0] + -1 ** figure.color][put[1]] = Void()
            self.board[take[0]][take[1]], self.board[put[0]][put[1]] = self.board[put[0]][put[1]], self.board[take[0]][take[1]]
            figure.move(put, checking=checking)

        elif put in ways:  # Ход на клетку
                self.board[take[0]][take[1]], self.board[put[0]][put[1]] = self.board[put[0]][put[1]], self.board[take[0]][take[1]]
                figure.move(put, checking=checking)

        elif put in kills:  # Ход на вражескую фигуру
            killed = self.board[put[0]][put[1]]
            self.board[put[0]][put[1]] = Void()
            self.board[take[0]][take[1]], self.board[put[0]][put[1]] = self.board[put[0]][put[1]], self.board[take[0]][take[1]]
            figure.move(put, checking=checking)
        else:
            if not checking:
                text = 'Невозможный ход'
                if CONSOLE:
                    print(text)
                else:
                    self.text = text
                    self.moves.clear()
            return False

        if self.kings[figure.color] in self.danger_zones()[figure.color]['kills']:  # Если король всё ещё под шахом
            if killed:  # Если фигура убила кого-то до этого
                self.board[take[0]][take[1]] = killed
            self.board[take[0]][take[1]], self.board[put[0]][put[1]] = self.board[put[0]][put[1]], self.board[take[0]][take[1]]  # Откат хода
            figure.move(take, checking=checking)
            if not checking:
                text = 'Вам стоит шах'
                if CONSOLE:
                    print(text)
                else:
                    self.text = text
                    self.moves.clear()
            return False
        
        if checking:
            if killed:  # Если фигура убила кого-то до этого
                self.board[take[0]][take[1]] = killed
            self.board[take[0]][take[1]], self.board[put[0]][put[1]] = self.board[put[0]][put[1]], self.board[take[0]][
                take[1]]  # Откат хода
            figure.move(take, checking=checking)
        else:
            self.shah = ''  # Шах не стоит
            uncolor = (color + 1) % 2  # Противоположный цвет
            if self.kings[uncolor] in self.danger_zones(bug=True)[uncolor]['kills']:  # Стоит шах противоположной команде
                self.shah = COLORS[uncolor][:-1] + 'м'

            if type(figure) is Peshka and figure.place[0] in (0, 7) and not checking:  # Пешка в конце доски становится ферзём
                self.board[put[0]][put[1]] = Ferz(figure.place, color)
            self.text = ''
            if is_king and not checking:
                self.kings[figure.color] = figure.place  # Обновление расположения королей
            if DEBUG:
                for key, value in self.kings.items():
                    print(f'{COLORS[key][:-1].capitalize()}й король - {value}')
        return True

    def danger_zones(self, bug=False):  # Опасные клетки

        info = [{'ways': set(), 'kills': set(), 'friends': set()}, {'ways': set(), 'kills': set(), 'friends': set()}]

        for i in range(len(self.board)):  # Простой перебор всех клеток
            row = self.board[i]
            for j in range(len(row)):
                place = row[j]
                if type(place) is Void:
                    continue
                uncolor = (place.color + 1) % 2
                ways, kills, friends = place.can_move(self.board)
                info[uncolor]['ways'] = info[uncolor]['ways'] | ways
                info[uncolor]['kills'] = info[uncolor]['kills'] | kills
                info[uncolor]['friends'] = info[uncolor]['friends'] | friends

        if DEBUG and bug:
            for item in info:
                print(COLORS[info.index(item)] + ':')
                for kind, vallues in item.items():
                    print(f'{kind} - {vallues}')
                print()
        return info

"""                                                                            main.py"""
import pygame

from scripts.const import COLORS, CONSOLE, CELL, SIZE, WIDTH, DEBUG, make_index

from scripts.buttons.again import Again
from scripts.buttons.bug import Bug
from scripts.buttons.flag import Flag

from scripts.chess import Chess

if __name__ == '__main__':
    play = True
    running = True

    clock, screen, buttons = None, None, None

    if not CONSOLE:
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(SIZE)
        buttons = (Flag(), Bug()) if DEBUG else (Flag(),)

    chess = Chess()
    while play:
        while running:
            chess.draw_board(screen=screen, buttons=buttons, clock=clock)

            if chess.shah:
                if CONSOLE:
                    print('Шах', chess.shah)

            if not CONSOLE:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play = False
                        running = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        coords = event.pos
                        if coords[0] in range(72, 639) and coords[1] in range(72, 639):
                            move = ' ABCDEFGH'[coords[0] // 71] + ' 12345678'[coords[1] // 71]
                            if move not in chess.moves:
                                chess.moves.append(move)
                                if DEBUG:
                                    print(chess.moves)
                            else:
                                chess.moves.clear()
                            if len(chess.moves) == 2:
                                if chess.check_move(color=chess.turn % 2, info=make_index(*chess.moves[-2:])):
                                    chess.history.append((COLORS[chess.turn % 2], *chess.moves))
                                    chess.moves.clear()
                                    chess.turn += 1
                                chess.check_over()
                                if chess.over:
                                    running = False
                            if len(chess.moves) > 2:
                                chess.moves.clear()
                        for button in buttons:
                            if button.check_coords(coords):
                                if type(button) is Flag:
                                    chess.over = 'Сдались'
                                    running = False
                                    break
                                if type(button) is Bug:
                                    with open('debugged.txt', 'w', encoding='utf-8') as file:

                                        file.write('Доска:\n')
                                        tub = '\t' * 1
                                        for i in range(len(chess.board)):
                                            tub = '\t' * 1
                                            row = chess.board[i]
                                            file.write(tub + f'{i + 1} ряд:\n')
                                            tub = '\t' * 2
                                            for j in range(len(row)):
                                                cell = row[j]
                                                figure = cell.information()
                                                info = ''
                                                for i in figure:
                                                    info += ', '
                                                    kind = type(i)
                                                    if kind is str:
                                                        info += i
                                                    elif kind is bool:
                                                        info += 'True' if i else 'False'
                                                    elif kind is int:
                                                        info += str(i)
                                                    elif kind is tuple or kind is list:
                                                        info += f'({i[0]}, {i[-1]})'
                                                file.write(
                                                    tub + f'Cтолб {"ABCDEFGH"[j]} - ' + info[2:] + '\n')

                                        file.write('\nОпасные клетки:\n')
                                        tub = '\t' * 1
                                        info = chess.danger_zones(bug=False)
                                        for item in info:
                                            tub = '\t' * 1
                                            file.write(tub + COLORS[info.index(item)].capitalize() + ':\n')
                                            tub = '\t' * 2
                                            for kind, values in item.items():
                                                file.write(tub + f'{kind.capitalize()} - {values}\n')

                                        file.write('\nРасположение королей:\n')
                                        tub = '\t' * 1
                                        for key, value in chess.kings.items():
                                            file.write(
                                                tub + f'{COLORS[key][:-1].capitalize()}й король - {value}\n')

            else:
                if chess.check_over() or chess.get_move():
                    running = False
        if DEBUG and chess.history:
            for move in chess.history:
                print(move)
            chess.history.clear()
        if CONSOLE:
            if chess.over:
                print(chess.over)
                print(f"Выйграли {COLORS[(chess.turn + 1) % 2]}")
            play = False
        else:
            screen.fill(pygame.Color('white'))
            font = pygame.font.Font(None, CELL * 2 - 30)
            text = font.render(chess.over, True, pygame.Color('black'))
            screen.blit(text, ((WIDTH - text.get_width()) // 2, CELL * 2 - 15))
            text = font.render(f"Выйграли {COLORS[(chess.turn + 1) % 2]}", True, pygame.Color('black'))
            screen.blit(text, ((WIDTH - text.get_width()) // 2, CELL * 3))
            button = Again()
            screen.blit(button.image, (button.coord_x, button.coord_y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.MOUSEBUTTONUP:
                    if button.check_coords(event.pos):
                        running = True
                        chess = Chess()
            pygame.display.flip()


"""pyinstaller --noconsole --onefile Game.py"""