import pygame

from .const import COLORS, CONSOLE, CELL, FPS, WIDTH, DEBUG, SURE, load_image, make_index

from .figures.ferz import Ferz
from .figures.kon import Kon
from .figures.korol import Korol
from .figures.ladia import Ladia
from .figures.oficer import Oficer
from .figures.peshka import Peshka
from .figures.void import Void


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