from random import choice, randint

import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
TEXT_COLOR = (255, 255, 255)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()

# Шрифт для текста
font = pygame.font.Font(None, 36)


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    
    Attributes:
        position (tuple): Текущая позиция объекта в пикселях (x, y).
        body_color (tuple): Цвет объекта в формате RGB.
    """
    
    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализирует игровой объект.
        
        Args:
            body_color (tuple, optional): Цвет объекта. По умолчанию черный.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color
        
    def draw(self):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """
    Класс, представляющий яблоко в игре.
    
    Attributes:
        body_color (tuple): Цвет яблока (красный).
    """
    
    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__(APPLE_COLOR)
        self.randomize_position()
        
    def randomize_position(self):
        """Устанавливает случайную позицию для яблока в пределах игрового поля."""
        self.position = (
            random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )
        
    def draw(self):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, представляющий змейку в игре.
    
    Attributes:
        positions (list): Список позиций всех сегментов змейки.
        direction (tuple): Текущее направление движения.
        next_direction (tuple): Следующее направление движения.
        length (int): Текущая длина змейки.
        last (tuple): Позиция последнего удаленного сегмента.
        score (int): Количество собранных яблок.
    """
    
    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(SNAKE_COLOR)
        self.reset()
        
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.score = 0
        
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
            
    def move(self):
        """Обновляет позицию змейки на основе текущего направления."""
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None
            
    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            
    def get_head_position(self):
        """Возвращает позицию головы змейки.
        
        Returns:
            tuple: Позиция головы змейки (x, y).
        """
        return self.positions[0]
        
    def grow(self):
        """Увеличивает длину змейки на 1 и добавляет очки."""
        self.length += 1
        self.score += 10
        
    def check_collision(self):
        """Проверяет столкновение змейки с самой собой.
        
        Returns:
            bool: True если произошло столкновение, иначе False.
        """
        return self.get_head_position() in self.positions[1:]


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для управления змейкой.
    
    Args:
        game_object (Snake): Объект змейки, которым управляет игрок.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def draw_score(score):
    """Отрисовывает счет на экране."""
    score_text = font.render(f'Счет: {score}', True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))


def draw_game_over():
    """Отрисовывает сообщение о конце игры."""
    game_over_text = font.render('ИГРА ОКОНЧЕНА! Нажмите R для рестарта', True, TEXT_COLOR)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))


def main():
    """
    Основная функция игры. Запускает и управляет игровым циклом.
    """
    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()
    
    game_over = False
    running = True
    
    while running:
        # Ограничение FPS
        clock.tick(SPEED)
        
        # Обработка ввода пользователя
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    # Рестарт игры
                    snake.reset()
                    apple.randomize_position()
                    game_over = False
        
        if not game_over:
            # Обработка управления
            handle_keys(snake)
            
            # Обновление направления змейки
            snake.update_direction()
            
            # Движение змейки
            snake.move()
            
            # Проверка столкновения с яблоком
            if snake.get_head_position() == apple.position:
                snake.grow()
                apple.randomize_position()
                # Убедимся, что яблоко не появляется на змейке
                while apple.position in snake.positions:
                    apple.randomize_position()
                    
            # Проверка столкновения с самой собой
            if snake.check_collision():
                game_over = True
        
        # Отрисовка игрового поля
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        draw_score(snake.score)
        
        if game_over:
            draw_game_over()
        
        pygame.display.update()
    
    pygame.quit()


if __name__ == '__main__':
    main()
