import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение размеров экрана
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
PLAY_WIDTH = 10 * BLOCK_SIZE  # 10 блоков в ширину
PLAY_HEIGHT = 20 * BLOCK_SIZE  # 20 блоков в высоту

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)  # Менее контрастная сетка
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Определение фигур
SHAPES = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],
    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],
    [['.....',
      '.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..']],
    [['.....',  # Исправленная L-образная фигура
      '.....',
      '..0..',
      '..0..',
      '.00..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '000..',
      '.....',
      '.....']]
]


class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice([RED, GREEN, BLUE])
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(10)] for _ in range(20)]

    for y in range(20):
        for x in range(10):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def draw_grid(surface, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for y in range(len(grid)):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (PLAY_WIDTH, y * BLOCK_SIZE))  # Менее контрастная сетка
    for x in range(len(grid[0])):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, PLAY_HEIGHT))

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(piece, grid):
    accepted_positions = [[(x, y) for x in range(10) if grid[y][x] == BLACK] for y in range(20)]
    accepted_positions = [x for sub in accepted_positions for x in sub]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] >= 0:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(SHAPES))

def draw_window(surface, grid, score=0):
    surface.fill(BLACK)

    # Рисуем счет в верхней части экрана
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(label, (10, 10))

    # Рисуем сетку
    draw_grid(surface, grid)

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if BLACK not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    paused = False  # Флаг паузы
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        if not paused:  # Остановка игрового процесса, если игра на паузе
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed and not paused:  # Если игра не на паузе
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Клавиша для паузы
                    paused = not paused  # Переключение флага паузы
                if not paused:  # Игровые действия разрешены только если не на паузе
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not valid_space(current_piece, grid):
                            current_piece.rotation -= 1  # Если нельзя повернуть, отменить вращение

        # ОТРИСОВКА ФИГУР ВСЕГДА, даже при паузе
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # Если нужно сменить фигуру (логика продолжает работать)
        if change_piece and not paused:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        # Отрисовка окна всегда
        draw_window(win, grid, score)

        # Если игра на паузе, показываем сообщение "Paused"
        if paused:
            font = pygame.font.SysFont('comicsans', 60)
            label = font.render("Paused", 1, WHITE)
            win.blit(label, (PLAY_WIDTH // 2 - label.get_width() // 2, PLAY_HEIGHT // 2 - label.get_height() // 2))

        pygame.display.update()

        if check_lost(locked_positions):
            run = False

def main_menu():
    global win
    win = pygame.display.set_mode((PLAY_WIDTH, PLAY_HEIGHT))
    pygame.display.set_caption('Tetris')

    run = True
    while run:
        win.fill(BLACK)
        font = pygame.font.SysFont('comicsans', 40)  # Уменьшенный шрифт для текста
        label = font.render('Press Any Key to Play', 1, WHITE)
        win.blit(label, (PLAY_WIDTH // 2 - label.get_width() // 2, PLAY_HEIGHT // 2 - label.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()

    pygame.quit()

if __name__ == '__main__':
    main_menu()
