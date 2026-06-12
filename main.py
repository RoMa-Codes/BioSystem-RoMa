import pygame
import sys
#makes this work
pygame.init()

flags = pygame.OPENGL | pygame.FULLSCREEN
window_surface = pygame.display.set_mode((1920, 1080), flags, vsync=1)
# Open a window on the screen

screen_width=1400
screen_height=800
screen=pygame.display.set_mode([screen_width, screen_height])
running = True
circle_x = 350 
circle_y = 200
animal_sprite = pygame.image.load("slug.png")
sprite_animal = pygame.transform.scale(animal_sprite, (100, 100))
speed = .5
while running:
    # Look for events (mouse clicks, key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # (Optional) Fill the screen with a color so it isn't black
    screen.fill((128, 128, 128)) 
    
    screen.blit(sprite_animal, (circle_x, circle_y))
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and circle_x > 0:
        circle_x -= speed
    if teclas[pygame.K_RIGHT] and circle_x < screen_width - 100:
        circle_x += speed
    if teclas[pygame.K_UP] and circle_y > 0:
        circle_y -= speed
    if teclas[pygame.K_DOWN] and circle_y < screen_height - 100:       
        circle_y += speed
    # Update the actual display
    pygame.display.flip()

# 4. Clean exit
pygame.quit()
sys.exit()
