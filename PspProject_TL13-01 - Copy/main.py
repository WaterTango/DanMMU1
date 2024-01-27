#*********************************************************
# Program: main.py
# Course: PSP0101 PROBLEM SOLVING AND PROGRAM DESIGN
# Class: TL13
# Year: 2023/24 Trimester 1
# Names: MUHAMMAD DANIEL IKMAL BIN ZAINAL | TOH ZHAN PHENG | 
# IDs: 1231101799 | MEMBER_ID_2 | 
# Emails: danielikmal1404@gmail.com | MEMBER_EMAIL_2 | 
# Phones: 01151122654 | 0182161516 |
# *********************************************************

import pygame,random,sys,os

#start the pygame
pygame.init()

WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000

display_surface = pygame.display.set_mode ((WINDOW_WIDTH , WINDOW_HEIGHT))
pygame.display.set_caption("Stardust Crusader") #jojo reference

FPS = 60
clock= pygame.time.Clock()

##############################################################################################################################################################################
##this just for background
##############################################################################################################################################################################

# https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
class Background():
    def __init__(self):
        self.image = pygame.image.load("background.webp")
        self.rect = self.image.get_rect()
        self.size = pygame.transform.scale(self.image,(WINDOW_WIDTH,(WINDOW_HEIGHT - 100)))
        display_surface.blit(self.size,self.rect)

