import pygame
import sys
flags = pygame.OPENGL | pygame.FULLSCREEN
window_surface = pygame.display.set_mode((1920, 1080), flags, vsync=1)
# Open a window on the screen
screen_width=700
screen_height=400
screen=pygame.display.set_mode([screen_width, screen_height])
running = True
while running:
    # Look for events (mouse clicks, key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # (Optional) Fill the screen with a color so it isn't black
    screen.fill((0, 128, 0)) 
    pygame.draw.circle(screen, (255, 0, 0), (350, 200), 50)
    # Update the actual display
    pygame.display.flip()

# 4. Clean exit
pygame.quit()
sys.exit()