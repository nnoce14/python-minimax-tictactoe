import pygame
import random
import math

pygame.init()

WIN_WIDTH = 300
WIN_HEIGHT = 300

BLACK = (0, 0, 0)

scores = {
    'O': 10,
    'tie': 0,
    'X': -10
}

def debug_board(board):
    for i in range(0, 3):
        print(board[i])

def text_objects(text, font):
    textSurface = font.render(text, True, (255, 0, 255))
    return textSurface, textSurface.get_rect()


def message_display(text, win):
    largeText = pygame.font.Font("freesansbold.ttf", 60)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (150, 150)
    win.blit(TextSurf, TextRect)


def draw_window(win, board):
    win.fill((255, 255, 255))

    # draws the lines for the board
    draw_board_outline(win)

    # draws the pieces onto the board
    draw_board_pieces(win, board)


def draw_board_pieces(win, board):
    w = 100
    h = 100
    for i in range(0, 3):
        for j in range(0, 3):
            x = w * i + w / 2
            y = h * j + h / 2
            spot = board[i][j]
            if spot == 'X':
                x_offset = w / 4
                pygame.draw.line(win, BLACK, (x - x_offset, y - x_offset), (x + x_offset, y + x_offset), 4)
                pygame.draw.line(win, BLACK, (x + x_offset, y - x_offset), (x - x_offset, y + x_offset), 4)
            elif spot == 'O':
                pygame.draw.circle(win, BLACK, (int(x), int(y)), 30, 3)


def draw_board_outline(win):
    pygame.draw.line(win, BLACK, (100, 0), (100, WIN_WIDTH), 2)
    pygame.draw.line(win, BLACK, (200, 0), (200, WIN_HEIGHT), 2)

    pygame.draw.line(win, BLACK, (0, 100), (WIN_WIDTH, 100), 2)
    pygame.draw.line(win, BLACK, (0, 200), (WIN_WIDTH, 200), 2)


def cpu_turn(available, board, player):
    move = []
    if len(available) < 9:
        bestScore = -10
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(available, board, 0, False)
                    board[i][j] = ''
                    if score > bestScore:
                        bestScore = score
                        move = [i, j]

        available.remove(move)
        board[move[0]][move[1]] = player
    else:
        available.pop(0)
        board[0][0] = 'O'


def minimax(available, board, depth, isMaximizing):
    result = check_winner(board, available)
    if result != 'none':
        if result == 'O':
            return scores[result] - depth
        elif result == 'X':
            return scores[result] + depth

        return scores[result]

    if isMaximizing:
        bestScore = -100
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(available, board, depth + 1, False)
                    board[i][j] = ''
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = 100
        for i in range(0, 3):
            for j in range(0, 3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    score = minimax(available, board, depth + 1, True)
                    board[i][j] = ''
                    bestScore = min(score, bestScore)
        return bestScore


def player_turn(board, pos, available):
    i = pos[0] // 100
    j = pos[1] // 100

    available.remove([i, j])
    board[i][j] = 'X'


def check_winner(board, available):
    for i in range(0, 3):
        # checks for horizontal victory
        if board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] != '':
            return board[i][0]
        # checks for vertical victory
        elif board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] != '':
            return board[0][i]

    # checks for diagonal victory
    if (board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != '') or (
            board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != ''):
        return board[1][1]

    if len(available) < 1:
        return 'tie'

    # if nothing returns, return 'none'
    return 'none'


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    # tic tac toe board
    board = [['', '', ''],
             ['', '', ''],
             ['', '', '']]

    available = []
    for i in range(0, 3):
        for j in range(0, 3):
            available.append([i, j])

    c_turn = True

    run = True
    while run:
        # game clock sets FPS to 30
        clock.tick(30)
        # event listener
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # quits the game when red X is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not c_turn:  # checks if c_turn is False, meaning it's the player's turn
                    player_turn(board, event.pos, available)
                    c_turn = True  # allows cpu to make a move
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # press 'r' to restart
                    main()
                elif event.key == pygame.K_q:  # press 'q' to quit program anytime
                    quit()


        # checks for winner
        if check_winner(board, available) != 'none':
            run = False

        # cpu turn
        if c_turn and run:
            cpu_turn(available, board, 'O')
            c_turn = False  # allows player to make a move

        # draws the window
        draw_window(win, board)
        # updates the screen
        pygame.display.update()

    # after game over, draws the window once and doesnt do anything else
    while not run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()  # quits the game when red X is clicked
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # press 'r' to restart
                    main()  # calls main to reset board

        # draws the game-winning board
        draw_window(win, board)

        # displays victory message based on outcome
        if check_winner(board, available) == 'X':
            message_display("X wins!", win)
        elif check_winner(board, available) == 'O':
            message_display('O wins!', win)
        else:
            message_display('It\'s a tie!', win)

        # updates the screen
        pygame.display.update()


main()
