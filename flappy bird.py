import pygame 
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird in Python")

# Clock for managing FPS
clock = pygame.time.Clock()


# Bird Class
class Bird:
    def __init__(self):
        self.image = pygame.Surface((34, 24))
        self.image.fill((255, 255, 0))  # Yellow bird
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -8

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 34, 24)


# Pipe Class
class Pipe:
    def __init__(self, x):
        self.width = 52
        self.height = random.randint(100, 350)
        self.x = x
        self.gap = 150
        self.top = self.height
        self.bottom = self.height + self.gap
        self.speed = 3

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, 0, self.width, self.top))  # Top pipe
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom))  # Bottom

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.top)

    def get_bottom_rect(self):
        return pygame.Rect(self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom)


# Main Game Function
def main():
    bird = Bird()
    pipes = [Pipe(300)]
    score = 0
    font = pygame.font.SysFont(None, 40)
    running = True

    while running:
        clock.tick(30)  # FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Bird update
        bird.update()

        # Pipe update
        for pipe in pipes:
            pipe.update()

        # Add new pipe
        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe(SCREEN_WIDTH))

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + pipe.width > 0]

        # Check collisions
        for pipe in pipes:
            if bird.get_rect().colliderect(pipe.get_top_rect()) or bird.get_rect().colliderect(pipe.get_bottom_rect()):
                running = False

        if bird.y <= 0 or bird.y >= SCREEN_HEIGHT - 24:
            running = False

        # Update score
        for pipe in pipes:
            if pipe.x + pipe.width == bird.x:
                score += 1

        # Drawing
        screen.fill(WHITE)
        bird.draw(screen)

        for pipe in pipes:
            pipe.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.update()

    print("Game Over! Your Score:", score)


# Run the game
if __name__ == "__main__":
    main()
