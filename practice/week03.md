# Pygame Project + 정리

## 📚 수업 정리

\[ChatGPT 대화 정리 - 상세 버전\]

생성일: 2026-03-17

1.  FPS 표시 문제 Q: FPS가 안나옴 → 화면에 표시되게 해줘 A:
    pygame.font를 이용해서 FPS를 계산하고 화면에 출력하는 코드 제공

2.  색상 좌표 질문 Q: 핑크 / 민트 색깔 좌표 알려줘 A: - Pink: (255,
    192, 203) - Mint: (152, 255, 152)

3.  도형 → 고양이 변경 Q: 원을 고양이 모양으로 바꿔줘 A: pygame.draw를
    이용해 귀/얼굴 추가

4.  pygame 오류 Q: ModuleNotFoundError: pygame A: pip install pygame로
    해결 방법 안내

5.  움직임 관련 Q: 캐릭터 이동 / 방향키 조작 A: pygame.key.get_pressed()
    사용법 설명 + 코드 제공

6.  캐릭터 2명 조작 Q: 두 캐릭터 움직이기 A: 키를 나눠서 각각 제어하는
    코드 제공

7.  게임 제작 시작 Q: 고양이 밥주는 게임 만들어줘 A: 기본 게임 구조 제공

→ 이후 피드백: "제대로 안됨"

A: 방향키 이동 + 사료 + 그릇 추가해서 개선

8.  게임 발전 (마인크래프트 스타일) Q: 광물 캐는 게임 + 점수 시스템 A:
    점수 10점 달성 시 이벤트 추가

9.  아오오니 게임 시작 Q: 아오오니가 사람 쫓는 게임 A: 추적 AI (거리
    계산) 기반 코드 제공

핵심 수학: - dx, dy - 거리 계산 (피타고라스)

10. 아오오니 능력 추가 Q: 대쉬 / 끌어당기기 A: 아오오니가 자동으로 스킬
    사용하도록 구현

→ 난이도 문제 발생 Q: 너무 어려움 A: 플레이어 유리하게 수정

11. 게임 시스템 추가 추가된 기능: - 숨기 (벽) - 공격 기능 - 체력 시스템

12. 아오오니 디자인 개선 Q: 얼굴 퀄리티 낮음 A: - 눈 크게 - 이빨 추가 -
    입 개선

13. 수학 질문 Q: 이 코드 이해하려면 필요한 수학? A: - 좌표 - 벡터 개념 -
    거리 공식 - 비율 이동

14. 화면 제한 Q: 화면 밖 못 나가게 A: player.x = max(0, min(player.x,
    width)) 방식으로 해결

15. 최종 완성 게임 구성: - 플레이어 이동 - 아오오니 추적 AI - 체력
    (HP) - 벽 충돌 - 열쇠 획득 - 문 탈출 - 게임오버 / 승리

핵심 개념 정리 1. 좌표 (x, y) 2. 거리 공식 3. 방향 벡터 4. 충돌 판정 5.
게임 루프

한줄 요약 "단순 이동 코드 → 완성형 추격 게임으로 발전"

------------------------------------------------------------------------

## 🎮 게임 코드

``` python
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
```
