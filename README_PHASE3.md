# Asteroids Game - Enhanced Edition

A feature-rich implementation of the classic Asteroids arcade game built with Python and Pygame. This enhanced version includes advanced gameplay mechanics, visual effects, and power-up systems.

## 🎮 Game Features

### Core Gameplay
- **Triangular Spaceship**: Navigate your ship with realistic acceleration physics
- **Lumpy Asteroids**: Irregular, visually interesting asteroid shapes that split when destroyed
- **Multiple Lives**: Start with 3 lives and respawn after collisions
- **Scoring System**: Earn points for destroying asteroids (100/50/20 for small/medium/large)
- **Screen Wrapping**: All objects wrap around screen edges seamlessly

### Phase 1 Features ✅
- ✅ Scoring system with different points for asteroid sizes
- ✅ Multiple lives (3 lives) and respawning system  
- ✅ Acceleration-based player movement with friction
- ✅ Screen wrapping for all objects
- ✅ Game over screen with restart functionality

### Phase 2 Features ✅
- ✅ Explosion particle effects for destroyed asteroids
- ✅ Lumpy asteroid shapes instead of perfect circles
- ✅ Triangular hitbox for the player ship
- ✅ Enhanced collision detection system

### Phase 3 Features ✅ **NEW!**
- ✅ **Multiple Weapon Types**:
  - Normal: Standard single shot
  - Rapid Fire: Fast automatic shooting
  - Spread Shot: Fires 3 bullets in a spread pattern
  - Laser: Instant-hit beam weapon
  
- ✅ **Power-Up System**:
  - Shield: 10 seconds of invulnerability (blue glow effect)
  - Speed Boost: 8 seconds of doubled movement speed (yellow tint)
  - Rapid Fire: Automatic weapon upgrade
  - Spread Shot: Multi-bullet weapon upgrade
  - Bomb: Restocks explosive bombs
  
- ✅ **Bomb System**:
  - Drop bombs with X key (max 3 bombs)
  - 2-second fuse timer with visual countdown
  - Large area-of-effect damage
  - Spectacular explosion animations
  
- ✅ **Animated Starfield Background**:
  - 100 twinkling stars of various sizes
  - Parallax scrolling effect based on player movement
  - Dynamic star brightness and cross patterns
  
- ✅ **Enhanced UI**:
  - Real-time weapon type display
  - Active power-up timers with color coding
  - Bomb count indicator
  - Control help overlay

## 🎯 Controls

| Key | Action |
|-----|---------|
| **WASD** or **Arrow Keys** | Move spaceship |
| **Space** | Shoot current weapon |
| **X** | Drop bomb |
| **R** | Restart game (when game over) |

## 🚀 Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Pascal509/Python_Asteroids_Game.git
   cd Python_Asteroids_Game
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv asteroids_env
   source asteroids_env/bin/activate  # On Windows: asteroids_env\\Scripts\\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game**:
   ```bash
   python main.py
   ```

## 🎨 Visual Features

### Particle Effects
- **Asteroid Explosions**: Multi-colored particle bursts scaled by asteroid size
- **Bomb Explosions**: Expanding ring effects with color gradients
- **Shield Effects**: Pulsing blue energy field around player
- **Speed Boost**: Yellow energy trail and ship tinting

### Dynamic Visuals
- **Lumpy Asteroids**: Procedurally generated irregular shapes
- **Twinkling Stars**: Animated background with size-based movement
- **Weapon Effects**: Distinct visual styles for each weapon type
- **Power-up Icons**: Color-coded rotating star shapes

## 🛠️ Technical Architecture

### Object-Oriented Design
- **CircleShape Base Class**: Common functionality for all game objects
- **Sprite Groups**: Efficient collision detection and rendering
- **Component Systems**: Modular weapon, power-up, and effect managers
- **Delta Time Physics**: Frame-rate independent movement

### Advanced Systems
- **Weapon Manager**: Handles multiple weapon types and laser collision
- **Power-Up Manager**: Spawning, collection, and effect application
- **Bomb Manager**: Area-of-effect damage with visual feedback  
- **Background System**: Parallax scrolling starfield
- **Effect Manager**: Particle system for explosions and visual effects

### Collision Detection
- **Triangle-Circle Collision**: Precise player-asteroid collision using barycentric coordinates
- **Line-Circle Intersection**: Laser beam collision detection
- **Area-of-Effect**: Bomb explosion radius calculations

## 📁 Project Structure

```
Asteroids_game/
├── main.py              # Main game loop and integration
├── constants.py         # Game configuration and balance
├── circleshape.py       # Base class for game objects
├── player.py            # Player ship with advanced features
├── asteroid.py          # Lumpy asteroids with splitting
├── shot.py              # Bullet projectiles
├── gamestate.py         # Score, lives, and UI management
├── effects.py           # Particle explosion system
├── powerup.py           # Power-up spawning and effects
├── weapon.py            # Multi-weapon system with lasers
├── bomb.py              # Explosive bomb system
├── background.py        # Animated starfield
└── requirements.txt     # Python dependencies
```

## 🎯 Gameplay Strategy

### Survival Tips
- **Collect Power-ups**: Look for colorful spinning stars after destroying asteroids
- **Use Shield Wisely**: Blue shield power-ups provide temporary invulnerability
- **Master Weapons**: Each weapon type has unique advantages:
  - Rapid Fire: Great for swarms of small asteroids
  - Spread Shot: Excellent for clustered asteroids
  - Laser: Instant hits for precise targeting
- **Bomb Strategically**: Save bombs for emergency situations or dense asteroid fields
- **Movement Mastery**: Use acceleration physics for precise maneuvering

### Scoring Optimization
- **Small Asteroids**: 100 points (highest value per hit)
- **Medium Asteroids**: 50 points
- **Large Asteroids**: 20 points
- **Strategy**: Let large asteroids split for maximum points

## 🔧 Customization

The game is highly configurable through `constants.py`:

### Weapon Balancing
```python
RAPID_FIRE_COOLDOWN = 0.1      # Adjust rapid fire speed
SPREAD_SHOT_COUNT = 3          # Number of spread bullets
LASER_RANGE = 600              # Laser beam distance
```

### Power-up Tuning
```python
POWERUP_SPAWN_CHANCE = 0.3     # Power-up drop rate
SHIELD_DURATION = 10.0         # Shield protection time
SPEED_BOOST_MULTIPLIER = 2.0   # Speed increase factor
```

### Visual Settings
```python
BACKGROUND_STAR_COUNT = 100    # Number of background stars
PARTICLE_COUNT_LARGE = 12      # Explosion particle density
```

## 🏆 Future Enhancements

Potential additional features for Phase 4:
- **Boss Enemies**: Large enemies with unique attack patterns
- **Asteroid Types**: Different asteroid materials with unique properties
- **Multiplayer Mode**: Local co-op or competitive gameplay
- **Sound Effects**: Audio feedback for weapons and explosions
- **Save System**: High score persistence and player profiles
- **Level Progression**: Increasing difficulty and wave-based gameplay

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**CodeWithEzeh**
- Enhanced implementation with advanced features
- Object-oriented architecture and visual effects
- Comprehensive documentation and testing

---

*Built with Python 3.13 and Pygame 2.6.1*