import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from gamestats import GameStats
from button import Button
from score_board import Scoreboard


def run_game():
    # initialize pygame ,settings and screen object
    pygame.init()
    ai_settings = Settings()
    ai_settings.default_settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    # make ship
    ship = Ship(ai_settings , screen)
    bullets = Group()
    aliens = Group()
    # Create the fleet of aliens
    gf.create_fleet(ai_settings , screen ,ship , aliens)
    # start the main loop for the game
    #stats = GameStats(ai_settings)
    stats = GameStats(ai_settings)
    play_button = Button(ai_settings, screen, "Play")
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        # watch for the keyword and mouse events
        gf.get_events(ai_settings,screen ,stats, sb, play_button, ship, bullets )
        if stats.game_active:
            pygame.mouse.set_visible(False)
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, stats, sb, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats ,ship ,aliens , sb, bullets,play_button)


run_game()

