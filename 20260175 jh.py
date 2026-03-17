import pygame
import sys
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("아오오니 탈출 게임 (최종)")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (100, 0, 180)
DARK = (60, 0, 120)
SKIN = (255, 220, 177)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# 👉 플레이어
player = pygame.Rect(100, 100, 30, 40)
speed = 5
hp = 3
has_key = False

# 👉 아오오니
oni = pygame.Rect(600, 400, 40, 40)
oni_speed = 3.8

# 👉 벽
walls = [
    pygame.Rect(200, 0, 20, 400),
    pygame.Rect(400, 200, 20, 400),
    pygame.Rect(600, 0, 20, 400)
]

# 👉 아이템
key = pygame.Rect(50, 500, 20, 20)
door = pygame.Rect(750, 250, 40, 80)

def draw_player():
    pygame.draw.rect(screen, SKIN, player)
    pygame.draw.circle(screen, SKIN, (player.x+15, player.y-10), 15)

def draw_oni():
    x, y = oni.center
    pygame.draw.circle(screen, PURPLE, (x, y), 40)
    pygame.draw.circle(screen, DARK, (x, y+10), 40)

    pygame.draw.ellipse(screen, WHITE, (x-20, y-15, 15, 22))
    pygame.draw.ellipse(screen, WHITE, (x+5, y-15, 15, 22))

    pygame.draw.circle(screen, BLACK, (x-12, y-5), 5)
    pygame.draw.circle(screen, BLACK, (x+12, y-5), 5)

    pygame.draw.rect(screen, BLACK, (x-15, y+10, 30, 12))

    pygame.draw.polygon(screen, WHITE, [(x-12, y+10), (x-6, y+22), (x, y+10)])
    pygame.draw.polygon(screen, WHITE, [(x+2, y+10), (x+8, y+22), (x+14, y+10)])

def move_player(dx, dy):
    player.x += dx
    for wall in walls:
        if player.colliderect(wall):
            player.x -= dx

    player.y += dy
    for wall in walls:
        if player.colliderect(wall):
            player.y -= dy

    # 🔥 화면 밖 못 나가게
    player.x = max(0, min(player.x, 800 - player.width))
    player.y = max(0, min(player.y, 600 - player.height))

running = True
game_over = False
win = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over and not win:
        keys = pygame.key.get_pressed()

        dx = dy = 0
        if keys[pygame.K_UP]:
            dy = -speed
        if keys[pygame.K_DOWN]:
            dy = speed
        if keys[pygame.K_LEFT]:
            dx = -speed
        if keys[pygame.K_RIGHT]:
            dx = speed

        move_player(dx, dy)

        # 👉 아오오니 추적
        dx = player.centerx - oni.centerx
        dy = player.centery - oni.centery
        dist = math.sqrt(dx**2 + dy**2)

        if dist != 0:
            oni.x += int((dx / dist) * oni_speed)
            oni.y += int((dy / dist) * oni_speed)

        # 🔥 아오오니도 화면 제한
        oni.x = max(0, min(oni.x, 800 - oni.width))
        oni.y = max(0, min(oni.y, 600 - oni.height))

        # 👉 충돌
        if player.colliderect(oni):
            hp -= 1
            player.x, player.y = 100, 100
            pygame.time.delay(300)

        # 👉 열쇠
        if player.colliderect(key):
            has_key = True

        # 👉 탈출
        if player.colliderect(door) and has_key:
            win = True

        if hp <= 0:
            game_over = True

    screen.fill(BLACK)

    # 👉 벽
    for wall in walls:
        pygame.draw.rect(screen, BLUE, wall)

    # 👉 아이템
    if not has_key:
        pygame.draw.rect(screen, YELLOW, key)

    pygame.draw.rect(screen, GREEN if has_key else RED, door)

    if not game_over and not win:
        draw_player()
        draw_oni()

        hp_text = font.render(f"HP: {hp}", True, WHITE)
        screen.blit(hp_text, (10, 10))

    elif game_over:
        text = font.render("GAME OVER", True, RED)
        screen.blit(text, (250, 250))

    elif win:
        text = font.render("YOU ESCAPED!", True, GREEN)
        screen.blit(text, (220, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()