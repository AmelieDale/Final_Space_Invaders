# SPACEINVADERS.py

import pygame
import sys
import random

# Import your modules (these should be in the same folder)
from alien import Alien
from laser import Laser
from mysteryship import MysteryShip
from obstacle import create_obstacles
from Spaceship import Spaceship

# Constants
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Custom events
ALIENLASER = pygame.USEREVENT + 1
MYSTERYSHIP = pygame.USEREVENT + 2

# Timers
pygame.time.set_timer(ALIENLASER, 1200)    
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

# Setup screen + clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game")
clock = pygame.time.Clock()

# Load music
try:
    pygame.mixer.music.load("Graphics/music.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
except Exception:
    # okay to run without music
    pass



# Game class 

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Player
        self.player = Spaceship(SCREEN_WIDTH, SCREEN_HEIGHT, offset=0)
        self.player_group = pygame.sprite.GroupSingle(self.player)

        # Aliens (start empty — you can spawn them later)
        self.aliens = pygame.sprite.Group()

        # Enemy lasers (from aliens)
        self.enemy_lasers = pygame.sprite.Group()

        # Player lasers are inside player.lasers_group
        # Mystery ship
        self.mystery_ship_group = pygame.sprite.Group()

        # Obstacles
        self.obstacles, self.blocks_group = create_obstacles(num=4, top_y=420, screen_width=SCREEN_WIDTH)

        # Score
        self.score = 0

        # Explosion sound
        try:
            pygame.mixer.Sound("Graphics/explosion.ogg")
            self.explosion_sound.set_volume(1.0)
        except Exception:
            self.explosion_sound = None

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(SCREEN_WIDTH, 60))

    def alien_shoot_from_random(self):
        if len(self.aliens) == 0:
            return
        shooter = random.choice(self.aliens.sprites())
        # create a downward laser: use positive speed but Laser.update subtracts speed
        # so pass negative speed to make it move down
        laser = Laser(shooter.rect.center, speed=-5, screen_height=SCREEN_HEIGHT)
        self.enemy_lasers.add(laser)

    def run(self):
        # update
        self.player_group.update()
        self.enemy_lasers.update()
        self.mystery_ship_group.update()
        self.player.lasers_group.update()
        self.aliens.update()

        # collisions: player lasers vs mystery ship (remove ship on hit)
        # dokill=True ensures the mystery ship is removed
        for player_laser in list(self.player.lasers_group):
            hit_mystery = pygame.sprite.spritecollide(player_laser, self.mystery_ship_group, dokill=True)
            if hit_mystery:
                player_laser.kill()
                self.score += 500
                if self.explosion_sound:
                    self.explosion_sound.play()

        # collisions: enemy lasers vs player
        if pygame.sprite.spritecollide(self.player, self.enemy_lasers, dokill=True):
            # placeholder: you can add lives or end-game logic here
            print("Player hit!")

        # draw
        self.screen.fill((30, 30, 30))
        self.blocks_group.draw(self.screen)
        self.mystery_ship_group.draw(self.screen)
        self.aliens.draw(self.screen)
        self.enemy_lasers.draw(self.screen)
        self.player_group.draw(self.screen)
        self.player.lasers_group.draw(self.screen)

        # Design 
        try:
            font = pygame.font.Font("Graphics/monogram.ttf", 24)
        except Exception:
            font = pygame.font.Font(None, 24)
        score_surf = font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.screen.blit(score_surf, (10, 10))

        pygame.display.flip()

# Main loop

def main():
    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MYSTERYSHIP:
                game.create_mystery_ship()
                pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

            if event.type == ALIENLASER:
                game.alien_shoot_from_random()

        game.run()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
