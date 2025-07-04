#LIbreia 
import pygame
import sys
import heapq
import random
import os
from scripts.player01 import Player
#inializacion 
pygame.init()
pygame.mixer.init()

# Inicializar joystick
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick conectado: {joystick.get_name()}")

#  Confihuracion de Pantalla
WIDTH, HEIGHT = 1300, 700
TILE_SIZE = 40
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Breed - Scroll - A* - Nivel completo")

# Mundo
WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Recursos gráficos y sonido
fondo = pygame.image.load(os.path.join('images', 'fondo.png')).convert()
fondo = pygame.transform.scale(fondo, (WORLD_WIDTH, WORLD_HEIGHT))
player_sheet = pygame.image.load(os.path.join('images', 'player_sheet.png')).convert_alpha()
enemy_img = pygame.image.load(os.path.join('images', 'Enemy.png')).convert_alpha()
disparo_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
pygame.mixer.music.load(os.path.join('sound', 'musica de fondo.mp3'))
pygame.mixer.music.play(-1)

# Mapa
grid = [[0 for _ in range(WORLD_WIDTH // TILE_SIZE)] for _ in range(WORLD_HEIGHT // TILE_SIZE)]
for _ in range(300):
    grid[random.randint(0, len(grid) - 1)][random.randint(0, len(grid[0]) - 1)] = 1
# colicion contra paredes
def collides_with_walls(rect):
    left = rect.left // TILE_SIZE
    right = rect.right // TILE_SIZE
    top = rect.top // TILE_SIZE
    bottom = rect.bottom // TILE_SIZE
    for y in range(top, bottom + 1):
        for x in range(left, right + 1):
            if 0 <= x < len(grid[0]) and 0 <= y < len(grid):
                if grid[y][x] == 1:
                    return True
    return False
#clase (jugado)
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_data = {
            "abajo": [{"x": 0, "y": 0, "w": 48.4, "h": 49.5},
                      {"x": 48.4, "y": 0, "w": 48.4, "h": 49.5},
                      {"x": 96.8, "y": 0, "w": 48.4, "h": 49.5}],
            "izquierda": [{"x": 0, "y": 49.5, "w": 48.4, "h": 49.5},
                          {"x": 48.4, "y": 49.5, "w": 48.4, "h": 49.5},
                          {"x": 96.8, "y": 49.5, "w": 48.4, "h": 49.5}],
            "derecha": [{"x": 0, "y": 96, "w": 48.4, "h": 49.5},
                        {"x": 48.4, "y": 96, "w": 48.4, "h": 49.5},
                        {"x": 96.8, "y": 96, "w": 48.4, "h": 49.5}],
            "arriba": [{"x": 0, "y": 148.5, "w": 48.4, "h": 49.5},
                       {"x": 48.4, "y": 148.5, "w": 48.4, "h": 49.5},
                       {"x": 96.8, "y": 148.5, "w": 48.4, "h": 49.5}]
        }
        self.direction = "abajo"
        self.frame_index = 0
        self.animation_timer = 0
        self.speed = 4
        self.image = self.get_frame()
        self.rect = self.image.get_rect(topleft=(x, y))
    #Frame  de animacio atual
    def get_frame(self):
        frame_info = self.sprite_data[self.direction][self.frame_index]
        frame = pygame.Surface((frame_info["w"], frame_info["h"]), pygame.SRCALPHA)
        frame.blit(player_sheet, (0, 0), (frame_info["x"], frame_info["y"], frame_info["w"], frame_info["h"]))
        return pygame.transform.scale(frame, (32, 32))
    #atualizar la posicion del jugador 
    def update(self, keys, joystick):
        moved = False
        dx, dy = 0, 0

        if keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "arriba"
            moved = True
        if keys[pygame.K_s]:
            dy += self.speed
            self.direction = "abajo"
            moved = True
        if keys[pygame.K_a]:
            dx -= self.speed
            self.direction = "izquierda"
            moved = True
        if keys[pygame.K_d]:
            dx += self.speed
            self.direction = "derecha"
            moved = True

        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            deadzone = 0.2
            if abs(axis_x) > deadzone or abs(axis_y) > deadzone:
                dx += int(axis_x * self.speed)
                dy += int(axis_y * self.speed)
                if abs(axis_x) > abs(axis_y):
                    self.direction = "derecha" if axis_x > 0 else "izquierda"
                else:
                    self.direction = "abajo" if axis_y > 0 else "arriba"
                moved = True

        self.rect.x += dx
        if collides_with_walls(self.rect):
            self.rect.x -= dx

        self.rect.y += dy
        if collides_with_walls(self.rect):
            self.rect.y -= dy

        self.rect.x = max(0, min(self.rect.x, WORLD_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, WORLD_HEIGHT - self.rect.height))

        if moved:
            self.animation_timer += 1
            if self.animation_timer >= 10:
                self.frame_index = (self.frame_index + 1) % len(self.sprite_data[self.direction])
                self.animation_timer = 0
        else:
            self.frame_index = 1
        self.image = self.get_frame()
    # clase Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_data = {
            "abajo": [{"x": 145.2, "y": 0, "w": 48.4, "h": 49.5},
                      {"x": 193.6, "y": 0, "w": 48.4, "h": 49.5},
                      {"x": 242, "y": 0, "w": 48.4, "h": 49.5}],
            "izquierda": [{"x": 145.2, "y": 49.5, "w": 48.4, "h": 49.5},
                          {"x": 193.6, "y": 49.5, "w": 48.4, "h": 49.5},
                          {"x": 242, "y": 49.5, "w": 48.4, "h": 49.5}],
            "derecha": [{"x": 145.2, "y": 96, "w": 48.4, "h": 49.5},
                        {"x": 193.6, "y": 96, "w": 48.4, "h": 49.5},
                        {"x": 242, "y": 96, "w": 48.4, "h": 49.5}],
            "arriba": [{"x": 145.2, "y": 148.5, "w": 48.4, "h": 49.5},
                       {"x": 193.6, "y": 148.5, "w": 48.4, "h": 49.5},
                       {"x": 242, "y": 148.5, "w": 48.4, "h": 49.5}]
        }
        self.direction = "abajo"
        self.frame_index = 0
        self.animation_timer = 0
        self.speed = 2
        self.image = self.get_frame()
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_frame(self):
        frame_info = self.sprite_data[self.direction][self.frame_index]
        frame = pygame.Surface((frame_info["w"], frame_info["h"]), pygame.SRCALPHA)
        frame.blit(enemy_img, (0, 0), (frame_info["x"], frame_info["y"], frame_info["w"], frame_info["h"]))
        return pygame.transform.scale(frame, (32, 32))

    def update(self, target_pos):
        ex, ey = self.rect.center
        tx, ty = target_pos
        distance = ((tx - ex) ** 2 + (ty - ey) ** 2) ** 0.5
        enemy_tile = (ex // TILE_SIZE, ey // TILE_SIZE)
        target_tile = (tx // TILE_SIZE, ty // TILE_SIZE)

        if distance < 500:
            path = astar(enemy_tile, target_tile)
            if path:
                next_tile = path[0]
                new_x, new_y = next_tile[0] * TILE_SIZE, next_tile[1] * TILE_SIZE
                dx, dy = new_x - self.rect.x, new_y - self.rect.y
                if abs(dx) > abs(dy):
                    self.direction = "derecha" if dx > 0 else "izquierda"
                else:
                    self.direction = "abajo" if dy > 0 else "arriba"

                if dx != 0:
                    move_x = self.speed if dx > 0 else -self.speed
                    self.rect.x += move_x
                    if collides_with_walls(self.rect):
                        self.rect.x -= move_x
                if dy != 0:
                    move_y = self.speed if dy > 0 else -self.speed
                    self.rect.y += move_y
                    if collides_with_walls(self.rect):
                        self.rect.y -= move_y

                self.animation_timer += 1
                if self.animation_timer >= 10:
                    self.frame_index = (self.frame_index + 1) % len(self.sprite_data[self.direction])
                    self.animation_timer = 0
        self.image = self.get_frame()

        if abs(self.rect.centerx - tx) < 20 and abs(self.rect.centery - ty) < 20:
            game_over()

def astar(start, goal):
    def heuristic(a, b): return abs(a[0] - b[0]) + abs(a[1] - b[1])
    open_set, came_from, g_score = [(0, start)], {}, {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            x, y = neighbor
            if 0 <= x < WORLD_WIDTH // TILE_SIZE and 0 <= y < WORLD_HEIGHT // TILE_SIZE and grid[y][x] == 0:
                tentative_g = g_score[current] + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    heapq.heappush(open_set, (tentative_g + heuristic(neighbor, goal), neighbor))
    return []

def shoot():
    dx, dy = 0, 0
    if player.direction == "arriba":
        dx, dy = 0, -8
    elif player.direction == "abajo":
        dx, dy = 0, 8
    elif player.direction == "izquierda":
        dx, dy = -8, 0
    elif player.direction == "derecha":
        dx, dy = 8, 0
    bullets.append([player.rect.centerx, player.rect.centery, dx, dy])
    disparo_sound.play()

def draw_map(camera_x, camera_y):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, (50, 50, 50),
                                 (x * TILE_SIZE - camera_x, y * TILE_SIZE - camera_y, TILE_SIZE, TILE_SIZE))

def draw_minimap(camera_x, camera_y):
    minimap_width = 200
    minimap_height = 200
    scale_x = minimap_width / WORLD_WIDTH
    scale_y = minimap_height / WORLD_HEIGHT
    minimap_surface = pygame.Surface((minimap_width, minimap_height))
    minimap_surface.fill((30, 30, 30))

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:
                rx = int(x * TILE_SIZE * scale_x)
                ry = int(y * TILE_SIZE * scale_y)
                pygame.draw.rect(minimap_surface, (80, 80, 80), (rx, ry, 2, 2))

    for enemy in enemies:
        ex = int(enemy.rect.centerx * scale_x)
        ey = int(enemy.rect.centery * scale_y)
        pygame.draw.circle(minimap_surface, (255, 0, 0), (ex, ey), 3)

    px = int(player.rect.centerx * scale_x)
    py = int(player.rect.centery * scale_y)
    pygame.draw.circle(minimap_surface, (0, 255, 0), (px, py), 4)
    pygame.draw.rect(minimap_surface, WHITE, (0, 0, minimap_width, minimap_height), 2)
    screen.blit(minimap_surface, (WIDTH - minimap_width - 10, 10))

def start_menu():
    font = pygame.font.SysFont(None, 48)
    text = font.render("Presiona ENTER o START para Iniciar", True, WHITE)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (200, 250))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
            if event.type == pygame.JOYBUTTONDOWN and joystick and event.button == 7:
                return

def level_complete():
    font = pygame.font.SysFont(None, 72)
    text = font.render("¡Has completado este nivel!", True, (0, 255, 0))
    text2 = pygame.font.SysFont(None, 36).render("Presiona R o A para reiniciar, ESC para salir", True, WHITE)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (150, 250))
        screen.blit(text2, (180, 330))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.JOYBUTTONDOWN and joystick and event.button == 0:
                main()
                return

def game_over():
    font = pygame.font.SysFont(None, 72)
    text = font.render("GAME OVER", True, RED)
    text2 = pygame.font.SysFont(None, 36).render("Presiona R o A para reiniciar, ESC para salir", True, WHITE)
    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, (250, 250)) 
        screen.blit(text2, (180, 330))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.JOYBUTTONDOWN and joystick and event.button == 0:
                main()
                return

player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
enemies = pygame.sprite.Group()
for _ in range(10):
    ex = random.randint(0, WORLD_WIDTH - 32)
    ey = random.randint(0, WORLD_HEIGHT - 32)
    enemies.add(Enemy(ex, ey))
bullets = []

def main():
    global player, enemies, bullets
    player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)
    enemies = pygame.sprite.Group()
    for _ in range(10):
        ex = random.randint(0, WORLD_WIDTH - 32)
        ey = random.randint(0, WORLD_HEIGHT - 32)
        enemies.add(Enemy(ex, ey))
    bullets = []
    clock = pygame.time.Clock()
    start_menu()
    camera_x, camera_y = 0, 0
    running = True
    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                shoot()
            if event.type == pygame.JOYBUTTONDOWN and joystick and event.button == 0:
                shoot()

        player.update(keys, joystick)
        for enemy in enemies:
            enemy.update(player.rect.center)

        for bullet in bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 5)
            if collides_with_walls(bullet_rect):
                bullets.remove(bullet)
                continue
            for enemy in enemies:
                if bullet_rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    if bullet in bullets:
                        bullets.remove(bullet)
                    break

        if len(enemies) == 0:
            level_complete()

        camera_x = max(0, min(player.rect.centerx - WIDTH // 2, WORLD_WIDTH - WIDTH))
        camera_y = max(0, min(player.rect.centery - HEIGHT // 2, WORLD_HEIGHT - HEIGHT))

        screen.blit(fondo, (-camera_x, -camera_y))
        draw_map(camera_x, camera_y)
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 255, 0), (bullet[0] - camera_x, bullet[1] - camera_y, 5, 5))
        screen.blit(player.image, (player.rect.x - camera_x, player.rect.y - camera_y))
        for enemy in enemies:
            screen.blit(enemy.image, (enemy.rect.x - camera_x, enemy.rect.y - camera_y))
        draw_minimap(camera_x, camera_y)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

