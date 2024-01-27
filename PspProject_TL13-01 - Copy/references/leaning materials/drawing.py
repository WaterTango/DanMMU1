import pygame

pygame.init()


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_HEIGHT,WINDOW_WIDTH))

black = ( 0,0,0)
white = (255,255,255)
blue = (0,0,255)
display_surface.fill(blue)


# line(surface,color,starting point, ending,point,thickness)
pygame.draw.line(display_surface,(255,0,0),(0,0),(600,600),5)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


pygame.quit()