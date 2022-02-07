import pygame

class Entity(pygame.sprite.Sprite):
	def __init__(self, groups, obstacle_sprites):
		super().__init__(*groups)

		self.obstacle_sprites = obstacle_sprites
		self.frame_index = 0
		self.animation_speed = 0.15
		self.direction = pygame.math.Vector2()

	def animate(self):
		animation = self.animations[self.status]
		self.frame_index = (self.frame_index + self.animation_speed) % len(animation)

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

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
