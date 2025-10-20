# view.py

import tkinter as tk
from tkinter import messagebox

class GameView:
    """
    Creates and manages all the graphical interface widgets.
    """
    def __init__(self, root, crystals_for_victory):
        self.root = root
        root.title("⭐ Space Miner ⭐")
        root.geometry("400x500")
        root.resizable(False, False)

        # Colors
        self.color_bg = "#0B1609"
        self.color_crystal = "#00ffaa"
        self.color_text = "#ffffff"
        self.color_button_bg = "#013314"
        self.color_special_button = "#2d7231"
        
        root.config(bg=self.color_bg)
        
        self._create_widgets(crystals_for_victory)

    def _create_widgets(self, crystals_for_victory):
        # --- Frames for organization ---
        top_frame = tk.Frame(self.root, bg=self.color_bg)
        top_frame.pack(pady=5, fill="x")

        button_frame = tk.Frame(self.root, bg=self.color_bg)
        button_frame.pack(pady=10, fill="x")

        # --- Widgets ---
        self.title_label = tk.Label(top_frame, text="🚀 SPACE MINER 🚀", font=("Arial", 18, "bold"), bg=self.color_bg, fg=self.color_crystal)
        self.crystals_label = tk.Label(top_frame, text="", font=("Arial", 24, "bold"), bg=self.color_bg, fg=self.color_crystal)
        self.per_click_label = tk.Label(top_frame, text="", font=("Arial", 10), bg=self.color_bg, fg=self.color_text)
        self.auto_mine_label = tk.Label(top_frame, text="", font=("Arial", 10), bg=self.color_bg, fg=self.color_text)
        self.stats_label = tk.Label(top_frame, text="", font=("Arial", 9), bg=self.color_bg, fg="#cccccc")
        self.timer_label = tk.Label(top_frame, text="Time: 0s", font=("Arial", 12), bg=self.color_bg, fg=self.color_text)

        self.mine_button = tk.Button(button_frame, text="⛏️ MINE ASTEROID ⛏️", font=("Arial", 14, "bold"), width=20, height=1, bg=self.color_special_button, fg=self.color_text)
        self.upgrade_drill_button = tk.Button(button_frame, text="", font=("Arial", 10), width=35, bg=self.color_button_bg, fg=self.color_text)
        self.buy_robot_button = tk.Button(button_frame, text="", font=("Arial", 10), width=35, bg=self.color_button_bg, fg=self.color_text)
        self.upgrade_scanner_button = tk.Button(button_frame, text="", font=("Arial", 10), width=35, bg=self.color_button_bg, fg=self.color_text)
        self.victory_button = tk.Button(button_frame, text=f"🏆 COMPLETE MISSION 🏆\n({crystals_for_victory:,} crystals)", font=("Arial", 11, "bold"), width=35, bg="#2a5a2a", fg=self.color_text)
        self.infinite_mode_button = tk.Button(button_frame, text="🌌 INFINITE EXPLORATION 🌌", font=("Arial", 12, "bold"), width=35, bg="#1a1a5a", fg=self.color_text, state=tk.DISABLED)

        # --- Layout ---
        self.title_label.pack(pady=(5,0))
        self.crystals_label.pack(pady=5)
        self.per_click_label.pack()
        self.auto_mine_label.pack()
        self.stats_label.pack(pady=(5,5))
        self.timer_label.pack()

        self.mine_button.pack(pady=15)
        self.upgrade_drill_button.pack(pady=3)
        self.buy_robot_button.pack(pady=3)
        self.upgrade_scanner_button.pack(pady=3)
        self.victory_button.pack(pady=10)

    def update_info(self, model):
        """Updates all labels and button states with data from the model."""
        self.crystals_label.config(text=f"💎 {int(model.crystals):,} Crystals")
        self.per_click_label.config(text=f"⛏️ Per click: {model.get_crystals_per_click()} crystals")
        self.auto_mine_label.config(text=f"🤖 Auto-mining: {model.automatic_income:,} crystals/sec")

        progress = min(100, (model.crystals / model.crystals_for_victory) * 100)
        stats_text = f"📊 Progress: {progress:.1f}% | Asteroids: {model.asteroids_mined} | Clicks: {model.total_clicks}"
        self.stats_label.config(text=stats_text)

        # Update buttons
        self._update_button_state(self.upgrade_drill_button, model.crystals >= model.drill_upgrade_cost, model)
        self._update_button_state(self.buy_robot_button, model.crystals >= model.robot_miner_cost, model)
        self._update_button_state(self.upgrade_scanner_button, model.crystals >= model.scanner_cost, model)
        
        if not model.is_infinite_mode:
            self.victory_button.config(state=tk.NORMAL if model.can_complete_mission() else tk.DISABLED)

    def update_button_texts(self, model):
        self.upgrade_drill_button.config(text=f"🔧 Upgrade Drill (Level {model.drill_level})\nCost: {model.drill_upgrade_cost:,} crystals")
        self.buy_robot_button.config(text=f"🤖 Buy Mining Robot (Own: {model.robot_miner_level})\nCost: {model.robot_miner_cost:,} crystals")
        
        scanner_bonus = model.scanner_level * model.scanner_efficiency
        scanner_text = f"📡 Upgrade Scanner (Level {model.scanner_level}"
        if model.scanner_level > 0:
            scanner_text += f" - +{scanner_bonus} crystals"
        scanner_text += f")\nCost: {model.scanner_cost:,} crystals"
        self.upgrade_scanner_button.config(text=scanner_text)

    def _update_button_state(self, button, can_afford, model):
        """Enables or disables a button based on a condition."""
        if model.is_game_active or model.is_infinite_mode:
            button.config(state=tk.NORMAL if can_afford else tk.DISABLED)
        else:
            button.config(state=tk.DISABLED)

    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def show_victory(self, time_str, model):
        message = (f"🎉 CONGRATULATIONS, MINER! 🎉\n\n"
                   f"⏱️ Time: {time_str}\n"
                   f"⛏️ Asteroids mined: {model.asteroids_mined}\n"
                   f"🤖 Robots deployed: {model.robot_miner_level}\n"
                   f"💎 Total crystals: {int(model.crystals):,}")
        self.show_message("🏆 MISSION COMPLETE! 🏆", message)
        self.infinite_mode_button.pack(pady=5)
        self.victory_button.config(state=tk.DISABLED)