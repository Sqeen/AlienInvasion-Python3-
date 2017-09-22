import pygame
from pygame.sprite import Sprite

class Stars(Sprite):
	
	
	def __init__(self, ai_settings, screen):
		"""Инициализирует звезду и задает ей начальную позицию"""
		self.screen = screen
		self.ai_settings = ai_settings
		super(Stars, self).__init__()
		
		#Загрузка изображения star и получение прямоугольника.
		self.image = pygame.image.load('images/star.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		# Сохранение точной позиции star
		self.x = float(self.rect.x)
		
		
	def blitme(self):
		"""Рисует star в текущей позиции."""
		self.screen.blit(self.image, self.rect)
		
