import pygame
from support import import_folder
from settings import *

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack):
		super().__init__(groups)

		self.obstacle_sprites = obstacle_sprites

		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -26)

		self.import_player_assets()
		self.status = 'down'
		self.fram_index = 0
		self.animation_speed = 0.15


		self.direction = pygame.math.Vector2()
		self.speed = 5
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.creat_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.weapon_switch_cooldown = 200

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

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.creat_attack()

			if keys[pygame.K_RETURN]:
				print('magic')
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				self.weapon_index = (self.weapon_index + 1) % len(list(WEAPON_DATA.keys()))
				self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0;
			self.direction.y = 0;
			if not 'attack' in self.status:
				self.status = self.status.split('_')[0] + '_attack'
		else:
			self.status = self.status.replace('_attack', '')

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
			self.destroy_attack()

		if not self.can_switch_weapon and current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
			self.can_switch_weapon = True

	def animate(self):
		animation = self.animations[self.status]
		self.fram_index = (self.fram_index + self.animation_speed) % len(animation)

		self.image = animation[int(self.fram_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move()
