import pygame
from settings import *
from random import randint

class MagicPlayer:
	def __init__(self, animation_player):
		self.animation_player = animation_player

	def heal(self, player, strength, cost, groups):
		if player.energy >= cost:
			player.energy -= cost
			player.health += strength

			if player.health >= player.stats['health']:
				player.health = player.stats['health']

			self.animation_player.create_particles('aura', player.rect.center, groups)
			self.animation_player.create_particles('heal', player.rect.center, groups)

	def flame(self, player, cost, groups):
		if player.energy >= cost:
			player.energy -= cost
			direction_status = player.status.split('_')[0]

			if direction_status == 'right':
				direction = pygame.math.Vector2(1, 0)
			elif direction_status == 'left':
				direction = pygame.math.Vector2(-1, 0)
			elif direction_status == 'up':
				direction = pygame.math.Vector2(0, -1)
			elif direction_status == 'down':
				direction = pygame.math.Vector2(0, 1)

			x = player.rect.centerx
			y = player.rect.centery

			for i in range(1, 6):
				if direction.x:
					fire_x = x + (direction.x * TILESIZE * i) + randint(-TILESIZE // 3, TILESIZE // 3)
					fire_y = y + randint(-TILESIZE // 3, TILESIZE // 3)
				else:
					fire_x = x + randint(-TILESIZE // 3, TILESIZE // 3)
					fire_y = y + (direction.y *  TILESIZE * i) + randint(-TILESIZE // 3, TILESIZE // 3)

				self.animation_player.create_particles('flame', (fire_x, fire_y), groups)
