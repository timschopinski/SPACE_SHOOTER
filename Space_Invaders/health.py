import pygame
from ship import Ship
import os
import random

FIRST_AID_KIT = pygame.transform.scale(pygame.image.load(os.path.join("assets/pixel_images", "first_aid_kit.png")), (50, 50))

class Health(Ship):

    def __init__(self, x, y, health=10):
        super().__init__(x,y,health)
        self.ship_img = FIRST_AID_KIT
        self.mask = pygame.mask.from_surface(self.ship_img)

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

