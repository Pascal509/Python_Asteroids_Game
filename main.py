# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *


def main(): 
    # Initialize pygame first
    pygame.init()

    # Create the screen after initialization
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Starting Asteroids! \nScreen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return

    while True:
        screen.fill((0, 0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()