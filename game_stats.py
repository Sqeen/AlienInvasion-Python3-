import json


class GameStats():
	"""Отслеживание статистики  для игры Alien Invasion"""
	
	def __init__(self, ai_settings):
		"""Инициализирует статистику"""
		self.ai_settings = ai_settings
		self.reset_stats()
		self.game_active = False
		# Рекорд не должен сбрасываться
		self.high_score = 0
		
		
	def reset_stats(self):
		"""Инициализирует статистику, изменяющуюся в ходе игры"""
		self.ship_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1

	def return_high_score(self):
		"""Извлекает рекорд из файла"""
		try:
			with open('high_score/high_score.json') as hs:
				top_score = json.load(hs)
		except FileNotFoundError:
			return 0
		else:
			return top_score
