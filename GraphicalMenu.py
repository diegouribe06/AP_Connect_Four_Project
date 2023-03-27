import pygame
#PyGame is a library that allows graphics. Not created by me.

from GraphicalClient import game as graphicalClient
#Line 4 imports the client game from the GraphicalClient file

from GraphicalHost import game as graphicalHost
#Line 7 imports the host game from the GraphicalHost file

from GraphicalLocal import game as graphicalLocal
#Line 10 imports the local game from the GraphicalLocal file

from update_stats import getText
#Line 13 imports the custom visual text function from the update_stats file

from update_stats import show_stats
#Line 16 imports the function to show the stats saved at the stats.txt file

#The code for the main menu is in an infinite loop, so the player can play again without having to re-run the file
while True:
    #Lines 22 through 27 are in an infinite loop to make sure that the user selects a valid game mode
    while True:
        game_mode = getText("Local, LAN, or Stats?", xpos=30, boxWidth=250, boxHeight=40).upper()
        #Line 23 uses the custom text function get the user's game mode choice. The response is formatted to ignore charachter case.
        #Line 26 is the conditional that checks to make sure that the game mode is a valid option. If it is not a valid option, it will tell the user, and ask again for the game mode. Otherwise, the requested game mode will run.
        if game_mode not in ["LOCAL", "LAN", "STATS"]:
            getText("Invalid Selection", xpos=50, boxHeight=40, boxWidth=200)
        else:
            break

    #Lines 32 through 41 are the conditional block that run the requested game mode based off of the user's input
    if game_mode == "LOCAL":
        graphicalLocal()
    elif game_mode == "LAN":
        #If the user requests the LAN mode, the program will then ask the user if they want to host or join a game.
        mode = getText("Host or Join?", xpos=75, boxHeight=40, boxWidth=160).upper()
        if mode == "HOST":
            graphicalHost()
        elif mode == "JOIN":
            graphicalClient()
    elif game_mode == "STATS":
        show_stats()

    #Once the user finishes a game and exits the game mode, the program will ask them if they want to play again
    if getText("Play Again? (Y/N)", xpos=50, boxHeight=40, boxWidth=205).upper() == "Y":
        #If the user decides to play again, the program restarts do to the infinite loop at line 20
        continue
    else:
        #If the user does not wish to continue playing, the game thanks the user for playing (line 50), closes all of pygames processes (line 51), and then closes since it reaches the end of the file.
        getText("Thank you for playing!", xpos=24, boxHeight=40, boxWidth=255)
        pygame.quit()
        break
    