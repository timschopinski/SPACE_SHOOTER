import pygame
import os
from ship import Ship
from laser import Laser


RED_SPACE_SHIP = pygame.image.load(os.path.join("assets/pixel_images", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets/pixel_images", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets/pixel_images", "pixel_ship_blue_small.png"))
RED_LASER = pygame.image.load(os.path.join("assets/pixel_images", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets/pixel_images", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets/pixel_images", "pixel_laser_green.png"))

RED_LASER_IMG = pygame.image.load(os.path.join("assets/images", "red_laser.png"))
RED_SPACE_SHIP_IMG = pygame.image.load(os.path.join("assets/images", "RED_SPACE_SHIP.png"))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        #self.ship_img, self.laser_img = RED_SPACE_SHIP_IMG, RED_LASER_IMG
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

