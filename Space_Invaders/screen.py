import pygame
import os
from  health import Health
import random
import pygame_menu
pygame.font.init()

WIDTH, HEIGHT = 750, 750

#Background


class Screen(pygame.Surface):
    BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/bg", "background.png")), (WIDTH, HEIGHT))
    MENU_BG = pygame.transform.scale(pygame.image.load(os.path.join("assets/bg", "space.png")), (WIDTH, HEIGHT))

    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 60)

    MENU_FONT = pygame_menu.font.FONT_NEVIS
    MY_THEME = pygame_menu.Theme(background_color=(0, 0, 0, 0),  # transparent background
                                 title_background_color=(0, 0, 0),
                                 title_font_shadow=True,
                                 widget_padding=20,
                                 widget_offset=(0, 0),
                                 widget_font=MENU_FONT,
                                 widget_font_color=(255, 255, 255)
                                 )

    BACKGROUND = pygame_menu.baseimage.BaseImage(
        image_path="assets/bg/space.png",
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY,
    )

    MY_THEME.background_color = BACKGROUND

    RESPAWN = random.randrange(15,45) * 60

    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.set_caption()
        self.first_aid_kits = []
        self.respawn_counter = 0
        self.difficulty = 'EASY'


    def display_start(self, lives, points, lvl):
        lives_label = self.main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        points_label = self.main_font.render(f"Points: {points}", 1, (255, 255, 255))
        level_label = self.main_font.render(f"Level: {lvl}", 1, (255, 255, 255))
        self.window.blit(self.BG, (0, 0))
        self.window.blit(lives_label, (10, 10))
        self.window.blit(points_label, (WIDTH / 2 - points_label.get_width() / 2, 10))
        self.window.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

    def display_lost(self):
        lost_label = self.lost_font.render("GAME OVER!", 1, (255, 255, 255))
        self.window.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

    def set_caption(self):
        pygame.display.set_caption("Space Shooter")

    def add_first_aid_kit(self):
        self.time()
        if self.respawn_counter == 0:
            health = Health(random.randrange(50,650), random.randrange(50,650))
            self.first_aid_kits.append(health)
            self.respawn_counter = 1

    def time(self):
        if self.respawn_counter >= self.RESPAWN:
            self.respawn_counter = 0
        elif self.respawn_counter > 0:
            self.respawn_counter += 1

    def destroy(self, obj):
        self.first_aid_kits.remove(obj)
