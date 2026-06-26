import pygame
import sys
import random
import os
import math
#makes this work
pygame.init()
###
# VARS
usles_var = 20
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

animal_sprite = immage_render("slug.webp")
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
    def __init__(self, spawn_x=None, spawn_y=None, name = None):
        if name == None:
            Identity = random.randint(1, 10)
            if Identity < 2:
                
                self.name = "Apple"
            elif Identity > 1 and Identity < 11:
                
                self.name = "Bush"
            elif Identity > 5:
                
                self.name = "Plant"
        else:
        
            self.name = name

        if self.name == "Apple":
            self.nutrients = 100
        elif self.name == "Bush":
            self.nutrients = 30
        elif self.name == "Plant":
            self.nutrients = 5
        #if the spawn isint defined it spawns them at random
        if spawn_x == None:
            self.x = random.randint(0, screen_width)
        else:
            self.x = spawn_x
        if spawn_y == None:
            self.y = random.randint(0, screen_height)
        else:
            self.y = spawn_y


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
        #this var is just the dest for a tick ago
        self.last_x = self.x
        self.last_y = self.y
        #creating timers vars
        self.waittimer = random.randint(20, 60)
        self.new_timer = 0 
        self.timer = 0
    def repoduce(self):
        # if it has enough nutrients to reproduce, it will create a new creature of the same type and give it some of its nutrients to start with, and then it will lose some of its own nutrients to account for the energy spent in reproduction. This way we can have a population of creatures that can grow and shrink over time depending on the availability of food and the success of their reproduction.
        if self.current_neutrients >= self.repro_nutrients:
            new_creature = herb_eating_Creatures(self.x, self.y)
            new_creature.current_neutrients = self.current_neutrients // 2
            self.current_neutrients //= 2
            animals_list.append(new_creature)
            print(f"{self.name} reproduced! New {new_creature.name} created at ({new_creature.x}, {new_creature.y})")
    def hungry(self):
        # Clear old random targets and look for the closest plant
        smallest_distance = self.sight  
        clowse_food = None

        for food in foods:
            dist_to_food = math.hypot(food.x - self.x, food.y - self.y)
            if dist_to_food <= smallest_distance:
                smallest_distance = dist_to_food
                clowse_food = food

        # If it finds a plant, override the destination straight to it
        if clowse_food is not None:
            self.dest_x = clowse_food.x
            self.dest_y = clowse_food.y
        return clowse_food # Pass this back so update knows if we are tracking food
    def idle(self):
        # if it reached its destination and it wasn't food, it means it was just a random point to walk to, so it will wait there for a bit and then choose a new random destination to walk to.
        self.timer += 1
        if self.new_timer == 1:
            self.current_neutrients += 1
        if self.timer >= self.waittimer:
            self.timer = 0
            self.waittimer = random.randint(20, 200) 
                    
            random_dx = random.randint(-self.radius, self.radius)
            random_dy = random.randint(-self.radius, self.radius)
                    
            if random_dx != 0 or random_dy != 0:
                self.dest_x = max(0, min(screen_width - creatures_size, self.x + random_dx))
                self.dest_y = max(0, min(screen_height - creatures_size, self.y + random_dy))
        
    
    def panic(self):
        pass
    def update(self):
        # die parts so if u aret eating ur neutients disapier
        if self.x != self.last_x or self.y != self.last_y:
            self.current_neutrients = -1/20
        #if u have no neutrients u die because thats just how it is    
        if self.current_neutrients < 0:
            play_sound("die.mp3")
            animals_list.remove(self)
            return

        # do i wander or look for food
        if self.current_neutrients < self.want_nutrients:
            # i am hungry
            active_target_food = self.hungry() 
        else:
            #i am not hungry
            active_target_food = None


        # movement code
        self.x_dist = self.dest_x - self.x
        self.y_dist = self.dest_y - self.y
        self.distance = math.hypot(self.x_dist, self.y_dist)

        if self.distance > self.norm_speed:
            self.x += (self.x_dist / self.distance) * self.norm_speed
            self.y += (self.y_dist / self.distance) * self.norm_speed
        else:
            # destination reached
            if active_target_food is not None:
                
                # FIRST check if the food is still alive in the global list!
                if active_target_food in foods:
                    # It is safe! Now we can read its nutrients
                    self.current_neutrients += active_target_food.nutrients
                    
                    if self.current_neutrients > self.want_nutrients:
                        self.current_neutrients = self.want_nutrients
                    
                    play_sound("eating_sound.mp3")
                    foods.remove(active_target_food)
                    self.timer = 0
                else:
                    # Someone else stole the food this frame! Reset to idle
                    self.idle()
            else:
                # The destination was just a random point
                self.idle()
        self.last_x = self.x
        self.last_y = self.y



                


        

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
    #food timer to spawn food evry x amount of time
    if food_timer >= random.randint(30, 120):
        food_timer = 0
        #len means that it looks at how many objects are in the list
        if len(foods) > 0:
            # 1. Pick a random parent plant that is already on the screen
            parent = random.choice(foods)
            
            # 2. Spawn a new food object instance
            new_seed = Food(name=parent.name)

            
            # 3. Quick & dirty radius offset math (Minimum 100 pixels away, max 180)
            offset_x = random.choice([random.randint(-bush_size*4, -bush_size*4), random.randint(bush_size*4, bush_size*4)])
            offset_y = random.choice([random.randint(-bush_size*4, -bush_size*4), random.randint(bush_size*4, bush_size*4)])
            
            # 4. Apply the offset to the parent's current position
            new_seed.x = parent.x + offset_x
            new_seed.y = parent.y + offset_y
            
            # 5. Fast map boundary clamp so they don't clip off-screen
            new_seed.x = max(0, min(screen_width - bush_size, new_seed.x))
            new_seed.y = max(0, min(screen_height - bush_size, new_seed.y))
            
            # 6. Drop it into the active simulation list!
            foods.append(new_seed)
        

    
    
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
