"""
Game Constants

This module contains all the constant values used throughout the Asteroids game.
Centralizing constants makes it easy to balance gameplay and modify game behavior.

Author: CodeWithEzeh
Date: October 2025
"""

# === SCREEN SETTINGS ===
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# === PLAYER SETTINGS ===
PLAYER_RADIUS = 20           # Size of the player triangle
PLAYER_TURN_SPEED = 300      # Degrees per second rotation speed
PLAYER_SPEED = 200           # Movement speed in pixels per second
PLAYER_SHOOT_SPEED = 500     # Bullet speed in pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3  # Time between shots in seconds

# === ASTEROID SETTINGS ===
ASTEROID_MIN_RADIUS = 20     # Smallest asteroid size
ASTEROID_KINDS = 3           # Number of different asteroid sizes
ASTEROID_SPAWN_RATE = 0.8    # Time between asteroid spawns in seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # Largest asteroid size (60)

# === PROJECTILE SETTINGS ===
SHOT_RADIUS = 5              # Size of bullet circles