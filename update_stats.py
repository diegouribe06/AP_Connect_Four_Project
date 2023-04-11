#Line one imports pygame, a graphics library not made by me.
import pygame

#This file contains functions used by multiple files.

#Update stats is used to update the stats.txt file
#The check parameter tells the function whether the user won or lost the game. Debug is used to print the current stats to the command line.
def update_stats(check, debug = False):
    #If "win" is passed as the check parameter the program opens the "stats.txt" file, and saves the information read from it as a variable (Lines 10-12).
    if check == "win":
        with open("stats.txt") as stats:
            current_stats = stats.read()

        #The program then splits the text at the newline charachter to be able to edit the number at the start of the string (Line 15).
        current_stats = current_stats.split("\n")
        #Line 17 uses the debug parameter to determine if the current stats should be printed to the console.
        if debug: print(current_stats)
        #Line 19 assigns the first line of current stats to the previous count of wins plus 1 wins.
        current_stats[0] = f"{int(current_stats[0][0]) + 1} wins"
    #Lines 21 through 27 work the same way as lines 9 through 19, except they count losses insteead of wins.
    elif check == "lose":
        with open("stats.txt") as stats:
            current_stats = stats.read()

        if debug: print(current_stats)
        current_stats = current_stats.split("\n")
        current_stats[-1] = f"{int(current_stats[1][0]) + 1} losses"
    #Line 29 then takes both the elements from the seperated text file and combine them into a string
    rewrite = f"{current_stats[0]}\n{current_stats[-1]}"
    #Lines 30 and 31 rewrite the stats file with the updated counts.
    with open("stats.txt", "w") as stats:
        stats.write(rewrite)

    #If the debug parameter was true, lines 35 through 38 reset the stats file to 0
    if debug:
        with open("stats.txt", "w") as stats:
            reset = "0 wins\n0losses"
            stats.write(reset)

#getText is used to get a text input from the user, or to display a message.
#The message parameter is the message displayed by the program, color changes the color of the highlight, xpos changes where the text appears, boxWidth and boxHeight change the sizwe of the highlight
def getText(message = "", color = (255,0,0), xpos = 100, boxWidth = 100, boxHeight = 25):
    #Line 43 initializes the graphical library, pygame
    pygame.init()
    #Lines 46 and 47 set the size of the window and the font to be used.
    text_screen = pygame.display.set_mode([300, 300])
    font = pygame.font.SysFont("comic_sans_ms", 25)
    #Line 49 initializes an empty string that will hold the user's input
    text = ""
    #Line 51 creates a rectangle across the bottom of the window where the user's input will display
    text_bar = pygame.Rect(0, 250, 300, 100)
    #Line 53 creates the rectangle where the message parameter will be displayed, using the xpos, boxWidth, and boxHeight to determine where the rectangle will be placed.
    message_bar = pygame.Rect(xpos, 50, boxWidth, boxHeight)
    #The running variable is used to to end the key detection loop.
    running = True
    while running:
        #Line 58 iterates through all the events detected by pygame
        for event in pygame.event.get():
            #If the user tried to close the game, lines 60 and 61 will close the game.
            if event.type == pygame.QUIT:
                pygame.quit()
            
            #Lines 64 through 72 detect the user's key presses. If the user pressed backspace, the last character from text will be deleted. If the user hits enter, the program closes the window amd returns the text value. For all other keys, the program adds them to the text variable.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif event.key == pygame.K_RETURN:
                    running = False
                    pygame.quit()
                    return text
                else:
                    text += event.unicode

        #Line 75 sets the background to black. Line 76 draws the input box on the window using the color parameter to set the color of the box.
        text_screen.fill((0,0,0))
        pygame.draw.rect(text_screen, color, text_bar)
        #Line 78 renders the user's text, and line 79 draws it on the window.
        text_surface = font.render(text, True, (255, 255, 255))
        text_screen.blit(text_surface, (text_bar.x, text_bar.y))

        #Lines 81 through 84 work the same way as lines 76 through 79, except they draw the rectangle and text for the message.
        pygame.draw.rect(text_screen, color, message_bar)
        message_surface = font.render(message, True, (255,255,255))
        text_screen.blit(message_surface, (xpos, 50))
        
        #Line 87 updates the window every frame.
        pygame.display.flip()

#Show stats is the function called in GraphicalMenu to show the user their stats. The function opens the stats file, reads it, and outputs the results using the getText function.
def show_stats():
    with open("stats.txt", "r") as stats:
        stats = stats.read().split("\n")
        getText(f"{stats[0][0]} wins, {stats[1][0]} losses", xpos=60, boxWidth=180, boxHeight=40)