"""
Enemy System

This module contains enemy ships including UFOs and boss enemies.
Enemies have AI behavior to hunt and attack the player.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import random
import math
from circleshape import CircleShape
from shot import Shot
from constants import *


class UFO(CircleShape):
    """
    UFO enemy that hunts the player and shoots at them.
    """
    
    def __init__(self, x, y):
        """
        Initialize a UFO enemy.
        
        Args:
            x (float): X position
            y (float): Y position
        """
        super().__init__(x, y, UFO_RADIUS)
        self.velocity = pygame.Vector2(
            random.uniform(-UFO_SPEED, UFO_SPEED),
            random.uniform(-UFO_SPEED, UFO_SPEED)
        )
        self.shoot_timer = 0
        self.target_player = None
        self.rotation = 0
        self.rotation_speed = random.uniform(50, 150)
        
    def update(self, dt):
        """
        Update UFO position and AI behavior.
        
        Args:
            dt (float): Delta time since last frame
        """
        # Update shooting timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            
        # Rotate for visual effect
        self.rotation += self.rotation_speed * dt
        
        # AI: Hunt the player if in range
        if self.target_player and self.target_player.alive():
            distance = (self.target_player.position - self.position).length()
            
            if distance < UFO_HUNT_RANGE:
                # Move toward player
                direction = (self.target_player.position - self.position).normalize()
                self.velocity = direction * UFO_SPEED
                
                # Shoot at player
                if self.shoot_timer <= 0:
                    self.shoot_at_player()
                    self.shoot_timer = UFO_SHOOT_COOLDOWN
            else:
                # Wander randomly
                if random.random() < 0.02:  # 2% chance per frame to change direction
                    angle = random.uniform(0, 2 * math.pi)
                    self.velocity = pygame.Vector2(
                        math.cos(angle) * UFO_SPEED,
                        math.sin(angle) * UFO_SPEED
                    )
        
        # Update position
        self.position += self.velocity * dt
        self.wrap_around_screen()
    
    def shoot_at_player(self):
        """Shoot a bullet toward the player."""
        if not self.target_player or not self.target_player.alive():
            return
            
        # Calculate direction to player
        direction = (self.target_player.position - self.position).normalize()
        
        # Create bullet
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = direction * PLAYER_SHOOT_SPEED * 0.8  # Slightly slower than player
        
        # Add to shots group (will be handled by main game)
        if hasattr(Shot, 'containers') and Shot.containers:
            for container in Shot.containers:
                if hasattr(container, 'add'):
                    container.add(shot)
    
    def draw(self, screen):
        """
        Draw the UFO as a classic flying saucer.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # UFO body (ellipse)
        body_rect = pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius // 2,
            self.radius * 2,
            self.radius
        )
        pygame.draw.ellipse(screen, (150, 150, 150), body_rect)
        pygame.draw.ellipse(screen, (200, 200, 200), body_rect, 2)
        
        # UFO dome
        dome_rect = pygame.Rect(
            self.position.x - self.radius // 2,
            self.position.y - self.radius,
            self.radius,
            self.radius
        )
        pygame.draw.ellipse(screen, (100, 100, 255), dome_rect)
        pygame.draw.ellipse(screen, (150, 150, 255), dome_rect, 2)
        
        # Lights around the edge
        for i in range(6):
            angle = (self.rotation + i * 60) * math.pi / 180
            light_x = self.position.x + (self.radius * 0.8) * math.cos(angle)
            light_y = self.position.y + (self.radius * 0.4) * math.sin(angle)
            
            # Blinking lights
            if (pygame.time.get_ticks() + i * 100) % 1000 < 500:
                color = (255, 255, 0)  # Yellow
            else:
                color = (100, 100, 0)  # Dim yellow
                
            pygame.draw.circle(screen, color, (int(light_x), int(light_y)), 3)


