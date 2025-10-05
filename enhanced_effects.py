"""
Enhanced Visual Effects

This module contains advanced visual effects including thruster flames,
particle trails, screen shake, and enhanced explosions.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from constants import *


class ThrusterFlame:
    """
    Particle effect for ship thrusters.
    """
    
    def __init__(self, x, y, direction, intensity=1.0):
        """
        Initialize a thruster flame effect.
        
        Args:
            x (float): X position
            y (float): Y position
            direction (pygame.Vector2): Direction opposite to thrust
            intensity (float): Flame intensity (0.0 to 1.0)
        """
        self.particles = []
        self.direction = direction.normalize()
        self.intensity = intensity
        
        # Create flame particles
        for _ in range(int(THRUSTER_PARTICLE_COUNT * intensity)):
            particle = {
                'pos': pygame.Vector2(x, y),
                'vel': self.direction * random.uniform(50, 150) + pygame.Vector2(
                    random.uniform(-30, 30), random.uniform(-30, 30)
                ),
                'lifetime': random.uniform(0.1, 0.3),
                'age': 0,
                'size': random.uniform(2, 6)
            }
            self.particles.append(particle)
    
    def update(self, dt):
        """
        Update thruster particles.
        
        Args:
            dt (float): Delta time since last frame
            
        Returns:
            bool: True if effect is still active
        """
        active_particles = []
        
        for particle in self.particles:
            particle['age'] += dt
            if particle['age'] < particle['lifetime']:
                particle['pos'] += particle['vel'] * dt
                active_particles.append(particle)
        
        self.particles = active_particles
        return len(self.particles) > 0
    
    def draw(self, screen):
        """
        Draw the thruster flame.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        for particle in self.particles:
            # Calculate color based on age
            life_ratio = 1.0 - (particle['age'] / particle['lifetime'])
            
            if life_ratio > 0.7:
                color = (255, 255, 255)  # White hot
            elif life_ratio > 0.4:
                color = (255, 200, 100)  # Orange
            else:
                color = (255, 100, 0)    # Red
            
            # Draw particle
            size = int(particle['size'] * life_ratio)
            if size > 0:
                pygame.draw.circle(screen, color, 
                                 (int(particle['pos'].x), int(particle['pos'].y)), size)


class MovementTrail:
    """
    Trail effect for fast-moving objects.
    """
    
    def __init__(self, max_length=TRAIL_LENGTH):
        """
        Initialize a movement trail.
        
        Args:
            max_length (int): Maximum number of trail segments
        """
        self.positions = []
        self.max_length = max_length
    
    def add_position(self, pos):
        """
        Add a new position to the trail.
        
        Args:
            pos (pygame.Vector2): Current position
        """
        self.positions.append(pygame.Vector2(pos))
        if len(self.positions) > self.max_length:
            self.positions.pop(0)
    
    def draw(self, screen, color=(100, 150, 255)):
        """
        Draw the movement trail.
        
        Args:
            screen: Pygame screen surface to draw on
            color (tuple): Trail color
        """
        if len(self.positions) < 2:
            return
            
        for i in range(1, len(self.positions)):
            # Calculate alpha based on position in trail
            alpha = (i / len(self.positions)) * 255
            trail_color = (*color, int(alpha))
            
            # Draw line segment
            start_pos = self.positions[i-1]
            end_pos = self.positions[i]
            
            # Create surface for alpha blending
            trail_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(trail_surface, trail_color, start_pos, end_pos, 2)
            screen.blit(trail_surface, (0, 0))


