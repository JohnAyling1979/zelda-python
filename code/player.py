import pygame
from support import import_folder
from settings import *
from entity import *

class Player(Entity):
	def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic, destroy_magic):
		super().__init__(groups, obstacle_sprites)

		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -26)

		self.import_player_assets()
		self.status = 'down'

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
		self.creat_magic = create_magic
		self.destroy_magic = destroy_magic
		self.magic_index = 0
		self.magic = list(MAGIC_DATA.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None
		self.magic_switch_cooldown = 200
		self.stats = {
			'health': 100,
			'energy': 60,
			'attack': 10,
			'magic': 4,
			'speed': 5,
		}
		self.health = self.stats['health']
		self.energy = self.stats['energy']
		self.speed = self.stats['speed']
		self.exp = 0

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
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				style = list(MAGIC_DATA.keys())[self.magic_index]
				strength = list(MAGIC_DATA.values())[self.magic_index]['strength'] + self.stats['magic']
				cost = list(MAGIC_DATA.values())[self.magic_index]['cost']
				self.creat_magic(style, strength, cost)

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				self.weapon_index = (self.weapon_index + 1) % len(list(WEAPON_DATA.keys()))
				self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

			if keys[pygame.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				self.magic_index = (self.magic_index + 1) % len(list(MAGIC_DATA.keys()))
				self.magic = list(MAGIC_DATA.keys())[self.magic_index]

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

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
			self.attacking = False
			self.destroy_attack()

		if not self.can_switch_weapon and current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
			self.can_switch_weapon = True

		if not self.can_switch_magic and current_time - self.magic_switch_time >= self.magic_switch_cooldown:
			self.can_switch_magic = True

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move()
