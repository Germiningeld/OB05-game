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

def main():
    # Основной игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Обновление экрана
        screen.fill((255, 255, 255))  # Заливка белым цветом

        # Отрисовка элементов (пока пусто)

        # Обновление окна
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(FPS)

    # Завершение работы Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
