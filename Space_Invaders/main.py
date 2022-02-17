import pygame
import time
import random
from laser import collide
from enemy import Enemy
from player import Player
from table import Table
from screen import Screen
from menu import Menu
from animation import Animation
import os
pygame.font.init()
pygame.init()

WIDTH, HEIGHT = 750, 750

WIN = Screen()
pygame.display.set_caption("Space Shooter")
scoreboard = Table()


def main():

    run = True
    lost = False
    FPS = 60
    level = 0
    lives = 5
    wave_length = 5
    enemy_vel = 1
    laser_vel = 6
    player_vel = 5
    lost_count = 0
    enemy_shoot_frequency = 200
    enemies = []
    clock = pygame.time.Clock()

    player = Player(300, 640)

    def redraw_window():
        WIN.display_start(lives, player.points, level)
        for enemy in enemies:
            enemy.draw(WIN.window)



        # EXPLOSION ANIMATION
        if player.animate:
            player.draw_explosion(WIN.window)

        #displaying first aid kids
        for kit in WIN.first_aid_kits:
            kit.draw(WIN.window)

        #DISPLAY GAME OVER
        player.draw(WIN.window)
        if lost:
            WIN.display_lost()

        pygame.display.update()

    while run:
        redraw_window()
        clock.tick(FPS)

        # GAME DIFFICULTY
        if WIN.difficulty == 'EASY':
            WIN.add_first_aid_kit()

        #GAME OVER
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        # 5 SECONDS BREAK
        if lost:
            if lost_count > FPS * 5:
                scoreboard.score = player.points
                scoreboard.write_score()
                run = False
            else:
                continue

        #RESPAWN
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            if enemy_shoot_frequency >= 10:
                enemy_shoot_frequency -= 10
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)


        #CONTORLS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel  > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        #Enemies
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, enemy_shoot_frequency) == 1:
                enemy.shoot()

            # ENEMY-PLAYER COLISIONS
            if collide(enemy, player):
                player.health -= 10
                player.points -= 15
                enemies.remove(enemy)
                player.animate_explosion(enemy.x, enemy.y)



            # ENEMY CROSS BORDER
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                player.points -= 50
                enemies.remove(enemy)


        # PLAYER - FIRST AID KIT COLLISION
        for kit in WIN.first_aid_kits:
            if collide(kit, player):
                if player.health < 100:
                    WIN.destroy(kit)
                    player.health += kit.health

        player.move_lasers(-laser_vel, enemies)


#MENU
def main_menu():

    def write_name(name):
        scoreboard.name  = name

    def set_difficulty(difficulty, x):
        if x == 1:
            WIN.difficulty = 'EASY'
        elif x == 2:
            WIN.difficulty = 'HARD'

    def show_scoreboard():
        scoreboard.show_scoreboard(main_menu, surface)


    surface = pygame.display.set_mode((750, 750))
    surface.blit(Screen.MENU_BG, (0,0))

    menu = Menu(750, 750)
    menu.set_highlight()
    menu.display_menu(write_name, set_difficulty, main, show_scoreboard, surface)
    menu.menu.mainloop(surface)

    pygame.quit()

main_menu()
