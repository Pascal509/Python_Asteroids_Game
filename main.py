"""
Asteroids Game - Main Module

A classic Asteroids arcade game built with Python and Pygame.
Navigate your spaceship through an asteroid field, shooting asteroids 
while avoiding collisions.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
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


def create_player():
    """Create a new player at the center of the screen."""
    player_x = SCREEN_WIDTH / 2
    player_y = SCREEN_HEIGHT / 2
    return Player(player_x, player_y)


def main():
    """
    Main game function that initializes pygame, sets up sprite groups,
    and runs the main game loop.
    """
    # Initialize pygame library
    pygame.init()

    # Create sprite groups for game object management
    updatable = pygame.sprite.Group()  # Objects that need update() called
    drawable = pygame.sprite.Group()   # Objects that need draw() called
    asteroids = pygame.sprite.Group()  # All asteroid objects
    shots = pygame.sprite.Group()      # All bullet objects

    # Set up sprite group containers for automatic group membership
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  # Only needs updates, not drawing
    Shot.containers = (shots, updatable, drawable)

    # Initialize the game display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids Game")
    print(f"Starting Asteroids! \nScreen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")

    # Initialize game timing
    clock = pygame.time.Clock()
    dt = 0  # Delta time for frame-rate independent movement

    # Initialize game state
    game_state = GameState()
    effect_manager = EffectManager()
    
    # Phase 3: Initialize new systems
    powerup_manager = PowerUpManager()
    weapon_manager = WeaponManager()
    bomb_manager = BombManager()
    background = Background()

    # Create game objects
    # Player spawns in the center of the screen
    player = create_player()
    
    # Phase 3: Connect weapon manager to player
    player.weapon_manager = weapon_manager

    # Create asteroid spawner
    asteroid_field = AsteroidField()

    # Main game loop
    while True:
        # Handle pygame events (window close, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_state.game_over:
                    # Restart game
                    game_state.reset_game()
                    # Clear all existing objects
                    for asteroid in asteroids:
                        asteroid.kill()
                    for shot in shots:
                        shot.kill()
                    # Create new player
                    player.kill()
                    player = create_player()
                    player.weapon_manager = weapon_manager
                    
                    # Reset Phase 3 systems
                    weapon_manager.current_weapon = WEAPON_NORMAL
                    powerup_manager.powerups.empty()
                    bomb_manager.bombs.empty()
                elif event.key == pygame.K_x and not game_state.game_over:
                    # Drop bomb
                    bomb_manager.drop_bomb(player.position.x, player.position.y)

        # Skip game logic if game is over
        if game_state.game_over:
            screen.fill((0, 0, 0))
            game_state.draw_ui(screen)
            pygame.display.flip()
            dt = clock.tick(60) / 1000
            continue

        # Clear the screen with black background
        screen.fill((0, 0, 0))
        
        # Phase 3: Draw background
        background.update(dt, player.velocity if 'player' in locals() and player.alive() else pygame.Vector2(0, 0))
        background.draw(screen)
        
        # Update all game objects (movement, input, spawning)
        updatable.update(dt)
        
        # Handle weapon shooting (after player update to avoid conflicts)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and weapon_manager.can_shoot():
            weapon_manager.shoot(player.position, player.rotation, shots)
        
        # Phase 3: Update new systems
        powerup_manager.update(dt)
        weapon_manager.update(dt)
        bomb_manager.update(dt)
        
        # Update visual effects
        effect_manager.update(dt)
        
        # === COLLISION DETECTION ===
        
        # Phase 3: Check power-up collection
        collected_powerup = powerup_manager.check_player_collision(player)
        if collected_powerup:
            if collected_powerup == POWERUP_BOMB:
                # Special case: bomb power-up doesn't change weapons, just restocks bombs
                pass  # Player automatically gets bomb capacity
            else:
                player.apply_powerup(collected_powerup)
        
        # Check for collisions between player and asteroids (Life lost)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if player.is_shielded():
                    # Shield protects player - destroy asteroid without losing life
                    if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:
                        game_state.add_score(SCORE_LARGE_ASTEROID)
                        effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "large")
                    elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                        game_state.add_score(SCORE_MEDIUM_ASTEROID)
                        effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "medium")
                    else:
                        game_state.add_score(SCORE_SMALL_ASTEROID)
                        effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "small")
                    asteroid.split()
                else:
                    # Normal collision - lose life
                    if game_state.lose_life():
                        # Player still has lives - respawn
                        player.kill()
                        player = create_player()
                        player.weapon_manager = weapon_manager
                    else:
                        # Game over
                        player.kill()
                break
        
        # Check for collisions between bullets and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    # Create explosion effect at asteroid position
                    if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:  # Large asteroid
                        game_state.add_score(SCORE_LARGE_ASTEROID)
                        effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "large")
                        # Phase 3: Maybe spawn power-up
                        powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
                    elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:  # Medium asteroid
                        game_state.add_score(SCORE_MEDIUM_ASTEROID)
                        effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "medium")
                        powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
                    else:  # Small asteroid
                        game_state.add_score(SCORE_SMALL_ASTEROID)
                        effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "small")
                        powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
                    
                    asteroid.split()  # Split asteroid into smaller pieces
                    shot.kill()       # Remove the bullet
        
        # Phase 3: Check laser hits
        laser_hits = weapon_manager.check_laser_hits(asteroids)
        for asteroid in laser_hits:
            if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:
                game_state.add_score(SCORE_LARGE_ASTEROID)
                effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "large")
                powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
            elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                game_state.add_score(SCORE_MEDIUM_ASTEROID)
                effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "medium")
                powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
            else:
                game_state.add_score(SCORE_SMALL_ASTEROID)
                effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "small")
                powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
            asteroid.split()
        
        # Phase 3: Check bomb explosions
        bomb_hits = bomb_manager.check_explosions(asteroids)
        for asteroid in bomb_hits:
            if asteroid.radius >= ASTEROID_MIN_RADIUS * 3:
                game_state.add_score(SCORE_LARGE_ASTEROID)
                effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "large")
                powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
            elif asteroid.radius >= ASTEROID_MIN_RADIUS * 2:
                game_state.add_score(SCORE_MEDIUM_ASTEROID)
                effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "medium")
                powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
            else:
                game_state.add_score(SCORE_SMALL_ASTEROID)
                effect_manager.create_explosion(asteroid.position.x, asteroid.position.y, "small")
                powerup_manager.maybe_spawn_powerup(asteroid.position.x, asteroid.position.y)
            asteroid.split()
        
        # === RENDERING ===
        
        # Draw all drawable objects to the screen
        for drawable_object in drawable:
            drawable_object.draw(screen)
        
        # Phase 3: Draw new systems
        powerup_manager.draw(screen)
        weapon_manager.draw(screen)  # For laser effects
        bomb_manager.draw(screen)
        
        # Draw visual effects
        effect_manager.draw(screen)
        
        # Draw UI elements
        game_state.draw_ui(screen)
        
        # Phase 3: Draw enhanced UI
        if 'player' in locals() and player.alive():
            game_state.draw_phase3_ui(screen, player, weapon_manager, bomb_manager)
        
        # Update the display
        pygame.display.flip()
        
        # Control frame rate and calculate delta time
        dt = clock.tick(60) / 1000  # 60 FPS, convert ms to seconds


if __name__ == "__main__":
    main()