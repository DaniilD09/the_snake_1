from random import randint

import pygame as pg

pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTRE = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Гейм палитра:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
WHITE_CUBE = (255, 255, 255)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR_APPLE = (0, 255, 0)
SNAKE_COLOR = (0, 255, 0)
BORDER_COLOR_SNAKE = (0, 255, 255)

SPEED = 10

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Родительский класс GameObject описывает класс змейка и яблоко.

    Методы
    ------
    draw():
        Предназначен для дочерних классах
    def draw_cell(self, position=CENTRE, border_color=WHITE_CUBE)
        Отрисовка ячейки.
    """

    def __init__(self, body_color=WHITE_CUBE):
        self.position = CENTRE
        self.body_color = body_color

    def draw(self):
        """Предназначен для дочерних классов."""
        raise NotImplementedError('Нету реализации метода.')

    def draw_cell(self, position, border_color=WHITE_CUBE):
        """Отрисовка ячейки."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия c ним."""

    def __init__(self, busy_positions=CENTRE):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(busy_positions)

    def randomize_position(self, busy_positions):
        """Описываем случайное появление яблока на игровом поле."""
        while self.position in busy_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        self.draw_cell(self.position, BORDER_COLOR_APPLE)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.reset()

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        self.draw_cell(self.get_head_position(), BORDER_COLOR_SNAKE)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self, direction):
        """Обновляет направление движения змейки."""
        self.direction = direction

    def move(self):
        """Обновляет позицию змейки."""
        position_x, position_y = self.get_head_position()
        new_position_x, new_position_y = self.direction
        position = ((position_x + (new_position_x * GRID_SIZE)) % SCREEN_WIDTH,
                    (position_y + (new_position_y * GRID_SIZE)) % SCREEN_HEIGHT
                    )
        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Cбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш
    чтобы изменить направление движения змейки.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
