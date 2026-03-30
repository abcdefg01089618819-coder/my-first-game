관찰 내용

1.  원형 vs AABB 모서리 쪽으로 다가가면 원형이 더 먼저 충돌로 뜸. 눈으로
    보기에는 아직 안 닿은 것 같은데도 HIT이 나와서 범위가 좀 더 크게
    잡히는 느낌이었음.

2.  AABB vs OBB 오브젝트를 회전시키니까 AABB는 그대로라서 실제보다 크게
    잡히는 경우가 있었음. 반면 OBB는 같이 회전해서 모양이 더 잘 맞고
    불필요한 충돌이 줄어드는 느낌이었음.

3.  어떤 방식이 더 적합한지 간단한 게임이면 AABB나 원형으로도 충분할 것
    같고 정확한 충돌이 필요한 경우에는 OBB를 쓰는 게 더 좋아 보였음.
    상황에 따라 같이 쓰는 게 가장 괜찮을 것 같다고 느낌.

4.  인상 깊었던 점 충돌을 무조건 정확하게 하기보다는 빠르게 처리하는 게
    더 중요하다는 점이 기억에 남았음.

4주차 실습 정리

오늘 한 것

-원형 / AABB / OBB Bounding Box 시각화 -세 방식의 충돌 판정 차이 관찰

관찰 내용

AI와의 대화에서 배운 것

충돌 판정을 항상 정확하게 하는 것보다 먼저 간단한 방식으로 빠르게 확인한
뒤 필요한 경우에만 정밀하게 검사하는 방식이 효율적이라는 점이 인상
깊었다.

내 게임에 적용한다면

기본적으로는 AABB나 원형을 사용해서 빠르게 충돌을 처리하고 정확한 판정이
필요한 상황에서만 OBB를 사용하는 방식이 적절할 것 같다.

------------------------------------------------------------------------

``` python
import pygame
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Comparison")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# 색상
GRAY = (150, 150, 150)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# 플레이어
player_rect = pygame.Rect(100, 100, 50, 50)
speed = 5

# 중앙 오브젝트
fixed_size = 80
fixed_center = [WIDTH // 2, HEIGHT // 2]

angle = 0
rotation_speed = 1

# -------------------------
# OBB 생성 함수
# -------------------------
def get_rotated_corners(center, width, height, angle_deg):
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    hw = width / 2
    hh = height / 2

    corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]

    result = []
    for x, y in corners:
        rx = x * cos_a - y * sin_a
        ry = x * sin_a + y * cos_a
        result.append((center[0] + rx, center[1] + ry))

    return result

# -------------------------
# SAT (OBB 충돌)
# -------------------------
def get_axes(corners):
    axes = []
    for i in range(len(corners)):
        p1 = corners[i]
        p2 = corners[(i + 1) % len(corners)]

        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])

        length = math.sqrt(normal[0]**2 + normal[1]**2)
        axes.append((normal[0]/length, normal[1]/length))

    return axes

def project(corners, axis):
    dots = [corner[0]*axis[0] + corner[1]*axis[1] for corner in corners]
    return min(dots), max(dots)

def sat_collision(c1, c2):
    axes = get_axes(c1) + get_axes(c2)

    for axis in axes:
        min1, max1 = project(c1, axis)
        min2, max2 = project(c2, axis)

        if max1 < min2 or max2 < min1:
            return False
    return True

# -------------------------
# 게임 루프
# -------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_LEFT]:
        player_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += speed
    if keys[pygame.K_UP]:
        player_rect.y -= speed
    if keys[pygame.K_DOWN]:
        player_rect.y += speed

    # 회전
    rotation_speed = 5 if keys[pygame.K_z] else 1
    angle += rotation_speed

    screen.fill(WHITE)

    # -------------------------
    # 🔵 Circle 충돌
    # -------------------------
    player_center = player_rect.center
    player_radius = 25
    fixed_radius = fixed_size // 2

    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]

    circle_hit = dx**2 + dy**2 < (player_radius + fixed_radius) ** 2

    # -------------------------
    # 🔴 AABB 충돌
    # -------------------------
    fixed_rect = pygame.Rect(
        fixed_center[0] - fixed_size // 2,
        fixed_center[1] - fixed_size // 2,
        fixed_size,
        fixed_size
    )

    aabb_hit = player_rect.colliderect(fixed_rect)

    # -------------------------
    # 🟩 OBB 충돌
    # -------------------------
    player_obb = get_rotated_corners(player_center, 50, 50, 0)
    fixed_obb = get_rotated_corners(tuple(fixed_center), fixed_size, fixed_size, angle)

    obb_hit = sat_collision(player_obb, fixed_obb)

    # -------------------------
    # 🎨 그리기
    # -------------------------
    # AABB
    pygame.draw.rect(screen, GRAY, player_rect)
    pygame.draw.rect(screen, RED, player_rect, 2)
    pygame.draw.rect(screen, RED, fixed_rect, 2)

    # OBB
    pygame.draw.polygon(screen, GRAY, fixed_obb)
    pygame.draw.polygon(screen, GREEN, fixed_obb, 2)

    # Circle
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)
    pygame.draw.circle(screen, BLUE, fixed_center, fixed_radius, 2)

    # -------------------------
    # 📍 텍스트 표시
    # -------------------------
    circle_text = font.render(f"Circle: {'HIT' if circle_hit else 'NO'}", True, (0,0,0))
    aabb_text = font.render(f"AABB: {'HIT' if aabb_hit else 'NO'}", True, (0,0,0))
    obb_text = font.render(f"OBB: {'HIT' if obb_hit else 'NO'}", True, (0,0,0))

    screen.blit(circle_text, (10, 10))
    screen.blit(aabb_text, (10, 40))
    screen.blit(obb_text, (10, 70))

    pygame.display.flip()
    clock.tick(60)
```
