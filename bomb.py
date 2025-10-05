"""
Bomb System

This module contains the Bomb class and BombManager for handling
area-of-effect explosive weapons.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import math
import random
from circleshape import CircleShape
from constants import *


class Bomb(CircleShape):
    """
    Explosive bomb that damages multiple asteroids in an area.
    """
    
    def __init__(self, x, y):
        """
        Initialize a bomb.
        
        Args:
            x (float): X position
            y (float): Y position
        """
        super().__init__(x, y, 10)  # Small initial size
        self.timer = 2.0  # 2 second fuse
        self.exploded = False
        self.explosion_radius = 0
        self.max_explosion_radius = BOMB_RADIUS
        self.explosion_speed = 300  # How fast explosion grows
        
    def update(self, dt):
        """
        Update bomb timer and explosion.
        
        Args:
            dt (float): Delta time since last frame
        """
        if not self.exploded:
            self.timer -= dt
            if self.timer <= 0:
                self.exploded = True
        else:
            # Grow explosion
            self.explosion_radius += self.explosion_speed * dt
            if self.explosion_radius >= self.max_explosion_radius:
                self.kill()
    
    def draw(self, screen):
        """
        Draw the bomb or its explosion.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        if not self.exploded:
            # Draw bomb with pulsing effect
            pulse = 0.8 + 0.2 * math.sin(self.timer * 10)
            radius = int(self.radius * pulse)
            
            # Red bomb with timer indicator
            color_intensity = max(100, int(255 * (self.timer / 2.0)))
            color = (255, color_intensity, color_intensity)
            
            pygame.draw.circle(screen, color, 
                             (int(self.position.x), int(self.position.y)), radius)
            pygame.draw.circle(screen, (255, 0, 0), 
                             (int(self.position.x), int(self.position.y)), radius, 2)
        else:
            # Draw explosion effect
            if self.explosion_radius < self.max_explosion_radius:
                # Expanding explosion ring
                alpha = 1.0 - (self.explosion_radius / self.max_explosion_radius)
                color_value = int(255 * alpha)
                
                # Draw multiple rings for better effect
                for i in range(3):
                    ring_radius = max(1, int(self.explosion_radius - i * 10))
                    ring_color = (255, color_value // (i + 1), 0)
                    
                    if ring_radius > 0:
                        pygame.draw.circle(screen, ring_color,
                                         (int(self.position.x), int(self.position.y)),
                                         ring_radius, 3)
    
    def get_damage_radius(self):
        """
        Get the current damage radius of the bomb.
        
        Returns:
            float: Current damage radius
        """
        if self.exploded:
            return min(self.explosion_radius, BOMB_DAMAGE_RADIUS)
        return 0


class BombManager:
    """
    Manages bomb deployment and explosions.
    """
    
    def __init__(self):
        """Initialize the bomb manager."""
        self.bombs = pygame.sprite.Group()
        self.bomb_cooldown = 0
        
    def can_drop_bomb(self):
        """
        Check if a bomb can be dropped.
        
        Returns:
            bool: True if bomb can be dropped
        """
        return self.bomb_cooldown <= 0 and len(self.bombs) < MAX_BOMBS
    
    def drop_bomb(self, x, y):
        """
        Drop a bomb at the specified location.
        
        Args:
            x (float): X position to drop bomb
            y (float): Y position to drop bomb
        """
        if self.can_drop_bomb():
            bomb = Bomb(x, y)
            self.bombs.add(bomb)
            self.bomb_cooldown = BOMB_COOLDOWN
    
    def update(self, dt):
        """
        Update all bombs and cooldown.
        
        Args:
            dt (float): Delta time since last frame
        """
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= dt
            
        self.bombs.update(dt)
    
    def draw(self, screen):
        """
        Draw all bombs.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        for bomb in self.bombs:
            bomb.draw(screen)
    
    def check_explosions(self, asteroids):
        """
        Check which asteroids are caught in bomb explosions.
        
        Args:
            asteroids (pygame.sprite.Group): Group of asteroids to check
            
        Returns:
            list: List of asteroids caught in explosions
        """
        destroyed_asteroids = []
        
        for bomb in self.bombs:
            if bomb.exploded:
                damage_radius = bomb.get_damage_radius()
                if damage_radius > 0:
                    for asteroid in asteroids:
                        distance = (asteroid.position - bomb.position).length()
                        if distance <= damage_radius + asteroid.radius:
                            if asteroid not in destroyed_asteroids:
                                destroyed_asteroids.append(asteroid)
        
        return destroyed_asteroids
    
    def get_bomb_count(self):
        """
        Get the current number of active bombs.
        
        Returns:
            int: Number of active bombs
        """
        return len(self.bombs)