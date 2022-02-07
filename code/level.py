import pygame
from ui import UI
from weapon import Weapon
from settings import *
from tile import Tile
from player import Player
from support import *
from random import choice

class Level:
	def __init__(self):
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()
		self.current_attack = None
		self.current_magic = None

		self.create_map()

		self.ui = UI()

	def create_map(self):
		layouts = {
			'boudary': import_csv_layout('../map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('../map/map_Grass.csv'),
			'object': import_csv_layout('../map/map_Objects.csv'),
		}
		graphics = {
			'grass': import_folder('../graphics/grass'),
			'objects': import_folder('../graphics/objects'),
		}

		self.player = Player(
			(2000, 1430),
			[self.visible_sprites],
			self.obstacle_sprites,
			self.create_attack,
			self.destroy_attack,
			self.create_magic,
			self.destroy_magic
		)

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boudary':
							Tile((x, y), [self.obstacle_sprites], 'invisable')
						if style == 'grass':
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], style, choice(graphics['grass']))
						if style == 'object':
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites], style, graphics['objects'][int(col)])

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
			self.current_attack = None

	def create_magic(self, style, strength, cost):
		print(style)
		print(strength)
		print(cost)

	def destroy_magic(self):
		if self.current_magic:
			self.current_magic.kill()
			self.current_magic = None

	def run(self):
		self.visible_sprites.draw(self.player)
		self.visible_sprites.update()
		self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()

		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft= (0, 0))

	def draw(self, player):

		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)
