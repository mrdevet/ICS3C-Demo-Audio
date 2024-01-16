# Programmer: Mr. Devet
# Date: 2022-01-10
# Description: A Whack-A-Mole game that makes use of mouse
#    events

# Import and initialize the pygame library
import pygame
from pygame.locals import *
pygame.init()

# Import sprite class
from sprite import *

# Other imports
from random import *
from sys import exit

# Create and open a pygame screen with the given size
screen = pygame.display.set_mode((640, 360))

# Set the title of the pygame screen
pygame.display.set_caption("Whack-A-Mole")

# Create a clock to keep track of time
clock = pygame.time.Clock()


### LOAD RESOURCES

# Load the images
mole_image = pygame.image.load("mole.png")
mole_image = pygame.transform.rotozoom(mole_image, 0, 0.2)

mallet_image = pygame.image.load("mallet.png")
mallet_image = pygame.transform.rotozoom(mallet_image, 0, 0.4)

pow_image = pygame.image.load("pow.png")
pow_image = pygame.transform.rotozoom(pow_image, 0, 0.6)

# Load the font
permanent_marker_72 = pygame.font.Font("PermanentMarker.ttf", 72)


# Group to hold all of the active sprites
all_sprites = pygame.sprite.Group()


### GAME SETUP

# Create the sprites
mole = Sprite(mole_image)
mole.x = randint(0, 575)
mole.y = randint(0, 304)
mole.add(all_sprites)

mallet = Sprite(mallet_image)
mallet.add(all_sprites)

pow = Sprite(pow_image)

# Create and start timers
MOVE_MOLE_EVENT = pygame.event.custom_type()
pygame.time.set_timer(MOVE_MOLE_EVENT, 2000, 30)

GAME_OVER_EVENT = pygame.event.custom_type()
pygame.time.set_timer(GAME_OVER_EVENT, 60000, 1)

# Create a Game Over sprite
game_over_image = permanent_marker_72.render("GAME OVER", True, "brown")
game_over = Sprite(game_over_image)
game_over.center = (320, 180)


# Main Loop
while True:
    # Set the frame rate to 30 frames per second
    clock.tick(30)

    # If there is a quit event, end the game
    if pygame.event.get(QUIT):
        exit()

    ### MANAGE IN-GAME EVENTS AND ANIMATIONS HERE

    # Loop through all of the events
    for event in pygame.event.get():
        # Show the pow when we click on the mole
        if event.type == MOUSEBUTTONDOWN:
            if mole.mask_contains_point(event.pos):
                pow.center = event.pos
                pow.add(all_sprites)

            # Rotate the mallet
            mallet.turn_left(60)

        # "Unrotate" the mallet when mouse released
        elif event.type == MOUSEBUTTONUP:
            mallet.turn_right(60)
                
        # Move the mallet with mouse motion
        elif event.type == MOUSEMOTION:
            mallet.center = event.pos
            
        # If the move mole timer expires, move the mole to a 
        # random location
        elif event.type == MOVE_MOLE_EVENT:
            mole.x = randint(0, 575)
            mole.y = randint(0, 304)
            pow.kill()

        # If the game over timer expires, kill the mole
        elif event.type == GAME_OVER_EVENT:
            mole.kill()
            game_over.add(all_sprites)

    # Clear the old images of the sprites from the screen
    screen.fill("lightgreen")

    # Update and draw the sprites
    all_sprites.update()
    all_sprites.draw(screen)

    # Flip the changes to the screen to the computer display
    pygame.display.flip()
