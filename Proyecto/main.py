import pygame
import sys
import heapq
import random
import os

pygame.init()
pygame.mixer.init()

# Inicializar joystick
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick conectado: {joystick.get_name()}")

 #Pantalla
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
 
 # Recursos
fondo = pygame.image.load(os.path.join('images', 'fondo.png')).convert()
fondo = pygame.transform.scale(fondo, (WORLD_WIDTH, WORLD_HEIGHT))
player_sheet = pygame.image.load(os.path.join('images', 'player_sheet.png')).convert_alpha()
enemy_img = pygame.image.load(os.path.join('images', 'Enemy.png')).convert_alpha()
disparo_sound = pygame.mixer.Sound(os.path.join('sound', 'shoot.wav'))
pygame.mixer.music.load(os.path.join('sound', 'musica de fondo.mp3'))
pygame.mixer.music.play(-1)

#Grid con muros
grid = [[0 for _ in range(WORLD_WIDTH // TILE_SIZE)] for _ in range(WORLD_HEIGHT // TILE_SIZE)]
for _ in range(300):
    grid[random.randint(0, len(grid) - 1)][random.randint(0, len(grid[0]) - 1)] = 1
# colisiones
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
# clase Player (jugador)
class player(pygame.sprite.Sprite):
    def __init__(self, x, y):
       super().__init__()
       self.sprite_data = {
               "bajo": [{"x": 0, "y": 0, "w": 48.4, "h": 49.5},
                        {"x": 48.4, "y": 0, "w": 48.4, "h": 49.5},
                        {"x": 96.8, "y": 0, "w": 48.4, "h": 49.5}],
            "izquierda":  [{"x": 0, "y": 49.5, "w": 48.4, "h": 49.5},
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
# frame de animacion
    def get_frame(self):
        frame_info = self.sprite_data[self.direction][self.frame_index]
        frame = pygame.Surface((frame_info["w"], frame_info["h"]), pygame.SRCALPHA)
        frame.blit(player_sheet, (0, 0), (frame_info["x"], frame_info["y"], frame_info["w"], frame_info["h"]))
        return pygame.transform.scale(frame, (32, 32))
# movimiento hacia  el jugador 
    def update(self, keys, joystick):
        moved = False
        dx, dy = 0, 0 


        # Movimiento de teclado
        if keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "arriba"
            moved = True

        if keys[pygame.K_w]:
            dy += self.speed
            self.direction = "abajo"
            moved = True   

        if keys[pygame.K_w]:
            dy -= self.speed
            self.direction = "izquierda"
            moved = True   

        # movimiento joystikc (stick izquierdo)    
        if joystick:
            axis_x = joystick.get_axis(0)
            axis_y = joystick.get_axis(1)
            deadzone = 0.2
            if abs(axis_x)  > deadzone or abs(axis_y) > deadzone:
                dx += int(axis_x * self.speed)
                dx += int(axis_y * self.speed)
                if abs(axis_x) > abs(axis_y):
                    self.direction = "derecha" if axis_x> 0 else "izquierda"
                else:
                    self.direction  = "abajo" if axis_y > 0 else "arriba"
                moved = True   
        
        # Mover en x y comprobar colisión
        self.rect.x += dx
        if collides_with_walls(self.rect):
            self.rect.x -= dx

        # Mover en y y comprobar colisión
        self.rect.y += dy
        if collides_with_walls(self.rect):
            self.rect.y -= dy

        # Limitar dentro del mundo
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
#clase Enemy (enemigo IA A*)
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
    # frame  de animaciom        

