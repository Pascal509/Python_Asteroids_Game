"""
Weapon System

This module contains different weapon types and the WeaponManager class
for handling various shooting patterns and weapon behaviors.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import math
from shot import Shot
from constants import *


class Laser:
    """
    Laser beam weapon that fires instant-hit beams.
    """
    
    def __init__(self, start_pos, direction, range_limit=LASER_RANGE):
        """
        Initialize a laser beam.
        
        Args:
            start_pos (pygame.Vector2): Starting position
            direction (pygame.Vector2): Direction vector (normalized)
            range_limit (float): Maximum laser range
        """
        self.start_pos = pygame.Vector2(start_pos)
        self.end_pos = start_pos + (direction * range_limit)
        self.width = LASER_WIDTH
        self.lifetime = 0.1  # Very short visual effect
        self.age = 0
        
    def update(self, dt):
        """
        Update laser beam (just lifetime tracking).
        
        Args:
            dt (float): Delta time since last frame
        """
        self.age += dt
        return self.age < self.lifetime
    
    def draw(self, screen):
        """
        Draw the laser beam.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Draw laser as a line with some transparency effect
        alpha = max(0, 255 * (1 - self.age / self.lifetime))
        color = (255, 50, 50, int(alpha))  # Red laser with fade
        
        # Draw main beam
        pygame.draw.line(screen, (255, 50, 50), 
                        self.start_pos, self.end_pos, self.width)
        
        # Draw bright core
        pygame.draw.line(screen, (255, 200, 200), 
                        self.start_pos, self.end_pos, max(1, self.width // 2))


class WeaponManager:
    """
    Manages different weapon types and shooting patterns.
    """
    
    def __init__(self):
        """Initialize the weapon manager."""
        self.current_weapon = WEAPON_NORMAL
        self.shoot_cooldown = 0
        self.lasers = []
        
    def set_weapon(self, weapon_type):
        """
        Set the current weapon type.
        
        Args:
            weapon_type (str): Type of weapon to set
        """
        self.current_weapon = weapon_type
        
    def can_shoot(self):
        """
        Check if the weapon can fire.
        
        Returns:
            bool: True if weapon can fire
        """
        return self.shoot_cooldown <= 0
    
    def get_cooldown(self):
        """
        Get the cooldown time for the current weapon.
        
        Returns:
            float: Cooldown time in seconds
        """
        if self.current_weapon == WEAPON_RAPID:
            return RAPID_FIRE_COOLDOWN
        else:
            return PLAYER_SHOOT_COOLDOWN
    
    def shoot(self, position, rotation, shot_group):
        """
        Fire the current weapon.
        
        Args:
            position (pygame.Vector2): Shooting position
            rotation (float): Shooting direction in degrees
            shot_group (pygame.sprite.Group): Group to add shots to
        """
        if not self.can_shoot():
            return
            
        # Calculate direction vector
        direction = pygame.Vector2(0, 1).rotate(rotation)
        
        if self.current_weapon == WEAPON_NORMAL or self.current_weapon == WEAPON_RAPID:
            # Single shot
            shot = Shot(position.x, position.y)
            velocity = direction * PLAYER_SHOOT_SPEED
            shot.velocity = velocity
            shot_group.add(shot)
            
        elif self.current_weapon == WEAPON_SPREAD:
            # Spread shot - multiple bullets
            for i in range(SPREAD_SHOT_COUNT):
                # Calculate spread angles
                angle_offset = (i - (SPREAD_SHOT_COUNT - 1) / 2) * SPREAD_ANGLE
                spread_direction = direction.rotate(angle_offset * 180 / math.pi)
                shot = Shot(position.x, position.y)
                velocity = spread_direction * PLAYER_SHOOT_SPEED
                shot.velocity = velocity
                shot_group.add(shot)
                
        elif self.current_weapon == WEAPON_LASER:
            # Laser beam
            laser = Laser(position, direction)
            self.lasers.append(laser)
        
        # Set cooldown
        self.shoot_cooldown = self.get_cooldown()
    
    def update(self, dt):
        """
        Update weapon systems.
        
        Args:
            dt (float): Delta time since last frame
        """
        # Update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
            
        # Update lasers
        self.lasers = [laser for laser in self.lasers if laser.update(dt)]
    
    def draw(self, screen):
        """
        Draw weapon effects (like lasers).
        
        Args:
            screen: Pygame screen surface to draw on
        """
        for laser in self.lasers:
            laser.draw(screen)
    
    def check_laser_hits(self, asteroids):
        """
        Check if any lasers hit asteroids.
        
        Args:
            asteroids (pygame.sprite.Group): Group of asteroids to check
            
        Returns:
            list: List of asteroids hit by lasers
        """
        hit_asteroids = []
        for laser in self.lasers:
            for asteroid in asteroids:
                # Simple line-circle intersection check
                # For simplicity, we'll check if laser passes near asteroid center
                line_vec = laser.end_pos - laser.start_pos
                to_asteroid = asteroid.position - laser.start_pos
                
                # Project asteroid position onto laser line
                line_length = line_vec.length()
                if line_length > 0:
                    projection = to_asteroid.dot(line_vec) / line_length
                    projection = max(0, min(line_length, projection))
                    
                    # Find closest point on line
                    closest_point = laser.start_pos + (line_vec.normalize() * projection)
                    distance = (asteroid.position - closest_point).length()
                    
                    if distance <= asteroid.radius:
                        hit_asteroids.append(asteroid)
        
        return hit_asteroids