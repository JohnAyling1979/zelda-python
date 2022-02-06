import pygame
from support import import_folder
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		super().__init__(groups)

		self.obstacle_sprites = obstacle_sprites

		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -26)

		self.import_player_assets()

		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {
			'up': [],
			'down': [],
			'left': [],
			'right': [],
			'up_idle': [],
			'down_idle': [],
			'left_idle': [],
			'right_idle': [],
			'up_attack': [],
			'down_attack': [],
			'left_attack': [],
			'right_attack': [],
		}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def move(self):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * self.speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * self.speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if (self.direction.x > 0):
						self.hitbox.right = sprite.hitbox.left
					if (self.direction.x < 0):
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if (self.direction.y > 0):
						self.hitbox.bottom = sprite.hitbox.top
					if (self.direction.y < 0):
						self.hitbox.top = sprite.hitbox.bottom

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
			self.attacking = False

	def update(self):
		self.input()
		self.cooldowns()
		self.move()
