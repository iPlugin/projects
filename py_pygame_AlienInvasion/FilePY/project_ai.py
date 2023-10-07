# # Project Alien Invasion:


import sys
from time import sleep

import pygame

from project_ai_class import Settings
from project_ai_class import Ship
from project_ai_class import Bullet
from project_ai_class import Alien
from project_ai_class import GameStats
from project_ai_class import Button
from project_ai_class import Scoreboard

class AlienInvasion:
    """Загальний клас, що керує русурсами та поведінкою гри"""
    def __init__(self):
        """Ініціалізувати гру, створити ресурси гри"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width, self.settings.screen_height))
                                        # + ...), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width # FullScreen
        #self.settings.screen_height = self.screen.get_rect().height # FullScreen

        namegame = "Alien Invasion"
        pygame.display.set_caption(namegame)
        icon = pygame.image.load('../FileIMAGES/icon.png')
        pygame.display.set_icon(icon)

        # Створити екземляр для збереження ігрової статистики та табло на екрані
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.create_fleet()

        # Створити кнопку PLAY
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Розпочати головний цикл гри"""
        while True:
            self.check_events()
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()
            self.update_screen()
    
    def check_events(self):
        """Реагувати на натискання клавіш та подій миші"""
        # Слідкувати за подіями миші та клавітури
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
    
    def _check_keydown_events(self, event):
        """Реагувати на натискання клавіш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        """Реагувати, коли клавіша не натиснута"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        
    def _check_play_button(self, mouse_pos):
        """Розпочати нову гру, коли користувач написне кнопку Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Анулювати статистику гри
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Позбавитися надлишку прибульців та куль
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати кораблем
            self.create_fleet()
            self.ship.center_ship()

            # Приховати курсор миші
            pygame.mouse.set_visible(False)

    def _ship_hit(self):
        """Реагувати на зіткнення прибульців з кораблем"""
        if self.stats.ships_left > 0:
            # Зменшити ships_left та оновити табло
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Позбавитися надлишку прибульців та куль
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель
            self.create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_bullets(self):
        """Оновити позицію куль та позбавитися старих куль"""
        # Оновити позиції куль
        self.bullets.update()

        # Позбавитися куль, що зникли
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) - кількість куль в грі
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Реакція на зіткнення куль з прибульцями"""
        # Перевірити, чи котрась із куль не влучила у прибульця
        # Якщо влучила, позбавитися кулі та прибульця
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Знищити наявні кулі та створити новий флот
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()

            # Збільшити рівень
            self.stats.level += 1
            self.sb.prep_level()

    def _fire_bullet(self):
        """Створити нову кулю та додати її до групи куль"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def create_fleet(self):
        """Створити флот прибульців"""
        # Створити прибульців та визначити кількість прибульців у ряду
        # Відстань між прибульцями дорівнює ширені одного прибульця
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Визначити, яка кількість рядків прибульців поміщається на екрані
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - 
                            (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Створити повний флот прибульців
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)
    
    def create_alien(self, alien_number, row_number):
        """Створити прибульця та поставити його до ряду"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def update_aliens(self):
        """Перевірити, чи флот знаходиться на краю,
        тоді оновити позиції всії прибульців у флоті"""
        self._check_fleet_edges()
        self.aliens.update()

        # Шукати зіткнення куль із прибуляцями
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Шукати, чи котрийсь із прибульців досяг нижнього краю екрану
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Перевірити, чи не досяг якийсь прибулець нижнього краю екрану"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Зреагувати так, ніби корабель було підбито
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Реагує відповідно до того,
        чи досяг котрийсь зі прибульців краю екрану"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._check_fleet_direction()
                break

    def _check_fleet_direction(self):
        """Спуск всього флоту та зміна його напрямку"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def update_screen(self): 
        """Оновити зображення на екрані та перемкнути на новий екран"""
        # Наново перемалювати екран на кожній ітерації циклу
        self.screen.blit(self.settings.background, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Намалювати інформацію про рахунок
        self.sb.show_score()

        # Намалювати кнопку Play, якщо гра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Показати остайній намальований екран
        pygame.display.flip()

if __name__ == '__main__':
    # Створити екземпляр гри та запустити гру
    ai = AlienInvasion()
    ai.run_game()