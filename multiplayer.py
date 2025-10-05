"""
Multiplayer System

This module handles local co-op multiplayer functionality
with multiple players sharing the same screen.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
from player import Player
from constants import *


class MultiplayerPlayer(Player):
    """
    Player class extended for multiplayer support.
    """
    
    def __init__(self, x, y, player_id=1, controls=None):
        """
        Initialize a multiplayer player.
        
        Args:
            x (float): Starting X position
            y (float): Starting Y position
            player_id (int): Player number (1 or 2)
            controls (dict): Control mapping for this player
        """
        super().__init__(x, y)
        self.player_id = player_id
        self.controls = controls or self._get_default_controls(player_id)
        self.color = self._get_player_color(player_id)
        self.score = 0
        self.individual_lives = PLAYER_LIVES
        
    def _get_default_controls(self, player_id):
        """Get default controls for player."""
        if player_id == 1:
            return {
                'left': pygame.K_a,
                'right': pygame.K_d,
                'up': pygame.K_w,
                'down': pygame.K_s,
                'shoot': pygame.K_SPACE,
                'bomb': pygame.K_x
            }
        else:
            return PLAYER_2_KEYS
    
    def _get_player_color(self, player_id):
        """Get color for this player."""
        colors = {
            1: (255, 255, 255),  # White
            2: (255, 255, 0)     # Yellow
        }
        return colors.get(player_id, (255, 255, 255))
    
    def update(self, dt):
        """
        Update player with custom controls.
        
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

        # Handle player input with custom controls
        if keys[self.controls['left']]:    # Rotate left
            self.rotate(-dt)
        if keys[self.controls['right']]:   # Rotate right
            self.rotate(dt)
        if keys[self.controls['up']]:      # Thrust forward
            self.thrust_forward(dt)
        if keys[self.controls['down']]:    # Thrust backward
            self.thrust_backward(dt)
        # Note: Shooting and bombs handled in main loop
            
        # Apply physics with speed boost
        self.velocity += self.acceleration * dt
        self.velocity *= PLAYER_FRICTION  # Apply friction
        self.position += self.velocity * dt * self.speed_multiplier
        
        # Reset acceleration for next frame
        self.acceleration = pygame.Vector2(0, 0)
        
        # Wrap around screen edges
        self.wrap_around_screen()
    
    def draw(self, screen):
        """
        Draw the player with player-specific color.
        
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
        
        # Draw player triangle with player color
        player_color = self.color
        if self.speed_boost_timer > 0:
            # Modify color when speed boosted
            player_color = tuple(min(255, c + 50) for c in self.color)
            
        pygame.draw.polygon(screen, player_color, self.triangle(), 2)
        
        # Draw player number
        font = pygame.font.Font(None, 24)
        number_text = font.render(str(self.player_id), True, self.color)
        screen.blit(number_text, (self.position.x - 6, self.position.y - self.radius - 30))


class MultiplayerManager:
    """
    Manages multiplayer game state and coordination.
    """
    
    def __init__(self, num_players=2):
        """
        Initialize multiplayer manager.
        
        Args:
            num_players (int): Number of players (1-2)
        """
        self.num_players = min(num_players, MAX_PLAYERS)
        self.players = []
        self.shared_lives = PLAYER_LIVES
        self.individual_scores = True
        self.cooperative_mode = True
        
    def create_players(self):
        """Create all players at their starting positions."""
        self.players.clear()
        
        if self.num_players == 1:
            # Single player at center
            player = MultiplayerPlayer(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 1)
            self.players.append(player)
        else:
            # Two players side by side
            player1 = MultiplayerPlayer(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 1)
            player2 = MultiplayerPlayer(2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, 2)
            self.players.extend([player1, player2])
        
        return self.players
    
    def handle_input(self, weapon_managers, bomb_managers):
        """
        Handle input for all players.
        
        Args:
            weapon_managers (list): Weapon managers for each player
            bomb_managers (list): Bomb managers for each player
        """
        keys = pygame.key.get_pressed()
        
        for i, player in enumerate(self.players):
            if not player.alive():
                continue
                
            # Handle shooting
            if keys[player.controls['shoot']] and i < len(weapon_managers):
                if weapon_managers[i].can_shoot():
                    # This will be handled in main loop
                    pass
            
            # Handle bombs
            if keys[player.controls['bomb']] and i < len(bomb_managers):
                bomb_managers[i].drop_bomb(player.position.x, player.position.y)
    
    def handle_player_death(self, player_index):
        """
        Handle when a player dies.
        
        Args:
            player_index (int): Index of the player who died
            
        Returns:
            bool: True if game should continue, False if game over
        """
        if player_index >= len(self.players):
            return False
            
        player = self.players[player_index]
        
        if self.cooperative_mode:
            # In co-op mode, share lives
            self.shared_lives -= 1
            if self.shared_lives > 0:
                # Respawn player
                self._respawn_player(player_index)
                return True
            else:
                # Game over for all players
                return False
        else:
            # Individual lives
            player.individual_lives -= 1
            if player.individual_lives > 0:
                self._respawn_player(player_index)
                return True
            else:
                # This player is out, but others might continue
                return any(p.alive() and p.individual_lives > 0 for p in self.players)
    
    def _respawn_player(self, player_index):
        """Respawn a player at a safe location."""
        if player_index >= len(self.players):
            return
            
        old_player = self.players[player_index]
        
        # Find safe spawn location
        spawn_x, spawn_y = self._find_safe_spawn_location()
        
        # Create new player with same properties
        new_player = MultiplayerPlayer(spawn_x, spawn_y, old_player.player_id, old_player.controls)
        new_player.score = old_player.score
        new_player.individual_lives = old_player.individual_lives
        
        # Replace in list
        self.players[player_index] = new_player
    
    def _find_safe_spawn_location(self):
        """Find a safe location to spawn a player."""
        # Simple implementation: spawn at center
        # In a full implementation, you'd check for nearby asteroids/enemies
        return SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    def get_total_score(self):
        """Get combined score of all players."""
        return sum(player.score for player in self.players)
    
    def add_score(self, player_index, points):
        """
        Add score to a specific player.
        
        Args:
            player_index (int): Player to award points
            points (int): Points to add
        """
        if 0 <= player_index < len(self.players):
            self.players[player_index].score += points
    
    def draw_multiplayer_ui(self, screen, font):
        """
        Draw multiplayer-specific UI elements.
        
        Args:
            screen: Pygame screen surface
            font: Font for rendering text
        """
        y_offset = 10
        
        if self.cooperative_mode:
            # Shared lives
            lives_text = font.render(f"Lives: {self.shared_lives}", True, "white")
            screen.blit(lives_text, (10, y_offset))
            y_offset += 30
        
        # Individual player scores
        for i, player in enumerate(self.players):
            score_text = font.render(f"P{player.player_id} Score: {player.score}", True, player.color)
            screen.blit(score_text, (10, y_offset))
            y_offset += 25
            
            if not self.cooperative_mode:
                lives_text = font.render(f"P{player.player_id} Lives: {player.individual_lives}", True, player.color)
                screen.blit(lives_text, (10, y_offset))
                y_offset += 25
    
    def get_living_players(self):
        """Get list of players that are still alive."""
        return [player for player in self.players if player.alive()]
    
    def reset_for_new_game(self):
        """Reset multiplayer state for a new game."""
        self.shared_lives = PLAYER_LIVES
        for player in self.players:
            player.score = 0
            player.individual_lives = PLAYER_LIVES