"""
Shot - Bullet/Projectile Class

This module contains the Shot class which represents bullets fired by the player
in the Asteroids game. Bullets are small circles that travel in straight lines.

Author: CodeWithEzeh
Date: October 2025
"""

from circleshape import CircleShape
from constants import SHOT_RADIUS
import pygame


class Shot(CircleShape):
    """
    Bullet/projectile class for player shots.
    
    Shots are small white circles that move in straight lines at high speed.
    They are destroyed when they collide with asteroids.
    """
    
    def __init__(self, x, y):
        """
        Initialize a bullet at the given position.
        
        Args:
            x (float): Starting x position
            y (float): Starting y position
        """
        super().__init__(x, y, SHOT_RADIUS)
        self.lifetime = 3.0  # Bullet disappears after 3 seconds
        self.age = 0.0

    def draw(self, screen):
        """
        Draw the bullet as a small white circle.
        
        Args:
            screen: pygame surface to draw on
        """
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        """
        Update bullet position based on velocity.
        
        Args:
            dt (float): Delta time since last frame
        """
        self.position += self.velocity * dt
        self.age += dt
        
        # Remove bullet if it's too old
        if self.age > self.lifetime:
            self.kill()
            
        # Optional: wrap around screen (bullets come back from other side)
        # self.wrap_around_screen()