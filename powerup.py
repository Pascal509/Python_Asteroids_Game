"""
Power-up System

This module contains the PowerUp class and PowerUpManager for handling
various power-ups that enhance player abilities.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from circleshape import CircleShape
from constants import *


class PowerUp(CircleShape):
    """
    Power-up items that provide temporary or permanent benefits to the player.
    """
    
    def __init__(self, x, y, powerup_type):
        """
        Initialize a power-up.
        
        Args:
            x (float): X position
            y (float): Y position
            powerup_type (str): Type of power-up (shield, speed, etc.)
        """
        super().__init__(x, y, POWERUP_SIZE)
        self.powerup_type = powerup_type
        self.velocity = pygame.Vector2(
            random.uniform(-POWERUP_SPEED, POWERUP_SPEED),
            random.uniform(-POWERUP_SPEED, POWERUP_SPEED)
        )
        self.rotation = 0
        self.rotation_speed = random.uniform(50, 150)  # Spinning effect
        
        # Color coding for different power-ups
        self.colors = {
            POWERUP_SHIELD: (0, 150, 255),      # Blue
            POWERUP_SPEED_BOOST: (255, 255, 0),       # Yellow
            POWERUP_RAPID_FIRE: (255, 100, 0),  # Orange
            POWERUP_SPREAD_SHOT: (255, 0, 255), # Magenta
            POWERUP_BOMB: (255, 0, 0)           # Red
        }
    
    def update(self, dt):
        """
        Update power-up position and rotation.
        
        Args:
            dt (float): Delta time since last frame
        """
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_around_screen()
    
    def draw(self, screen):
        """
        Draw the power-up as a rotating diamond/star shape.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        color = self.colors.get(self.powerup_type, (255, 255, 255))
        
        # Create diamond/star shape
        points = []
        for i in range(8):  # 8-pointed star
            angle = (self.rotation + i * 45) * math.pi / 180
            if i % 2 == 0:  # Outer points
                radius = self.radius
            else:  # Inner points
                radius = self.radius * 0.5
            
            x = self.position.x + radius * math.cos(angle)
            y = self.position.y + radius * math.sin(angle)
            points.append((x, y))
        
        # Draw the star shape
        pygame.draw.polygon(screen, color, points)
        
        # Draw inner circle for visibility
        pygame.draw.circle(screen, color, 
                          (int(self.position.x), int(self.position.y)), 
                          int(self.radius * 0.3), 2)


class PowerUpManager:
    """
    Manages power-up spawning and effects on the player.
    """
    
    def __init__(self):
        """Initialize the power-up manager."""
        self.powerups = pygame.sprite.Group()
        
    def maybe_spawn_powerup(self, x, y):
        """
        Maybe spawn a power-up at the given location.
        
        Args:
            x (float): X position to spawn at
            y (float): Y position to spawn at
        """
        if random.random() < POWERUP_SPAWN_CHANCE:
            powerup_type = random.choice([
                POWERUP_SHIELD,
                POWERUP_SPEED_BOOST,
                POWERUP_RAPID_FIRE,
                POWERUP_SPREAD_SHOT,
                POWERUP_BOMB
            ])
            powerup = PowerUp(x, y, powerup_type)
            PowerUp.containers = (self.powerups,)
            self.powerups.add(powerup)
    
    def update(self, dt):
        """
        Update all power-ups.
        
        Args:
            dt (float): Delta time since last frame
        """
        self.powerups.update(dt)
    
    def draw(self, screen):
        """
        Draw all power-ups.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        for powerup in self.powerups:
            powerup.draw(screen)
    
    def check_player_collision(self, player):
        """
        Check if player collides with any power-ups and apply effects.
        
        Args:
            player: Player object to check collision with
            
        Returns:
            str or None: Type of power-up collected, or None if no collision
        """
        for powerup in self.powerups:
            if player.collides_with(powerup):
                powerup_type = powerup.powerup_type
                powerup.kill()
                return powerup_type
        return None