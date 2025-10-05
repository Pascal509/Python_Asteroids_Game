"""
Asteroid - Asteroid and Asteroid Field Classes

This module contains the Asteroid class (representing individual asteroids)
and the AsteroidField class (responsible for spawning asteroids at the screen edges).

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    """
    Individual asteroid object.
    
    Asteroids come in three sizes (large, medium, small) and split into
    smaller asteroids when shot, following classic Asteroids game mechanics.
    """
    
    def __init__(self, x, y, radius):
        """
        Initialize an asteroid at the given position and size.
        
        Args:
            x (float): Starting x position
            y (float): Starting y position  
            radius (float): Size of the asteroid
        """
        super().__init__(x, y, radius)
        # Generate lumpy shape by creating random vertex offsets
        self.shape_vertices = self._generate_lumpy_shape()
        
    def _generate_lumpy_shape(self):
        """
        Generate a lumpy, irregular shape for the asteroid.
        
        Returns:
            list: List of pygame.Vector2 points forming the asteroid shape
        """
        vertices = []
        num_vertices = random.randint(8, 12)  # Random number of vertices
        
        for i in range(num_vertices):
            angle = (2 * math.pi * i) / num_vertices
            # Add randomness to the radius for lumpy effect
            variation = random.uniform(0.7, 1.3)
            vertex_radius = self.radius * variation
            
            x = vertex_radius * math.cos(angle)
            y = vertex_radius * math.sin(angle)
            vertices.append(pygame.Vector2(x, y))
            
        return vertices

    def get_world_vertices(self):
        """
        Get the asteroid vertices in world coordinates.
        
        Returns:
            list: List of world-space vertex positions
        """
        return [self.position + vertex for vertex in self.shape_vertices]

    def draw(self, screen):
        """
        Draw the asteroid as a lumpy polygon outline.
        
        Args:
            screen: pygame surface to draw on
        """
        world_vertices = self.get_world_vertices()
        if len(world_vertices) >= 3:  # Need at least 3 points for a polygon
            pygame.draw.polygon(screen, "white", world_vertices, 2)

    def update(self, dt):
        """
        Update asteroid position based on velocity.
        
        Args:
            dt (float): Delta time since last frame
        """
        self.position += self.velocity * dt
        self.wrap_around_screen()  # Enable screen wrapping

    def split(self):
        """
        Split this asteroid into two smaller asteroids.
        
        Large asteroids split into medium, medium into small, 
        small asteroids are destroyed completely.
        """
        # Remove this asteroid from the game
        self.kill()
        
        # Small asteroids don't split further
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # Calculate size for the two new asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Generate random split angle (20-50 degrees)
        random_angle = random.uniform(20, 50)
        
        # Create two velocity vectors in opposite directions
        velocity1 = self.velocity.rotate(random_angle)
        velocity2 = self.velocity.rotate(-random_angle)
        
        # Make the new asteroids move faster than the original
        velocity1 = velocity1 * 1.2
        velocity2 = velocity2 * 1.2
        
        # Create two new smaller asteroids at the same position
        new_asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid1.velocity = velocity1
        
        new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid2.velocity = velocity2


class AsteroidField(pygame.sprite.Sprite):
    """
    Asteroid spawning system.
    
    Continuously spawns asteroids at random edges of the screen at regular intervals.
    Asteroids spawn with random sizes, speeds, and directions.
    """
    
    # Define the four screen edges with their direction vectors and spawn positions
    edges = [
        # Left edge: asteroids move right, spawn off-screen left
        [
            pygame.Vector2(1, 0),  # Direction: move right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        # Right edge: asteroids move left, spawn off-screen right  
        [
            pygame.Vector2(-1, 0),  # Direction: move left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        # Top edge: asteroids move down, spawn off-screen top
        [
            pygame.Vector2(0, 1),  # Direction: move down
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        # Bottom edge: asteroids move up, spawn off-screen bottom
        [
            pygame.Vector2(0, -1),  # Direction: move up
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        """Initialize the asteroid field spawner."""
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0  # Timer for controlling spawn rate

    def spawn(self, radius, position, velocity):
        """
        Create a new asteroid with the given properties.
        
        Args:
            radius (float): Size of the asteroid
            position (pygame.Vector2): Starting position
            velocity (pygame.Vector2): Movement velocity
        """
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        """
        Update the spawner and create new asteroids at regular intervals.
        
        Args:
            dt (float): Delta time since last frame
        """
        self.spawn_timer += dt
        
        # Check if it's time to spawn a new asteroid
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # Choose a random edge to spawn from
            edge = random.choice(self.edges)
            
            # Generate random properties for the new asteroid
            speed = random.randint(40, 100)                    # Random speed
            velocity = edge[0] * speed                         # Base direction
            velocity = velocity.rotate(random.randint(-30, 30)) # Add random angle
            position = edge[1](random.uniform(0, 1))           # Random position on edge
            kind = random.randint(1, ASTEROID_KINDS)           # Random size (1, 2, or 3)
            
            # Create the asteroid
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)