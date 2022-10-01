from os import walk
from typing import List
import pygame


def import_folder(path: str, scale: int, flip: bool = False)-> List[pygame.Surface]:
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			image_surf = pygame.transform.scale(image_surf, [image_surf.get_width() * scale, image_surf.get_height() * scale])
			if flip: 
				image_surf = pygame.transform.flip(image_surf, True, False)
			surface_list.append(image_surf)

	return surface_list