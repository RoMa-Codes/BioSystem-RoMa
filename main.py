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
        if Identity < 2:
            self.nutrients = 100
            self.name = "Apple"
        elif Identity > 1 and Identity < 11:
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

        self.radius = 200      # movemnt range
        self.sight = 50

        self.name = "Deer"
        self.hp = 100

        # posición base.
        self.base_x = random.randint(0, screen_width)
        self.base_y = random.randint(0, screen_height)

        # posición actual
        self.x = self.base_x
        self.y = self.base_y

        self.timer = 0

        # new: variables to remember the destination and a timer for waiting
        self.dest_x = self.x
        self.dest_y = self.y

        self.waittimer = random.randint(20, 60) 

    def update(self):
        # NEW: Check if there is an apple inside the sight range before moving
        clowse_food = None
        smallest_distance = self.sight  # Only care if it is within self.sight

        for food in foods:
            dist_to_food = math.hypot(food.x - self.x, food.y - self.y)
            if dist_to_food <= smallest_distance:
                smallest_distance = dist_to_food
                clowse_food = food

        # NEW: If an apple is found, override destination directly to its location
        if clowse_food is not None:
            self.dest_x = clowse_food.x
            self.dest_y = clowse_food.y

        # checks the distance to the destinacion
        dx_dist = self.dest_x - self.x
        dy_dist = self.dest_y - self.y
        distance = math.hypot(dx_dist, dy_dist)

        # if it hasn't reached the destination, move towards it
        if distance > self.norm_speed:
            self.x += (dx_dist / distance) * self.norm_speed
            self.y += (dy_dist / distance) * self.norm_speed
             
        else:
            # NEW: If it reached an apple, don't trigger the idle wander timer, just wait to eat it
            if clowse_food is None:
                # if its has arrived to the destinacion, it will choose a new one but olso set a timer to rest
                self.timer += 1
                
                if self.timer >= self.waittimer:  # Mantiene tu límite original de 30 frames
                    self.timer = 0
                    self.waittimer = random.randint(20, 200) 
                    
                    # we pick a random destination within the sight range
                    random_dx = random.randint(-self.sight, self.radius)
                    random_dy = random.randint(-self.sight, self.radius)
                    
                    # to stop the animal from standing still, we only set a new destination if the random values are not both zero
                    if random_dx != 0 or random_dy != 0:
                        #the new destination respects the screen boundaries, so the animal doesnt go off the screen
                        self.dest_x = max(0, min(screen_width - creatures_size, self.x + random_dx))
                        self.dest_y = max(0, min(screen_height - creatures_size, self.y + random_dy))
            else:
                # Reset timer while on top of food so it doesn't get stuck in idle state later
                self.timer = 0
        

animals_list = []
for i in range(20):
    foods.append(Food())
for i in range(5):
    animals_list.append(herb_eating_Creatures())


# Obtiene la carpeta donde reside main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
slug_immage_path = os.path.join(BASE_DIR, "slug.png")
apple_immage_path = os.path.join(BASE_DIR, "apple.png")
bush_immage_path = os.path.join(BASE_DIR, "bush.png")

apple_sprite = pygame.image.load(apple_immage_path)
bush_sprite = pygame.image.load(bush_immage_path)

animal_sprite = pygame.image.load(slug_immage_path)
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
    for food in foods:
        if food.name == "Bush":
            screen.blit(bush_sprite, (food.x, food.y))
    
        
    for a in animals_list:
        a.update()

    
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
