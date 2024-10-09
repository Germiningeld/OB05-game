import pygame
import sys
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
platform_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150]  # Центр экрана по горизонтали, высота фиксирована

# Параметры шарнира
JOINT_RADIUS = 10
JOINT_COLOR = (150, 50, 50)

# Функция для отрисовки платформы с шарниром
def draw_platform_with_joint(screen, platform_pos):
    # Создаем прямоугольник для платформы
    platform_rect = pygame.Rect(0, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    platform_rect.center = platform_pos

    # Отрисовка платформы (без вращения)
    pygame.draw.rect(screen, PLATFORM_COLOR, platform_rect)

    # Отрисовка шарнира (шарика) под платформой
    joint_pos = (platform_pos[0], platform_pos[1] + PLATFORM_HEIGHT // 2 + JOINT_RADIUS)  # Шарнир под платформой
    pygame.draw.circle(screen, JOINT_COLOR, joint_pos, JOINT_RADIUS)

# Функция для отрисовки градиентного фона
def draw_gradient_background(screen, start_color, end_color):
    """Отрисовка градиента от верхней к нижней части экрана."""
    for i in range(SCREEN_HEIGHT):
        r = start_color[0] + (end_color[0] - start_color[0]) * i // SCREEN_HEIGHT
        g = start_color[1] + (end_color[1] - start_color[1]) * i // SCREEN_HEIGHT
        b = start_color[2] + (end_color[2] - start_color[2]) * i // SCREEN_HEIGHT
        pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

# Функция для отрисовки очков
def draw_score(screen, score):
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Очки: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def main():
    score = 0  # Инициализация счетчика очков
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление экрана
        draw_gradient_background(screen, (173, 216, 230), (255, 255, 255))  # Заливка градиентом

        # Отрисовка платформы с шарниром
        draw_platform_with_joint(screen, platform_pos)

        # Отрисовка очков
        draw_score(screen, score)

        # Обновление окна
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

    # Завершение работы Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
