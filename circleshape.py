"""
CircleShape - Base Game Object Class

This module provides the base class for all circular game objects in the Asteroids game.
It handles common functionality like position, velocity, collision detection, and
pygame sprite group management.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame


class CircleShape(pygame.sprite.Sprite):
    """
    Base class for all circular game objects (Player, Asteroid, Shot).
    
    Inherits from pygame.sprite.Sprite to enable automatic sprite group management.
    Provides basic physics (position, velocity) and collision detection.
    """
    
    def __init__(self, x, y, radius):
        """
        Initialize a circular game object.
        
        Args:
            x (float): Initial x position
            y (float): Initial y position
            radius (float): Radius of the circular object
        """
        # Initialize pygame sprite with automatic group membership
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)    # Current position
        self.velocity = pygame.Vector2(0, 0)    # Current velocity vector
        self.radius = radius                    # Collision radius

    def draw(self, screen):
        """
        Draw the object to the screen.
        Must be overridden by subclasses.
        
        Args:
            screen: pygame surface to draw on
        """
        pass

    def update(self, dt):
        """
        Update the object's state.
        Must be overridden by subclasses.
        
        Args:
            dt (float): Delta time since last frame
        """
        pass

    def collides_with(self, other):
        """
        Check if this object collides with another CircleShape object.
        
        Uses circle-to-circle collision detection by comparing the distance
        between centers to the sum of their radii.
        
        Args:
            other (CircleShape): Another circular object to check collision with
            
        Returns:
            bool: True if the objects are colliding, False otherwise
        """
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)