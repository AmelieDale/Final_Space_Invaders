import pygame, sys
import numpy as np
from random import choice, randint
import os

from alien import Alien
from laser import Laser
from obstacle import Obstacle
from Spaceship import Spaceship
from mysteryship import MysteryShip
pygame.init()

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, randint(4000, 8000))

ASSET_DIR = "Graphics"  # folder where your assets live

def asset_path(name):
    return os.path.join(ASSET_DIR, name)

def load_sound_try(choices):
    for name in choices:
        p = asset_path(name)
        if os.path.exists(p):
            try:
                return pygame.mixer.Sound(p)
            except Exception:
                continue
    return None

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

CELL_SIZE = 4

big_grid = [
[0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1]
]
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill((0, 220, 0))   # Green bunkers
        self.rect = self.image.get_rect(topleft=(x, y))

class Shield:
    def __init__(self, x, y):
        self.blocks = pygame.sprite.Group()
        for r in range(len(big_grid)):
            for c in range(len(big_grid[0])):
                if big_grid[r][c] == 1:
                    bx = x + c * CELL_SIZE
                    by = y + r * CELL_SIZE
                    block = Block(bx, by)
                    self.blocks.add(block)

class Game:
    def __init__(self):
        #Alien Setup
        self.aliens = pygame.sprite.Group()
        self.alien_grid(rows=6, cols=8)
        self.alien_direction = 1
        self.alien_speed = 1 
        self.base_alien_speed = 1
        self.max_alien_speed = 5
        self.previous_alien_count = len(self.aliens.sprites())
        self.alien_timer_interval = 800
        self.screen_w = 600
        self.screen_h = 600

        #Alien Lasers
        self.alien_lasers = pygame.sprite.Group()

        #Start Menu Setup
        self.show_menu = True
        self.buttons = []
        self.use_numpy = False
        self.pattern = 'Easy'
        self.speed_multiplier = 1

        self.alien_positions = None
        self.base_y = None
        self.phase_per_alien = None
        self.wave_offset = 0

        self.invader_font = pygame.font.Font("Fonts\Invaders-6RY1.ttf", 40)

        self.inv_text = self.invader_font.render("x x x x x x x x x x ", True, (240,240,240))
        self.inv_width = self.inv_text.get_width()
        self.inv_height = self.inv_text.get_height()

        self.inv_x1 = 0
        self.inv_x2 = self.inv_width

        self.inv_speed = -1

        self.inv_y_offset = 20

        #Obstacle Setup
        self.shields = []  # list of Shield instances
        self.all_shield_blocks = pygame.sprite.Group()
        self.create_shields()

        #Player Setup
        self.player = Spaceship(self.screen_w, self.screen_h, offset=10)
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.mystery_group = pygame.sprite.Group()

        #Health and score
        self.score = 0
        self.lives = 3
        self.live_surf = pygame.image.load('Graphics/player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0]*2 + 20)
        self.font = pygame.font.Font('Fonts/RETROTECH.ttf', 30)

        #Sounds
        self.explosion_sound = load_sound_try(["explosion.ogg", "explosion.wav"])
        self.alien_laser_sound = load_sound_try(["Graphics/laser.ogg", "laser.wav"])

        #Background music if present
        music = asset_path("music.ogg")
        if os.path.exists(music):
            try:
                pygame.mixer.music.load(music)
                pygame.mixer.music.play(-1)
            except Exception:
                pass

    def run(self):
        #Start Menu
        if self.show_menu:
            self.draw_start_menu()
            return
        
        self.mode_speed = self.alien_speed * self.speed_multiplier

        if self.use_numpy:
            self.update_alien_pattern()

        #Aliens Run Code
        self.aliens.update(self.alien_direction * self.mode_speed)
        self.aliens.draw(screen)
        self.alien_finder()
        self.check_alien_speed_up()

        #Alien Lasers Run Code
        self.alien_lasers.update()
        self.alien_lasers.draw(screen)

        #Draw Obstacles
        self.all_shield_blocks.draw(screen)

        #Player Run
        self.player.update()
        self.player_group.draw(screen)

        #Player lasers
        self.player.lasers.draw(screen)

        #Collision Checks
        self.collision_checks()

        #Health and Score
        self.display_score()
        self.display_lives()

        #draw mystery
        self.mystery_group.draw(screen)
        self.mystery_group.update()
 


    def create_shields(self):
        # place four shields mid-bottom, above player
        shield_count = 4
        total_width = shield_count * (len(big_grid[0]) * CELL_SIZE) + (shield_count-1)*40
        start_x = (self.screen_w - total_width) // 2
        y = self.screen_h - 180  # mid-bottom area
        for i in range(shield_count):
            x = start_x + i * ((len(big_grid[0]) * CELL_SIZE) + 40)
            s = Shield(x, y)
            self.shields.append(s)
            self.all_shield_blocks.add(*s.blocks.sprites())

    def create_mystery(self):
        # spawn at top with a little vertical offset (40)
        ms = MysteryShip(self.screen_w, y_offset=55, speed=-3)
        self.mystery_group.add(ms)

    def alien_grid(self, rows, cols, x_distance = 60, y_distance = 48, x_offset = 70, y_offset = 100):
        row_indices = np.repeat(np.arange(rows), cols)
        col_indices = np.tile(np.arange(cols), rows)

        x_positions = col_indices * x_distance + x_offset
        y_positions = row_indices * y_distance + y_offset

        total = len(x_positions)
        for i in range(total):
            row = row_indices[i]
            x = x_positions[i]
            y = y_positions[i]

            if row == 0: color = 'yellow'
            elif 1 <= row <= 2: color = 'green'
            else: color = 'red'

            alien_sprite = Alien(color, x, y)
            alien_sprite.initial_y = y
            alien_sprite.phase = (i / total)*(2.0 * np.pi)
            self.aliens.add(alien_sprite)

        self.create_alien_positions()

    def draw_start_menu(self):
        self.screen_fill_menu = (10,10,30)
        screen.fill(self.screen_fill_menu)

        title_font = pygame.font.Font("Fonts\RETROTECH.ttf", 56)
        btn_font = pygame.font.Font("Fonts\RETROTECH.ttf", 30)

        title = title_font.render("SPACE INVADERS", True, (240,240,240))
        title_rect = title.get_rect(center=(screen_width//2, 60 + title.get_height()//2))
        screen.blit(title, (screen_width//2 - title.get_width()//2, 60))
        
        self.invader_initialised = True
        
        self.inv_x1 += self.inv_speed
        self.inv_x2 += self.inv_speed

        inv_y = title_rect.bottom + self.inv_y_offset

        if self.inv_x1 + self.inv_width < 300:
            self.inv_x1 = self.inv_x2 + self.inv_width
        if self.inv_x2 + self.inv_width < 300:
            self.inv_x2 = self.inv_x1 + self.inv_width

        total_width = self.inv_width * 2
        center_offset = screen_width // 2 - total_width // 2
        screen.blit(self.inv_text, (self.inv_x1 + center_offset, inv_y))
        screen.blit(self.inv_text, (self.inv_x2 + center_offset, inv_y))

        labels = [("Easy", (80,200,120)), ("Medium", (240,200,80)), ("Hard", (240, 120, 120))]
        btn_w, btn_h = 180, 50
        spacing = 20
        start_y = 220

        self.buttons = []
        for i, (text, color) in enumerate(labels):
            rect = pygame.Rect(screen_width//2 - btn_w//2, start_y + i*(btn_h + spacing),btn_w, btn_h)
            pygame.draw.rect(screen, color, rect)
            txt = btn_font.render(text, True, (0,0,0))
            screen.blit(txt, (rect.centerx - txt.get_width()//2, rect.centery - txt.get_height()//2))
            self.buttons.append((rect, text.lower()))

        instruction = btn_font.render("Choose a diffiiculty to start", True, (200,200,200))
        screen.blit(instruction, (screen_width//2 - instruction.get_width()//2, start_y + 4*(btn_h + spacing)))

    def menu_clicks(self, pos):
        for rect, key in self.buttons:
            if rect.collidepoint(pos):
                if key == 'easy':
                    self.set_difficulty('easy')
                elif key == 'medium':
                    self.set_difficulty('medium')
                elif key == 'hard':
                    self.set_difficulty('hard')
                self.show_menu = False
                break

    def set_difficulty(self, level):
        level = level.lower()
        if level == 'easy':
            self.use_numpy = False
            self.pattern = 'easy'
            self.speed_multiplier = 1
            self.alien_timer_interval = 800
            self.base_alien_speed = 0.9
        elif level == 'medium':
            self.use_numpy = True
            self.pattern = 'sine'
            self.speed_multiplier = 1.25
            self.alien_timer_interval = 700
            self.base_alien_speed = 1
        elif level == 'hard':
            self.use_numpy = True
            self.pattern = 'sine+phase'
            self.speed_multiplier = 1.5
            self.alien_timer_interval = 600
            self.base_alien_speed = 1.1
        
        self.alien_speed = float(self.base_alien_speed)

        self.create_alien_positions()
        pygame.time.set_timer(ALIENLASER, self.alien_timer_interval)

    def create_alien_positions(self):
        sprites = list(self.aliens.sprites())
        if not sprites:
            self.alien_positions = np.zeros((0,2), dtype=float)
            self.base_y = np.zeros((0,), dtype=float)
            self.phase_per_alien = np.zeros((0,), dtype=float)
            return
        
        pos = np.array([[s.rect.x, s.rect.y] for s in sprites], dtype=float)
        self.alien_positions = pos
        self.base_y = np.array([getattr(s, "initial_y", s.rect.y) for s in sprites], dtype=float)
        self.phase_per_alien = np.array([getattr(s, "phase", idx * 2*np.pi / len(sprites))
                                    for idx, s in enumerate(sprites)], dtype=float)

    def update_alien_pattern(self):                     
        if self.alien_positions is None or len(self.alien_positions) == 0:
            return

        N = len(self.alien_positions)

        if self.pattern == 'easy':
            return

        elif self.pattern == 'sine':
            amplitude = 3.0
            phases = self.phase_per_alien
            wave = np.sin(self.wave_offset + phases) * amplitude
            self.alien_positions[:,1] = self.base_y + wave
            self.wave_offset += 0.08

        elif self.pattern == 'sine+phase':
            amplitude = 5.0
            phases = self.phase_per_alien * 2.0
            wave = np.sin(self.wave_offset + phases) * amplitude
            noise = (np.random.rand(N) - 0.5) * 1.5
            self.alien_positions[:,1] = self.base_y + wave + noise
            self.wave_offset += 0.12

        sprites = self.aliens.sprites()
        for idx, sprite in enumerate(sprites):
            sprite.rect.y = int(self.alien_positions[idx, 1])

    def alien_finder(self):
        all_aliens = self.aliens.sprites()

        #Alien Directional Changes
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
    
    def alien_move_down(self, distance):
        #Move the aliens down
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance
        
                if self.use_numpy: 
                    if not hasattr(alien, "initial_y"): 
                        alien.initial_y = alien.rect.y 
            
                    else: 
                        alien.initial_y += distance 
        
        if self.use_numpy:
            self.create_alien_positions()

    def alien_shoot(self):
        #Alien Shooting Mechanics
        if self.aliens:
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)

    def check_alien_speed_up(self):
        #Speeds up aliens when killed
        alien_count = len(self.aliens.sprites())

        if alien_count < self.previous_alien_count:
            base_speed_increase = 0.03
            speed_increase = base_speed_increase * self.speed_multiplier

            self.alien_speed = min(self.alien_speed + speed_increase, self.max_alien_speed)
            print('Speed:', self.alien_speed, 'Alien Count:', alien_count)

            if self.use_numpy:
                self.create_alien_positions()    
        
        self.previous_alien_count = alien_count

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))
    
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft =(10,10))
        screen.blit(score_surf, score_rect)
    
    def collision_checks(self):
        #Player Lasers
        if self.player.lasers:
            for laser in self.player.lasers:
                if pygame.sprite.spritecollide(laser, self.all_shield_blocks, True):
                    laser.kill()
        
            #Alien Collisions
                aliens_shot = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_shot:
                    for alien in aliens_shot:
                        self.score += alien.value
                        laser.kill()
                
                if pygame.sprite.spritecollide(laser, self.mystery_group, dokill=True):
                    if self.explosion_sound:
                        try: self.explosion_sound.play()
                        except: pass
                    laser.kill()
                    self.score += 300
        
        if self.alien_lasers:
            for laser in self.alien_lasers:
                if pygame.sprite.spritecollide(laser, self.all_shield_blocks, True):
                    laser.kill()
                
                if pygame.sprite.spritecollide(laser, self.player_group, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.all_shield_blocks, True)
            
            if pygame.sprite.spritecollide(alien, self.player_group, False):
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MYSTERYSHIP:
                if len(game.mystery_group) == 0:
                    game.create_mystery()
                pygame.time.set_timer(MYSTERYSHIP, randint(4000, 8000))

            if game.show_menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.menu_clicks(event.pos)
            
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()
        pygame.display.flip()
        clock.tick(60)

