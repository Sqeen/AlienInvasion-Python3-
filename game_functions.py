import sys
import random
import pygame
from time import sleep
import json

from bullet import Bullet
from alien import Alien
from stars import Stars
from game_stats import GameStats


def check_keydown_events(event, ai_settings, screen, ship, bullets):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_events(ai_settings, screen, stats, sb, play_button, ship,
			aliens, bullets):
	"""Обрабатывает нажатия клавиш и события мыши"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			dump_high_score(stats)
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb,
					play_button, ship, aliens, bullets, mouse_x, mouse_y)
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship,
					bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.K_q:
			sys.exit()
		elif event.type == pygame.K_p:
			start_game(ai_settings, screen, stats, sb, ship, aliens,
			 bullets)
			
def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Запускает новую игру"""
	if  not stats.game_active:
		#Сброс игровых настроек
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		# Сброс игровой статистики
		stats.reset_stats()
		stats.game_active = True
		# Сброс изображений счетов и уровня
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		# Очистка списков пришельцев и пуль
		aliens.empty()
		bullets.empty()
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
			
def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
			aliens, bullets, mouse_x, mouse_y):
	"""Запускает новую игру при нажатии кнопки Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#Сброс игровых настроек
		ai_settings.initialize_dynamic_settings()
		pygame.mouse.set_visible(False)
		if play_button.rect.collidepoint(mouse_x, mouse_y):
			# Сброс игровой статистики
			stats.reset_stats()
			stats.game_active = True
			# Сброс изображений счетов и уровня
			sb.prep_score()
			sb.prep_high_score()
			sb.prep_level()
			sb.prep_ships()
			# Очистка списков пришельцев и пуль
			aliens.empty()
			bullets.empty()
			create_fleet(ai_settings, screen, ship, aliens)
			ship.center_ship()
			

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
			stars, play_button):
	"""Обновляет изображение на экране и отображает новый экран"""
	# При каждом проходе цикла перерисовывает экран
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	stars.draw(screen)
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	# Кнопка Play  отображается в том случае, если игра неактивна
	if not stats.game_active:
		play_button.draw_button()
		
	# Отображение последнего прорисованонного экрана
	pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Обвновляет позиции пуль и удаляет старые пули"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	# Проверка попаданий в пришельцев
	# При обнаружение попадания удалить пулю и пришельца
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
	aliens, bullets)
	
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
			aliens, bullets):
	"""Обработка коллизий пуль с пришельцами"""
	# Удаление пуль и пришельцев учавствующих в коллизиях
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
	sb.prep_score()
	check_high_score(stats, sb)
	if len(aliens) == 0:
		# Если весь флот уничтожен, начинается следующий уровень
		create_fleet(ai_settings, screen, ship, aliens)
		bullets.empty()
		ai_settings.increase_speed()
		# Увеличение уровня
		stats.level += 1
		sb.prep_level()
		
		
def fire_bullet(ai_settings, screen, ship, bullets):
	if len(bullets) < ai_settings.bullets_allowed:
			new_bullet = Bullet(ai_settings, screen, ship)
			bullets.add(new_bullet)

def create_fleet(ai_settings, screen, ship, aliens):
	"""Создает флот пришельцев"""
	# Создание пришельца и вычисление количества прищельцев в ряду
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height,
	 alien.rect.height)
	
	# Создание флота пришельцев
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number,
			 row_number)

def get_number_alien_x(ai_settings, alien_width):
	"""Вычисляет кол-во пришельцев в ряду"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x
	
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Создает флот пришельцев"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Определяет кол-во рядом помещяющихся на экране"""
	available_space_y = (ai_settings.screen_height -
						(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
	
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
			bullets):
	"""Проверяет, добрались ли пришельцы до нижнего края экрана"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Происходит то же, что при столкновении с кораблем
			ship_hit(ai_settings, screen, stats, sb, ship, aliens,
			 bullets)
			break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Проверяет, достиг ли флот края экрана, после чего
	 обновляет позиции всех пришельцев"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	# Проверка коллизий "пришелец-корабль"
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
	check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
	 bullets)

def check_fleet_edges(ai_settings, aliens):
	"""Реагирует на достижение пришельцем экрана"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break
		
def change_fleet_direction(ai_settings, aliens):
	"""Опускает весь флот и меняет направление флота"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def create_starsky(ai_settings, screen, stars):
	"""Создает звездное небо"""
	# Создание звезды и вычисление количества звезд в ряду
	star = Stars(ai_settings, screen)
	number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
	number_rows = get_number_rows_stars(ai_settings, star.rect.height)
	
	# Создание звездного неба
	for row_number in range(number_rows):
		for star_number in range(random.randint(-5, 5), number_stars_x,
			random.randint(2, 5)):
			create_star(ai_settings, screen, stars, star_number,
			 row_number)

def get_number_stars_x(ai_settings, star_width):
	"""Вычисляет  максимальное кол-во звезд в ряду"""
	available_space_x = ai_settings.screen_width - 2 * star_width
	number_stars_x = int(available_space_x / (2 * star_width))
	return number_stars_x
	
def create_star(ai_settings, screen, stars, star_number, row_number):
	"""Создает звезды"""
	star = Stars(ai_settings, screen)
	star_width = star.rect.width
	star.x = star_width + 2 * star_width * star_number
	star.rect.x = star.x
	star.rect.y = star.rect.height +  2 * star.rect.height * row_number
	stars.add(star)

def get_number_rows_stars(ai_settings, star_height):
	"""Определяет кол-во рядов помещяющихся на экране"""
	available_space_y = (ai_settings.screen_height -
						(3 * star_height))
	number_rows = int(available_space_y / (star_height))
	return number_rows

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
	"""Обрабатывает столкновения корабля с пришельцем"""
	if stats.ship_left > 0:
		# Уменьшение ships_left
		stats.ship_left -= 1
		# Обновление игровой информации
		sb.prep_ships()
	
		# Очистка списков пришельцев и пуль
		aliens.empty()
		bullets.empty()
	
		# Создание нового флота и размещение корабля в центре
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		# Пауза
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
	"""Проверяет, появился ли новый рекорд"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()

def dump_high_score(stats):
	"""Записывает рекорд в файл"""
	if stats.high_score > stats.return_high_score():
		with open('high_score/high_score.json', 'w') as hs:
				json.dump(stats.high_score, hs)




























