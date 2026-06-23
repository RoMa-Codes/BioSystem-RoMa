import pygame
import sys
import random
import os
import math
#makes this work
pygame.init()
###
# VARS
usles_var = 4
# screen vars
screen_width=1400
screen_height=800
screen=pygame.display.set_mode([screen_width, screen_height])
#name the window
pygame.display.set_caption("BioSystem-RoMa") 

#vars
clock = pygame.time.Clock()

running = True
creatures_size = 50
player_x =  screen_width // 2 - creatures_size // 2
player_y = screen_height // 2 - creatures_size // 2

bush_size = 100


def immage_render(immage_name):
    # lerns the way to this folder and sets it up so that future vars can set themselves as the sprite
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    immage_path = os.path.join(BASE_DIR, "assets", "sprites", immage_name)
    final_immage = pygame.image.load(immage_path)
    return final_immage



apple_sprite = immage_render("apple.png")
bush_sprite = immage_render("bush.png")

animal_sprite = immage_render("slug.png")
sprite_animal = pygame.transform.scale(animal_sprite, (creatures_size, creatures_size))
apple_sprite = pygame.transform.scale(apple_sprite, (bush_size/2, bush_size/2))
bush_sprite = pygame.transform.scale(bush_sprite, (bush_size, bush_size))

#sets the speed of the user
speed = 5

# chaing the backround color to any RGB value
screen.fill((0, 128, 0))

#created the food_timer var that will be necesary laiter
food_timer = 0

#seting up a sound player
pygame.mixer.init()
def play_sound(filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sound_path = os.path.join(BASE_DIR, "assets", "sounds", filename)
    try:
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
    except pygame.error as e:
        print(f"Error al reproducir '{sound_path}': {e}") 


# creates foods (that are actualy just plants but ig its fine)
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

#generates the herb eating creatures (btw adding var = non there makes them opcional)
class herb_eating_Creatures:
    def __init__(self, spawn_x = None, spawn_y =None):
       
        # Stats del Deer
        #neurtrient vars
        self.needed_nutrients = 50
        self.repro_nutrients = 80
        self.want_nutrients = 100
        self.current_neutrients = random.randint(50, self.want_nutrients)
        #speed vars
        self.norm_speed = 3
        self.panic_speed = 4

        self.radius = 200      # movemnt range
        self.sight = 100       #seeing range

        self.name = "Deer"
        self.hp = 100

        # setting the pozition were it spawns with the self.x var that means its curent pozition
        if spawn_x == None:
            self.x = random.randint(0, screen_width)
        else:
            self.x = spawn_x
        if spawn_y == None:
            self.y = random.randint(0, screen_height)
        else:
            self.y = spawn_y


        
        

        # variables to remember the destination and a timer for waiting
        self.dest_x = self.x
        self.dest_y = self.y
        #creating timers vars
        self.waittimer = random.randint(20, 60)
        self.new_timer = 0 
        self.timer = 0

    def update(self):
        #here we create a timer so in the future we can remove its curent neutriates
        
        self.new_timer += 1
        if self.new_timer >= 20: # this will make it lose nutrients every second, because the game runs at 60 frames per second, so every 60 updates it will lose nutrients. This way we can make it lose nutrients over time and make it need to eat to survive.
            self.new_timer = 0
            self.current_neutrients -= 1
        if self.current_neutrients < 0:
            #here we remove the creature from the simulation if it dies of hunger, but for now we will just set its nutrients to 0 and make it stop moving, because we haven't implemented death yet and it would break the system if it could die without being removed from the simulation.
            play_sound("die.mp3")
            animals_list.remove(self)
            

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

        if self.current_neutrients > self.repro_nutrients:
            pass
                
        # movement code, it will move towards the destination set by the food searching code if it found some, otherwise it will just keep moving towards a random destination that changes every few seconds. When it reaches the destination, if it's a food, it will eat it and gain nutrients, if it's just a random point, it will wait there for a bit and then choose a new random destination to walk to.
        self.x_dist = self.dest_x - self.x
        self.y_dist = self.dest_y - self.y
        self.distance = math.hypot(self.x_dist, self.y_dist)

        if self.distance > self.norm_speed:
            self.x += (self.x_dist / self.distance) * self.norm_speed
            self.y += (self.y_dist / self.distance) * self.norm_speed
             
        else:
            # Si llegó a su destino y era un alimento, lo come y gana nutrientes:
            if clowse_food is not None:
                self.current_neutrients += clowse_food.nutrients 
                
                # if the nutrients gained by eating the food exceed the creature's want_nutrients, it will just set its current_neutrients to want_nutrients, because it doesn't need more than that and it would break the system if it could keep gaining nutrients infinitely.


                print(f"ate: {clowse_food.name} | +{clowse_food.nutrients} nutrientes")
                print(f"entity current nutrients: {self.current_neutrients}")
                
                if clowse_food in foods:
                    play_sound("eating_sound.mp3")
                    foods.remove(clowse_food)
                
                self.x = self.dest_x
                self.y = self.dest_y
                clowse_food = None 
                self.timer = 0
                
            else:
                # if it reached its destination and it wasn't food, it means it was just a random point to walk to, so it will wait there for a bit and then choose a new random destination to walk to.
                self.timer += 1
                if self.new_timer == 0:
                    self.current_neutrients += 1
                if self.timer >= self.waittimer:
                    self.timer = 0
                    self.waittimer = random.randint(20, 200) 
                    
                    random_dx = random.randint(-self.radius, self.radius)
                    random_dy = random.randint(-self.radius, self.radius)
                    
                    if random_dx != 0 or random_dy != 0:
                        self.dest_x = max(0, min(screen_width - creatures_size, self.x + random_dx))
                        self.dest_y = max(0, min(screen_height - creatures_size, self.y + random_dy))
        

        

animals_list = []
#this controlls the amount of food and animals that spawns at the start of the simulation, but they will keep spawning over time as well, so it's not like they will be the only ones in the simulation, but it will give it a good start and make it more interesting to watch from the beginning.

for i in range(20):
    foods.append(Food())
for i in range(5):
    animals_list.append(herb_eating_Creatures())



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
            screen.blit(apple_sprite, (food.x -bush_size/4, food.y -bush_size/4))
    for food in foods:
        if food.name == "Bush":
            screen.blit(bush_sprite, (food.x -bush_size/2, food.y -bush_size/2))
    
        
    for a in animals_list:
        a.update()

    
    for a in animals_list:
        screen.blit(sprite_animal, (a.x - creatures_size/2, a.y - creatures_size/2))
    
    screen.blit(sprite_animal, (player_x, player_y))
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT] and player_x > 0:
        player_x -= speed
    if teclas[pygame.K_RIGHT] and player_x < screen_width - creatures_size:
        player_x += speed
    
        
    if teclas[pygame.K_UP] and player_y > 0:
        player_y -= speed
    if teclas[pygame.K_DOWN] and player_y < screen_height - creatures_size:       
        player_y += speed
    if teclas[pygame.K_ESCAPE]:
        running = False
    # Update the actual display
    pygame.display.flip()

# 4. Clean exit
pygame.quit()
sys.exit()
