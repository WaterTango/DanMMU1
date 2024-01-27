import pygame

pygame.init()

#display surface
WINDOW_WIDTH = 1280 
WINDOW_HEIGHT = 720

display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption("Continuous movement")

#Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

#set game value
VELOCITY = 5

#load image
spaceship_image = pygame.image.load("spaceship.png")
spaceship_rect = spaceship_image.get_rect()
spaceship_rect.center = ((WINDOW_HEIGHT//2 ,WINDOW_WIDTH//2))

#main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #get list of all keys being pressed
    keys = pygame.key.get_pressed()
    
    #sprite move continously
    if keys[pygame.K_a]:
        spaceship_rect.x -= VELOCITY
    if keys[pygame.K_d]:
        spaceship_rect.x += VELOCITY
    if keys[pygame.K_w]:
        spaceship_rect.y -= VELOCITY
    if keys[pygame.K_s]:
        spaceship_rect.y += VELOCITY

    #fill display
    display_surface.fill((0,0,0,))

    #blit
    display_surface.blit(spaceship_image,spaceship_rect)

    #updater
    pygame.display.update()

    #tick the clock
    clock.tick(FPS)

pygame.quit()

