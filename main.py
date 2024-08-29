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