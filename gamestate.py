"""
Game State Manager

Handles game state, scoring, lives, and UI elements.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
from constants import *


class GameState:
    """
    Manages the overall game state including score, lives, and UI.
    """
    
    def __init__(self):
        """Initialize game state."""
        self.score = 0
        self.lives = PLAYER_LIVES
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.game_over = False
        
    def add_score(self, points):
        """
        Add points to the player's score.
        
        Args:
            points (int): Points to add
        """
        self.score += points
        
    def lose_life(self):
        """
        Remove one life from the player.
        
        Returns:
            bool: True if player still has lives, False if game over
        """
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            return False
        return True
        
    def reset_game(self):
        """Reset game state for a new game."""
        self.score = 0
        self.lives = PLAYER_LIVES
        self.game_over = False
        
    def draw_ui(self, screen):
        """
        Draw the game UI including score, lives, and game over screen.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        if self.game_over:
            # Game over screen
            game_over_text = self.large_font.render("GAME OVER", True, "white")
            score_text = self.font.render(f"Final Score: {self.score}", True, "white")
            restart_text = self.font.render("Press R to Restart", True, "white")
            
            # Center the text
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - 100))
            screen.blit(score_text, 
                       (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - 30))
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 + 30))
        else:
            # In-game UI
            score_text = self.font.render(f"Score: {self.score}", True, "white")
            lives_text = self.font.render(f"Lives: {self.lives}", True, "white")
            
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))
    
    def draw_phase3_ui(self, screen, player, weapon_manager, bomb_manager):
        """
        Draw Phase 3 UI elements including weapon type, power-ups, and bomb count.
        
        Args:
            screen: Pygame screen surface to draw on
            player: Player object to check status
            weapon_manager: Weapon manager for current weapon
            bomb_manager: Bomb manager for bomb count
        """
        if self.game_over:
            return
            
        y_offset = 90  # Start below basic UI
        
        # Current weapon display
        if weapon_manager:
            weapon_text = self.font.render(f"Weapon: {weapon_manager.current_weapon.title()}", True, "white")
            screen.blit(weapon_text, (10, y_offset))
            y_offset += 30
        
        # Bomb count
        if bomb_manager:
            bomb_text = self.font.render(f"Bombs: {MAX_BOMBS - bomb_manager.get_bomb_count()}", True, "white")
            screen.blit(bomb_text, (10, y_offset))
            y_offset += 30
        
        # Active power-up effects
        if player.is_shielded():
            shield_time = max(0, player.shield_timer)
            shield_text = self.font.render(f"Shield: {shield_time:.1f}s", True, (0, 150, 255))
            screen.blit(shield_text, (10, y_offset))
            y_offset += 30
            
        if player.speed_boost_timer > 0:
            speed_time = max(0, player.speed_boost_timer)
            speed_text = self.font.render(f"Speed Boost: {speed_time:.1f}s", True, (255, 255, 0))
            screen.blit(speed_text, (10, y_offset))
            y_offset += 30
            
        # Controls help (top right corner)
        help_texts = [
            "WASD/Arrows: Move",
            "Space: Shoot",
            "X: Drop Bomb",
            "Power-ups: Auto-collect"
        ]
        
        for i, text in enumerate(help_texts):
            help_surface = self.font.render(text, True, (150, 150, 150))
            screen.blit(help_surface, (SCREEN_WIDTH - help_surface.get_width() - 10, 10 + i * 25))