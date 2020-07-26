# The aim of this game is to avoid hitting the oncoming enemy spaceships
# and to try and hit the winning powerup star. If you miss the enemy spaceships
# and miss the star, you lose. If you hit the enemy spaceships, you lose.

# Import the necassary libraries.
import pygame
import random
import os

# Initialize pygame.
pygame.init()

# Create a main function.
def main():

    # Determine the size of the games window and create the window.
    screen_width = 1040
    screen_height = 680
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Set caption of game.
    pygame.display.set_caption("Hit the Star!!!")

    # Due to pygame running from where it is installed, we need to
    # determine the path where the resources are located. If the
    # resources were located in the same folder as where pygame was
    # installed, we wouldn't have to point to that folder. See below
    # where we use this variable to join the path to the resources.
    current_path = os.path.dirname(__file__)
    
    # Set the velocity at which the spaceships and the winning powerup
    # star should move.
    velocity = 5
    winning_velocity = 3

    # We create a hitbox boolean to determine if the hitbox has been drawn
    # or not. See below how we use this variable.
    draw_hitbox = False
    print("Press 1 to enable hitbox visibility")

    # Create an object for the player spaceship where we can pass all the
    # variable information needed.
    class player(object):
        
        # Load the image to a variable. Here we can see the use of the curren_path
        # variable to point to the correct directory where the image is.
        player_spaceship = pygame.image.load(os.path.join(current_path, "playerShip2_blue.png"))

        # Create a function that sets the initial variables applicable.
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.height = self.player_spaceship.get_height()    #Set the height and width of the object to that of the image.
            self.width = self.player_spaceship.get_width()
            self.hitbox = pygame.Rect(self.player_spaceship.get_rect())     #Create the rectangle for the hitbox.
            self.hitbox.h += 20     # Because the image of the spaceship is rotated (see below) the dimensions
                                    # of the hitbox is incorrect. We manually adjust the hitbox size to be as
                                    # close to the actual size as possible.
            self.hitbox.w -= 60

        # Create a function that redraws the player at its new coordinates.
        def draw (self, screen): 
            self.hitbox.top = self.y + 10    #Set the coordinates of the hitbox.
            self.hitbox.left = self.x

            # Draw the image to the screen. 
            # Here we rotate the spaceship to the correct direction.
            screen.blit(pygame.transform.rotate(self.player_spaceship, 270), (self.x, self.y))

    # Create an enemy object. Similar to "player" object. See above.
    class enemy(object):
        enemy_spaceship = pygame.image.load(os.path.join(current_path, "enemyRed3.png"))

        def __init__(self, x):
            self.x = x

            #Set the y-coordinate of the enemy to a random number.
            self.y = random.randint(0, screen_height - self.enemy_spaceship.get_height())
            self.height = self.enemy_spaceship.get_height()
            self.width = self.enemy_spaceship.get_width()
            self.hitbox = pygame.Rect(self.enemy_spaceship.get_rect())
            self.hitbox.w -= 40

        def draw (self, screen):
            self.x -= velocity  # This is the movement of the enemy on the x-axis at the velocity
            self.hitbox.top = self.y + 10
            self.hitbox.left = self.x + 20
            screen.blit(pygame.transform.rotate(self.enemy_spaceship, 270), (self.x, self.y))

    # Create the winning powerup star object.
    class powerup(object):
        powerup = pygame.image.load(os.path.join(current_path, "star_gold.png"))

        def __init__(self, x):
            self.x = x
            self.y = random.randint(0, screen_height - self.powerup.get_height())
            self.height = self.powerup.get_height()
            self.width = self.powerup.get_width()
            self.hitbox = pygame.Rect(self.powerup.get_rect())

        def draw (self, screen): 
            self.x -= winning_velocity
            self.hitbox.top = self.y
            self.hitbox.left = self.x
            screen.blit(self.powerup, (self.x, self.y))


    # Create a redraw function. Here the draw functions of each
    # spaceship is called and the hitboxes are drawn to screen.
    def redraw_game_window():
        fighter1.draw(screen)
        fighter2.draw(screen)
        fighter3.draw(screen)
        player1.draw(screen)
        winner.draw(screen)
        if draw_hitbox:     #Only draw the hitbox if the boolean is true
            pygame.draw.rect(screen, (255, 0, 0), player1.hitbox, 2)
            pygame.draw.rect(screen, (255, 0, 0), fighter1.hitbox, 2)
            pygame.draw.rect(screen, (255, 0, 0), fighter2.hitbox, 2)
            pygame.draw.rect(screen, (255, 0, 0), fighter3.hitbox, 2)
            pygame.draw.rect(screen, (255, 0, 0), winner.hitbox, 2)
        
        # Update the screen.
        pygame.display.update()

    # Create the player, enemies and the powerup
    fighter1 = enemy(screen_width)
    fighter2 = enemy(screen_width)
    fighter3 = enemy(screen_width)
    player1 = player(50, 300)
    winner = powerup(screen_width)

    # Create and run the main game loop.
    run = True
    while run:
        redraw_game_window()    # Call the redraw function.

        # If the game window has been closed, stop the game loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Register the key that is being pressed in the keys variable.
        keys = pygame.key.get_pressed()

        # Based on the key being pressed, update the coordinates of the player.
        if keys[pygame.K_UP]:
            if player1.y > 0:
                player1.y -= velocity

        if keys[pygame.K_DOWN]:
            if player1.y < screen_height - player1.hitbox.h:
                player1.y += velocity

        if keys[pygame.K_LEFT]:
            if player1.x > 0:
                player1.x -= velocity

        if keys[pygame.K_RIGHT]:
            if player1.x < screen_width - player1.hitbox.w:
                player1.x += velocity

        # Toggle hitboxes on/off. This is to ensure that if the player presses 1
        # the hitbox is only toggled once.
        if keys[pygame.K_1]:
            if not pressed:
                draw_hitbox = not draw_hitbox
                pressed = True
        
        if not keys[pygame.K_1]:
            pressed = False

        # Test collision of the boxes. If the player hits one of the enemies, the player loses.
        if player1.hitbox.colliderect(fighter1.hitbox) or player1.hitbox.colliderect(fighter2.hitbox) or player1.hitbox.colliderect(fighter3.hitbox):
            print("You lose!")
            pygame.quit()
            exit(0)

        # If the powerup star is off the screen the player loses the game.
        elif winner.hitbox.x < 0 - winner.width:
            print("You Lose")
            pygame.quit()
            exit(0)

        # If the player hits the powerup star, the player wins.
        elif player1.hitbox.colliderect(winner.hitbox):
            print("You win!!!")
            pygame.quit()
            exit(0)

        # Clear the background of the screen.
        else:
            screen.fill(0)

# Initialize the main function (run the program).
if __name__ == "__main__":
    main()
