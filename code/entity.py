from math import sin
import pygame

class Entity(pygame.sprite.Sprite):
	def __init__(self, groups, obstacle_sprites):
		super().__init__(*groups)

		self.obstacle_sprites = obstacle_sprites
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pygame.math.Vector2()

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

	def wave_value(self):
		if sin(pygame.time.get_ticks()) >= 0:
			return 255
		else:
			return 0