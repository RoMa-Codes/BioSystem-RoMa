import pygame
import sys
import random
import os
import math
#makes this work
pygame.init()

# Open a window on the screen
flags = pygame.OPENGL | pygame.FULLSCREEN
window_surface = pygame.display.set_mode((1920, 1080), flags, vsync=1)

#name the window
pygame.display.set_caption("BioSystem-RoMa") 
#vars
clock = pygame.time.Clock()
screen_width=1400
screen_height=800
screen=pygame.display.set_mode([screen_width, screen_height])
running = True
creatures_size = 50
circle_x =  screen_width // 2 - creatures_size // 2
circle_y = screen_height // 2 - creatures_size // 2
food_timer = 0


# Creant aliment
class Food:
    def __init__(self):
        Identity = random.randint(1, 10)
        if Identity < 11:
            self.nutrients = 100
            self.name = "Apple"
        elif Identity > 1 and food < 6:
            self.nutrients = 30
            self.name = "Bush"
        elif Identity > 5:
            self.nutrients = 5
            self.name = "Plant"
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
foods = []


class herb_eating_Creatures:
    def __init__(self):
        # Stats del Deer
        self.needed_nutrients = 50
        self.repro_nutrients = 80
        self.want_nutrients = 100

        self.norm_speed = 3
        self.panic_speed = 4

        self.radius = 100      # rango de movimiento
        self.sight = 50

        self.name = "Deer"
        self.hp = 100

        # posición base
        self.base_x = random.randint(0, screen_width)
        self.base_y = random.randint(0, screen_height)

        # posición actual
        self.x = self.base_x
        self.y = self.base_y

        self.timer = 0

def update(self):
    self.timer += 1

    if self.timer >= 30:
         self.timer = 0

    while True:
        dx = random.randint(-self.radius, self.radius)
        dy = random.randint(-self.radius, self.radius)

        if dx*dx + dy*dy <= self.radius*self.radius:
            self.x = self.base_x + dx
            self.y = self.base_y + dy
            break
    
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
animals_list = []
for i in range(0):
    foods.append(Food())
for i in range(5):
    animals_list.append(herb_eating_Creatures())

# Obtiene la carpeta donde reside main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
slug_immage_path = os.path.join(BASE_DIR, "slug.png")
apple_immage_path = os.path.join(BASE_DIR, "apple.png")
apple_sprite = pygame.image.load(apple_immage_path)

animal_sprite = pygame.image.load(slug_immage_path)
apple_sprite = pygame.image.load(apple_immage_path)
sprite_animal = pygame.transform.scale(animal_sprite, (creatures_size, creatures_size))
apple_sprite = pygame.transform.scale(apple_sprite, (50, 50))

# chaing the backround color to any RGB value
screen.fill((0, 128, 0))
speed = 5
while running:
    # Look for events (mouse clicks, key presses)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 
    clock.tick(60)
    food_timer += 1
    if food_timer >= 180:
        food_timer = 0
        foods.append(Food())
    
    screen.fill((0, 128, 0))
    
    for food in foods:
        if food.name == "Apple":
            screen.blit(apple_sprite, (food.x, food.y))
    for a in animals_list:
        screen.blit(sprite_animal, (a.x, a.y))
    
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
