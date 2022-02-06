import pygame
from csv import reader
from os import walk

def import_csv_layout(path):
	terrain_map =[]

	with open(path) as level_map:
		layout = reader(level_map, delimiter = ',')
		for row in layout:
			terrain_map.append(list(row))

		return terrain_map

def import_folder(path):
	surface_list = []
	file_list = []

	for _, __, img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			file_list.append(full_path)

		file_list.sort()

		for file_name in file_list:
			surface_list.append(pygame.image.load(file_name).convert_alpha())

	return surface_list
