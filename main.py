import pygame
import sys
#makes this work
pygame.init()

# Open a window on the screen
flags = pygame.OPENGL | pygame.FULLSCREEN
window_surface = pygame.display.set_mode((1920, 1080), flags, vsync=1)

#name the window
pygame.display.set_caption("BioSystem-RoMa") 

screen_width=1400
screen_height=800
screen=pygame.display.set_mode([screen_width, screen_height])
running = True
creatures_size = 100
circle_x =  screen_width // 2 - creatures_size // 2
circle_y = screen_height // 2 - creatures_size // 2
animal_sprite = pygame.image.load("slug.png")
sprite_animal = pygame.transform.scale(animal_sprite, (creatures_size, creatures_size))
speed = .5
while running:
    # Look for events (mouse clicks, key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # chaing the backround color to any RGB value
    screen.fill((0, 128, 0)) 
    
    screen.blit(sprite_animal, (circle_x, circle_y))
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and circle_x > 0:
        circle_x -= speed
    if teclas[pygame.K_RIGHT] and circle_x < screen_width - creatures_size:
        circle_x += speed
    if teclas[pygame.K_UP] and circle_y > 0:
        circle_y -= speed
    if teclas[pygame.K_DOWN] and circle_y < screen_height - creatures_size:       
        circle_y += speed
    # Update the actual display
    pygame.display.flip()

# 4. Clean exit
pygame.quit()
sys.exit()
