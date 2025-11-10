import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 990, 990
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooting Game with Moving Targets")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load images and scale
player_img = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), (50, 50))
bullet_img = pygame.transform.scale(pygame.image.load("bullet.png").convert_alpha(), (10, 5))
target_img = pygame.transform.scale(pygame.image.load("target.png").convert_alpha(), (40, 40))
background_img = pygame.transform.scale(pygame.image.load("background.png").convert_alpha(), (WIDTH, HEIGHT))

# Player setup
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT - 50))
player_speed = 5

# Bullet setup
bullets = []
bullet_speed = -10

# Target setup
NUM_TARGETS = 10

class Target:
    def __init__(self, x, y, speed_x):
        self.rect = target_img.get_rect(topleft=(x, y))
        self.speed_x = speed_x

# Create targets
targets = [Target(random.randint(0, WIDTH - 40),
                  random.randint(50, 300),
                  random.choice([-2, 2])) for _ in range(NUM_TARGETS)]

# Font
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 40)

# Restart button
restart_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60)

clock = pygame.time.Clock()
score = 0
game_over = False

def draw_restart_button():
    pygame.draw.rect(screen, (200, 200, 200), restart_rect)
    text_surf = button_font.render("Restart Game", True, (0, 0, 0))
    screen.blit(text_surf, (restart_rect.x + 15, restart_rect.y + 15))

def reset_game():
    global bullets, targets, score, game_over
    bullets = []
    score = 0
    targets.clear()
    for _ in range(NUM_TARGETS):
        targets.append(Target(random.randint(0, WIDTH - 40),
                              random.randint(50, 300),
                              random.choice([-2, 2])))
    game_over = False

# Game loop
running = True
while running:
    screen.blit(background_img, (0, 0))  # Draw background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                bullet_rect = bullet_img.get_rect(midbottom=player_rect.midtop)
                bullets.append(bullet_rect)
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_rect.collidepoint(event.pos):
                reset_game()

    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and player_rect.top > 0:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN] and player_rect.bottom < HEIGHT:
            player_rect.y += player_speed

    # Update bullets
    for bullet in bullets[:]:
        bullet.y += bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)
        else:
            for target in targets[:]:
                if bullet.colliderect(target.rect):
                    bullets.remove(bullet)
                    targets.remove(target)
                    score += 1
                    break

    # Update targets movement
    for target in targets:
        target.rect.x += target.speed_x
        if target.rect.left < 0 or target.rect.right > WIDTH:
            target.speed_x *= -1  # bounce off edges

    # Draw player, bullets, and targets
    screen.blit(player_img, player_rect)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)
    for target in targets:
        screen.blit(target_img, target.rect)

    # Draw score
    score_surf = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_surf, (10, 10))

    # Check game over
    if not targets and not game_over:
        game_over = True

    if game_over:
        draw_restart_button()

    pygame.display.flip()
    clock.tick(60)

