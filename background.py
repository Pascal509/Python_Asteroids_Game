"""
Background System

This module contains the Background class for creating a starfield
background that moves with parallax scrolling.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from constants import *


class Star:
    """
    Individual star in the background.
    """
    
    def __init__(self):
        """Initialize a star with random properties."""
        self.x = random.uniform(0, SCREEN_WIDTH)
        self.y = random.uniform(0, SCREEN_HEIGHT)
        self.brightness = random.uniform(0.3, 1.0)
        self.size = random.choice([1, 1, 1, 2, 2, 3])  # Weighted towards smaller stars
        self.twinkle_speed = random.uniform(1.0, 3.0)
        self.twinkle_offset = random.uniform(0, 6.28)  # Random phase
        
    def update(self, dt, player_velocity):
        """
        Update star position with parallax effect.
        
        Args:
            dt (float): Delta time since last frame
            player_velocity (pygame.Vector2): Player's current velocity
        """
        # Move stars opposite to player movement for parallax effect
        parallax_factor = STAR_SPEED_MULTIPLIER * (self.size / 3.0)  # Larger stars move more
        self.x -= player_velocity.x * parallax_factor * dt
        self.y -= player_velocity.y * parallax_factor * dt
        
        # Wrap around screen
        if self.x < -10:
            self.x = SCREEN_WIDTH + 10
            self.y = random.uniform(0, SCREEN_HEIGHT)
        elif self.x > SCREEN_WIDTH + 10:
            self.x = -10
            self.y = random.uniform(0, SCREEN_HEIGHT)
            
        if self.y < -10:
            self.y = SCREEN_HEIGHT + 10
            self.x = random.uniform(0, SCREEN_WIDTH)
        elif self.y > SCREEN_HEIGHT + 10:
            self.y = -10
            self.x = random.uniform(0, SCREEN_WIDTH)
    
    def draw(self, screen, time):
        """
        Draw the star with twinkling effect.
        
        Args:
            screen: Pygame screen surface to draw on
            time (float): Current game time for twinkling
        """
        # Calculate twinkling brightness
        twinkle = 0.5 + 0.5 * abs(math.sin(time * self.twinkle_speed + self.twinkle_offset))
        brightness = self.brightness * twinkle
        
        # Color based on brightness
        color_value = int(255 * brightness)
        
        if self.size == 1:
            # Single pixel star
            pygame.draw.circle(screen, (color_value, color_value, color_value),
                             (int(self.x), int(self.y)), 1)
        elif self.size == 2:
            # Small cross pattern
            pygame.draw.circle(screen, (color_value, color_value, color_value),
                             (int(self.x), int(self.y)), 1)
            # Add slight cross effect for brighter stars
            if brightness > 0.7:
                pygame.draw.line(screen, (color_value // 2, color_value // 2, color_value // 2),
                               (self.x - 2, self.y), (self.x + 2, self.y))
                pygame.draw.line(screen, (color_value // 2, color_value // 2, color_value // 2),
                               (self.x, self.y - 2), (self.x, self.y + 2))
        else:
            # Larger star with cross pattern
            pygame.draw.circle(screen, (color_value, color_value, color_value),
                             (int(self.x), int(self.y)), 2)
            # Cross effect
            pygame.draw.line(screen, (color_value, color_value, color_value),
                           (self.x - 3, self.y), (self.x + 3, self.y))
            pygame.draw.line(screen, (color_value, color_value, color_value),
                           (self.x, self.y - 3), (self.x, self.y + 3))


class Background:
    """
    Scrolling starfield background.
    """
    
    def __init__(self):
        """Initialize the background with stars."""
        self.stars = []
        self.time = 0
        
        # Create stars
        for _ in range(BACKGROUND_STAR_COUNT):
            self.stars.append(Star())
    
    def update(self, dt, player_velocity=pygame.Vector2(0, 0)):
        """
        Update background animation.
        
        Args:
            dt (float): Delta time since last frame
            player_velocity (pygame.Vector2): Player's current velocity for parallax
        """
        self.time += dt
        
        # Update all stars
        for star in self.stars:
            star.update(dt, player_velocity)
    
    def draw(self, screen):
        """
        Draw the background.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Draw all stars
        for star in self.stars:
            star.draw(screen, self.time)