import pygame
import os

ASSET_DIR = "Graphics"  # folder where your assets live

def asset_path(name):
    return os.path.join(ASSET_DIR, name)

def load_image_try(choices, convert_alpha=True):
    for name in choices:
        p = asset_path(name)
        if os.path.exists(p):
            try:
                img = pygame.image.load(p)
                return img.convert_alpha() if convert_alpha else img.convert()
            except Exception:
                continue
    return None


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, screen_w, y_offset=80, speed=-3):
        super().__init__()
        img = load_image_try(["mystery.png", "mysteryship.png", "mystery.PNG"])
        if img:
            self.image = img
        else:
            self.image = pygame.Surface((60, 28))
            self.image.fill((255, 200, 50))
        # start off right edge
        self.rect = self.image.get_rect(midleft=(screen_w + 40, y_offset))
        self.speed = speed
        self.screen_w = screen_w

    def update(self):
        self.rect.x += self.speed
        # if fully gone off left, remove
        if self.rect.right < -10 or self.rect.left > self.screen_w + 50:
            self.kill()