"""
Game Constants

This module contains all the constant values used throughout the Asteroids game.
Centralizing constants makes it easy to balance gameplay and modify game behavior.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame

# === SCREEN SETTINGS ===
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# === SCORING SETTINGS ===
SCORE_LARGE_ASTEROID = 20    # Points for destroying large asteroids
SCORE_MEDIUM_ASTEROID = 50   # Points for destroying medium asteroids  
SCORE_SMALL_ASTEROID = 100   # Points for destroying small asteroids

# === PLAYER SETTINGS ===
PLAYER_RADIUS = 20           # Size of the player triangle
PLAYER_TURN_SPEED = 400      # Degrees per second rotation speed (increased from 300)
PLAYER_SPEED = 300           # Movement speed in pixels per second (increased from 200)
PLAYER_ACCELERATION = 1200   # Acceleration when moving (increased from 800 for rapid movement)
PLAYER_FRICTION = 0.88       # Friction coefficient (reduced from 0.92 for less drag)
PLAYER_SHOOT_SPEED = 500     # Bullet speed in pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3  # Time between shots in seconds
PLAYER_LIVES = 3             # Starting number of lives

# === ASTEROID SETTINGS ===
ASTEROID_MIN_RADIUS = 20     # Smallest asteroid size
ASTEROID_KINDS = 3           # Number of different asteroid sizes
ASTEROID_SPAWN_RATE = 0.8    # Time between asteroid spawns in seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS  # Largest asteroid size (60)

# === PROJECTILE SETTINGS ===
SHOT_RADIUS = 5              # Size of bullet circles

# === EFFECTS SETTINGS ===
PARTICLE_COUNT_SMALL = 5
PARTICLE_COUNT_MEDIUM = 8
PARTICLE_COUNT_LARGE = 12
PARTICLE_SPEED = 100
PARTICLE_LIFETIME = 1.0

# === PHASE 3: ADVANCED FEATURES ===

# Weapon types
WEAPON_NORMAL = "normal"
WEAPON_RAPID = "rapid"
WEAPON_SPREAD = "spread"
WEAPON_LASER = "laser"

# Weapon settings
RAPID_FIRE_COOLDOWN = 0.1    # Faster shooting
SPREAD_SHOT_COUNT = 3        # Number of bullets in spread
SPREAD_ANGLE = 0.5           # Angle between spread bullets
LASER_WIDTH = 5              # Laser beam width
LASER_RANGE = 600            # Laser beam range

# Power-up settings
POWERUP_SPEED = 50           # Power-up movement speed
POWERUP_SIZE = 15            # Power-up radius
POWERUP_SPAWN_CHANCE = 0.3   # Chance to spawn power-up when asteroid destroyed
SHIELD_DURATION = 10.0       # Shield protection time
SPEED_BOOST_DURATION = 8.0   # Speed boost time
SPEED_BOOST_MULTIPLIER = 2.0 # Speed increase factor

# Bomb settings
BOMB_RADIUS = 150            # Bomb explosion radius
BOMB_DAMAGE_RADIUS = 200     # Damage radius (larger than visual)
MAX_BOMBS = 3                # Maximum bombs player can carry
BOMB_COOLDOWN = 1.0          # Time between bomb drops

# Power-up types
POWERUP_SHIELD = "shield"
POWERUP_SPEED_BOOST = "speed"
POWERUP_RAPID_FIRE = "rapid_fire"
POWERUP_SPREAD_SHOT = "spread_shot"
POWERUP_BOMB = "bomb"

# Background
BACKGROUND_STAR_COUNT = 100
STAR_SPEED_MULTIPLIER = 0.1  # Stars move slower than objects

# === PHASE 4: ADVANCED FEATURES ===

# Audio settings
ENABLE_SOUND = True
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.5

# Enemy settings
UFO_SPAWN_CHANCE = 0.005     # Chance per frame to spawn UFO
UFO_SPEED = 100              # UFO movement speed
UFO_SHOOT_COOLDOWN = 1.5     # Time between UFO shots
UFO_HUNT_RANGE = 300         # Distance at which UFO targets player
UFO_RADIUS = 25              # UFO collision radius
UFO_SCORE = 500              # Points for destroying UFO

# Boss settings
BOSS_HEALTH = 100            # Boss hit points
BOSS_SPEED = 50              # Boss movement speed
BOSS_RADIUS = 80             # Boss collision radius
BOSS_SHOOT_COOLDOWN = 0.8    # Boss firing rate
BOSS_SCORE = 5000            # Points for defeating boss
BOSS_SPAWN_SCORE = 10000     # Score threshold to spawn boss

# Wave progression
WAVE_ASTEROID_INCREASE = 2   # Additional asteroids per wave
WAVE_SPEED_INCREASE = 1.1    # Speed multiplier per wave
MAX_WAVE = 20                # Maximum wave number

# Visual effects
THRUSTER_PARTICLE_COUNT = 3  # Particles per thruster flame
TRAIL_LENGTH = 5             # Length of movement trails
SCREEN_SHAKE_INTENSITY = 10  # Pixels of screen shake
SCREEN_SHAKE_DURATION = 0.3  # Seconds of screen shake

# Asteroid types
ASTEROID_ICE = "ice"
ASTEROID_METAL = "metal"
ASTEROID_CRYSTAL = "crystal"
ASTEROID_NORMAL = "normal"

# Asteroid type properties
ICE_SPEED_MULTIPLIER = 0.8   # Ice asteroids move slower
METAL_HEALTH = 2             # Metal asteroids take 2 hits
CRYSTAL_SPLIT_BONUS = 3      # Crystal asteroids split into more pieces

# Gravity wells
GRAVITY_WELL_RADIUS = 100    # Gravity effect radius
GRAVITY_WELL_STRENGTH = 200  # Gravity pull strength
GRAVITY_WELL_COUNT = 2       # Number of gravity wells

# Resource system
RESOURCE_ICE = "ice"
RESOURCE_METAL = "metal"
RESOURCE_CRYSTAL = "crystal"
MINING_RANGE = 50            # Range for mining asteroids

# Ship upgrades
UPGRADE_HULL = "hull"
UPGRADE_ENGINES = "engines"
UPGRADE_WEAPONS = "weapons"
UPGRADE_SHIELDS = "shields"

# Multiplayer
MAX_PLAYERS = 2              # Maximum players in co-op
PLAYER_2_KEYS = {            # Player 2 controls
    'left': pygame.K_j,
    'right': pygame.K_l,
    'up': pygame.K_i,
    'down': pygame.K_k,
    'shoot': pygame.K_u,
    'bomb': pygame.K_o
}

# === PROJECTILE SETTINGS ===
SHOT_RADIUS = 5              # Size of bullet circles