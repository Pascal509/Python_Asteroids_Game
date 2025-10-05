"""
Audio System

This module handles all sound effects and background music for the game.
Provides a centralized audio manager with volume controls and sound caching.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
import os
from constants import *

# Try to import numpy for advanced audio synthesis
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("NumPy not available - using basic audio effects")


class AudioManager:
    """
    Manages all game audio including sound effects and background music.
    """
    
    def __init__(self):
        """Initialize the audio system."""
        self.enabled = ENABLE_SOUND
        self.sounds = {}
        self.music_playing = False
        
        if self.enabled:
            try:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                self.load_sounds()
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
            except pygame.error:
                print("Warning: Could not initialize audio system")
                self.enabled = False
    
    def load_sounds(self):
        """Load all sound effects. Creates placeholder sounds if files don't exist."""
        # Create simple synthesized sounds since we don't have audio files
        self.create_synthesized_sounds()
    
    def create_synthesized_sounds(self):
        """Create simple synthesized sound effects using pygame."""
        try:
            # Shooting sound - short beep
            shoot_sound = pygame.sndarray.make_sound(
                self._generate_tone(440, 0.1, 22050)  # 440Hz for 0.1 seconds
            )
            shoot_sound.set_volume(SFX_VOLUME * 0.3)
            self.sounds['shoot'] = shoot_sound
            
            # Explosion sound - noise burst
            explosion_sound = pygame.sndarray.make_sound(
                self._generate_noise(0.3, 22050)  # 0.3 seconds of noise
            )
            explosion_sound.set_volume(SFX_VOLUME * 0.5)
            self.sounds['explosion'] = explosion_sound
            
            # Power-up sound - ascending tone
            powerup_sound = pygame.sndarray.make_sound(
                self._generate_sweep(220, 880, 0.4, 22050)  # 220Hz to 880Hz sweep
            )
            powerup_sound.set_volume(SFX_VOLUME * 0.4)
            self.sounds['powerup'] = powerup_sound
            
            # Thrust sound - low rumble
            thrust_sound = pygame.sndarray.make_sound(
                self._generate_tone(60, 0.2, 22050)  # 60Hz rumble
            )
            thrust_sound.set_volume(SFX_VOLUME * 0.2)
            self.sounds['thrust'] = thrust_sound
            
            # UFO sound - warbling tone
            ufo_sound = pygame.sndarray.make_sound(
                self._generate_warble(200, 300, 0.5, 22050)  # Warbling effect
            )
            ufo_sound.set_volume(SFX_VOLUME * 0.3)
            self.sounds['ufo'] = ufo_sound
            
        except (pygame.error, ImportError):
            print("Warning: Could not create synthesized sounds")
            self.enabled = False
    
    def _generate_tone(self, frequency, duration, sample_rate):
        """Generate a simple sine wave tone."""
        if not NUMPY_AVAILABLE:
            # Return a simple beep sound array
            frames = int(duration * sample_rate)
            arr = []
            for i in range(frames):
                # Simple sine wave approximation
                import math
                wave = math.sin(2 * math.pi * frequency * i / sample_rate)
                fade = 1.0 if i < frames * 0.8 else (frames - i) / (frames * 0.2)
                sample = int(wave * fade * 16383)  # Reduced amplitude
                arr.extend([sample, sample])  # Stereo
            return arr
        
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            wave = np.sin(2 * np.pi * frequency * i / sample_rate)
            # Apply fade out to prevent clicking
            fade = 1.0 if i < frames * 0.8 else (frames - i) / (frames * 0.2)
            arr[i] = [wave * fade * 32767, wave * fade * 32767]
        
        return arr.astype(np.int16)
    
    def _generate_noise(self, duration, sample_rate):
        """Generate white noise for explosion effects."""
        if not NUMPY_AVAILABLE:
            # Simple noise approximation
            frames = int(duration * sample_rate)
            arr = []
            import random
            for i in range(frames):
                noise = random.uniform(-16383, 16383)
                fade = (frames - i) / frames
                sample = int(noise * fade)
                arr.extend([sample, sample])
            return arr
        
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.random.uniform(-32767, 32767, (frames, 2))
        
        # Apply envelope for more natural explosion sound
        for i in range(frames):
            fade = (frames - i) / frames  # Fade out
            arr[i] *= fade
        
        return arr.astype(np.int16)
    
    def _generate_sweep(self, start_freq, end_freq, duration, sample_rate):
        """Generate a frequency sweep."""
        if not NUMPY_AVAILABLE:
            # Simple sweep approximation
            frames = int(duration * sample_rate)
            arr = []
            import math
            for i in range(frames):
                progress = i / frames
                frequency = start_freq + (end_freq - start_freq) * progress
                wave = math.sin(2 * math.pi * frequency * i / sample_rate)
                envelope = math.sin(math.pi * progress)
                sample = int(wave * envelope * 16383)
                arr.extend([sample, sample])
            return arr
        
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Linear frequency interpolation
            progress = i / frames
            frequency = start_freq + (end_freq - start_freq) * progress
            wave = np.sin(2 * np.pi * frequency * i / sample_rate)
            # Apply envelope
            envelope = np.sin(np.pi * progress)  # Sine envelope
            arr[i] = [wave * envelope * 32767, wave * envelope * 32767]
        
        return arr.astype(np.int16)
    
    def _generate_warble(self, base_freq, mod_freq, duration, sample_rate):
        """Generate a warbling effect for UFO sounds."""
        if not NUMPY_AVAILABLE:
            # Simple warble approximation
            frames = int(duration * sample_rate)
            arr = []
            import math
            for i in range(frames):
                mod = math.sin(2 * math.pi * 5 * i / sample_rate)
                frequency = base_freq + mod * (mod_freq - base_freq) * 0.5
                wave = math.sin(2 * math.pi * frequency * i / sample_rate)
                sample = int(wave * 16383 * 0.5)
                arr.extend([sample, sample])
            return arr
        
        import numpy as np
        frames = int(duration * sample_rate)
        arr = np.zeros((frames, 2))
        
        for i in range(frames):
            # Frequency modulation
            mod = np.sin(2 * np.pi * 5 * i / sample_rate)  # 5Hz modulation
            frequency = base_freq + mod * (mod_freq - base_freq) * 0.5
            wave = np.sin(2 * np.pi * frequency * i / sample_rate)
            arr[i] = [wave * 32767 * 0.5, wave * 32767 * 0.5]
        
        return arr.astype(np.int16)
    
    def play_sound(self, sound_name):
        """
        Play a sound effect.
        
        Args:
            sound_name (str): Name of the sound to play
        """
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except pygame.error:
                pass  # Sound system may not be available
    
    def play_music(self, music_file=None):
        """
        Play background music.
        
        Args:
            music_file (str): Path to music file (optional)
        """
        if self.enabled and not self.music_playing:
            try:
                # Since we don't have music files, we'll create ambient space sound
                self._create_ambient_music()
                self.music_playing = True
            except pygame.error:
                pass
    
    def _create_ambient_music(self):
        """Create simple ambient background music."""
        # For now, we'll skip background music to keep it simple
        # In a full implementation, you would load and loop music files
        pass
    
    def stop_music(self):
        """Stop background music."""
        if self.enabled:
            try:
                pygame.mixer.music.stop()
                self.music_playing = False
            except pygame.error:
                pass
    
    def set_volume(self, volume):
        """
        Set the master volume.
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        if self.enabled:
            for sound in self.sounds.values():
                sound.set_volume(volume * SFX_VOLUME)
    
    def cleanup(self):
        """Clean up audio resources."""
        if self.enabled:
            self.stop_music()
            pygame.mixer.quit()