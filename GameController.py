# controller.py

import time
import tkinter as tk
from GameModel import GameModel
from GameView import GameView

class GameController:
    def __init__(self, root):
        self.model = GameModel()
        self.view = GameView(root, self.model.crystals_for_victory)
        self.root = root
        
        self.start_time = time.time()
        self._bind_events()
        
        # Start game loops
        self.update_all()
        self._mining_tick()
        self._update_timer()

    def _bind_events(self):
        """Assigns functions to the button commands."""
        self.view.mine_button.config(command=self.mine_asteroid)
        self.view.upgrade_drill_button.config(command=self.upgrade_drill)
        self.view.buy_robot_button.config(command=self.buy_robot)
        self.view.upgrade_scanner_button.config(command=self.upgrade_scanner)
        self.view.victory_button.config(command=self.complete_mission)
        self.view.infinite_mode_button.config(command=self.activate_infinite_mode)

    def mine_asteroid(self):
        crystals_earned = self.model.mine_asteroid()
        
        # Temporary visual feedback on the button
        original_text = self.view.mine_button.cget("text")
        self.view.mine_button.config(text=f"💎 +{crystals_earned} crystals! 💎")
        self.root.after(300, lambda: self.view.mine_button.config(text=original_text))
        
        self.update_all()

    def upgrade_drill(self):
        if self.model.upgrade_drill():
            self.update_all()

    def buy_robot(self):
        if self.model.buy_robot():
            self.update_all()

    def upgrade_scanner(self):
        if self.model.upgrade_scanner():
            self.update_all()

    def complete_mission(self):
        if self.model.can_complete_mission():
            self.model.is_game_active = False
            final_time = int(time.time() - self.start_time)
            minutes = final_time // 60
            seconds = final_time % 60
            time_str = f"{minutes}m {seconds}s"
            
            self.view.show_victory(time_str, self.model)
            self.update_all()
        else:
            needed = self.model.crystals_for_victory - self.model.crystals
            self.view.show_message("Mission Incomplete", f"❗ You need {needed:,.0f} more crystals.")

    def activate_infinite_mode(self):
        self.model.activate_infinite_mode()
        self.view.show_message(
            "Infinite Mode Activated",
            "🚀 Welcome to infinite exploration!\nYou can now continue mining without limits."
        )
        self.view.infinite_mode_button.config(state=tk.DISABLED)
        self.update_all()

    def update_all(self):
        """Central function to refresh the entire UI."""
        self.view.update_info(self.model)
        self.view.update_button_texts(self.model)

    def _mining_tick(self):
        """Loop for automatic mining."""
        self.model.automatic_mining_tick()
        self.update_all()
        self.root.after(1000, self._mining_tick)

    def _update_timer(self):
        """Loop for the timer."""
        if self.model.is_game_active:
            elapsed_time = int(time.time() - self.start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            self.view.timer_label.config(text=f"Time: {minutes}m {seconds}s")
            self.root.after(1000, self._update_timer)
        elif self.model.is_infinite_mode:
            self.view.timer_label.config(text="🌌 Infinite Exploration Active 🌌")