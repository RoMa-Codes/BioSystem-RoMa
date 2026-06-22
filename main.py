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
        #neurtrient vars
        self.needed_nutrients = 50
        self.repro_nutrients = 80
        self.want_nutrients = 100
        self.current_neutrients = 80
        #speed vars
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
        #here we create a timer so in the future we can remove its curent neutriates
        self.current_neutrients -= 0.05
        # we create a new variable to store the closest food found in this update cycle, if any
        clowse_food = None

        # it only looks for food if it needs it, otherwise it just walks around randomly. This way it doesn't break the system by trying to eat when it's not hungry, and also it doesn't waste time looking for food when it's not needed.
        if self.current_neutrients < self.want_nutrients:
            
            # Solo si tiene hambre extrema, ejecuta el código de buscar comida:
            smallest_distance = self.sight  

            for food in foods:
                dist_to_food = math.hypot(food.x - self.x, food.y - self.y)
                if dist_to_food <= smallest_distance:
                    smallest_distance = dist_to_food
                    clowse_food = food

            # if it find food, it sets the destination to the food's position, otherwise it will just keep walking randomly until it finds some or gets hungry enough to look for it again.
            if clowse_food is not None:
                self.dest_x = clowse_food.x
                self.dest_y = clowse_food.y

        # movement code, it will move towards the destination set by the food searching code if it found some, otherwise it will just keep moving towards a random destination that changes every few seconds. When it reaches the destination, if it's a food, it will eat it and gain nutrients, if it's just a random point, it will wait there for a bit and then choose a new random destination to walk to.
        dx_dist = self.dest_x - self.x
        dy_dist = self.dest_y - self.y
        distance = math.hypot(dx_dist, dy_dist)

        if distance > self.norm_speed:
            self.x += (dx_dist / distance) * self.norm_speed
            self.y += (dy_dist / distance) * self.norm_speed
             
        else:
            # Si llegó a su destino y era un alimento, lo come y gana nutrientes:
            if clowse_food is not None:
                self.current_neutrients += clowse_food.nutrients 
                
                # if the nutrients gained by eating the food exceed the creature's want_nutrients, it will just set its current_neutrients to want_nutrients, because it doesn't need more than that and it would break the system if it could keep gaining nutrients infinitely.


                print(f"ate: {clowse_food.name} | +{clowse_food.nutrients} nutrientes")
                print(f"entity current nutrients: {self.current_neutrients}")
                
                if clowse_food in foods:
                    foods.remove(clowse_food)
                
                self.x = self.dest_x
                self.y = self.dest_y
                clowse_food = None 
                self.timer = 0
                
            else:
                # if it reached its destination and it wasn't food, it means it was just a random point to walk to, so it will wait there for a bit and then choose a new random destination to walk to.
                self.timer += 1
                if self.timer >= self.waittimer:
                    self.timer = 0
                    self.waittimer = random.randint(20, 200) 
                    
                    random_dx = random.randint(-self.radius, self.radius)
                    random_dy = random.randint(-self.radius, self.radius)
                    
                    if random_dx != 0 or random_dy != 0:
                        self.dest_x = max(0, min(screen_width - creatures_size, self.x + random_dx))
                        self.dest_y = max(0, min(screen_width - creatures_size, self.y + random_dy))
        

        

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
    if teclas[pygame.K_ESCAPE]:
        running = False
    # Update the actual display
    pygame.display.flip()

# 4. Clean exit
pygame.quit()
sys.exit()
