import pygame


class Ship():

    def __init__(self, ai_settings, screen):
        """initialize the ship and starting position"""
        self.screen = screen
        # load the ship image and get it rect.
        self.image = pygame.image.load('images/myship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        # start each new ship at the bottom of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.ai_settings = ai_settings
        self.move_right = False
        self.move_left = False

    def blitme(self):
        """Draw ship in curent location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += self.ai_settings.ship_speed
        if self.move_left and self.rect.left > 0:
            self.rect.centerx -= self.ai_settings.ship_speed

    def center_ship(self):
        """Center the ship on the screen."""

        self.rect.centerx = self.screen_rect.centerx