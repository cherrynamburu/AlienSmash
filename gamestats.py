class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.high_score = 0
        self.game_active = False
        self.ships_left = self.ai_settings.ship_fleet_limit

    def reset_stats(self):
        """Initialize statistics that can change durings the game"""
        self.score = 0
        self.level = 1




