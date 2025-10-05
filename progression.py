"""
Wave Progression System

This module handles wave-based gameplay with increasing difficulty,
high scores, and player statistics.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import json
import os
from constants import *


class WaveManager:
    """
    Manages wave progression and difficulty scaling.
    """
    
    def __init__(self):
        """Initialize the wave manager."""
        self.current_wave = 1
        self.asteroids_remaining = 0
        self.asteroids_spawned = 0
        self.wave_complete = False
        self.wave_start_time = 0
        self.bonus_timer = 5.0  # Time to show wave completion bonus
        
    def start_wave(self, wave_number):
        """
        Start a new wave.
        
        Args:
            wave_number (int): Wave number to start
        """
        self.current_wave = wave_number
        self.asteroids_remaining = self._calculate_asteroid_count(wave_number)
        self.asteroids_spawned = 0
        self.wave_complete = False
        self.wave_start_time = pygame.time.get_ticks()
        
    def _calculate_asteroid_count(self, wave_number):
        """
        Calculate how many asteroids should spawn in this wave.
        
        Args:
            wave_number (int): Current wave number
            
        Returns:
            int: Number of asteroids for this wave
        """
        base_count = 4  # Starting asteroid count
        return base_count + (wave_number - 1) * WAVE_ASTEROID_INCREASE
    
    def get_wave_speed_multiplier(self):
        """
        Get the speed multiplier for this wave.
        
        Returns:
            float: Speed multiplier for asteroids
        """
        return WAVE_SPEED_INCREASE ** (self.current_wave - 1)
    
    def asteroid_destroyed(self):
        """Call when an asteroid is destroyed."""
        self.asteroids_remaining -= 1
        if self.asteroids_remaining <= 0:
            self.wave_complete = True
            self.bonus_timer = 5.0
    
    def update(self, dt):
        """
        Update wave state.
        
        Args:
            dt (float): Delta time since last frame
        """
        if self.wave_complete and self.bonus_timer > 0:
            self.bonus_timer -= dt
    
    def is_wave_complete(self):
        """
        Check if current wave is complete.
        
        Returns:
            bool: True if wave is complete
        """
        return self.wave_complete
    
    def should_advance_wave(self):
        """
        Check if we should advance to the next wave.
        
        Returns:
            bool: True if should advance to next wave
        """
        return self.wave_complete and self.bonus_timer <= 0
    
    def get_wave_bonus(self):
        """
        Calculate bonus points for completing the wave quickly.
        
        Returns:
            int: Bonus points
        """
        if not self.wave_complete:
            return 0
            
        time_taken = (pygame.time.get_ticks() - self.wave_start_time) / 1000.0
        max_bonus = 1000 * self.current_wave
        time_bonus = max(0, max_bonus - int(time_taken * 10))
        return time_bonus


class HighScoreManager:
    """
    Manages high scores and player statistics.
    """
    
    def __init__(self, filename="high_scores.json"):
        """
        Initialize the high score manager.
        
        Args:
            filename (str): File to store high scores
        """
        self.filename = filename
        self.high_scores = []
        self.player_stats = {
            'games_played': 0,
            'total_score': 0,
            'best_wave': 1,
            'asteroids_destroyed': 0,
            'enemies_destroyed': 0,
            'total_time_played': 0
        }
        self.load_data()
    
    def load_data(self):
        """Load high scores and statistics from file."""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.high_scores = data.get('high_scores', [])
                    self.player_stats = data.get('player_stats', self.player_stats)
        except (json.JSONDecodeError, IOError):
            # File doesn't exist or is corrupted, use defaults
            pass
    
    def save_data(self):
        """Save high scores and statistics to file."""
        try:
            data = {
                'high_scores': self.high_scores,
                'player_stats': self.player_stats
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            print("Warning: Could not save high scores")
    
    def add_score(self, score, wave_reached, player_name="Player"):
        """
        Add a new score to the high score list.
        
        Args:
            score (int): Final score
            wave_reached (int): Highest wave reached
            player_name (str): Player name
        """
        score_entry = {
            'name': player_name,
            'score': score,
            'wave': wave_reached,
            'date': pygame.time.get_ticks()
        }
        
        self.high_scores.append(score_entry)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10
        
        # Update statistics
        self.player_stats['games_played'] += 1
        self.player_stats['total_score'] += score
        self.player_stats['best_wave'] = max(self.player_stats['best_wave'], wave_reached)
        
        self.save_data()
    
    def update_stats(self, **kwargs):
        """
        Update player statistics.
        
        Args:
            **kwargs: Statistics to update
        """
        for key, value in kwargs.items():
            if key in self.player_stats:
                self.player_stats[key] += value
    
    def get_high_scores(self, count=10):
        """
        Get the top high scores.
        
        Args:
            count (int): Number of scores to return
            
        Returns:
            list: Top high scores
        """
        return self.high_scores[:count]
    
    def is_high_score(self, score):
        """
        Check if a score qualifies as a high score.
        
        Args:
            score (int): Score to check
            
        Returns:
            bool: True if it's a high score
        """
        if len(self.high_scores) < 10:
            return True
        return score > self.high_scores[-1]['score']


class ProgressionUI:
    """
    UI elements for displaying wave progression and statistics.
    """
    
    def __init__(self):
        """Initialize the progression UI."""
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_wave_info(self, screen, wave_manager):
        """
        Draw current wave information.
        
        Args:
            screen: Pygame screen surface
            wave_manager: WaveManager instance
        """
        # Wave number
        wave_text = self.font.render(f"Wave: {wave_manager.current_wave}", True, "white")
        screen.blit(wave_text, (SCREEN_WIDTH - wave_text.get_width() - 10, 10))
        
        # Asteroids remaining
        asteroids_text = self.font.render(f"Asteroids: {wave_manager.asteroids_remaining}", True, "white")
        screen.blit(asteroids_text, (SCREEN_WIDTH - asteroids_text.get_width() - 10, 50))
        
        # Wave completion bonus
        if wave_manager.wave_complete and wave_manager.bonus_timer > 0:
            bonus = wave_manager.get_wave_bonus()
            bonus_text = self.large_font.render(f"Wave Complete! Bonus: {bonus}", True, "yellow")
            text_x = SCREEN_WIDTH // 2 - bonus_text.get_width() // 2
            text_y = SCREEN_HEIGHT // 2 - 100
            screen.blit(bonus_text, (text_x, text_y))
    
    def draw_high_scores(self, screen, high_score_manager, y_offset=100):
        """
        Draw the high score table.
        
        Args:
            screen: Pygame screen surface
            high_score_manager: HighScoreManager instance
            y_offset (int): Y position offset
        """
        title = self.large_font.render("HIGH SCORES", True, "white")
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        screen.blit(title, (title_x, y_offset))
        
        scores = high_score_manager.get_high_scores(5)
        for i, score_entry in enumerate(scores):
            rank_text = f"{i+1}. {score_entry['name']}: {score_entry['score']} (Wave {score_entry['wave']})"
            score_surface = self.font.render(rank_text, True, "white")
            score_x = SCREEN_WIDTH // 2 - score_surface.get_width() // 2
            screen.blit(score_surface, (score_x, y_offset + 60 + i * 40))
    
    def draw_statistics(self, screen, high_score_manager):
        """
        Draw player statistics.
        
        Args:
            screen: Pygame screen surface
            high_score_manager: HighScoreManager instance
        """
        stats = high_score_manager.player_stats
        
        stat_texts = [
            f"Games Played: {stats['games_played']}",
            f"Total Score: {stats['total_score']}",
            f"Best Wave: {stats['best_wave']}",
            f"Asteroids Destroyed: {stats['asteroids_destroyed']}",
            f"Enemies Destroyed: {stats['enemies_destroyed']}"
        ]
        
        title = self.font.render("STATISTICS", True, "white")
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        screen.blit(title, (title_x, 350))
        
        for i, stat_text in enumerate(stat_texts):
            stat_surface = self.small_font.render(stat_text, True, "white")
            stat_x = SCREEN_WIDTH // 2 - stat_surface.get_width() // 2
            screen.blit(stat_surface, (stat_x, 390 + i * 25))