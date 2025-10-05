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

    # Create game objects
    # Player spawns in the center of the screen
    player_x = SCREEN_WIDTH / 2
    player_y = SCREEN_HEIGHT / 2
    player = Player(player_x, player_y)

    # Create asteroid spawner
    asteroid_field = AsteroidField()

    # Main game loop
    while True:
        # Handle pygame events (window close, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Clear the screen with black background
        screen.fill((0, 0, 0))
        
        # Update all game objects (movement, input, spawning)
        updatable.update(dt)
        
        # === COLLISION DETECTION ===
        
        # Check for collisions between player and asteroids (Game Over)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                return
        
        # Check for collisions between bullets and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()  # Split asteroid into smaller pieces
                    shot.kill()       # Remove the bullet
        
        # === RENDERING ===
        
        # Draw all drawable objects to the screen
        for drawable_object in drawable:
            drawable_object.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Control frame rate and calculate delta time
        dt = clock.tick(60) / 1000  # 60 FPS, convert ms to seconds


if __name__ == "__main__":
    main()