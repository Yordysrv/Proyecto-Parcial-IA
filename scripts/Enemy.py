import pygame

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

   