###############################################################################################################################################################################
##Class for the game (basically contains all the variable,collision detect and ui)
###################################################################################
class Game():
    def __init__(self, player , asteroid_group,powerup_group):
        global running
        self.player = player
        self.asteroid_group = asteroid_group
        self.powerup_group = powerup_group

        #game values can change 
        self.score = 0
        self.high_score = 0
        self.round_number = 0
        self.lives = 5
        self.grace = 1
        self.boost = 100
        #this is for round values
        self.round_time = 0
        self.frame_count = 0
        
        #how manhy asteroids can spawn at beginning
        self.asteroid_number = random.randint(8,12)

        #this is for counting how many powerup to spawn and how often
        self.powerup_number = 1
        self.powerup_spawn_timecount = 3

        #bg music that will play during game i (value) = 
        self.bg_music = pygame.mixer.music.load("bg_music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        #sfx for the game feel free to change
        self.hit_sound = pygame.mixer.Sound("hit.wav")
        self.hit_sound.set_volume(0.1)
        self.fail_sound = pygame.mixer.Sound("fail_sound.mp3")
        self.fail_sound.set_volume(0.1)
        self.game_over_sound = pygame.mixer.Sound("game_over.mp3")
        self.game_over_sound.set_volume(0.1)
        self.powerup_sound = pygame.mixer.Sound("powerup.mp3")
        self.powerup_sound.set_volume(0.1)


        #set font 
        self.font = pygame.font.Font("Starwars.ttf",45)
##########################################################################################################################################
    #update the score every 1 seconds or 60 FPS
        #got this idea https://www.tutorialspoint.com/pygame/pygame_quick_guide.htm 
        
        #since the code go 60 time per second i can count 1 second using farme_count and add score severy second
    def update(self):
        self.frame_count += 1
        #increase score every second
        if self.frame_count == FPS:
            self.score += 100
            self.frame_count = 0

        #check if lives low and spawn powerup
        if self.lives == 1 and self.score > 100 and self.frame_count == 1 and self.powerup_spawn_timecount > 0:
            self.powerup_spawn_timecount -= 1
            self.spawn_powerup()
        
        self.check_collisions()
##########################################################################################################################################
        #check if score_txt exist
    def check_highscore(self):
        if os.path.exists('score.txt'):
            with open('score.txt', 'r') as file:
                self.high_score  = int(file.read())
        else:
            self.high_score = 0

##########################################################################################################################################     
    def draw(self):

        #values for colors Im lazy to type it multiple times
        BLACK = (0,0,0,)
        WHITE = (255,255,255)
        GREEN = (0,255,0)
        RED = (255,0,0)     
        font = pygame.font.Font("Starwars.ttf" ,45)


        #this for diplay score top left
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (16,16)


        #this need optimize idk how to do better(please change if can)
        title_text = font.render("Stardust Crusader", True,RED)
        title_rect = title_text.get_rect()
        title_rect.centerx = WINDOW_WIDTH//2

        title_rect.y = 16

        #Lives text right side(holy shit there has to be a better way to do this )
        lives_text = font.render("Lives: " + str(self.lives) , True , WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 16,16)

        #grace ( tp the player to safe zone)
        grace_text = font.render("Recall: " + str(self.grace) + " 'space'", True,WHITE,BLACK)
        grace_rect = grace_text.get_rect()
        grace_rect.center = (WINDOW_WIDTH-200,WINDOW_HEIGHT-60)

        # boosts
        boost_text = font.render("Boost: " + str(self.boost) + "%" + " 'Rshift'", True,WHITE,BLACK)
        boost_rect = boost_text.get_rect()
        boost_rect.center = (250,WINDOW_HEIGHT-60)

        #boost icon
        self.boost_image = pygame.image.load("boost.png")
        self.boost_rect = self.boost_image.get_rect()
        self.boost_rect.center = (WINDOW_WIDTH//2-230,WINDOW_HEIGHT-55)
        display_surface.blit(self.boost_image,self.boost_rect)
        #health icon
        self.health_image = pygame.image.load("health.png")
        self.health_rect = self.health_image.get_rect()
        self.health_rect.topright = (WINDOW_WIDTH - 215,27)
        display_surface.blit(self.health_image,self.health_rect)
        # blit hud  and drawing lines  on display surface
        display_surface.blit(score_text,score_rect)
        display_surface.blit(title_text,title_rect)
        display_surface.blit(lives_text,lives_rect)
        display_surface.blit(grace_text,grace_rect)
        display_surface.blit(boost_text,boost_rect)
        pygame.draw.line(display_surface, WHITE,(0,64),(WINDOW_WIDTH,64),2)
        pygame.draw.line(display_surface, WHITE,(0,WINDOW_HEIGHT-100),(WINDOW_WIDTH,WINDOW_HEIGHT-100),2)

##########################################################################################################################################
    # collision check
        #this one i got from https://www.pygame.org/docs/ref/sprite.html 
    def check_collisions(self):
        #check colision thankfully pygame have a fucntion for it
        if pygame.sprite.groupcollide(self.player,self.asteroid_group,False,True):
            self.hit_sound.play()
            my_player.died()
            self.lives -= 1

        #check collision between player and powerups
        if pygame.sprite.groupcollide(self.player,self.powerup_group,False,True):
            self.powerup_sound.play()
            my_player.reset()
            self.lives += 1
            self.grace = 1
            self.boost += 100
        #check if lives go to 0
        if self.lives == 0:
            pygame.mixer.music.pause()
            self.game_over_sound.set_volume(0.08)
            self.game_over_sound.play() 
            if self.score > self.high_score:
                self.high_score = self.score
                with open('score.txt','w') as file:
                    file.write(str(self.high_score))

            self.reset_game("Final Score: " + str(self.score),"Highscore: " + str(self.high_score))

########################################################################################################################################################################################
            
    def menu_game(self):
        global running 

        BLACK = (0,0,0)
        display_surface.fill(BLACK)

        #DISPLAY MAIN MENU
        #menu image
        self.menu_image = pygame.image.load("Menu.jpg")
        self.menu_rect = self.menu_image.get_rect()
        self.menu_size = pygame.transform.scale(self.menu_image,(WINDOW_WIDTH,(WINDOW_HEIGHT)))
        display_surface.blit(self.menu_size,self.menu_rect)
        pygame.display.update()
        ##pause the game it self
        pause = True

        #start menu
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False
##########################################################################################################################################   
    def reset_game(self,game_over_text,highscore_text,):
        global running
        WHITE = (255,255,255)
        BLACK = (0,0,0)

        #Render text
        game_over_text = self.font.render(game_over_text,True,WHITE)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2)

        highscore_text = self.font.render(highscore_text,True,WHITE)
        highscore_rect = highscore_text.get_rect()
        highscore_rect.center = (WINDOW_WIDTH//2,WINDOW_HEIGHT//2+200)


        display_surface.fill(BLACK)

        #load gackground image for end screen
        self.menu_image = pygame.image.load("GameOver.jpg")
        self.menu_rect = self.menu_image.get_rect()
        self.menu_size = pygame.transform.scale(self.menu_image,(WINDOW_WIDTH,(WINDOW_HEIGHT)))
        display_surface.blit(self.menu_size,self.menu_rect)


        display_surface.blit(game_over_text,game_over_rect)
        display_surface.blit(highscore_text,highscore_rect)

        pygame.display.update()

        #check if player wanna quit or play again 'Enter'
        end = True
        while end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.clean_start()
                        end = False
##########################################################################################################################################
    #for loops to spawn asteroid ...........Asteroids(x coordinate,y coordniate) and range = asteroids number (see game class on top)
    def spawn_asteroid(self):
        for i in range(self.asteroid_number):
            asteroid = Asteroid(random.randint(0,WINDOW_WIDTH) , random.randint(-100,0))
            self.asteroid_group.add(asteroid)
        for i in range(self.asteroid_number):
            asteroid = Asteroid_sideway(random.randint(-132,-1) , random.randint(0,WINDOW_HEIGHT-132))
            self.asteroid_group.add(asteroid)
##########################################################################################################################################
            
    #spawns multiple powerups
    def powerup(self):
        for i in range(self.powerup_number):
            powerup = Powerup(random.randint(0,WINDOW_WIDTH) , random.randint(-100,0))
            self.powerup_group.add(powerup)        
##########################################################################################################################################
            
    #spawns asteroids
    def start_round(self):
        self.spawn_asteroid()
##########################################################################################################################################
        
    #spawnpowerup
    def spawn_powerup(self):
        self.powerup()
##########################################################################################################################################
        
    #ressting the game after gameover
    def clean_start(self):
        for asteroid in self.asteroid_group:
            self.asteroid_group.remove(asteroid)
        for powerup in self.powerup_group:
            self.powerup_group.remove(powerup)
        self.score = 0
        self.round_number = 0
        self.lives = 5
        self.grace = 1
        self.boost = 100
        pygame.mixer.music.play(-1)
        self.spawn_asteroid()
        self.spawn_powerup
        my_player.reset()

##############################################################################################################################################################################
        

#This is for player Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        #image and rect of player (can change later if want)
        self.image = pygame.image.load("Red_spaceship32.png")
        self.rect = self.image.get_rect()
        self.rect.x = WINDOW_WIDTH//2
        self.rect.y = WINDOW_HEIGHT - 75

        #player speed
        self.velocity = 10
        #recall sound
        self.recall_sound = pygame.mixer.Sound("recall_sound.mp3")
        self.recall_sound.set_volume(0.1)

    def update(self):
        #get list of all keys being pressed
        keys = pygame.key.get_pressed()
        #for movement of the player (last row is for not allowing player to go back to the safe zone)
        if keys[pygame.K_a] and self.rect.left > 0  :
            self.rect.x -= self.velocity
        if keys[pygame.K_d] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity
        if keys[pygame.K_w] and self.rect.top > 64 :
            self.rect.y -= self.velocity
        if keys[pygame.K_s] and self.rect.bottom < WINDOW_HEIGHT-100:
            self.rect.y += self.velocity

        #detect if Right Shift is pressed and boost
        if keys[pygame.K_a] and keys[pygame.K_RSHIFT] and self.rect.left > 0 and my_game.boost >=1:
            self.rect.x -= self.velocity+20
            my_game.boost -= 1
            
        if keys[pygame.K_d] and keys[pygame.K_RSHIFT] and self.rect.right < WINDOW_WIDTH and my_game.boost >= 1:
            self.rect.x += self.velocity +20
            my_game.boost -= 1
            

        if keys[pygame.K_w] and keys[pygame.K_RSHIFT] and self.rect.top > 64 and my_game.boost >= 1:
            self.rect.y -= self.velocity + 20
            my_game.boost -= 1
            

        if keys[pygame.K_s] and keys[pygame.K_RSHIFT] and self.rect.bottom < WINDOW_HEIGHT-100 and my_game.boost >= 1:
            self.rect.y += self.velocity +20
            my_game.boost -= 1
            


        if keys[pygame.K_SPACE]:
            if my_game.grace > 0:
                my_game.grace -= 1
                self.recall_sound.play()
                my_player.reset()


    #this is for reseting player pos after death
    def died(self):
        self.rect.x = WINDOW_WIDTH//2
        self.rect.y = WINDOW_HEIGHT - 200
            #this one is for when player press 'space' (see while loop) player go to safe room
    def reset(self):
        self.rect.x = WINDOW_WIDTH//2
        self.rect.y = WINDOW_HEIGHT - 75
##############################################################################################################################################################################
#this for asteroid coming from top
class Asteroid(pygame.sprite.Sprite):

    def __init__(self , x , y,):
        super().__init__()

        self.game = Game

        self.image = pygame.image.load("asteroidPixel.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x , y)

        #set the asteroid velocity using random (so can have different speed)
        self.velocity = random.randint(4,8)
        
        #this for updating the class each time game loops
        #also reset the position of asteroid when it hits the bottom 
        #it basically recycle the objects 
    def update(self):
        self.rect.y += self.velocity

        if self.rect.bottom >= WINDOW_HEIGHT-100:
            self.velocity = random.randint(4,8)
            self.rect.y = self.velocity
            self.rect.x = random.randint(0,WINDOW_WIDTH)

##############################################################################################################################################################################
#this for asteroids coming from left (same as top only change the value of directions)
class Asteroid_sideway(pygame.sprite.Sprite): #<------pygame library
    def __init__(self , x , y,):
        super().__init__()

        self.image = pygame.image.load("asteroids.png")
        self.rect = self.image.get_rect()

        self.rect.center = (x , y)

        self.velocity = random.randint(4,8)
        
    def update(self):
        self.rect.x += self.velocity
        if self.rect.right >= WINDOW_WIDTH:
            self.velocity = random.randint(4,8)
            self.rect.y = random.randint(132,WINDOW_HEIGHT-132)
            self.rect.x = 0

##############################################################################################################################################################################


##############################################################################################################################################################################
#poweup
class Powerup(pygame.sprite.Sprite):  
    def __init__(self , x , y,):
        super().__init__()
        self.image = pygame.image.load("battery.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.velocity = random.randint(5,10)
    #update the movement of powerups
    def update(self):
        self.rect.y += self.velocity
        if self.rect.bottom >= WINDOW_HEIGHT-100:
            self.rect.y = 100
            self.rect.x = random.randint(0,WINDOW_WIDTH)

##############################################################################################################################################################################

#player group
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#asteroid group
my_asteroid_group = pygame.sprite.Group()

#asteroid sideways group
my_asteroidside_group = pygame.sprite.Group()

#powerupgroup
my_powerup_group = pygame.sprite.Group()

#game group
my_game = Game(my_player_group,my_asteroid_group,my_powerup_group)

#this is to display the main menu
my_game.menu_game()
my_game.start_round()
my_game.spawn_powerup()


#############################################################################################################################################################
#### MAIN GAME LOOP NO TOUCH
#############################################################################################################################################################

running = True
while running:
    for event  in pygame.event.get():
        #to check if user click the x on top right of window it stops the progeram and quits
        if event.type == pygame.QUIT:
            running = False
        #same on top but check esc btton instead while in game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #fill/update display surface
    display_surface.fill((0,0,0))
    Background()

    #update and draw spirte group
    my_asteroid_group.update()
    my_asteroid_group.draw(display_surface)

    my_powerup_group.update()
    my_powerup_group.draw(display_surface)

    my_player_group.update()
    my_player_group.draw(display_surface)

    my_game.update()
    my_game.check_highscore()
    my_game.draw()

    #update
    pygame.display.update()

    #tik
    clock.tick(FPS)

pygame.quit()