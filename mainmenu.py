import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Game - Main Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (50, 150, 255)

# Fonts
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = GRAY
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = button_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos) and self.action:
            self.action()

# Button actions
def start_game():
    print("Start Game")  # Replace with game logic

def settings():
    print("Settings Menu")  # Replace with settings logic

def quit_game():
    pygame.quit()
    sys.exit()

# Create buttons
buttons = [
    Button(300, 200, 200, 60, "Start Game", start_game),
    Button(300, 300, 200, 60, "Settings", settings),
    Button(300, 400, 200, 60, "Quit", quit_game),
]

def main_menu():
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in buttons:
                        button.check_click(event.pos)

        # Draw title
        title_surf = font.render("Spaceship Game", True, BLUE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title_surf, title_rect)

        # Draw buttons
        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
