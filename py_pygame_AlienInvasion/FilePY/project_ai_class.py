# # Project Alien Invasion:


import pygame
import pygame.font
from pygame.sprite import Sprite
from pygame.sprite import Group

class Settings:
    """Клас для збереження всіх налаштувань гри"""
    def __init__(self):
        """Ініціалізувати постійні налаштування гри"""
        # Налаштування екрану
        self.background = pygame.image.load('../FileIMAGES/zoribg_img.jpeg') # 1200, 760
        self.screen_width = 1200
        self.screen_height = 760
        self.bg_color = (0, 0, 0) # update_screen (color)
                    #(self.screen.fill(self.settings.bg_color))

        # Налаштування корабля
        self.ship_speed = 2
        self.ship_limit = 3

        # Налаштування кулі
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 225, 77)
        self.bullet_allowed = 10

        # Налаштування прибульця
            # fleet_direction = 1 -- праворуч, -1 -- ліворуч
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Як швидко гра має прискорюватися
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        # Як швидко збільшується вартість прибульців
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """Ініціалізація змінних налаштувань"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction 1 представляє напрямок приворуч; -1 -- ліворуч;
        self.fleet_direction = 1

        # Отримано балів
        self.alien_points = 50

    def increase_speed(self):
        """Збільшення налаштувань швидкості та вартості прибульців"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)

class Ship(Sprite):
    """Клас для керування кораблем"""
    def __init__(self, ai_game):
        """Ініціалізувати корабель і встановити його вхідне положення"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Завантажити зображення корабля
        self.image = pygame.image.load('../FileIMAGES/spaceship.jpeg')
        self.rect = self.image.get_rect()

        # Створити кожен новий корабель внизу екрана, по центру
        self.rect.midbottom = self.screen_rect.midbottom

        # Зберегти десяткове значення для позиції корабля по горизонталі
        self.x = float(self.rect.x)

        # Індикатор руху
        self.moving_right = False
        self.moving_left= False
    
    def update(self):
        """Оновити поточну позицію коробля на основі індикаторів руху"""
        # Оновити значення ship.x, а не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Оновити об'єкт rect з self.x
        self.rect.x = self.x

    def center_ship(self):
        """Відцентрувати корабель на екрані"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Намалювати корабель у його поточному розташуванні"""
        self.screen.blit(self.image, self.rect)

class Bullet(Sprite):
    """Клас для керування кулями, випущеними з корабля"""
    def __init__(self, ai_game):
        """Створити об'єкт bullet у поточній позиції корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        
        # Створити rect кулі у (0, 0) та задати правильну позицію
        self.rect = pygame.Rect(0, 0,
            self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Зберігати позицію кулі як десяткове значення
        self.y = float(self.rect.y)

    def update(self):
        """Посунути кулю нагору екраном"""
        # Оновити десяткову позицію кулі
        self.y -= self.settings.bullet_speed
        # Оновити позицію rect
        self.rect.y = self.y

    def draw_bullet(self):
        """Намалювати кулю на екрані"""
        pygame.draw.rect(self.screen, self.color, self.rect)

class Alien(Sprite):
    """Клас, що представляє одного прибульця з флоту"""
    def __init__(self, ai_game):
        """Ініціалізувати прибульця та
        задати його початкове розташування"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribule
        self.image = pygame.image.load('../FileIMAGES/alien.png')
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien`s exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        """Повертає істину, якщо прибудець знаходиться на краю екрана"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
    
    def update(self):
        """Замість прибульця - ліворуч чи ліворуч"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

class GameStats:
    """Відстежувати статистики гри"""
    def __init__(self, ai_game):
        """Ініціалізація статистики"""
        self.settings = ai_game.settings
        self.reset_stats()

        # Розпочати гру в активному стані
        self.game_active = False
        
        # Рекорд не анульовується
        self.high_score = 0

    def reset_stats(self):
        """Ініціалізація статистики, що може змінюватися впродовж гри"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

class Button:
    """"""
    def __init__(self, ai_game, msg):
        """Ініціалізація атрибутів кнопки"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Задати розміри та властивості кнопки
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Створити об'єкт rect кнопки та відцентрувати його
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Повідомлення на кнопці треба показати лише один раз
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Перетворити текст на зображення та розмістити по центру кнопки"""
        self.msg_image = self.font.render(msg, True,
                                        self.text_color,
                                        self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Намалювати порожню кнопку, а тоді -- повідомлення"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Scoreboard:
    """Клас, що виводить рахунок"""

    def __init__(self, ai_game):
        """Ініціалізація атрибутів, пов'язаних із рахунком"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Налаштування шрифту для відображення рахунку
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Підготувати зображення з початкового рахунку
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
    
    def prep_score(self):
        """Перетворити рахунок на зображення"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                        self.text_color, self.settings.bg_color)

        # Показати рахунок у верхньому правому куті екрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Згенерувати рекорд у зображення"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                    self.text_color, self.settings.bg_color)
    
        # Відцентрувати рекорд по горизонталі
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def show_score(self):
        """Показати рахунок, рівень та кораблі на екрані"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Перевірити, чи встановлено новий рекорд"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
    
    def prep_level(self):
        """Перетворити рівень у зображення"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                self.text_color, self.settings.bg_color)
        
        # Розташування рівень під рахунком
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Показує, скільки лишилося кораблів"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)