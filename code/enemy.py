from turtle import distance
import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemey(Entity):
	def __init__(self, monster_name, pos, groups, obstacle_sprites):
		super().__init__(groups, obstacle_sprites)

		self.sprite_type = 'enemy'

		self.monster_name = monster_name
		monster_info = MONSTER_DATA[self.monster_name]
		self.import_graphics()
		self.status = 'idle'
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, 10)
		self.health = monster_info['health']
		self.exp = monster_info['exp']
		self.speed = monster_info['speed']
		self.attack_damage = monster_info['damage']
		self.resistance = monster_info['resistance']
		self.attack_radius = monster_info['attack_radius']
		self.notice_radius = monster_info['notice_radius']
		self.attack_type = monster_info['attack_type']

	def import_graphics(self):
		self.animations = {
			'idle': [],
			'move': [],
			'attack': [],
		}
		main_path = f'../graphics/monsters/{self.monster_name}/'

		for animation in self.animations.keys():
			full_path = main_path + animation
			self.animations[animation] = import_folder(full_path)

	def get_player_distance_direction(self, player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)

		distance = (player_vec - enemy_vec).magnitude()
		direction = pygame.math.Vector2()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()

		return (distance, direction)


	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius:
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self, player):
		if self.status == 'attack':
			pass
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def enemy_update(self, player):
		self.actions(player)
		self.get_status(player)
		self.animate()
		self.move()
