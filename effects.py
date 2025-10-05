"""
Particle System for Explosions and Effects

Handles visual effects like asteroid explosions and particle systems.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from circleshape import CircleShape


class Particle:
    """
    Individual particle for explosion effects.
    """
    
    def __init__(self, x, y, velocity, color="white", lifetime=1.0):
        """
        Initialize a particle.
        
        Args:
            x (float): Starting x position
            y (float): Starting y position
            velocity (pygame.Vector2): Initial velocity
            color (str): Particle color
            lifetime (float): How long the particle lasts in seconds
        """
        self.position = pygame.Vector2(x, y)
        self.velocity = velocity
        self.color = color
        self.lifetime = lifetime
        self.age = 0.0
        self.size = random.uniform(1, 3)
        
    def update(self, dt):
        """
        Update particle position and age.
        
        Args:
            dt (float): Delta time
            
        Returns:
            bool: True if particle is still alive, False if expired
        """
        self.position += self.velocity * dt
        self.age += dt
        
        # Fade out over time
        alpha = 1.0 - (self.age / self.lifetime)
        if alpha <= 0:
            return False
            
        # Slow down over time
        self.velocity *= 0.98
        return True
        
    def draw(self, screen):
        """
        Draw the particle.
        
        Args:
            screen: pygame surface to draw on
        """
        alpha = 1.0 - (self.age / self.lifetime)
        if alpha > 0:
            # Create fading effect
            size = max(1, int(self.size * alpha))
            pygame.draw.circle(screen, self.color, self.position, size)


class Explosion:
    """
    Explosion effect made of multiple particles.
    """
    
    def __init__(self, x, y, particle_count=15, colors=None):
        """
        Create an explosion at the given position.
        
        Args:
            x (float): Explosion center x
            y (float): Explosion center y
            particle_count (int): Number of particles to create
            colors (list): List of possible particle colors
        """
        if colors is None:
            colors = ["white", "yellow", "orange", "red"]
            
        self.particles = []
        
        for _ in range(particle_count):
            # Random direction and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            velocity = pygame.Vector2(
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            
            # Random color and lifetime
            color = random.choice(colors)
            lifetime = random.uniform(0.5, 1.5)
            
            particle = Particle(x, y, velocity, color, lifetime)
            self.particles.append(particle)
            
    def update(self, dt):
        """
        Update all particles in the explosion.
        
        Args:
            dt (float): Delta time
            
        Returns:
            bool: True if explosion is still active, False if all particles are gone
        """
        # Update particles and remove expired ones
        self.particles = [p for p in self.particles if p.update(dt)]
        return len(self.particles) > 0
        
    def draw(self, screen):
        """
        Draw all particles in the explosion.
        
        Args:
            screen: pygame surface to draw on
        """
        for particle in self.particles:
            particle.draw(screen)


class EffectManager:
    """
    Manages all visual effects in the game.
    """
    
    def __init__(self):
        """Initialize the effect manager."""
        self.explosions = []
        
    def create_explosion(self, x, y, size="medium"):
        """
        Create an explosion effect.
        
        Args:
            x (float): Explosion x position
            y (float): Explosion y position
            size (str): Size of explosion ("small", "medium", "large")
        """
        particle_counts = {
            "small": 8,
            "medium": 15,
            "large": 25
        }
        
        count = particle_counts.get(size, 15)
        explosion = Explosion(x, y, count)
        self.explosions.append(explosion)
        
    def update(self, dt):
        """
        Update all active effects.
        
        Args:
            dt (float): Delta time
        """
        # Update explosions and remove finished ones
        self.explosions = [exp for exp in self.explosions if exp.update(dt)]
        
    def draw(self, screen):
        """
        Draw all active effects.
        
        Args:
            screen: pygame surface to draw on
        """
        for explosion in self.explosions:
            explosion.draw(screen)