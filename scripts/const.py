import os
import pygame.image

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
