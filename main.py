import sys, math
import pygame
from pygame.locals import *

# Initialize pygame object
pygame.init()

# Set FPS
FPS = 60
GameClock = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the game window
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1500
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")


# Paddles for P1 and P2
class Paddle(pygame.sprite.Sprite):
    def __init__(self, position, upkey, downkey):
        super().__init__()
        # Initialize the rect position
        self.rect = pygame.Rect(position, (20, 100))

        # Bound checking for paddles
        self.rect.x = min(self.rect.x, SCREEN_WIDTH - self.rect.width)
        self.rect.x = max(self.rect.x, 0)
        self.rect.y = min(self.rect.y, SCREEN_HEIGHT - self.rect.height)
        self.rect.y = max(self.rect.y, 0)

        # Set keys for movement
        self.upkey = upkey
        self.downkey = downkey

        # Set player speed
        self.speed = 10

    # Update position based on user input
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[self.upkey]:
            self.move_up()
        elif keys[self.downkey]:
            self.move_down()

    def move_up(self):
        self.move(-self.speed)

    def move_down(self):
        self.move(self.speed)

    # Move within the player space
    def move(self, offset):
        if 0 < self.rect.y + offset < SCREEN_HEIGHT - self.rect.height:
            self.rect.move_ip(0, offset)

    # Draw the game object on the screen
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)


# Ball object
class Ball(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # Track movement of the ball by its center position because it's easier
        self.rect = pygame.Rect((0, 0), (20, 20))
        self.rect.center = position
        self.radius = 20

        # Set direction and magnitude for ball movement
        self.speed = 4
        self.direction = pygame.math.Vector2(1, 0)

    def update(self):
        self.move()

    def move(self):
        # Creating movement vector
        movement_vec = pygame.math.Vector2((self.direction.x, self.direction.y))
        movement_vec.scale_to_length(self.speed)

        # Moving the ball
        self.rect.centerx = math.floor(self.rect.centerx + movement_vec.x)
        self.rect.centery = math.floor(self.rect.centery + movement_vec.y)

        # Collision with walls
        if self.rect.centery - self.radius < 0:
            self.wall_reflect(pygame.math.Vector2(0, -1), (self.rect.centerx, self.radius))
        elif self.rect.centery + self.radius > SCREEN_HEIGHT:
            self.wall_reflect(pygame.math.Vector2(0, 1), (self.rect.centerx, SCREEN_HEIGHT - self.radius))
        elif self.rect.centerx - self.radius < 0:
            self.wall_reflect(pygame.math.Vector2(1, 0), (self.radius, self.rect.centery))
        elif self.rect.centerx + self.radius > SCREEN_WIDTH:
            self.wall_reflect(pygame.math.Vector2(-1, 0), (SCREEN_WIDTH - self.radius, self.rect.centery))

    # Reflect ball off of a wall
    def wall_reflect(self, nv, new_center):
        ball.direction.reflect_ip(nv)
        ball.direction.normalize_ip()
        self.rect.center = new_center

    # Draw the ball object
    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, self.rect.center, self.radius)


# Sprite Groups
paddles = pygame.sprite.Group()
paddles.add(Paddle((0, 0), K_w, K_s), Paddle((SCREEN_WIDTH, 0), K_UP, K_DOWN))
ball = Ball((SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
all_sprites = pygame.sprite.Group()
all_sprites.add(paddles, ball)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE)

    for sprite in all_sprites:
        sprite.update()

    # Code for reflection off of paddle is still in progress
    paddle_hits = pygame.sprite.spritecollide(ball, paddles, False)
    for paddle in paddle_hits:
        x_dir = 1 if ball.rect.centerx < SCREEN_WIDTH/2 else -1
        new_dir = pygame.math.Vector2(x_dir, 0)

        height_of_intersection = paddle.rect.centery - ball.rect.centery
        relative_intersection = height_of_intersection / (paddle.rect.height/2)
        angle_of_reflection = 75 * relative_intersection

        if x_dir > 0:
            new_dir.rotate_ip(-angle_of_reflection)
        else:
            new_dir.rotate_ip(angle_of_reflection)

        new_dir.normalize_ip()
        ball.direction = new_dir
        ball.speed += 1

    for sprite in all_sprites:
        sprite.draw(DISPLAYSURF)

    pygame.display.update()
    GameClock.tick(FPS)
