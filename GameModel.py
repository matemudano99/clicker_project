# model.py

class GameModel:
    """
    Contains the game's state and logic, without any GUI code.
    """
    def __init__(self):
        # Game variables
        self.crystals = 0
        self.drill_level = 1
        self.drill_upgrade_cost = 15
        self.base_crystals_per_click = 1

        self.robot_miner_level = 0
        self.robot_miner_cost = 50
        self.crystals_per_robot = 2
        self.automatic_income = 0

        self.scanner_level = 0
        self.scanner_cost = 100
        self.scanner_efficiency = 2  # Extra crystals per level

        # Game state
        self.crystals_for_victory = 25000
        self.is_game_active = True
        self.is_infinite_mode = False

        # Statistics
        self.total_clicks = 0
        self.asteroids_mined = 0

    def get_crystals_per_click(self):
        """Calculates how many crystals are earned in a single click."""
        base = self.base_crystals_per_click + (self.drill_level - 1) * 2
        scanner_bonus = self.scanner_level * self.scanner_efficiency
        return base + scanner_bonus

    def mine_asteroid(self):
        """Processes a mining click."""
        crystals_earned = self.get_crystals_per_click()
        self.crystals += crystals_earned
        self.total_clicks += 1
        self.asteroids_mined += 1
        return crystals_earned

    def upgrade_drill(self):
        """Attempts to upgrade the drill if there are enough crystals."""
        if self.crystals >= self.drill_upgrade_cost:
            self.crystals -= self.drill_upgrade_cost
            self.drill_level += 1
            self.drill_upgrade_cost = int(self.drill_upgrade_cost * 2.2)
            return True
        return False

    def buy_robot(self):
        """Attempts to buy a robot if there are enough crystals."""
        if self.crystals >= self.robot_miner_cost:
            self.crystals -= self.robot_miner_cost
            self.robot_miner_level += 1
            self.robot_miner_cost = int(self.robot_miner_cost * 2.5)
            self._recalculate_automatic_mining()
            return True
        return False

    def upgrade_scanner(self):
        """Attempts to upgrade the scanner if there are enough crystals."""
        if self.crystals >= self.scanner_cost:
            self.crystals -= self.scanner_cost
            self.scanner_level += 1
            self.scanner_cost = int(self.scanner_cost * 3.0)
            return True
        return False

    def _recalculate_automatic_mining(self):
        """Updates passive income based on the number of robots."""
        self.automatic_income = self.robot_miner_level * self.crystals_per_robot
    
    def automatic_mining_tick(self):
        """Adds automatically generated crystals in one 'tick'."""
        if self.is_game_active or self.is_infinite_mode:
            self.crystals += self.automatic_income

    def can_complete_mission(self):
        """Checks if the crystal goal has been reached."""
        return self.crystals >= self.crystals_for_victory

    def activate_infinite_mode(self):
        self.is_infinite_mode = True
        self.is_game_active = False