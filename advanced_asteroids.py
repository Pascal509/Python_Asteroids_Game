"""
Advanced Asteroid System

This module extends the asteroid system with different asteroid types,
mining mechanics, and enhanced properties.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from asteroid import Asteroid
from constants import *


class AdvancedAsteroid(Asteroid):
    """
    Enhanced asteroid with different types and properties.
    """
    
    def __init__(self, x, y, radius, asteroid_type=ASTEROID_NORMAL):
        """
        Initialize an advanced asteroid.
        
        Args:
            x (float): X position
            y (float): Y position
            radius (float): Asteroid radius
            asteroid_type (str): Type of asteroid
        """
        super().__init__(x, y, radius)
        self.asteroid_type = asteroid_type
        self.health = self._get_health_for_type(asteroid_type)
        self.max_health = self.health
        self.resources = self._generate_resources()
        
        # Apply type-specific speed modifications
        if asteroid_type == ASTEROID_ICE:
            self.velocity *= ICE_SPEED_MULTIPLIER
        
        # Visual properties based on type
        self.color = self._get_color_for_type(asteroid_type)
        
    def _get_health_for_type(self, asteroid_type):
        """Get health based on asteroid type."""
        if asteroid_type == ASTEROID_METAL:
            return METAL_HEALTH
        return 1
    
    def _get_color_for_type(self, asteroid_type):
        """Get color based on asteroid type."""
        colors = {
            ASTEROID_NORMAL: (139, 69, 19),    # Brown
            ASTEROID_ICE: (173, 216, 230),     # Light blue
            ASTEROID_METAL: (169, 169, 169),   # Dark gray
            ASTEROID_CRYSTAL: (138, 43, 226)   # Purple
        }
        return colors.get(asteroid_type, (139, 69, 19))
    
    def _generate_resources(self):
        """Generate resources this asteroid contains."""
        resources = {}
        
        if self.asteroid_type == ASTEROID_ICE:
            resources[RESOURCE_ICE] = random.randint(1, 3)
        elif self.asteroid_type == ASTEROID_METAL:
            resources[RESOURCE_METAL] = random.randint(2, 5)
        elif self.asteroid_type == ASTEROID_CRYSTAL:
            resources[RESOURCE_CRYSTAL] = random.randint(1, 2)
        
        return resources
    
    def take_damage(self, damage=1):
        """
        Take damage and return if asteroid is destroyed.
        
        Args:
            damage (int): Amount of damage
            
        Returns:
            bool: True if asteroid is destroyed
        """
        self.health -= damage
        return self.health <= 0
    
    def split(self):
        """Override split behavior for different asteroid types."""
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        split_count = 2
        if self.asteroid_type == ASTEROID_CRYSTAL:
            split_count = CRYSTAL_SPLIT_BONUS
        
        for _ in range(split_count):
            angle = random.uniform(0, 2 * math.pi)
            new_radius = self.radius / 2
            new_x = self.position.x + math.cos(angle) * self.radius
            new_y = self.position.y + math.sin(angle) * self.radius
            
            new_asteroid = AdvancedAsteroid(new_x, new_y, new_radius, self.asteroid_type)
            new_asteroid.velocity = pygame.Vector2(
                math.cos(angle) * random.uniform(20, 50),
                math.sin(angle) * random.uniform(20, 50)
            )
            
            # Add to containers
            if hasattr(self, 'containers') and self.containers:
                for container in self.containers:
                    container.add(new_asteroid)
        
        self.kill()
    
    def draw(self, screen):
        """
        Draw the asteroid with type-specific appearance.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Draw health bar for damaged asteroids
        if self.health < self.max_health and self.max_health > 1:
            bar_width = self.radius * 2
            bar_height = 4
            bar_x = self.position.x - bar_width // 2
            bar_y = self.position.y - self.radius - 10
            
            # Background
            pygame.draw.rect(screen, (100, 100, 100), 
                            (bar_x, bar_y, bar_width, bar_height))
            
            # Health
            health_percentage = self.health / self.max_health
            health_width = bar_width * health_percentage
            pygame.draw.rect(screen, (255, 0, 0), 
                            (bar_x, bar_y, health_width, bar_height))
        
        # Draw asteroid shape with type color
        if len(self.shape_vertices) > 2:
            points = []
            for vertex in self.shape_vertices:
                world_pos = self.position + vertex
                points.append((world_pos.x, world_pos.y))
            
            # Fill with type color
            pygame.draw.polygon(screen, self.color, points)
            
            # Add type-specific visual effects
            if self.asteroid_type == ASTEROID_ICE:
                # Add sparkles
                for _ in range(3):
                    sparkle_pos = self.position + pygame.Vector2(
                        random.uniform(-self.radius, self.radius),
                        random.uniform(-self.radius, self.radius)
                    )
                    pygame.draw.circle(screen, (255, 255, 255), 
                                     (int(sparkle_pos.x), int(sparkle_pos.y)), 1)
            
            elif self.asteroid_type == ASTEROID_METAL:
                # Add metallic shine
                shine_pos = self.position + pygame.Vector2(-self.radius * 0.3, -self.radius * 0.3)
                pygame.draw.circle(screen, (200, 200, 200), 
                                 (int(shine_pos.x), int(shine_pos.y)), int(self.radius * 0.2))
            
            elif self.asteroid_type == ASTEROID_CRYSTAL:
                # Add crystal facets
                for i in range(6):
                    angle = i * 60 * math.pi / 180
                    facet_pos = self.position + pygame.Vector2(
                        math.cos(angle) * self.radius * 0.5,
                        math.sin(angle) * self.radius * 0.5
                    )
                    pygame.draw.circle(screen, (200, 100, 255), 
                                     (int(facet_pos.x), int(facet_pos.y)), 2)
            
            # Outline
            pygame.draw.polygon(screen, "white", points, 2)


