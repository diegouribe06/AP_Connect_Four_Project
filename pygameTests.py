import pygame
pygame.init()

max_height = 300
max_width = 350

screen = pygame.display.set_mode([max_width, max_height])
# Chips will be 100 * 100
# Lines are currently 20 thick

running = True

def grid_lines(x1, y1, x2, y2):
    return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

def red_chip(x, y):
    return [screen, (255, 0, 0), (x, y), 25, 25]

def yellow_chip(x, y):
    return [screen, (255, 255, 0), (x,y), 25, 25]

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    tracker = 50
    for i in range(6):
        pygame.draw.line(*grid_lines(tracker, 0, tracker, max_height))
        pygame.draw.line(*grid_lines(0, tracker, max_width, tracker))
        if i == 5:
            pygame.draw.line(*grid_lines(0, 0, max_width, 0))
        tracker += 50

    pygame.display.flip()
    
pygame.quit()