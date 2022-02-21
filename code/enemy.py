import pygame
from settings import *
from entity import Entity
from support import import_folder

class Enemey(Entity):
	def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, trigger_death_particles):
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
		self.can_attack = True
		self.attack_time = None
		self.attack_cooldown = 400
		self.damage_player = damage_player
		self.vulnerable = True
		self.hit_time = None
		self.invincibility = 300
		self.trigger_death_particles = trigger_death_particles

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

	def get_damage(self, player, attack_type):
		if (self.vulnerable):
			if attack_type == 'weapon':
				self.health -= player.get_full_weapon_damage()
			else:
				self.health -= player.get_full_magic_damage()

			self.vulnerable = False
			self.hit_time = pygame.time.get_ticks()

	def get_status(self, player):
		distance = self.get_player_distance_direction(player)[0]

		if distance <= self.attack_radius and self.can_attack:
			if self.status != 'attack':
				self.frame_index = 0
			self.status = 'attack'
		elif distance <= self.notice_radius:
			self.status = 'move'
		else:
			self.status = 'idle'

	def actions(self, player):
		if self.status == 'attack':
			self.attack_time = pygame.time.get_ticks()
			self.damage_player(self.attack_damage, self.attack_type)
		elif self.status == 'move':
			self.direction = self.get_player_distance_direction(player)[1]
		else:
			self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index = (self.frame_index + self.animation_speed) % len(animation)

		if (self.frame_index + self.animation_speed >= len(animation) and self.status == 'attack'):
			self.can_attack = False

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			self.image.set_alpha(self.wave_value())
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
				self.can_attack = True

		if not self.vulnerable and current_time - self.hit_time >= self.invincibility:
				self.vulnerable = True

	def check_death(self):
		if self.health <= 0:
			self.kill()
			self.trigger_death_particles(self.rect.center, self.monster_name )

	def hit_reaction(self):
		if not self.vulnerable:
			self.direction *= -self.resistance

	def enemy_update(self, player):
		self.actions(player)
		self.get_status(player)
		self.animate()
		self.cooldowns()
		self.hit_reaction()
		self.move()
		self.check_death()
