"""
Ship Upgrade System

This module handles ship upgrades and customization using
resources collected from mining asteroids.

Author: CodeWithEzeh
Date: October 2025
"""

import pygame
from constants import *


class ShipUpgrade:
    """
    Individual ship upgrade with specific effects.
    """
    
    def __init__(self, upgrade_type, level=0):
        """
        Initialize a ship upgrade.
        
        Args:
            upgrade_type (str): Type of upgrade
            level (int): Current upgrade level
        """
        self.upgrade_type = upgrade_type
        self.level = level
        self.max_level = 5
        
    def get_effect_multiplier(self):
        """
        Get the effect multiplier for this upgrade level.
        
        Returns:
            float: Effect multiplier
        """
        return 1.0 + (self.level * 0.2)  # 20% increase per level
    
    def can_upgrade(self):
        """
        Check if this upgrade can be leveled up.
        
        Returns:
            bool: True if can upgrade
        """
        return self.level < self.max_level
    
    def upgrade(self):
        """Increase the upgrade level."""
        if self.can_upgrade():
            self.level += 1
            return True
        return False


class UpgradeManager:
    """
    Manages all ship upgrades and their effects.
    """
    
    def __init__(self):
        """Initialize the upgrade manager."""
        self.upgrades = {
            UPGRADE_HULL: ShipUpgrade(UPGRADE_HULL),
            UPGRADE_ENGINES: ShipUpgrade(UPGRADE_ENGINES),
            UPGRADE_WEAPONS: ShipUpgrade(UPGRADE_WEAPONS),
            UPGRADE_SHIELDS: ShipUpgrade(UPGRADE_SHIELDS)
        }
        self.show_upgrade_menu = False
        self.selected_upgrade = 0
        
    def apply_upgrades_to_player(self, player):
        """
        Apply all upgrades to a player object.
        
        Args:
            player: Player object to upgrade
        """
        # Hull upgrades affect collision radius (smaller = harder to hit)
        hull_effect = self.upgrades[UPGRADE_HULL].get_effect_multiplier()
        player.radius = max(PLAYER_RADIUS * 0.7, PLAYER_RADIUS / hull_effect)
        
        # Engine upgrades affect acceleration and max speed
        engine_effect = self.upgrades[UPGRADE_ENGINES].get_effect_multiplier()
        player.max_acceleration = PLAYER_ACCELERATION * engine_effect
        player.max_speed = PLAYER_SPEED * engine_effect
        
        # Weapon upgrades are handled by weapon manager
        # Shield upgrades affect shield duration
        shield_effect = self.upgrades[UPGRADE_SHIELDS].get_effect_multiplier()
        if hasattr(player, 'shield_duration_multiplier'):
            player.shield_duration_multiplier = shield_effect
    
    def get_weapon_damage_multiplier(self):
        """Get damage multiplier from weapon upgrades."""
        return self.upgrades[UPGRADE_WEAPONS].get_effect_multiplier()
    
    def get_shield_duration_multiplier(self):
        """Get shield duration multiplier."""
        return self.upgrades[UPGRADE_SHIELDS].get_effect_multiplier()
    
    def toggle_upgrade_menu(self):
        """Toggle the upgrade menu visibility."""
        self.show_upgrade_menu = not self.show_upgrade_menu
    
    def handle_upgrade_input(self, keys, resource_manager):
        """
        Handle input for the upgrade menu.
        
        Args:
            keys: Pygame key state
            resource_manager: Resource manager for checking costs
            
        Returns:
            bool: True if an upgrade was purchased
        """
        if not self.show_upgrade_menu:
            return False
            
        upgrade_types = list(self.upgrades.keys())
        
        # Navigate menu
        if keys[pygame.K_UP]:
            self.selected_upgrade = (self.selected_upgrade - 1) % len(upgrade_types)
        elif keys[pygame.K_DOWN]:
            self.selected_upgrade = (self.selected_upgrade + 1) % len(upgrade_types)
        elif keys[pygame.K_RETURN]:
            # Purchase selected upgrade
            selected_type = upgrade_types[self.selected_upgrade]
            return self.purchase_upgrade(selected_type, resource_manager)
        elif keys[pygame.K_ESCAPE]:
            self.show_upgrade_menu = False
            
        return False
    
    def purchase_upgrade(self, upgrade_type, resource_manager):
        """
        Purchase an upgrade if affordable.
        
        Args:
            upgrade_type (str): Type of upgrade to purchase
            resource_manager: Resource manager
            
        Returns:
            bool: True if purchase successful
        """
        if upgrade_type not in self.upgrades:
            return False
            
        upgrade = self.upgrades[upgrade_type]
        if not upgrade.can_upgrade():
            return False
            
        # Check if player can afford it
        if resource_manager.can_afford_upgrade(upgrade_type):
            if resource_manager.purchase_upgrade(upgrade_type):
                upgrade.upgrade()
                return True
                
        return False
    
    def draw_upgrade_menu(self, screen, font, resource_manager):
        """
        Draw the upgrade menu.
        
        Args:
            screen: Pygame screen surface
            font: Font for rendering text
            resource_manager: Resource manager for showing costs
        """
        if not self.show_upgrade_menu:
            return
            
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Menu background
        menu_width = 400
        menu_height = 300
        menu_x = SCREEN_WIDTH // 2 - menu_width // 2
        menu_y = SCREEN_HEIGHT // 2 - menu_height // 2
        
        pygame.draw.rect(screen, (50, 50, 50), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (100, 100, 100), (menu_x, menu_y, menu_width, menu_height), 3)
        
        # Title
        title = font.render("SHIP UPGRADES", True, "white")
        title_x = menu_x + menu_width // 2 - title.get_width() // 2
        screen.blit(title, (title_x, menu_y + 20))
        
        # Upgrade options
        upgrade_info = {
            UPGRADE_HULL: ("Hull Plating", "Reduces ship size", "Metal: 5"),
            UPGRADE_ENGINES: ("Engine Boost", "Increases speed", "Ice: 3, Metal: 2"),
            UPGRADE_WEAPONS: ("Weapon Systems", "Increases damage", "Crystal: 2, Metal: 3"),
            UPGRADE_SHIELDS: ("Shield Generator", "Longer shield duration", "Crystal: 3, Ice: 2")
        }
        
        upgrade_types = list(self.upgrades.keys())
        
        for i, upgrade_type in enumerate(upgrade_types):
            upgrade = self.upgrades[upgrade_type]
            name, description, cost = upgrade_info[upgrade_type]
            
            y_pos = menu_y + 70 + i * 50
            
            # Highlight selected upgrade
            if i == self.selected_upgrade:
                pygame.draw.rect(screen, (100, 100, 150), 
                               (menu_x + 10, y_pos - 5, menu_width - 20, 40))
            
            # Upgrade name and level
            name_text = f"{name} (Level {upgrade.level}/{upgrade.max_level})"
            color = "white" if upgrade.can_upgrade() else "gray"
            
            name_surface = font.render(name_text, True, color)
            screen.blit(name_surface, (menu_x + 20, y_pos))
            
            # Description and cost
            desc_surface = font.render(description, True, "gray")
            screen.blit(desc_surface, (menu_x + 20, y_pos + 20))
            
            cost_surface = font.render(f"Cost: {cost}", True, "yellow")
            screen.blit(cost_surface, (menu_x + 250, y_pos + 20))
            
            # Affordability indicator
            if resource_manager.can_afford_upgrade(upgrade_type) and upgrade.can_upgrade():
                afford_text = "✓"
                afford_color = "green"
            else:
                afford_text = "✗"
                afford_color = "red"
                
            afford_surface = font.render(afford_text, True, afford_color)
            screen.blit(afford_surface, (menu_x + 360, y_pos + 10))
        
        # Instructions
        instruction_text = "↑↓: Navigate, Enter: Purchase, Esc: Close"
        instruction_surface = font.render(instruction_text, True, "white")
        instruction_x = menu_x + menu_width // 2 - instruction_surface.get_width() // 2
        screen.blit(instruction_surface, (instruction_x, menu_y + menu_height - 30))
    
    def get_upgrade_summary(self):
        """
        Get a summary of all upgrades for display.
        
        Returns:
            dict: Upgrade summary
        """
        summary = {}
        for upgrade_type, upgrade in self.upgrades.items():
            summary[upgrade_type] = {
                'level': upgrade.level,
                'max_level': upgrade.max_level,
                'effect': upgrade.get_effect_multiplier()
            }
        return summary
    
    def save_upgrades(self):
        """
        Save upgrade state to file.
        
        Returns:
            dict: Serializable upgrade data
        """
        return {upgrade_type: upgrade.level for upgrade_type, upgrade in self.upgrades.items()}
    
    def load_upgrades(self, upgrade_data):
        """
        Load upgrade state from data.
        
        Args:
            upgrade_data (dict): Upgrade data to load
        """
        for upgrade_type, level in upgrade_data.items():
            if upgrade_type in self.upgrades:
                self.upgrades[upgrade_type].level = min(level, self.upgrades[upgrade_type].max_level)