class ScreenShake:
    """
    Screen shake effect for impacts and explosions.
    """
    
    def __init__(self):
        """Initialize screen shake effect."""
        self.shake_duration = 0
        self.shake_intensity = 0
        self.offset = pygame.Vector2(0, 0)
    
    def start_shake(self, duration=SCREEN_SHAKE_DURATION, intensity=SCREEN_SHAKE_INTENSITY):
        """
        Start a screen shake effect.
        
        Args:
            duration (float): Duration in seconds
            intensity (float): Shake intensity in pixels
        """
        self.shake_duration = duration
        self.shake_intensity = intensity
    
    def update(self, dt):
        """
        Update screen shake.
        
        Args:
            dt (float): Delta time since last frame
        """
        if self.shake_duration > 0:
            self.shake_duration -= dt
            
            # Calculate shake offset
            current_intensity = self.shake_intensity * (self.shake_duration / SCREEN_SHAKE_DURATION)
            self.offset.x = random.uniform(-current_intensity, current_intensity)
            self.offset.y = random.uniform(-current_intensity, current_intensity)
        else:
            self.offset = pygame.Vector2(0, 0)
    
    def get_offset(self):
        """
        Get current screen shake offset.
        
        Returns:
            pygame.Vector2: Current shake offset
        """
        return self.offset
    
    def is_shaking(self):
        """
        Check if screen is currently shaking.
        
        Returns:
            bool: True if shaking
        """
        return self.shake_duration > 0


