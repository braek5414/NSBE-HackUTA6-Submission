import pygame, sys
import random
import time
from button import Button

# Initialize Pygame
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Black.jpeg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Create the screen (for both game and menu)
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Platformer")

# Updated Game loop function
def game_loop():
    running = True
    clock = pygame.time.Clock()
    score = 0
    high_score = 0
    lives = 3
    game_over = False
    platform_count = 10  # Increased initial platform count to 10
    camera_movement = 0  # For upward camera movement
    lava_y = SCREEN_HEIGHT  # Set lava to be stationary at the bottom

    player = Player()
    player_group = pygame.sprite.Group()
    player_group.add(player)

    # Create platforms with an additional starting platform
    platforms = create_platforms(platform_count)

    # Add a starting platform directly below the player's initial position
    starting_platform = Platform(SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, player.rect.bottom + 20)
    platforms.add(starting_platform)

    while running:
        clock.tick(FPS)
        SCREEN.fill(BLACK)  # Use SCREEN instead of screen

        if lives <= 0:
            game_over = True
        if not game_over:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # Update player and platforms
            player_group.update()
            platforms.update(camera_movement)

            # Draw lava at the bottom without moving it
            pygame.draw.rect(SCREEN, RED, (0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20))  # Lava remains at the bottom

            # Check if the player falls into the lava
            if player.rect.bottom >= SCREEN_HEIGHT - 20:
                lives -= 1
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 1000)

            # Check for collision between player and platforms
            if pygame.sprite.spritecollide(player, platforms, False):
                player.velocity_y = PLAYER_JUMP
                score += 1

                # Increase platform count initially, then gradually reduce it as time goes on
                if score % 5 == 0 and platform_count < 12:
                    platform = Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH), random.randint(-100, 0))
                    platforms.add(platform)
                    platform_count += 1

                # After a certain score, start reducing platforms
                if score % 10 == 0 and platform_count > 5:
                    platform_to_remove = platforms.sprites()[0]
                    platforms.remove(platform_to_remove)
                    platform_count -= 1

            # Camera movement (slowly moving upwards)
            camera_movement += 0.01
            player.rect.y += camera_movement

            # Draw everything
            player_group.draw(SCREEN)
            platforms.draw(SCREEN)

            # Display score, high score, lives
            score_text = font.render(f"Score: {score}", True, YELLOW)
            SCREEN.blit(score_text, (10, 10))  # Use SCREEN
            
            high_score = max(high_score, score)
            high_score_text = font.render(f"High Score: {high_score}", True, CORAL)
            SCREEN.blit(high_score_text, (10, 40))  # Use SCREEN

            lives_text = font.render(f"Lives: {lives}", True, GREEN)
            SCREEN.blit(lives_text, (10, 70))  # Use SCREEN


        else:
            # Game Over screen with Retry and Exit options
            game_over_text = font.render("Game Over", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, ORANGE)
            high_score_text = font.render(f"High Score: {high_score}", True, CORAL)
            retry_text = font.render("Press SPACE to Retry", True, YELLOW)
            exit_text = font.render("Press ESC to Exit", True, WHITE)  # Exit option

            SCREEN.blit(game_over_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 50))
            SCREEN.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            SCREEN.blit(high_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40))
            SCREEN.blit(retry_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 80))
            SCREEN.blit(exit_text, (SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 120))  # Display Exit option

            # Event handling for retrying or exiting after game over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        score = 0
                        lives = 3
                        player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                        player.velocity_y = 0
                        platform_count = 10  # Reset platform count
                        platforms.empty()
                        platforms = create_platforms(platform_count)

                        # Add starting platform again
                        starting_platform = Platform(SCREEN_WIDTH // 2 - PLATFORM_WIDTH // 2, player.rect.bottom + 20)
                        platforms.add(starting_platform)

                        lava_y = SCREEN_HEIGHT  # Keep lava at the bottom
                        camera_movement = 0  # Reset camera movement
                        game_over = False
                    if event.key == pygame.K_ESCAPE:  # Exit game if ESC is pressed
                        running = False


        # Update the display
        pygame.display.flip()

    pygame.quit()


def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

# Game constants
FPS = 60
GRAVITY = 0.4
PLAYER_JUMP = -11
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 3
INITIAL_PLATFORM_COUNT = 8  # Starting number of platforms
LAVA_SPEED = 1  # Speed at which the lava rises

# Load ninja image
ninja_image = pygame.image.load("assets/ninja.gif")  # Use the uploaded ninja image

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 69, 0)
CORAL = (255, 127, 80)
YELLOW = (255, 240, 0)
GREEN = (50, 205, 50)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Lava Ninja")

# Font for displaying score and game over
font = pygame.font.Font(None, 36)

# Class for the player character
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ninja_image, (40, 50))  # Resize ninja image to fit player size
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        self.velocity_y = 0

    def update(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        jump_counter = 0 

        # Horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

         # Jumping and ing 
        if keys[pygame.K_SPACE]:
            self.velocity_y = PLAYER_JUMP 
            jump_counter += 1
        if jump_counter >= 3:
            jump_counter = 0
            time.sleep(2)


            
           


        # Wrap around the screen horizontally
        if self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

    def jump(self):
        self.velocity_y = PLAYER_JUMP 

# Class for the platforms
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, camera_movement):
        self.rect.y += PLATFORM_SPEED + camera_movement
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.y = random.randint(-100, -40)
            self.rect.x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)

# Create player and platform groups
def create_platforms(num_platforms):
    platforms = pygame.sprite.Group()
    for i in range(num_platforms):
        platform = Platform(random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH), random.randint(50, SCREEN_HEIGHT - 50))
        platforms.add(platform)
    return platforms




def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("LAVA NINJA", True, "#F7342B")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play_Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options_Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit_Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
