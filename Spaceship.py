import pygame
from laser import Laser

# Screen & Position Setup
class Spaceship(pygame.sprite.Sprite):
	def __init__(self, screen_width, screen_height, offset):
		super().__init__()
		self.offset = offset
		self.screen_width = screen_width
		self.screen_height = screen_height
		# Player Sprite Setup
		self.image = pygame.image.load("Graphics/spaceship.png")
		self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
		self.speed = 6
		self.lasers = pygame.sprite.Group()
		# Laser Setup
		self.laser_ready = True
		self.laser_time = 0
		self.laser_delay = 300
		self.laser_sound = pygame.mixer.Sound("Graphics/laser.ogg")
# Handle Player Input
	def get_user_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.rect.x += self.speed

		if keys[pygame.K_LEFT]:
			self.rect.x -= self.speed

		if keys[pygame.K_SPACE] and self.laser_ready:
			self.laser_ready = False
			laser = Laser(self.rect.center, -5, self.screen_height)
			self.lasers.add(laser)
			self.laser_time = pygame.time.get_ticks()
			self.laser_sound.play()
# Update Player
	def update(self):
		self.get_user_input()
		self.constrain_movement()
		self.lasers.update()
		self.recharge_laser()
# Keep Player Inside Screen Bounds
	def constrain_movement(self):
		if self.rect.right > self.screen_width:
			self.rect.right = self.screen_width
		if self.rect.left < self.offset:
			self.rect.left = self.offset
# Recharge Laser After Cooldown
	def recharge_laser(self):
		if not self.laser_ready:
			current_time = pygame.time.get_ticks()
			if current_time - self.laser_time >= self.laser_delay:
				self.laser_ready = True
# Reset Laser After Cooldown
	def reset(self):
		self.rect = self.image.get_rect(midbottom = (self.screen_width / 2, self.screen_height))
		self.lasers.empty()
		self.laser_ready = True
		self.laser_time = 0
		
