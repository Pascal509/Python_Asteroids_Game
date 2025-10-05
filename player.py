"""
Player - Player Character Class

This module contains the Player class which represents the player's spaceship
in the Asteroids game. Handles player input, movement, rotation, and shooting.

Author: CodeWithEzeh
Date: October 2025
"""

from circleshape import CircleShape
from constants import *
from shot import Shot
import pygame
import time


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
        self.acceleration = pygame.Vector2(0, 0)  # Current acceleration vector
        
        # Phase 3: Power-up effects
        self.has_shield = False
        self.shield_timer = 0
        self.speed_boost_timer = 0
        self.speed_multiplier = 1.0
        
        # Phase 3: Weapon system
        self.weapon_manager = None  # Will be set by main game
        
        # Phase 3: Visual effects
        self.shield_pulse = 0

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
        Also draws shield effect if active.
        
        Args:
            screen: pygame surface to draw on
        """
        # Draw shield effect if active
        if self.has_shield:
            shield_alpha = 0.3 + 0.2 * abs(pygame.math.Vector2(0, 1).rotate(self.shield_pulse * 200).x)
            shield_color = (0, 150, 255)  # Blue shield
            shield_radius = int(self.radius * 1.5)
            
            # Create a surface for the shield with alpha
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (*shield_color, int(shield_alpha * 255)), 
                             (shield_radius, shield_radius), shield_radius, 3)
            
            screen.blit(shield_surface, 
                       (self.position.x - shield_radius, self.position.y - shield_radius))
        
        # Draw player triangle
        player_color = "white"
        if self.speed_boost_timer > 0:
            # Yellow tint when speed boosted
            player_color = (255, 255, 150)
            
        pygame.draw.polygon(screen, player_color, self.triangle(), 2)
    
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
            
        # Update power-up timers
        if self.shield_timer > 0:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.has_shield = False
                
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed_multiplier = 1.0
                
        # Update shield visual effect
        self.shield_pulse += dt

        # Handle player input
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:    # Rotate left
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:   # Rotate right
            self.rotate(dt)
        if keys[pygame.K_w] or keys[pygame.K_UP]:      # Thrust forward
            self.thrust_forward(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:    # Thrust backward
            self.thrust_backward(dt)
        # Note: SPACE shooting is handled in main loop with weapon manager
            
        # Apply physics with speed boost
        self.velocity += self.acceleration * dt
        self.velocity *= PLAYER_FRICTION  # Apply friction
        self.position += self.velocity * dt * self.speed_multiplier
        
        # Reset acceleration for next frame
        self.acceleration = pygame.Vector2(0, 0)
        
        # Wrap around screen edges
        self.wrap_around_screen()

    def accelerate(self, dt):
        """
        Accelerate the player in the direction they are facing.
        Positive dt = forward, negative dt = backward.
        
        Args:
            dt (float): Delta time for frame-rate independent acceleration
                       Positive values accelerate forward, negative backward
        """
        # Calculate forward direction based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Apply acceleration in that direction (dt can be negative for reverse)
        self.acceleration += forward * PLAYER_ACCELERATION * dt
    
    def thrust_forward(self, dt):
        """
        Thrust forward in the direction the ship is facing.
        
        Args:
            dt (float): Delta time for frame-rate independent acceleration
        """
        # Calculate forward direction based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Apply strong forward acceleration for responsive movement
        self.acceleration += forward * PLAYER_ACCELERATION
    
    def thrust_backward(self, dt):
        """
        Thrust backward (reverse) relative to the direction the ship is facing.
        
        Args:
            dt (float): Delta time for frame-rate independent acceleration
        """
        # Calculate forward direction based on current rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        
        # Apply strong backward acceleration for responsive movement
        self.acceleration -= forward * PLAYER_ACCELERATION

    def move(self, dt):
        """
        Legacy move method - now replaced by accelerate().
        Kept for backward compatibility.
        
        Args:
            dt (float): Delta time for frame-rate independent movement
        """
        self.accelerate(dt)

    def get_triangle_vertices(self):
        """
        Get the actual triangle vertices for collision detection.
        
        Returns:
            list: List of pygame.Vector2 points forming the triangle
        """
        return self.triangle()
        
    def triangle_collides_with_circle(self, circle_obj):
        """
        Check if this triangular player collides with a circular object.
        Uses point-in-triangle and circle-line intersection tests.
        
        Args:
            circle_obj: Object with position and radius attributes
            
        Returns:
            bool: True if collision detected
        """
        triangle_points = self.get_triangle_vertices()
        circle_center = circle_obj.position
        circle_radius = circle_obj.radius
        
        # Check if circle center is inside triangle
        if self._point_in_triangle(circle_center, triangle_points):
            return True
            
        # Check if circle intersects any triangle edge
        for i in range(3):
            p1 = triangle_points[i]
            p2 = triangle_points[(i + 1) % 3]
            
            if self._circle_line_intersection(circle_center, circle_radius, p1, p2):
                return True
                
        return False
        
    def _point_in_triangle(self, point, triangle):
        """
        Check if a point is inside a triangle using barycentric coordinates.
        
        Args:
            point (pygame.Vector2): Point to test
            triangle (list): List of three pygame.Vector2 triangle vertices
            
        Returns:
            bool: True if point is inside triangle
        """
        p1, p2, p3 = triangle
        
        # Calculate barycentric coordinates
        denom = (p2.y - p3.y) * (p1.x - p3.x) + (p3.x - p2.x) * (p1.y - p3.y)
        if abs(denom) < 0.001:  # Degenerate triangle
            return False
            
        a = ((p2.y - p3.y) * (point.x - p3.x) + (p3.x - p2.x) * (point.y - p3.y)) / denom
        b = ((p3.y - p1.y) * (point.x - p3.x) + (p1.x - p3.x) * (point.y - p3.y)) / denom
        c = 1 - a - b
        
        return a >= 0 and b >= 0 and c >= 0
        
    def _circle_line_intersection(self, circle_center, circle_radius, line_start, line_end):
        """
        Check if a circle intersects with a line segment.
        
        Args:
            circle_center (pygame.Vector2): Center of circle
            circle_radius (float): Radius of circle
            line_start (pygame.Vector2): Start point of line
            line_end (pygame.Vector2): End point of line
            
        Returns:
            bool: True if intersection exists
        """
        # Vector from line start to line end
        line_vec = line_end - line_start
        # Vector from line start to circle center
        to_circle = circle_center - line_start
        
        # Project circle center onto line
        line_length_sq = line_vec.length_squared()
        if line_length_sq == 0:
            # Degenerate line (point)
            return circle_center.distance_to(line_start) <= circle_radius
            
        t = max(0, min(1, to_circle.dot(line_vec) / line_length_sq))
        closest_point = line_start + t * line_vec
        
        # Check distance from circle center to closest point on line
        distance = circle_center.distance_to(closest_point)
        return distance <= circle_radius

    def collides_with(self, other):
        """
        Override collision detection to use triangle-circle collision.
        
        Args:
            other: Another game object with position and radius
            
        Returns:
            bool: True if collision detected
        """
        return self.triangle_collides_with_circle(other)

    def shoot(self):
        """
        Create a bullet that travels in the direction the player is facing.
        Uses weapon manager if available, otherwise uses basic shooting.
        """
        if self.weapon_manager:
            # Use weapon manager for advanced shooting
            return  # Weapon manager will handle shooting
        else:
            # Fallback to basic shooting
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
    
    def apply_powerup(self, powerup_type):
        """
        Apply a power-up effect to the player.
        
        Args:
            powerup_type (str): Type of power-up to apply
        """
        if powerup_type == POWERUP_SHIELD:
            self.has_shield = True
            self.shield_timer = SHIELD_DURATION
        elif powerup_type == POWERUP_SPEED_BOOST:
            self.speed_boost_timer = SPEED_BOOST_DURATION
            self.speed_multiplier = SPEED_BOOST_MULTIPLIER
        elif powerup_type == POWERUP_RAPID_FIRE and self.weapon_manager:
            self.weapon_manager.set_weapon(WEAPON_RAPID)
        elif powerup_type == POWERUP_SPREAD_SHOT and self.weapon_manager:
            self.weapon_manager.set_weapon(WEAPON_SPREAD)
            
    def is_shielded(self):
        """
        Check if player is currently protected by shield.
        
        Returns:
            bool: True if shield is active
        """
        return self.has_shield and self.shield_timer > 0
        
    def get_speed_multiplier(self):
        """
        Get current speed multiplier.
        
        Returns:
            float: Current speed multiplier
        """
        return self.speed_multiplier
