import pygame
from pygame.sprite import Group

from button import Button
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from scoreboard import Scoreboard

def run_game():
	"""Инициализирует игру и создает объект экрана"""
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode(
		(ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')
	# Создание кнопки Play
	play_button = Button(ai_settings, screen, "Play")
	# Создание экземпляра для хранение игровой статистики
	stats = GameStats(ai_settings)
	
	# Создание корабля, группы пуль и группы прищельцев
	ship = Ship(ai_settings, screen)
	stars = Group()
	bullets = Group()
	aliens = Group()
	
	
	# Создание флота пришельцев
	gf.create_fleet(ai_settings, screen, ship, aliens)
	gf.create_starsky(ai_settings, screen, stars)
	
	# Создание экземпляров GameStats и Scoreboard
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	# Запуск основного цикла игры.
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button,
				ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship,
					aliens, bullets)
			gf.update_aliens(ai_settings, screen, stats, sb, ship,
					aliens, bullets)
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,
					bullets, stars, play_button)
					
run_game()
