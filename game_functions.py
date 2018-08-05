import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def get_events(ai_settings, screen, stats, sb, play_button, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, sb, ai_settings, play_button, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            if event.key  == pygame.K_RIGHT:
                ship.move_right = True
            elif event.key == pygame.K_LEFT:
                ship.move_left = True
            elif event.key == pygame.K_SPACE:
                if len(bullets) < ai_settings.bullets_allowed:
                    new_bullet = Bullet(ai_settings, screen, ship)
                    bullets.add(new_bullet)
            elif event.key == pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_UP:
                if stats.game_active:
                    stats.game_active = False
                else:
                    sleep(0.5)
                    stats.game_active = True


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.move_right = False
            elif event.key == pygame.K_LEFT:
                ship.move_left = False


def check_play_button(stats, sb, ai_settings, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True
        sb.prep_score()
        #sb.prep_high_score()
        sb.prep_level()
        stats.ships_left = ai_settings.ship_fleet_limit
        sb.show_ships()

def update_screen(ai_settings , screen ,stats,
                  ship , aliens , sb, bullets, play_button):
    screen.fill(ai_settings.screen_color)
    ship.blitme()
    aliens.draw(screen)
    if stats.game_active:
        for bullet in bullets.sprites():
            bullet.draw_bullet()

    # draw the play button if the game is inactive
    if not stats.game_active:
        bullets.empty()
        play_button.draw_button()

    sb.show_score()


    # make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, stats, sb, aliens, bullets):
    bullets.update()
    # get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, stats, sb, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, stats, sb, aliens, bullets):
    """Respond to bullet-alien collisions."""

    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points *  len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings , alien_width):
    """Determine the no of aliens in a row"""
    available_space_x = ai_settings.screen_width - 2* alien_width
    number_aliens_x = int(available_space_x / 2* alien_width)
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine no of rows that fit in the screen"""
    available_space_y = (
        ai_settings.screen_height - (3* alien_height)- ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def create_alien(ai_settings , screen , aliens , alien_number , row_number):
    """Create an alien and place it in a row"""
    alien = Alien( ai_settings ,screen )
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width  * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(ai_settings , screen)
    number_aliens_x = 6#get_number_aliens_x(ai_settings , alien.rect.width)
    number_rows = 3#get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Create the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_fleet_edges(ai_settings, aliens):
    """Respond appx if any lines have reached edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop entire fleet and change directions"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, stats, screen, sb,ship, aliens, bullets):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien."""

    if stats.ships_left >= 2:
        # Decrement ships_left.
        stats.ships_left -= 1
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        sb.show_ships()
        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        # Pause.
        sleep(1)
    else:
        stats.ships_left -= 1
        sb.show_ships()
        sleep(3)
        stats.game_active = False
        aliens.empty()
        stats.reset_stats()
        ai_settings.default_settings()
        ship.center_ship()
        create_fleet(ai_settings, screen, ship, aliens)
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            sb.prep_high_score()












