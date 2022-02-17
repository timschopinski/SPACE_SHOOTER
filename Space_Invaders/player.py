import pygame
import os
from ship import Ship
from animation import Animation


dict_explosions = {
    "1": pygame.image.load(os.path.join("assets/animations", "explosion_1.png")),
    "2": pygame.image.load(os.path.join("assets/animations", "explosion_2.png")),
    "3": pygame.image.load(os.path.join("assets/animations", "explosion_3.png")),
    "4": pygame.image.load(os.path.join("assets/animations", "explosion_4.png")),
    "5": pygame.image.load(os.path.join("assets/animations", "explosion_5.png")),
    "6": pygame.image.load(os.path.join("assets/animations", "explosion_6.png")),
}


WIDTH, HEIGHT = 750, 750
YELLOW_LASER = pygame.image.load(os.path.join("assets/pixel_images", "pixel_laser_yellow.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets/pixel_images", "pixel_ship_yellow.png"))

DARK_SPACE_SHIP = pygame.image.load(os.path.join("assets/images", "PLAYER_SPACESHIP.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets/images", "blue_laser.png"))

class Player(Ship):
    explosions = []
    animate = False

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.points = 0
        self.name = ''
        self.TIME = 3
        self.step = 0
        self.index = 0


    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision((obj)):
                        self.points += 10
                        objs.remove(obj)
                        if self.lasers.__contains__(laser):
                            self.lasers.remove(laser)
                            self.animate_explosion(laser.x, laser.y)


    def animate_explosion(self, x, y):
        for key in dict_explosions.keys():
            explosion = Animation(dict_explosions[key], x, y)
            self.explosions.append(explosion)
            self.animate = True

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() *  (self.health/ self.max_health), 10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)


    def time(self):
        if self.step >= self.TIME:
            self.step = 0
            self.index += 1
        elif self.step > 0:
            self.step += 1


    def draw_explosion(self, window):
        self.time()
        if self.step == 0:
            explosion = self.explosions[self.index]
            window.blit(explosion.img, (explosion.x - 320, explosion.y))
            self.step = 1
        if self.index >= len(self.explosions) - 1:
            self.index = 0
            self.explosions.clear()
            self.animate = False

