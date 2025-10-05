"""
Asteroids Game - Phase 4 Enhanced Main

Complete integration of all Phase 4 advanced features including:
- Audio system with sound effects
- Enemy ships (UFOs and bosses)
- Wave progression with high scores
- Enhanced visual effects with thruster flames and screen shake
- Advanced asteroid types with mining
- Ship upgrades and customization
- Local multiplayer support

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import sys
import random
from constants import *
from player import Player
from asteroid import Asteroid, AsteroidField
from shot import Shot
from gamestate import GameState
from effects import EffectManager
from powerup import PowerUpManager
from weapon import WeaponManager
from bomb import BombManager
from background import Background

# Phase 4 imports
from audio import AudioManager
from enemies import EnemyManager
from progression import WaveManager, HighScoreManager, ProgressionUI
from enhanced_effects import EnhancedEffectManager
from advanced_asteroids import AdvancedAsteroid, GravityWell, ResourceManager
from upgrades import UpgradeManager
from multiplayer import MultiplayerManager


class GameMode:
    """Game mode constants."""
    SINGLE_PLAYER = "single"
    MULTIPLAYER = "multiplayer"
    MENU = "menu"


class AsteroidsGamePhase4:
    """
    Main game class for Phase 4 enhanced Asteroids game.
    """
    
    def __init__(self):
        """Initialize the enhanced game."""
        pygame.init()
        
        # Core game setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids Game - Phase 4 Enhanced")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.game_mode = GameMode.MENU
        self.running = True
        self.paused = False
        
        # Sprite groups
        self.setup_sprite_groups()
        
        # Phase 4 managers
        self.audio_manager = AudioManager()
        self.enemy_manager = EnemyManager()
        self.wave_manager = WaveManager()
        self.high_score_manager = HighScoreManager()
        self.progression_ui = ProgressionUI()
        self.enhanced_effects = EnhancedEffectManager()
        self.resource_manager = ResourceManager()
        self.upgrade_manager = UpgradeManager()
        self.multiplayer_manager = MultiplayerManager()
        
        # Original managers
        self.game_state = GameState()
        self.effect_manager = EffectManager()
        self.powerup_manager = PowerUpManager()
        self.background = Background()
        
        # Player-specific managers (support for multiplayer)
        self.weapon_managers = []
        self.bomb_managers = []
        
        # Game objects
        self.players = []
        self.asteroid_field = None
        self.gravity_wells = []
        
        # UI state
        self.show_menu = True
        self.menu_selection = 0
        self.menu_options = ["Single Player", "Multiplayer", "High Scores", "Quit"]
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        print("Phase 4 Enhanced Asteroids initialized!")
        
    def setup_sprite_groups(self):
        """Set up sprite groups for game objects."""
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        
        # Set up containers
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AdvancedAsteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = (self.updatable,)
        Shot.containers = (self.shots, self.updatable, self.drawable)
    
    def start_game(self, mode=GameMode.SINGLE_PLAYER):
        """
        Start a new game.
        
        Args:
            mode (str): Game mode to start
        """
        self.game_mode = mode
        self.show_menu = False
        
        # Clear existing game objects
        self.clear_game_objects()
        
        # Set up multiplayer
        if mode == GameMode.MULTIPLAYER:
            self.multiplayer_manager = MultiplayerManager(2)
            self.players = self.multiplayer_manager.create_players()
        else:
            self.multiplayer_manager = MultiplayerManager(1)
            self.players = self.multiplayer_manager.create_players()
        
        # Set up player-specific managers
        self.weapon_managers = [WeaponManager() for _ in self.players]
        self.bomb_managers = [BombManager() for _ in self.players]
        
        # Connect weapon managers to players
        for i, player in enumerate(self.players):
            if i < len(self.weapon_managers):
                player.weapon_manager = self.weapon_managers[i]
        
        # Set up enemy AI
        for player in self.players:
            self.enemy_manager.set_player_reference(player)
        
        # Create asteroid field
        self.asteroid_field = AsteroidField()
        
        # Start first wave
        self.wave_manager.start_wave(1)
        
        # Create gravity wells
        self.create_gravity_wells()
        
        # Reset game state
        self.game_state.reset_game()
        self.multiplayer_manager.reset_for_new_game()
        
        # Play background music
        self.audio_manager.play_music()
        
        print(f"Started {mode} game!")
    
    def create_gravity_wells(self):
        """Create gravity wells at random locations."""
        self.gravity_wells.clear()
        for _ in range(GRAVITY_WELL_COUNT):
            x = random.uniform(100, SCREEN_WIDTH - 100)
            y = random.uniform(100, SCREEN_HEIGHT - 100)
            self.gravity_wells.append(GravityWell(x, y))
    
    def clear_game_objects(self):
        """Clear all game objects."""
        for group in [self.updatable, self.drawable, self.asteroids, self.shots]:
            group.empty()
        self.enemy_manager.clear_all()
        self.enhanced_effects.clear_trails()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            if event.type == pygame.KEYDOWN:
                if self.show_menu:
                    self.handle_menu_input(event.key)
                else:
                    self.handle_game_input(event.key)
    
    def handle_menu_input(self, key):
        """Handle menu navigation."""
        if key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
        elif key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
        elif key == pygame.K_RETURN:
            option = self.menu_options[self.menu_selection]
            if option == "Single Player":
                self.start_game(GameMode.SINGLE_PLAYER)
            elif option == "Multiplayer":
                self.start_game(GameMode.MULTIPLAYER)
            elif option == "High Scores":
                self.game_mode = "high_scores"
                self.show_menu = False
            elif option == "Quit":
                self.running = False
        elif key == pygame.K_ESCAPE:
            self.running = False
    
    def handle_game_input(self, key):
        """Handle in-game input."""
        if key == pygame.K_ESCAPE:
            if self.game_mode in ["high_scores"]:
                self.show_menu = True
                self.game_mode = GameMode.MENU
            else:
                self.paused = not self.paused
        elif key == pygame.K_r and self.game_state.game_over:
            # Restart game
            self.start_game(self.game_mode)
        elif key == pygame.K_u:  # Upgrade menu
            self.upgrade_manager.toggle_upgrade_menu()
        elif key == pygame.K_m and self.game_state.game_over:
            # Return to menu
            self.show_menu = True
            self.game_mode = GameMode.MENU
    
    def update_game(self, dt):
        """
        Update game logic.
        
        Args:
            dt (float): Delta time since last frame
        """
        if self.paused or self.show_menu:
            return
            
        # Handle multiplayer input
        if self.game_mode in [GameMode.SINGLE_PLAYER, GameMode.MULTIPLAYER]:
            self.multiplayer_manager.handle_input(self.weapon_managers, self.bomb_managers)
            
            # Handle weapon shooting for each player
            keys = pygame.key.get_pressed()
            for i, player in enumerate(self.players):
                if player.alive() and i < len(self.weapon_managers):
                    if keys[player.controls['shoot']] and self.weapon_managers[i].can_shoot():
                        self.weapon_managers[i].shoot(player.position, player.rotation, self.shots)
                        self.audio_manager.play_sound('shoot')
        
        # Handle upgrade menu
        keys = pygame.key.get_pressed()
        if self.upgrade_manager.handle_upgrade_input(keys, self.resource_manager):
            # Apply upgrades to all players
            for player in self.players:
                self.upgrade_manager.apply_upgrades_to_player(player)
        
        # Update background
        player_velocity = pygame.Vector2(0, 0)
        if self.players and self.players[0].alive():
            player_velocity = self.players[0].velocity
        self.background.update(dt, player_velocity)
        
        # Update all game objects
        self.updatable.update(dt)
        
        # Update Phase 4 systems
        self.powerup_manager.update(dt)
        for weapon_manager in self.weapon_managers:
            weapon_manager.update(dt)
        for bomb_manager in self.bomb_managers:
            bomb_manager.update(dt)
        
        # Update enhanced systems
        total_score = self.multiplayer_manager.get_total_score()
        self.enemy_manager.update(dt, total_score)
        self.wave_manager.update(dt)
        self.enhanced_effects.update(dt)
        for gravity_well in self.gravity_wells:
            gravity_well.update(dt)
        
        # Apply gravity effects
        for gravity_well in self.gravity_wells:
            for player in self.players:
                if player.alive():
                    gravity_well.apply_gravity(player)
            for asteroid in self.asteroids:
                gravity_well.apply_gravity(asteroid)
        
        # Add thruster effects for moving players
        for player in self.players:
            if player.alive() and keys[player.controls['up']]:
                thrust_direction = pygame.Vector2(0, -1).rotate(player.rotation)
                self.enhanced_effects.create_thruster_flame(
                    player.position.x, player.position.y, 
                    thrust_direction, 0.8
                )
                self.audio_manager.play_sound('thrust')
        
        # Update collision detection
        self.handle_collisions()
        
        # Check wave progression
        if self.wave_manager.is_wave_complete():
            if self.wave_manager.should_advance_wave():
                self.advance_to_next_wave()
        
        # Check if all asteroids are destroyed
        if len(self.asteroids) == 0 and not self.wave_manager.is_wave_complete():
            self.wave_manager.asteroid_destroyed()
    
    def handle_collisions(self):
        """Handle all collision detection."""
        living_players = self.multiplayer_manager.get_living_players()
        
        # Power-up collection
        for i, player in enumerate(living_players):
            collected_powerup = self.powerup_manager.check_player_collision(player)
            if collected_powerup:
                player.apply_powerup(collected_powerup)
                self.audio_manager.play_sound('powerup')
        
        # Player-asteroid collisions
        for i, player in enumerate(living_players):
            for asteroid in self.asteroids:
                if player.collides_with(asteroid):
                    if player.is_shielded():
                        # Shield protects - destroy asteroid
                        self.destroy_asteroid(asteroid, i)
                    else:
                        # Player takes damage
                        self.enhanced_effects.create_explosion(player.position.x, player.position.y, "medium")
                        if not self.multiplayer_manager.handle_player_death(i):
                            self.end_game()
                        self.audio_manager.play_sound('explosion')
                    break
        
        # Player-enemy collisions
        for i, player in enumerate(living_players):
            for enemy in self.enemy_manager.get_all_enemies():
                if player.collides_with(enemy):
                    if not player.is_shielded():
                        self.enhanced_effects.create_explosion(player.position.x, player.position.y, "medium")
                        if not self.multiplayer_manager.handle_player_death(i):
                            self.end_game()
                        self.audio_manager.play_sound('explosion')
                    break
        
        # Shot-asteroid collisions
        for asteroid in list(self.asteroids):
            for shot in list(self.shots):
                if asteroid.collides_with(shot):
                    self.destroy_asteroid(asteroid, 0)  # Award to player 0 for now
                    shot.kill()
                    break
        
        # Shot-enemy collisions
        for enemy in list(self.enemy_manager.get_all_enemies()):
            for shot in list(self.shots):
                if hasattr(enemy, 'collides_with') and enemy.collides_with(shot):
                    # Award points and destroy enemy
                    if hasattr(enemy, 'take_damage'):
                        if enemy.take_damage():
                            score = UFO_SCORE if hasattr(enemy, 'shoot_timer') else BOSS_SCORE
                            self.multiplayer_manager.add_score(0, score)
                            self.enhanced_effects.create_explosion(enemy.position.x, enemy.position.y, "large")
                            enemy.kill()
                            self.audio_manager.play_sound('explosion')
                    shot.kill()
                    break
        
        # Laser hits
        for i, weapon_manager in enumerate(self.weapon_managers):
            laser_hits = weapon_manager.check_laser_hits(self.asteroids)
            for asteroid in laser_hits:
                self.destroy_asteroid(asteroid, i)
        
        # Bomb explosions
        for i, bomb_manager in enumerate(self.bomb_managers):
            bomb_hits = bomb_manager.check_explosions(self.asteroids)
            for asteroid in bomb_hits:
                self.destroy_asteroid(asteroid, i)
    
    def destroy_asteroid(self, asteroid, player_index):
        """
        Destroy an asteroid and handle rewards.
        
        Args:
            asteroid: Asteroid to destroy
            player_index (int): Player who destroyed it
        """
        # Award points
        if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:
            points = SCORE_LARGE_ASTEROID
            explosion_size = "large"
        elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
            points = SCORE_MEDIUM_ASTEROID
            explosion_size = "medium"
        else:
            points = SCORE_SMALL_ASTEROID
            explosion_size = "small"
        
        self.multiplayer_manager.add_score(player_index, points)
        
        # Create explosion
        self.enhanced_effects.create_explosion(asteroid.position.x, asteroid.position.y, explosion_size)
        
        # Maybe spawn power-up
        self.powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
        
        # Collect resources if it's an advanced asteroid
        if hasattr(asteroid, 'resources'):
            self.resource_manager.add_resources(asteroid.resources)
        
        # Update statistics
        self.high_score_manager.update_stats(asteroids_destroyed=1)
        
        # Split asteroid
        asteroid.split()
        
        # Update wave progress
        self.wave_manager.asteroid_destroyed()
        
        self.audio_manager.play_sound('explosion')
    
    def advance_to_next_wave(self):
        """Advance to the next wave."""
        # Award wave completion bonus
        bonus = self.wave_manager.get_wave_bonus()
        for i in range(len(self.players)):
            self.multiplayer_manager.add_score(i, bonus)
        
        # Start next wave
        next_wave = self.wave_manager.current_wave + 1
        self.wave_manager.start_wave(next_wave)
        
        # Spawn new asteroids with increased difficulty
        if self.asteroid_field:
            self.asteroid_field.kill()
        self.asteroid_field = AsteroidField()
    
    def end_game(self):
        """End the current game."""
        self.game_state.game_over = True
        
        # Record high score
        total_score = self.multiplayer_manager.get_total_score()
        wave_reached = self.wave_manager.current_wave
        self.high_score_manager.add_score(total_score, wave_reached)
        
        self.audio_manager.stop_music()
    
    def draw(self):
        """Render the game."""
        self.screen.fill((0, 0, 0))
        
        if self.show_menu:
            self.draw_menu()
        elif self.game_mode == "high_scores":
            self.draw_high_scores()
        else:
            self.draw_game()
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Draw the main menu."""
        # Title
        title = self.large_font.render("ASTEROIDS PHASE 4", True, "white")
        title_x = SCREEN_WIDTH // 2 - title.get_width() // 2
        self.screen.blit(title, (title_x, 100))
        
        subtitle = self.font.render("Enhanced Edition", True, "gray")
        subtitle_x = SCREEN_WIDTH // 2 - subtitle.get_width() // 2
        self.screen.blit(subtitle, (subtitle_x, 160))
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            color = "yellow" if i == self.menu_selection else "white"
            option_text = self.font.render(option, True, color)
            option_x = SCREEN_WIDTH // 2 - option_text.get_width() // 2
            self.screen.blit(option_text, (option_x, 250 + i * 50))
        
        # Instructions
        instruction = self.font.render("↑↓: Navigate, Enter: Select, Esc: Quit", True, "gray")
        instruction_x = SCREEN_WIDTH // 2 - instruction.get_width() // 2
        self.screen.blit(instruction, (instruction_x, 500))
    
    def draw_high_scores(self):
        """Draw the high scores screen."""
        self.progression_ui.draw_high_scores(self.screen, self.high_score_manager)
        self.progression_ui.draw_statistics(self.screen, self.high_score_manager)
        
        # Back instruction
        back_text = self.font.render("Press ESC to return to menu", True, "white")
        back_x = SCREEN_WIDTH // 2 - back_text.get_width() // 2
        self.screen.blit(back_text, (back_x, SCREEN_HEIGHT - 50))
    
    def draw_game(self):
        """Draw the main game."""
        # Background
        self.background.draw(self.screen)
        
        # Game objects
        for drawable_object in self.drawable:
            drawable_object.draw(self.screen)
        
        # Phase 4 objects
        self.powerup_manager.draw(self.screen)
        for weapon_manager in self.weapon_managers:
            weapon_manager.draw(self.screen)
        for bomb_manager in self.bomb_managers:
            bomb_manager.draw(self.screen)
        
        # Enhanced effects
        self.enhanced_effects.draw(self.screen)
        
        # Enemies
        self.enemy_manager.draw(self.screen)
        
        # Gravity wells
        for gravity_well in self.gravity_wells:
            gravity_well.draw(self.screen)
        
        # UI
        self.draw_ui()
        
        # Upgrade menu
        self.upgrade_manager.draw_upgrade_menu(self.screen, self.font, self.resource_manager)
        
        # Pause overlay
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.large_font.render("PAUSED", True, "white")
            pause_x = SCREEN_WIDTH // 2 - pause_text.get_width() // 2
            pause_y = SCREEN_HEIGHT // 2 - pause_text.get_height() // 2
            self.screen.blit(pause_text, (pause_x, pause_y))
    
    def draw_ui(self):
        """Draw the game UI."""
        # Basic game state
        self.game_state.draw_ui(self.screen)
        
        # Multiplayer UI
        if self.game_mode == GameMode.MULTIPLAYER:
            self.multiplayer_manager.draw_multiplayer_ui(self.screen, self.font)
        
        # Wave information
        self.progression_ui.draw_wave_info(self.screen, self.wave_manager)
        
        # Resources
        self.resource_manager.draw_resources(self.screen, self.font)
        
        # Phase 3 UI (weapons, power-ups, bombs)
        if self.players and self.players[0].alive():
            weapon_manager = self.weapon_managers[0] if self.weapon_managers else None
            bomb_manager = self.bomb_managers[0] if self.bomb_managers else None
            self.game_state.draw_phase3_ui(self.screen, self.players[0], weapon_manager, bomb_manager)
    
    def run(self):
        """Main game loop."""
        print("Starting Phase 4 Enhanced Asteroids Game...")
        
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS
            
            self.handle_events()
            self.update_game(dt)
            self.draw()
        
        # Cleanup
        self.audio_manager.cleanup()
        pygame.quit()
        sys.exit()


def main():
    """Main function to start the enhanced game."""
    game = AsteroidsGamePhase4()
    game.run()


if __name__ == "__main__":
    main()