class EnhancedExplosion:
    """
    Enhanced explosion effect with multiple particle types.
    """
    
    def __init__(self, x, y, size="medium"):
        """
        Initialize enhanced explosion.
        
        Args:
            x (float): X position
            y (float): Y position
            size (str): Explosion size ("small", "medium", "large")
        """
        self.position = pygame.Vector2(x, y)
        self.particles = []
        self.sparks = []
        self.shockwave_radius = 0
        self.max_shockwave_radius = {"small": 30, "medium": 50, "large": 80}[size]
        self.particle_count = {"small": 15, "medium": 25, "large": 40}[size]
        self.age = 0
        self.max_age = 2.0
        
        # Create main explosion particles
        for _ in range(self.particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            particle = {
                'pos': pygame.Vector2(x, y),
                'vel': pygame.Vector2(math.cos(angle), math.sin(angle)) * speed,
                'lifetime': random.uniform(0.5, 1.5),
                'age': 0,
                'size': random.uniform(3, 8),
                'color_type': random.choice(['fire', 'smoke', 'spark'])
            }
            self.particles.append(particle)
        
        # Create sparks
        for _ in range(self.particle_count // 2):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            spark = {
                'pos': pygame.Vector2(x, y),
                'vel': pygame.Vector2(math.cos(angle), math.sin(angle)) * speed,
                'lifetime': random.uniform(0.2, 0.8),
                'age': 0,
                'length': random.uniform(5, 15)
            }
            self.sparks.append(spark)
    
    def update(self, dt):
        """
        Update explosion effect.
        
        Args:
            dt (float): Delta time since last frame
            
        Returns:
            bool: True if explosion is still active
        """
        self.age += dt
        
        # Update shockwave
        if self.shockwave_radius < self.max_shockwave_radius:
            self.shockwave_radius += 200 * dt
        
        # Update particles
        active_particles = []
        for particle in self.particles:
            particle['age'] += dt
            if particle['age'] < particle['lifetime']:
                particle['pos'] += particle['vel'] * dt
                particle['vel'] *= 0.95  # Slow down over time
                active_particles.append(particle)
        self.particles = active_particles
        
        # Update sparks
        active_sparks = []
        for spark in self.sparks:
            spark['age'] += dt
            if spark['age'] < spark['lifetime']:
                spark['pos'] += spark['vel'] * dt
                active_sparks.append(spark)
        self.sparks = active_sparks
        
        return self.age < self.max_age
    
    def draw(self, screen):
        """
        Draw the enhanced explosion.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Draw shockwave
        if self.shockwave_radius < self.max_shockwave_radius:
            alpha = 1.0 - (self.shockwave_radius / self.max_shockwave_radius)
            color = (255, 200, 100, int(alpha * 128))
            
            shockwave_surface = pygame.Surface((self.max_shockwave_radius * 2, self.max_shockwave_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shockwave_surface, color, 
                             (self.max_shockwave_radius, self.max_shockwave_radius), 
                             int(self.shockwave_radius), 3)
            screen.blit(shockwave_surface, 
                       (self.position.x - self.max_shockwave_radius, 
                        self.position.y - self.max_shockwave_radius))
        
        # Draw particles
        for particle in self.particles:
            life_ratio = 1.0 - (particle['age'] / particle['lifetime'])
            size = int(particle['size'] * life_ratio)
            
            if size > 0:
                if particle['color_type'] == 'fire':
                    if life_ratio > 0.7:
                        color = (255, 255, 255)  # White hot
                    elif life_ratio > 0.4:
                        color = (255, 200, 0)    # Yellow
                    else:
                        color = (255, 100, 0)    # Red
                elif particle['color_type'] == 'smoke':
                    gray_value = int(100 * life_ratio)
                    color = (gray_value, gray_value, gray_value)
                else:  # spark
                    color = (255, 255, 200)
                
                pygame.draw.circle(screen, color, 
                                 (int(particle['pos'].x), int(particle['pos'].y)), size)
        
        # Draw sparks
        for spark in self.sparks:
            life_ratio = 1.0 - (spark['age'] / spark['lifetime'])
            
            if life_ratio > 0:
                # Draw spark as a line
                start_pos = spark['pos']
                end_pos = spark['pos'] - spark['vel'].normalize() * spark['length'] * life_ratio
                
                color = (255, 255, 100) if life_ratio > 0.5 else (255, 200, 0)
                pygame.draw.line(screen, color, start_pos, end_pos, 2)


class EnhancedEffectManager:
    """
    Enhanced effect manager for all visual effects.
    """
    
    def __init__(self):
        """Initialize the enhanced effect manager."""
        self.explosions = []
        self.thruster_flames = []
        self.trails = {}  # Object ID -> MovementTrail
        self.screen_shake = ScreenShake()
    
    def create_explosion(self, x, y, size="medium"):
        """
        Create an enhanced explosion effect.
        
        Args:
            x (float): X position
            y (float): Y position
            size (str): Explosion size
        """
        explosion = EnhancedExplosion(x, y, size)
        self.explosions.append(explosion)
        
        # Start screen shake for large explosions
        if size == "large":
            self.screen_shake.start_shake(0.5, 15)
        elif size == "medium":
            self.screen_shake.start_shake(0.3, 10)
    
    def create_thruster_flame(self, x, y, direction, intensity=1.0):
        """
        Create a thruster flame effect.
        
        Args:
            x (float): X position
            y (float): Y position  
            direction (pygame.Vector2): Thrust direction
            intensity (float): Flame intensity
        """
        flame = ThrusterFlame(x, y, direction, intensity)
        self.thruster_flames.append(flame)
    
    def add_trail_position(self, object_id, pos):
        """
        Add a position to an object's movement trail.
        
        Args:
            object_id: Unique identifier for the object
            pos (pygame.Vector2): Current position
        """
        if object_id not in self.trails:
            self.trails[object_id] = MovementTrail()
        self.trails[object_id].add_position(pos)
    
    def update(self, dt):
        """
        Update all effects.
        
        Args:
            dt (float): Delta time since last frame
        """
        # Update explosions
        self.explosions = [exp for exp in self.explosions if exp.update(dt)]
        
        # Update thruster flames
        self.thruster_flames = [flame for flame in self.thruster_flames if flame.update(dt)]
        
        # Update screen shake
        self.screen_shake.update(dt)
    
    def draw(self, screen):
        """
        Draw all effects.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Apply screen shake offset
        shake_offset = self.screen_shake.get_offset()
        
        # Create shaken surface
        if self.screen_shake.is_shaking():
            shaken_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            shaken_surface.fill((0, 0, 0))
            
            # Draw effects on shaken surface
            self._draw_effects(shaken_surface)
            
            # Blit with shake offset
            screen.blit(shaken_surface, shake_offset)
        else:
            self._draw_effects(screen)
    
    def _draw_effects(self, screen):
        """Draw all effects on the given surface."""
        # Draw trails
        for trail in self.trails.values():
            trail.draw(screen)
        
        # Draw explosions
        for explosion in self.explosions:
            explosion.draw(screen)
        
        # Draw thruster flames
        for flame in self.thruster_flames:
            flame.draw(screen)
    
    def clear_trails(self):
        """Clear all movement trails."""
        self.trails.clear()