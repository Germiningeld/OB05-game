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

# Функция для отрисовки градиентного фона
def draw_gradient_background(screen, start_color, end_color):
    """Отрисовка градиента от верхней к нижней части экрана."""
    for i in range(SCREEN_HEIGHT):
        # Расчет промежуточного цвета для градиента
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
        # Заливка градиентом (от голубого к белому)
        draw_gradient_background(screen, (173, 216, 230), (255, 255, 255))

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
