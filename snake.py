import pygame
import random

pygame.init()

GRAY = (192, 192, 192)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - CELL_SIZE, HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        if not self.grow:
            self.body.pop()
        head = (self.body[0][0] + self.direction[0] * CELL_SIZE,
                self.body[0][1] + self.direction[1] * CELL_SIZE)
        self.body.insert(0, head)
        self.grow = False

    def grow_snake(self):
        self.grow = True

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

class Food:
    def __init__(self):
        self.position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, CELL_SIZE, CELL_SIZE))

def draw_retry_button(screen):
    font = pygame.font.Font(None, 36)
    text = font.render("Reintentar", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, RED, text_rect, border_radius=10)
    screen.blit(text, text_rect)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game by Bliss<3")
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    snake = Snake()
                    food = Food()
                    game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if WIDTH // 2 - 75 <= event.pos[0] <= WIDTH // 2 + 75 and HEIGHT // 2 - 25 <= event.pos[1] <= HEIGHT // 2 + 25:
                    snake = Snake()
                    food = Food()
                    game_over = False
            elif not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_s and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_a and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_d and snake.direction != LEFT:
                    snake.direction = RIGHT

        if not game_over:
            snake.move()
            if snake.body[0] == food.position:
                snake.grow_snake()
                food = Food()

            if (snake.body[0][0] < 0 or snake.body[0][0] >= WIDTH or
                    snake.body[0][1] < 0 or snake.body[0][1] >= HEIGHT or
                    snake.body[0] in snake.body[1:]):
                game_over = True

        screen.fill(GRAY)
        if game_over:
            draw_retry_button(screen)
        else:
            snake.draw(screen)
            food.draw(screen)
        pygame.display.flip()

        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