class GravityWell:
    """
    Gravity well that affects nearby objects.
    """
    
    def __init__(self, x, y):
        """
        Initialize a gravity well.
        
        Args:
            x (float): X position
            y (float): Y position
        """
        self.position = pygame.Vector2(x, y)
        self.radius = GRAVITY_WELL_RADIUS
        self.strength = GRAVITY_WELL_STRENGTH
        self.pulse_timer = 0
    
    def update(self, dt):
        """
        Update gravity well animation.
        
        Args:
            dt (float): Delta time since last frame
        """
        self.pulse_timer += dt
    
    def apply_gravity(self, obj):
        """
        Apply gravitational force to an object.
        
        Args:
            obj: Object with position and velocity attributes
        """
        distance_vec = self.position - obj.position
        distance = distance_vec.length()
        
        if distance < self.radius and distance > 0:
            # Calculate gravitational force (inverse square law, but capped)
            force_magnitude = min(self.strength / (distance * distance), self.strength)
            force_direction = distance_vec.normalize()
            
            # Apply force to object's velocity
            obj.velocity += force_direction * force_magnitude * 0.016  # Assume ~60 FPS
    
    def draw(self, screen):
        """
        Draw the gravity well.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Pulsing effect
        pulse = 0.8 + 0.2 * math.sin(self.pulse_timer * 3)
        
        # Draw gravity field rings
        for i in range(3):
            ring_radius = int(self.radius * (0.3 + i * 0.25) * pulse)
            alpha = int(50 - i * 15)
            
            # Create surface for alpha blending
            ring_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ring_surface, (100, 0, 200, alpha), 
                             (ring_radius, ring_radius), ring_radius, 2)
            
            screen.blit(ring_surface, 
                       (self.position.x - ring_radius, self.position.y - ring_radius))
        
        # Draw center
        pygame.draw.circle(screen, (150, 50, 255), 
                          (int(self.position.x), int(self.position.y)), 5)


class ResourceManager:
    """
    Manages player resources from mining asteroids.
    """
    
    def __init__(self):
        """Initialize the resource manager."""
        self.resources = {
            RESOURCE_ICE: 0,
            RESOURCE_METAL: 0,
            RESOURCE_CRYSTAL: 0
        }
    
    def add_resources(self, resource_dict):
        """
        Add resources to the player's inventory.
        
        Args:
            resource_dict (dict): Resources to add
        """
        for resource_type, amount in resource_dict.items():
            if resource_type in self.resources:
                self.resources[resource_type] += amount
    
    def can_afford_upgrade(self, upgrade_type):
        """
        Check if player can afford an upgrade.
        
        Args:
            upgrade_type (str): Type of upgrade
            
        Returns:
            bool: True if affordable
        """
        costs = {
            UPGRADE_HULL: {RESOURCE_METAL: 5},
            UPGRADE_ENGINES: {RESOURCE_ICE: 3, RESOURCE_METAL: 2},
            UPGRADE_WEAPONS: {RESOURCE_CRYSTAL: 2, RESOURCE_METAL: 3},
            UPGRADE_SHIELDS: {RESOURCE_CRYSTAL: 3, RESOURCE_ICE: 2}
        }
        
        if upgrade_type not in costs:
            return False
        
        for resource_type, required in costs[upgrade_type].items():
            if self.resources.get(resource_type, 0) < required:
                return False
        
        return True
    
    def purchase_upgrade(self, upgrade_type):
        """
        Purchase an upgrade if affordable.
        
        Args:
            upgrade_type (str): Type of upgrade
            
        Returns:
            bool: True if purchase successful
        """
        if not self.can_afford_upgrade(upgrade_type):
            return False
        
        costs = {
            UPGRADE_HULL: {RESOURCE_METAL: 5},
            UPGRADE_ENGINES: {RESOURCE_ICE: 3, RESOURCE_METAL: 2},
            UPGRADE_WEAPONS: {RESOURCE_CRYSTAL: 2, RESOURCE_METAL: 3},
            UPGRADE_SHIELDS: {RESOURCE_CRYSTAL: 3, RESOURCE_ICE: 2}
        }
        
        for resource_type, cost in costs[upgrade_type].items():
            self.resources[resource_type] -= cost
        
        return True
    
    def draw_resources(self, screen, font, x=10, y=200):
        """
        Draw resource inventory.
        
        Args:
            screen: Pygame screen surface
            font: Font to use for text
            x (int): X position
            y (int): Y position
        """
        resource_names = {
            RESOURCE_ICE: "Ice",
            RESOURCE_METAL: "Metal", 
            RESOURCE_CRYSTAL: "Crystal"
        }
        
        colors = {
            RESOURCE_ICE: (173, 216, 230),
            RESOURCE_METAL: (169, 169, 169),
            RESOURCE_CRYSTAL: (138, 43, 226)
        }
        
        for i, (resource_type, amount) in enumerate(self.resources.items()):
            name = resource_names[resource_type]
            color = colors[resource_type]
            text = font.render(f"{name}: {amount}", True, color)
            screen.blit(text, (x, y + i * 25))