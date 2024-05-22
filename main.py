import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brawl Stars Simplified")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player settings
player_pos = [WIDTH // 2, HEIGHT // 2]
player_size = 20
player_color = BLUE
player_speed = 5
player_health = 100

# Bullet settings
bullet_color = GREEN
bullet_speed = 10
bullets = []

# Enemy settings
enemy_size = 20
enemy_colors = [RED, YELLOW, WHITE]
enemy_types = ["chaser", "shooter", "fast"]
enemies = []
enemy_bullets = []
enemy_spawn_time = 2000  # milliseconds

# Game loop control
running = True
clock = pygame.time.Clock()

def spawn_enemy():
    enemy_type = random.choice(enemy_types)
    x = random.randint(0, WIDTH-enemy_size)
    y = random.randint(0, HEIGHT-enemy_size)
    if enemy_type == "chaser":
        speed = 2
        color = RED
    elif enemy_type == "shooter":
        speed = 1
        color = YELLOW
    elif enemy_type == "fast":
        speed = 4
        color = WHITE
    enemies.append([x, y, speed, enemy_type, color, pygame.time.get_ticks()])

def move_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] - player_speed > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] + player_speed < HEIGHT - player_size:
        player_pos[1] += player_speed
    if keys[pygame.K_a] and player_pos[0] - player_speed > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] + player_speed < WIDTH - player_size:
        player_pos[0] += player_speed

def shoot_bullet():
    mouse_pos = pygame.mouse.get_pos()
    angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
    bullet_dx = math.cos(angle) * bullet_speed
    bullet_dy = math.sin(angle) * bullet_speed
    bullets.append([player_pos[0] + player_size // 2, player_pos[1] + player_size // 2, bullet_dx, bullet_dy])

def move_bullets():
    for bullet in bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets.remove(bullet)

def move_enemy_bullets():
    for bullet in enemy_bullets:
        bullet[0] += bullet[2]
        bullet[1] += bullet[3]
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)

def move_enemies():
    for enemy in enemies:
        if enemy[3] == "chaser" or enemy[3] == "fast":
            dx = player_pos[0] - enemy[0]
            dy = player_pos[1] - enemy[1]
            dist = math.sqrt(dx ** 2 + dy ** 2)
            if dist > 0:
                enemy[0] += dx / dist * enemy[2]
                enemy[1] += dy / dist * enemy[2]
        elif enemy[3] == "shooter":
            # Shooter enemies shoot bullets towards the player
            current_time = pygame.time.get_ticks()
            if current_time - enemy[5] > 2000:  # Shoot every 2 seconds
                enemy[5] = current_time
                angle = math.atan2(player_pos[1] - enemy[1], player_pos[0] - enemy[0])
                bullet_dx = math.cos(angle) * bullet_speed
                bullet_dy = math.sin(angle) * bullet_speed
                enemy_bullets.append([enemy[0], enemy[1], bullet_dx, bullet_dy])

def check_collisions():
    global player_health
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_size, enemy_size)
        if player_rect.colliderect(enemy_rect):
            player_health -= 1
            if player_health <= 0:
                return True
        for bullet in bullets:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            if bullet_rect.colliderect(enemy_rect):
                try:
                    enemies.remove(enemy)
                    bullets.remove(bullet)
                    break
                except ValueError:
                    continue

    for bullet in enemy_bullets:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
        if player_rect.colliderect(bullet_rect):
            player_health -= 5
            if player_health <= 0:
                return True
            enemy_bullets.remove(bullet)

    return False

def draw_health_bar():
    pygame.draw.rect(screen, RED, (10, 10, 100, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, player_health, 20))

# Main game loop
spawn_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_event, enemy_spawn_time)

while running:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot_bullet()
        if event.type == spawn_event:
            spawn_enemy()

    move_player()
    move_bullets()
    move_enemy_bullets()
    move_enemies()
    if check_collisions():
        running = False

    # Draw player
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, enemy[4], (enemy[0], enemy[1], enemy_size, enemy_size))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, bullet_color, (int(bullet[0]), int(bullet[1])), 5)

    # Draw enemy bullets
    for bullet in enemy_bullets:
        pygame.draw.circle(screen, RED, (int(bullet[0]), int(bullet[1])), 5)

    draw_health_bar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
