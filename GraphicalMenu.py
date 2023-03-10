import pygame
from GraphicalClient import game as graphicalClient
from GraphicalHost import game as graphicalHost
from GraphicalLocal import game as graphicalLocal

def getText(message = "", color = (255,0,0), xpos = 100, boxWidth = 100, boxHeight = 25):
    pygame.init()
    text_screen = pygame.display.set_mode([300, 300])
    font = pygame.font.SysFont("comic_sans_ms", 25)
    text = ""
    text_bar = pygame.Rect(0, 250, 300, 100)
    message_bar = pygame.Rect(xpos, 50, boxWidth, boxHeight)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    running = False
                    pygame.quit()
                    return text
                else:
                    text += event.unicode

        text_screen.fill((0,0,0))
        pygame.draw.rect(text_screen, color, text_bar)
        text_surface = font.render(text, True, (255, 255, 255))
        text_screen.blit(text_surface, (text_bar.x, text_bar.y))
        #text_bar.w = max(100, text_surface.get_width() + 10)

        pygame.draw.rect(text_screen, color, message_bar)
        message_surface = font.render(message, True, (255,255,255))
        text_screen.blit(message_surface, (xpos, 50))
        
        pygame.display.flip()

while True:
    while True:
        game_mode = getText("Local, LAN, or Stats?", xpos=30, boxWidth=250, boxHeight=40).upper()
        if game_mode not in ["LOCAL", "LAN", "STATS"]:
            getText("Invalid Selection", xpos=50, boxHeight=40, boxWidth=200)
        else:
            break
    if game_mode == "LOCAL":
        graphicalLocal()
    elif game_mode == "LAN":
        mode = getText("Host or Join?", xpos=75, boxHeight=40, boxWidth=160).upper()
        if mode == "HOST":
            graphicalHost()
        elif mode == "JOIN":
            graphicalClient()
    elif game_mode == "STATS":
        print("Stats")

    if getText("Play Again? (Y/N)", xpos=50, boxHeight=40, boxWidth=205).upper() == "Y":
        continue
    else:
        getText("Thank you for playing!", xpos=24, boxHeight=40, boxWidth=255)
        pygame.quit()
        break
    