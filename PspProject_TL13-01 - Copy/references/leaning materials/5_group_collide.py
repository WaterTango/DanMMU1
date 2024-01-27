import pygame,random

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Group Collide!")

FPS = 60
clock = pygame.time.Clock()

#define classes
class Game():
    def __init__(self, monster_group , knight_group):
        self.monster_group = monster_group
        self.knight_group = knight_group

    def update(self):
        self.check_collisions()

    def check_collisions(self):
        pygame.sprite.groupcollide(self.monster_group,self.knight_group, True , False)



class Monster (pygame.sprite.Sprite):
    """Class to represent a monster"""
    def __init__(self, x, y,):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        self.velocity = random.randint(1,5)

    def update(self):
        """Update and move monster"""
        self.rect.y += self.velocity

class Knight (pygame.sprite.Sprite):
    """Class to represent a knight"""
    def __init__(self, x, y,):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x , y)

        self.velocity = random.randint(1,5)

    def update(self):
        """Update and move monster"""
        self.rect.y -= self.velocity


#create a monster group
my_monster_group = pygame.sprite.Group()
for i in range (12):
    monster = Monster(i*64 , 10)
    my_monster_group.add(monster)

#create a knight group
my_knight_group = pygame.sprite.Group()
for i in range (12):
    knight = Knight(i*64 ,WINDOW_HEIGHT-64)
    my_knight_group.add(knight)

#create a game object
my_game = Game(my_monster_group,my_knight_group)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    #fill screen
    display_surface.fill((0,0,0))

    #update and draw spirte group
    my_monster_group.update()
    my_monster_group.draw(display_surface)

    my_knight_group.update()
    my_knight_group.draw(display_surface)

    my_game.update()

    pygame.display.update()
    clock.tick(FPS)

pygame.quit