import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


# Define the Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.elements = [[100, 50]]
        self.radius = 10
        self.dx = 0
        self.dy = 0
        self.is_growing = False

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(win, BLACK, element, self.radius)

    def move(self):
        if self.is_growing:
            self.elements.append([0, 0])
            self.is_growing = False

        for i in range(len(self.elements) - 1, 0, -1):
            self.elements[i] = list(self.elements[i - 1])

        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy

        # Screen wrapping
        self.elements[0][0] = self.elements[0][0] % WIDTH
        self.elements[0][1] = self.elements[0][1] % HEIGHT

    def grow(self):
        self.is_growing = True

    def check_collision(self):
        # Check if the snake collides with itself
        head = self.elements[0]
        for segment in self.elements[1:]:
            if head == segment:
                return True
        return False


# Define the Food class
class Food:
    def __init__(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT - 20)
        self.radius = 10

    def draw(self):
        pygame.draw.circle(win, RED, (self.x, self.y), self.radius)

    def relocate(self):
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(20, HEIGHT - 20)


# Display score
def show_score(score):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, BLACK)
    win.blit(score_text, (10, 10))


# Main function
def main():
    snake = Snake()
    food = Food()
    score = 0

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(10)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.dy == 0:
                    snake.dx = 0
                    snake.dy = -snake.radius * 2
                elif event.key == pygame.K_DOWN and snake.dy == 0:
                    snake.dx = 0
                    snake.dy = snake.radius * 2
                elif event.key == pygame.K_LEFT and snake.dx == 0:
                    snake.dx = -snake.radius * 2
                    snake.dy = 0
                elif event.key == pygame.K_RIGHT and snake.dx == 0:
                    snake.dx = snake.radius * 2
                    snake.dy = 0

        # Move snake
        snake.move()

        # Check if snake eats food
        if (snake.elements[0][0] - food.x) ** 2 + (
            snake.elements[0][1] - food.y
        ) ** 2 <= (snake.radius + food.radius) ** 2:
            food.relocate()
            score += 1
            snake.grow()

        # Check for collision with itself
        if snake.check_collision():
            running = False

        # Draw everything
        win.fill(WHITE)
        snake.draw()
        food.draw()
        show_score(score)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
