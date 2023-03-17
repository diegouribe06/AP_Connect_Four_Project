import pygame
from GraphicalClient import game as graphicalClient
from GraphicalHost import game as graphicalHost
from GraphicalLocal import game as graphicalLocal
from update_stats import getText

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
    