class Boss(CircleShape):
    """
    Large boss enemy with multiple attack patterns and high health.
    """
    
    def __init__(self, x, y):
        """
        Initialize a boss enemy.
        
        Args:
            x (float): X position
            y (float): Y position
        """
        super().__init__(x, y, BOSS_RADIUS)
        self.health = BOSS_HEALTH
        self.max_health = BOSS_HEALTH
        self.velocity = pygame.Vector2(0, 0)
        self.shoot_timer = 0
        self.target_player = None
        self.rotation = 0
        self.attack_pattern = 0
        self.pattern_timer = 0
        self.movement_timer = 0
        
    def update(self, dt):
        """
        Update boss behavior and attack patterns.
        
        Args:
            dt (float): Delta time since last frame
        """
        # Update timers
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        self.pattern_timer += dt
        self.movement_timer += dt
        
        # Rotate for intimidation
        self.rotation += 30 * dt
        
        # Change attack pattern every 5 seconds
        if self.pattern_timer > 5.0:
            self.attack_pattern = (self.attack_pattern + 1) % 3
            self.pattern_timer = 0
            
        # Movement patterns
        if self.movement_timer > 3.0:
            # Change movement direction
            angle = random.uniform(0, 2 * math.pi)
            self.velocity = pygame.Vector2(
                math.cos(angle) * BOSS_SPEED,
                math.sin(angle) * BOSS_SPEED
            )
            self.movement_timer = 0
        
        # Attack patterns
        if self.target_player and self.target_player.alive() and self.shoot_timer <= 0:
            if self.attack_pattern == 0:
                self.attack_direct()
            elif self.attack_pattern == 1:
                self.attack_spread()
            else:
                self.attack_spiral()
            
            self.shoot_timer = BOSS_SHOOT_COOLDOWN
        
        # Update position
        self.position += self.velocity * dt
        self.wrap_around_screen()
    
    def attack_direct(self):
        """Direct shot at player."""
        if not self.target_player:
            return
            
        direction = (self.target_player.position - self.position).normalize()
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = direction * PLAYER_SHOOT_SPEED
        self._add_shot(shot)
    
    def attack_spread(self):
        """Spread shot pattern."""
        if not self.target_player:
            return
            
        base_direction = (self.target_player.position - self.position).normalize()
        
        # Fire 5 shots in a spread
        for i in range(5):
            angle_offset = (i - 2) * 0.3  # Spread of 0.3 radians each
            direction = base_direction.rotate(angle_offset * 180 / math.pi)
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * PLAYER_SHOOT_SPEED
            self._add_shot(shot)
    
    def attack_spiral(self):
        """Spiral shot pattern."""
        # Fire shots in all directions
        for i in range(8):
            angle = (self.rotation + i * 45) * math.pi / 180
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = direction * PLAYER_SHOOT_SPEED * 0.7
            self._add_shot(shot)
    
    def _add_shot(self, shot):
        """Add shot to appropriate containers."""
        if hasattr(Shot, 'containers') and Shot.containers:
            for container in Shot.containers:
                if hasattr(container, 'add'):
                    container.add(shot)
    
    def take_damage(self, damage=1):
        """
        Take damage and return if boss is destroyed.
        
        Args:
            damage (int): Amount of damage to take
            
        Returns:
            bool: True if boss is destroyed
        """
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen):
        """
        Draw the boss enemy.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        # Main body
        pygame.draw.circle(screen, (100, 50, 50), 
                          (int(self.position.x), int(self.position.y)), 
                          int(self.radius), 3)
        
        # Inner core
        pygame.draw.circle(screen, (150, 75, 75), 
                          (int(self.position.x), int(self.position.y)), 
                          int(self.radius * 0.7), 2)
        
        # Rotating arms
        for i in range(4):
            angle = (self.rotation + i * 90) * math.pi / 180
            start_x = self.position.x + (self.radius * 0.3) * math.cos(angle)
            start_y = self.position.y + (self.radius * 0.3) * math.sin(angle)
            end_x = self.position.x + self.radius * math.cos(angle)
            end_y = self.position.y + self.radius * math.sin(angle)
            
            pygame.draw.line(screen, (200, 100, 100), 
                           (start_x, start_y), (end_x, end_y), 4)
        
        # Health bar
        bar_width = self.radius * 2
        bar_height = 8
        bar_x = self.position.x - bar_width // 2
        bar_y = self.position.y - self.radius - 20
        
        # Background
        pygame.draw.rect(screen, (100, 100, 100), 
                        (bar_x, bar_y, bar_width, bar_height))
        
        # Health
        health_percentage = self.health / self.max_health
        health_width = bar_width * health_percentage
        health_color = (255, 0, 0) if health_percentage < 0.3 else (255, 255, 0) if health_percentage < 0.7 else (0, 255, 0)
        
        pygame.draw.rect(screen, health_color, 
                        (bar_x, bar_y, health_width, bar_height))


class EnemyManager:
    """
    Manages spawning and behavior of all enemy types.
    """
    
    def __init__(self):
        """Initialize the enemy manager."""
        self.ufos = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.player_reference = None
        self.boss_spawned = False
        
    def set_player_reference(self, player):
        """
        Set reference to player for enemy AI.
        
        Args:
            player: Player object for enemies to target
        """
        self.player_reference = player
        
        # Update existing enemies
        for ufo in self.ufos:
            ufo.target_player = player
        for boss in self.bosses:
            boss.target_player = player
    
    def update(self, dt, current_score):
        """
        Update all enemies and handle spawning.
        
        Args:
            dt (float): Delta time since last frame
            current_score (int): Current player score for boss spawning
        """
        # Spawn UFOs randomly
        if random.random() < UFO_SPAWN_CHANCE:
            self.spawn_ufo()
        
        # Spawn boss if score threshold reached
        if current_score >= BOSS_SPAWN_SCORE and not self.boss_spawned and len(self.bosses) == 0:
            self.spawn_boss()
            self.boss_spawned = True
        
        # Update all enemies
        self.ufos.update(dt)
        self.bosses.update(dt)
    
    def spawn_ufo(self):
        """Spawn a UFO at a random edge of the screen."""
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        
        if edge == 'top':
            x, y = random.uniform(0, SCREEN_WIDTH), -UFO_RADIUS
        elif edge == 'bottom':
            x, y = random.uniform(0, SCREEN_WIDTH), SCREEN_HEIGHT + UFO_RADIUS
        elif edge == 'left':
            x, y = -UFO_RADIUS, random.uniform(0, SCREEN_HEIGHT)
        else:  # right
            x, y = SCREEN_WIDTH + UFO_RADIUS, random.uniform(0, SCREEN_HEIGHT)
        
        ufo = UFO(x, y)
        ufo.target_player = self.player_reference
        self.ufos.add(ufo)
    
    def spawn_boss(self):
        """Spawn a boss at the center of the screen."""
        boss = Boss(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        boss.target_player = self.player_reference
        self.bosses.add(boss)
    
    def draw(self, screen):
        """
        Draw all enemies.
        
        Args:
            screen: Pygame screen surface to draw on
        """
        for ufo in self.ufos:
            ufo.draw(screen)
        for boss in self.bosses:
            boss.draw(screen)
    
    def get_all_enemies(self):
        """
        Get all enemy objects for collision detection.
        
        Returns:
            list: All enemy objects
        """
        return list(self.ufos) + list(self.bosses)
    
    def clear_all(self):
        """Clear all enemies."""
        self.ufos.empty()
        self.bosses.empty()
        self.boss_spawned = False