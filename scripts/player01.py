import pygame

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

    