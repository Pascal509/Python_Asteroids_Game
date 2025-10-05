"""
Player - Player Character Class

This module contains the Player class which represents the player's spaceship
in the Asteroids game. Handles player input, movement, rotation, and shooting.

Author: CodeWithEzeh
Date: October 2025
"""

from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN
from shot import Shot
import pygame


class Player(CircleShape):
    """
    Player spaceship class.
    
    Controls:
    - A/D: Rotate left/right
    - W/S: Move forward/backward
    - SPACE: Shoot bullets
    """
    
    def __init__(self, x, y):
        """
        Initialize the player at the given position.
        
        Args:
            x (float): Starting x position
            y (float): Starting y position
        """
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0      # Current rotation angle in degrees
        self.timer = 0         # Shooting cooldown timer

    def triangle(self):
        """
        Calculate the triangle vertices for drawing the player ship.
        
        Returns:
            list: List of three pygame.Vector2 points forming a triangle
        """
        # Calculate direction vectors based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        
        # Calculate triangle points
        tip = self.position + forward * self.radius                    # Front tip
        left_base = self.position - forward * self.radius - right      # Left base
        right_base = self.position - forward * self.radius + right     # Right base
        
        return [tip, left_base, right_base]

    def draw(self, screen):
        """
        Draw the player as a white triangle pointing in the facing direction.
        
        Args:
            screen: pygame surface to draw on
        """
        pygame.draw.polygon(screen, "white", self.triangle(), 2)
    
    def rotate(self, dt):
        """
        Rotate the player by the turn speed.
        
        Args:
            dt (float): Delta time for frame-rate independent rotation
        """
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        """
        Update player state and handle input.
        
        Args:
            dt (float): Delta time since last frame
        """
        keys = pygame.key.get_pressed()

        # Update shooting cooldown timer
        if self.timer > 0:
            self.timer -= dt

        # Handle player input
        if keys[pygame.K_a]:           # Rotate left
            self.rotate(-dt)
        if keys[pygame.K_d]:           # Rotate right
            self.rotate(dt)
        if keys[pygame.K_w]:           # Move forward
            self.move(dt)
        if keys[pygame.K_s]:           # Move backward
            self.move(-dt)
        if keys[pygame.K_SPACE]:       # Shoot
            self.shoot()

    def move(self, dt):
        """
        Move the player in the direction they are facing.
        
        Args:
            dt (float): Delta time for frame-rate independent movement
        """
        # Calculate forward direction based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Scale by speed and delta time for smooth movement
        movement = forward * PLAYER_SPEED * dt
        
        # Apply movement to position
        self.position += movement

    def shoot(self):
        """
        Create a bullet that travels in the direction the player is facing.
        Respects shooting cooldown to prevent bullet spam.
        """
        # Check shooting cooldown
        if self.timer > 0:
            return
            
        # Create bullet at player position
        shot = Shot(self.position.x, self.position.y)
        
        # Calculate bullet velocity in facing direction
        velocity = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = velocity * PLAYER_SHOOT_SPEED
        shot.velocity = velocity
        
        # Start cooldown timer
        self.timer = PLAYER_SHOOT_COOLDOWN
