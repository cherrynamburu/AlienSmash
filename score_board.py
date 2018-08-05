import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard():
    """A class to report scoring"""
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # font settings for scorings
        self.text_color  = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        #self.prep_ships()
        self.show_ships()


    def prep_score(self):
        #rounded_score = int(round(self.stats.score, -1))
        #score_str = "{:,}".format(rounded_score)

        score_str = str(self.stats.score)
        self.score_image = self.font.render(
            score_str, True,self.text_color, self.ai_settings.screen_color)
    # display the score at the top right corner
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right =self.screen_rect.right- 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        #self.ships.draw(self.screen)
        self.screen.blit(self.ship_score_image, self.ship_score_rect)

    def prep_high_score(self):
        """Turn high score into a rendered image"""
        #high_score = int(round(self.stats.high_score, -1))
        self.high_score_string = str(self.stats.high_score)
        self.high_score_image = self.font.render(
            self.high_score_string, True, self.text_color,
            self.ai_settings.screen_color)
        # center the high score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(
            str(self.stats.level), True,
            self.text_color, self.ai_settings.screen_color)
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_num in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_num * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_ships(self):
        #rounded_score = int(round(self.stats.score, -1))
        #score_str = "{:,}".format(rounded_score)
        #if self.stats.schips_left >= 2:
            ship_score_str = str(self.stats.ships_left)
        #if self.stats.ships_left == 0:
            #ship_score_str = str(self.stats.ships_left - 1)
            self.ship_score_image = self.font.render(
                ship_score_str, True,self.text_color, self.ai_settings.screen_color)
            # display the score at the top right corner
            self.ship_score_rect = self.ship_score_image.get_rect()
            self.ship_score_rect.left =self.screen_rect.left + 20
            self.ship_score_rect.top = 20
