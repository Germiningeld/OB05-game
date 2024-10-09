import pygame
import sys
import random
from abc import ABC, abstractmethod
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# Инициализация Pygame
pygame.init()

# Настройка окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Шаткий баланс")

# Настройка таймера
clock = pygame.time.Clock()

# Параметры платформы (доски)
PLATFORM_WIDTH = 300
PLATFORM_HEIGHT = 20
PLATFORM_COLOR = (100, 100, 100)
platform_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150]

# Параметры шарнира
JOINT_RADIUS = 10
JOINT_COLOR = (150, 50, 50)

# Параметры для фигур тетриса
TETROMINO_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]
TETROMINO_SHAPES = {
    "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
    "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
    "T": [(0, 0), (-1, 0), (1, 0), (0, 1)],
    "L": [(0, 0), (0, 1), (0, 2), (1, 2)],
    "J": [(0, 0), (0, 1), (0, 2), (-1, 2)]
}


class GameObject(ABC):
    """Базовый класс для всех объектов игры"""

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def update(self):
        pass


class Tetromino(GameObject):
    def __init__(self, shape, color):
        self.shape = shape  # Координаты блоков фигуры
        self.color = color  # Цвет фигуры
        self.position = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4]  # Изначальная позиция
        self._falling = True  # Фигура привязана к мыши
        self.gravity = 5  # Скорость падения

    @property
    def falling(self):
        return self._falling

    @falling.setter
    def falling(self, value):
        self._falling = value

    def rotate(self):
        """Поворот фигуры на 90 градусов по центру масс"""
        center_x = sum(block[0] for block in self.shape) / len(self.shape)
        center_y = sum(block[1] for block in self.shape) / len(self.shape)

        new_shape = []
        for block in self.shape:
            relative_x = block[0] - center_x
            relative_y = block[1] - center_y
            rotated_x = -relative_y
            rotated_y = relative_x
            new_shape.append((rotated_x + center_x, rotated_y + center_y))
        self.shape = new_shape

    def draw(self, screen):
        """Отрисовка фигуры"""
        for block in self.shape:
            block_x = self.position[0] + block[0] * 20
            block_y = self.position[1] + block[1] * 20
            pygame.draw.rect(screen, self.color, (block_x, block_y, 20, 20))

    def update(self):
        """Обновление позиции фигуры"""
        if not self.falling:
            self.position[1] += self.gravity  # Шаг падения

    def snap_to_grid_x(self):
        """Привязка фигуры к сетке с шагом 20 по оси X"""
        self.position[0] = (self.position[0] // 20) * 20

    def is_about_to_collide_with_platform(self, platform_pos, platform_width, platform_height):
        """Проверка на то, что фигура на следующем шаге вплотную приблизится к платформе"""
        platform_top = platform_pos[1] - platform_height // 2
        platform_left = platform_pos[0] - platform_width // 2
        platform_right = platform_pos[0] + platform_width // 2

        for block in self.shape:
            block_x = self.position[0] + block[0] * 20
            block_y = self.position[1] + block[1] * 20
            # Проверяем, окажется ли фигура вплотную к платформе на следующем шаге
            if platform_top - (block_y + self.gravity) <= 0 and platform_left <= block_x <= platform_right:
                return True
        return False

    def is_about_to_collide_with_others(self, static_tetrominos):
        """Проверка на то, что фигура на следующем шаге вплотную приблизится к другой фигуре"""
        for static_tetromino in static_tetrominos:
            for block in self.shape:
                block_x = self.position[0] + block[0] * 20
                block_y = self.position[1] + block[1] * 20
                for static_block in static_tetromino.shape:
                    static_x = static_tetromino.position[0] + static_block[0] * 20
                    static_y = static_tetromino.position[1] + static_block[1] * 20
                    # Проверяем, окажется ли фигура вплотную к другой фигуре на следующем шаге
                    if static_y - (block_y + self.gravity) <= 0 and block_x == static_x:
                        return True
        return False


class GameManager:
    """Класс для управления игрой"""

    def __init__(self):
        self.score = 0
        self.falling_tetromino = None
        self.static_tetrominos = []
        self.game_over = False

    def reset(self):
        """Перезапуск игры"""
        self.__init__()

    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                if event.button == 1 and self.falling_tetromino:  # Левая кнопка мыши
                    if not self.falling_tetromino.is_about_to_collide_with_others(self.static_tetrominos):
                        self.falling_tetromino.falling = False  # Открепляем фигуру
                elif event.button == 3 and self.falling_tetromino:  # Правая кнопка мыши
                    if self.falling_tetromino.falling:
                        self.falling_tetromino.rotate()
            elif event.type == pygame.KEYDOWN and self.game_over:
                if event.key == pygame.K_r:
                    self.reset()

    def update(self):
        """Обновление состояния игры"""
        if self.game_over:
            return

        if not self.falling_tetromino:
            shape_name = random.choice(list(TETROMINO_SHAPES.keys()))
            shape = TETROMINO_SHAPES[shape_name]
            color = random.choice(TETROMINO_COLORS)
            self.falling_tetromino = Tetromino(shape, color)

        if self.falling_tetromino.falling:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.falling_tetromino.position = [mouse_x, mouse_y]
            self.falling_tetromino.snap_to_grid_x()  # Привязываем позицию к сетке только по оси X
        else:
            self.falling_tetromino.update()
            # Проверяем, находится ли фигура на расстоянии соприкосновения с платформой или другими фигурами
            if (self.falling_tetromino.is_about_to_collide_with_platform(platform_pos, PLATFORM_WIDTH,
                                                                         PLATFORM_HEIGHT) or
                    self.falling_tetromino.is_about_to_collide_with_others(self.static_tetrominos)):
                self.falling_tetromино.falling = False
                self.static_tetrominos.append(self.falling_tetromino)
                self.falling_tetromino = None
                self.score += 10

    def draw(self, screen):
        """Отрисовка элементов игры"""
        draw_gradient_background(screen, (173, 216, 230), (255, 255, 255))
        draw_platform_with_joint(screen, platform_pos)
        for tetromino in self.static_tetrominos:
            tetromino.draw(screen)
        if self.falling_tetromino:
            self.falling_tetromino.draw(screen)
        draw_score(screen, self.score)


def draw_gradient_background(screen, start_color, end_color):
    for i in range(SCREEN_HEIGHT):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // SCREEN_HEIGHT
        g = start_color[1] + (end_color[1] - start_color[1]) * i // SCREEN_HEIGHT
        b = start_color[2] + (end_color[2] - start_color[2]) * i // SCREEN_HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))


def draw_platform_with_joint(screen, platform_pos):
    platform_rect = pygame.Rect(0, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform_rect.center = platform_pos
    pygame.draw.rect(screen, PLATFORM_COLOR, platform_rect)
    joint_pos = (platform_pos[0], platform_pos[1] + PLATFORM_HEIGHT // 2 + JOINT_RADIUS)
    pygame.draw.circle(screen, JOINT_COLOR, joint_pos, JOINT_RADIUS)


def draw_score(screen, score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))


def main():
    game_manager = GameManager()

    while True:
        game_manager.handle_events()
        game_manager.update()
        game_manager.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
