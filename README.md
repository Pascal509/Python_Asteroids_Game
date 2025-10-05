# 🚀 Asteroids Game

A modern recreation of the classic Asteroids arcade game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 Description

Navigate your spaceship through a dangerous asteroid field! Use your thrusters to move around and your laser cannon to blast asteroids into smaller pieces. Be careful - the smaller asteroids move faster and are harder to avoid!

## ✨ Features

- 🎮 **Classic arcade-style gameplay** - Authentic Asteroids experience
- 🚀 **Smooth spaceship controls** - Frame-rate independent movement and rotation
- 💥 **Asteroid destruction mechanics** - Large asteroids split into smaller ones
- 🎯 **Collision detection** - Precise circle-to-circle collision system
- ⚡ **Shooting system** - Rapid-fire laser cannon with cooldown
- 🌌 **Endless gameplay** - Continuous asteroid spawning from screen edges
- 📊 **Sprite group management** - Efficient object handling with pygame groups

## 🎮 Controls

| Key | Action |
|-----|--------|
| `A` | Rotate left |
| `D` | Rotate right |
| `W` | Move forward |
| `S` | Move backward |
| `SPACE` | Shoot |
| `ESC` or Close Window | Quit game |

## 🛠️ Requirements

- **Python 3.7+**
- **Pygame 2.0+**

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/Python_Asteroids_Game.git
   cd Python_Asteroids_Game
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the game:**
   ```bash
   python3 main.py
   ```

## 📁 Project Structure

```
Asteroids_game/
├── main.py          # Main game loop and initialization
├── constants.py     # Game configuration and constants
├── circleshape.py   # Base class for circular game objects
├── player.py        # Player spaceship class
├── asteroid.py      # Asteroid and spawning system classes
├── shot.py          # Bullet/projectile class
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## 🎯 Game Mechanics

### Asteroid Splitting System
- **Large asteroids** (radius 60) → Split into 2 medium asteroids (radius 40)
- **Medium asteroids** (radius 40) → Split into 2 small asteroids (radius 20)  
- **Small asteroids** (radius 20) → Destroyed completely

### Physics
- **Frame-rate independent movement** using delta time
- **Momentum-based spaceship controls**
- **Vector-based velocity calculations**
- **Smooth rotation and movement**

### Collision Detection
- **Circle-to-circle collision** for precise hit detection
- **Player vs Asteroids** → Game Over
- **Bullets vs Asteroids** → Asteroid splits/destruction

## 🔧 Configuration

Game settings can be modified in `constants.py`:

```python
# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Player settings  
PLAYER_SPEED = 200
PLAYER_TURN_SPEED = 300
PLAYER_SHOOT_SPEED = 500
PLAYER_SHOOT_COOLDOWN = 0.3

# Asteroid settings
ASTEROID_MIN_RADIUS = 20
ASTEROID_SPAWN_RATE = 0.8
```

## 🏗️ Architecture

The game follows object-oriented design principles:

- **`CircleShape`** - Base class providing collision detection and sprite management
- **`Player`** - Handles user input, movement, rotation, and shooting
- **`Asteroid`** - Individual asteroid behavior and splitting mechanics  
- **`Shot`** - Bullet physics and movement
- **`AsteroidField`** - Procedural asteroid spawning system

## 🐛 Known Issues

- Bullets may occasionally pass through very small asteroids at high speeds
- No boundary wrapping (objects disappear when leaving screen edges)
- No scoring system implemented yet

## 🚧 Future Enhancements

- [ ] Score tracking and high scores
- [ ] Sound effects and background music
- [ ] Screen wrapping for player and asteroids
- [ ] Power-ups (rapid fire, shield, etc.)
- [ ] Multiple lives system
- [ ] UFO enemies
- [ ] Particle effects for explosions
- [ ] Menu system with pause functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original Asteroids game by Atari (1979)
- Boot.dev for the educational framework
- Pygame community for excellent documentation
- Classic arcade game enthusiasts

## 👨‍💻 Author

**CodeWithEzeh**
- GitHub: [@YourGitHubUsername](https://github.com/YourGitHubUsername)
- Email: your.email@example.com

---

Made with ❤️ and Python 🐍

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd asteroids-game
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pygame
   ```

## How to Play

1. Run the game:
   ```bash
   python3 main.py
   ```

2. Controls:
   - Arrow keys or WASD: Move your spaceship
   - Spacebar: Shoot lasers
   - ESC: Quit game

## Game Rules

- Destroy all asteroids to advance to the next level
- Avoid colliding with asteroids - you only have one life!
- Large asteroids split into medium asteroids when shot
- Medium asteroids split into small asteroids when shot
- Small asteroids are destroyed completely when shot

## Project Structure

```
asteroids-game/
├── main.py          # Main game loop and initialization
├── constants.py     # Game constants and settings
├── requirements.txt # Python dependencies
└── README.md       # This file
```

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## License

This project is open source and available under the MIT License.