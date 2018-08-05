class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 700
        self.screen_color = (100,100, 100)

        self.ship_fleet_limit = 3

        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        self.fleet_drop_speed = 30
        #fleet direction represents right; -1 represents left.
        self.fleet_direction = 1

        # How quickly the game speed up
        self.speedup_scale = 1.5
        self.score_scale = 1.5

    def increase_speed(self):
        """Increase speed settings"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points =int(self.alien_points * self.score_scale)
        print(self.alien_points)

    def default_settings(self):
        self.ship_speed =  2
        self.bullet_speed = 3
        self.alien_speed =  0.5
        self.alien_points = 50





