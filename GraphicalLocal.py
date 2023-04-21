#Line 2 imports the copy module which is used to make copies of objects. Not created by me
import copy
#Line 4 imports pygame, a graphics library. Not created by me
import pygame
#Lines 6 and 7 import the functions to update stats and the custom text function
from update_stats import update_stats
from update_stats import getText

#The whole mode is inside a "temporary" function to be able to be called in an infinite loop, so the user can play again without having to go through the menu.
def tempGame():
    #Lines 12 and 13 get the names of the players to be used in the game. 
    player1 = getText("Player 1:")
    player2 = getText("Player 2:", (0, 255, 0))

    #player_turn is used for the logic of the turn system. When player_turn is 0, it's player1's turn and when player_turn is 1, it's player2's turn.
    player_turn = 0

    #Text is the variable that displays information about the game at the bottom of the screen. It is constantly changed by actions in the game.
    text = f"{player1}'s Turn"

    #Lines 22 through 24 define tuples of RGB values as variables to improve readibility of the program
    blank = (0,0,0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)

    #Lines 27 through 33 are used for both the logic to draw the grid, and the win detection. Each dictionary represents a row of the grid, each key is a spot on the corresponding row, and the value is the status of the spot
    row_a = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_b = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_c = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_d = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_e = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_f = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_g = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}

    #Lines 36 through 43 are used to apply a scale factor to the game window. This can be used to make the game window bigger and easier to see. The lines are in an infinite loop to make sure that the user enters a valid scale factor
    while True:
        #Line 39 is in a try-except block to make sure that the user enters a number. Since pygame works with pixel measurments the scale factor has to be an integer, so the program automaticaly rounds to a whole number.
        try:
            scaling = round(float(getText("Scale: ", (0, 0, 255))))
            break
        except:
            #If the user enters a string, the program will tell them to enter a valid number and prompt them to enter the scale factor again.
            getText("Enter a valid number", boxHeight=40, xpos=30, boxWidth=245)

    #300 * 350 is the default size of the game. If the user enters a scale factor other than one, the size is increases by that factor. 
    max_height = 300 * scaling
    max_width = 350 * scaling

    #Line 50 initializes pygame, the library used for graphics
    pygame.init()

    #Line 53 tells pygame what font to use for text and the font size. If the font is not installed on the computer, pygame uses the system default font.
    font = pygame.font.SysFont("comic_sans_ms", 25 * scaling)

    #Line 56 sets the size of the game window, with a little extra added to the height to leave room for a message.
    screen = pygame.display.set_mode([max_width, max_height + 50 * scaling])

    #The grid_lines function simplifies the pygame.draw.line() function to only the start and endpoints
    def grid_lines(x1, y1, x2, y2):
        return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

    #The chip function simplifies the pygame.draw.circle() function to only need the center coordinate, and the color.
    def chip(x, y, color):
        return [screen, color, (x, y), 20 * scaling, 25 * scaling]

    #The get_grid() function returns the grid dictionaries in a list in order to be able to both iterate through the entire grid, and to compare "snapshots" of the grid before and after moves.
    def get_grid():
        return [row_a, row_b, row_c, row_d, row_e, row_f, row_g]

    #Moves 2 is the function that places the player's chip in the grid, using the row parameter.
    def moves2(row):
        #Lines 73 and 74 allow the function to check and change both what the text says, and who's turn it is
        nonlocal player_turn
        nonlocal text
        
        #Lines 77 and 78 are used to take a "snapshot" of the grid before a turn occurs by making a copy of the results from the get_grid() function.
        rows = get_grid()
        precheck = copy.deepcopy(rows)

        #Lines 81 through 84 set the bottom text to the player's turn.
        if player_turn == 0:
            text = f'{player2}\'s turn'
        elif player_turn == 1:
            text = f'{player1}\'s turn'
        
        #Line 87 sets the following algorithm's variable to the passed parameter
        desired_row = row

        #The loop in line 90 is used to check every "spot" in the user's selected row.
        for spot in rows[desired_row]:
            if player_turn == 0 and rows[desired_row][spot] == blank:
                #If it's player one's turn, the algorithm places an empty chip in the first empty spot and exits the loop
                rows[desired_row][spot] = yellow
                break
            elif player_turn == 1 and rows[desired_row][spot] == blank:
                #If it's player two's turn, it'll place a red chip instead and exit the loop
                rows[desired_row][spot] = red
                break
        
        #Line 101 compares the grid before a move was attempted to the grid after a move was attempted. If there is a difference, meaning that a chip was successfully placed, the program will continue and change the player's turn.
        if list(precheck) != get_grid():
            if player_turn == 0:
                player_turn = 1
            elif player_turn == 1:
                player_turn = 0
            #Line 107 deletes the cloned grid to reduce memory usage.
            del precheck
        else:
            #If no change was detected between the old and new grids, the program knows that the row that the player selected is full, and tells the player that they selected an invalid option.
            text = "Invalid Choice"

    #The draw_check() function is used to check if there is a tie. The function iterates through the entire grid, and returns false for the first empty spot it finds. If draw_check() iterates through the whole grid without finding an empty spot, it returns true.
    def draw_check():
            #Line 115 lets the function edit the game's bottom text if there is a draw.
            nonlocal text
            rows = get_grid()
            for row in rows:
                for spot in row:
                    if row[spot] == blank:
                        return False
            text = "   It's a tie!    "
            return True

    #The win_check() function contains all of the algorithms to detect a winning condition
    def win_check():
            nonlocal player_turn
            nonlocal text
            #The vert_check() function scans through the grid from down up, left to right, looking for four consecutive, same color chips up and down
            def vert_check(row, additional):
                #The conditional first checks to see if the spot that it's checking is not blank. The algorithm then checks if four spots in the row parameter are the same. The "additional" paramater shifts the four spots the algorithm is looking at by the specified number. Finally, vert_check() returns true if all the "chips" were the same and false if not.
                if((row[1 + additional] == yellow) or (row[1 + additional] == red)) and (row[1 + additional] == row[2 + additional]) and (row[2 + additional] == row[3 + additional]) and (row[3 + additional] == row[4 + additional]):
                    return True
                else:
                    return False

            #The first loop goes through each row, and the second loop moves the "chips" up 2 times to cover the entire row.
            for row in get_grid():
                for additional in range(3): #2 added for all up and down
                    if vert_check(row, additional) and player_turn == 1:
                        text = f'{player1} Wins!'
                        #If player1 wins, the program adds one win to the stats
                        update_stats("win")
                        return True
                    elif vert_check(row, additional) and player_turn == 0:
                        text = f'{player2} Wins!'
                        #If player1 loses, the program adds a loss to the stats
                        update_stats("lose")
                        return True
                    
            #The horiz_check function scans the grid down-up, left to right for four consecutive, same color chips, left to right
            def horiz_check(additional, vertical):
                #The "additional" parameter shifts the four chips that the algorithm is looking at to the right, and the "vertical" parameter shifts the four chips the algorithm is looking at towards the top of the grid. 
                #The if-else statement splices the output of the get_grid() function to the four rows the algorithm needs to look at, based off of the "additional" parameter
                if additional == 0:
                    check = get_grid()[0:4]
                elif additional == 1:
                    check = get_grid()[1:5]
                elif additional == 2:
                    check = get_grid()[2:6]
                elif additional == 3:
                    check = get_grid()[3:7]

                #The conditional in line 164 first checks to make sure that the "chips" that its evaluating aren't blank, and then compares them all to make sure they are the same. If they are, the function returns true.
                if ((check[0][vertical] == yellow) or (check[0][vertical] == red)) and ((check[0][vertical] == check[1][vertical]) and (check[1][vertical] == check[2][vertical]) and (check[2][vertical] == check[3][vertical])):
                    return True
            
            #The first loop is to scan across all the rows, and the second loop is to scan up the selected rows, using the horiz_check() function to check for winning conditions. If the algorithm detects a win, then it informs the player, and updates the stats in the same way as previously shown
            for additional in range(4):
                for vertical in range(1, 7):
                    if horiz_check(additional, vertical) and player_turn == 1:
                        text = (f'{player1} Wins!')
                        update_stats("win")
                        return True
                    elif horiz_check(additional, vertical) and player_turn == 0:
                        text = (f'{player2} Wins!')
                        update_stats("lose")
                        return True

            #The diag_ur_checking() function checks for wins diagonally from the bottom of the grid to the top, left to right.
            def diag_ur_checking(additional, vertical):
                #The function creates a "check" list from the outpust of the get_grid() function. The first element in the list starts at the bottom left corner of the area that the algorithm is checking, then progressively moves up and right one space for the folowing elements.
                rows = get_grid()
                check = [rows[additional][vertical], rows[additional + 1][vertical + 1], rows[additional + 2][vertical + 2], rows[additional + 3][vertical + 3]]
                #The conditional in line 185 first checks if the "spots" aren't empty, and then if the current status of all of the spots are the same. If they are, then the algorithm returns true, as it detected a winning condition.
                if ((check[0] == red) or (check[0] == yellow)) and ((check[0] == check[1]) and (check[1] == check[2]) and (check[2] == check[3])):
                    return True
                
            #The first loop moves the selected spots from left to right, and the second loop moves them from the bottom of the grid towards the top. Both the stat updates and the win detection work the same way as before.
            for additional in range(4):
                for vertical in range(1, 4):
                    if diag_ur_checking(additional, vertical) and player_turn == 1:
                        text = (f'{player1} Wins!')
                        update_stats("win")
                        return True
                    elif diag_ur_checking(additional, vertical) and player_turn == 0:
                        text = (f'{player2} Wins!')
                        update_stats("lose")
                        return True

            #The diag_ul_checking() function checks for four consecutive, same color "chips" in the top to bottom, left to right diagonal direction.
            def diag_ul_checking(additional, horizontal):
                #The logic here is the same as in the diag_ur_checking() function, except the "check" list starts in the top right "chip" and moves down and right one spot on the grid for every element.
                rows = get_grid()
                check = [rows[additional][horizontal + 3], rows[additional + 1][horizontal + 2], rows[additional + 2][horizontal + 1], rows[additional + 3][horizontal]]
                if ((check[0] == red) or (check[0] == yellow)) and ((check[0] == check[1]) and (check[1] == check[2]) and (check[2] == check[3])):
                    return True
                
            #The algorithm here works in the same manner as the algorithm for the diag_ur_checking() function.
            for additional in range(4):
                for vertical in range(1, 4):
                    if diag_ul_checking(additional, vertical) and player_turn == 1:
                        text = (f'{player1} Wins!')
                        update_stats("win")
                        return True
                    elif diag_ul_checking(additional, vertical) and player_turn == 0:
                        text = (f'{player2} Wins!')
                        update_stats("lose")
                        return True

    #The "running" variable is used to end the loop and close the program if the user tries to exit the application.
    running = True
    #The win variable is used to update the screen one final time before the program ends to display the results of the game.
    win = False
    while running:
        #If a win is detected, the bottom message will update, and the window will freeze for 5 seconds to allow the user to see how they won or lost the match.
        if win:
            #Messege is the text rendered using pygame. Message_rect is a rectangle created by pygame around the text. The message_rect is centered at the middle on the bottom of the screen. screen.blit overlays the rectangle onto the surface where the rest of the game is, allowing the user to see the message. pygame.display.flip() updates the screen.
            message = font.render(text, True, (255, 255, 255), (0, 0, 0))
            message_rect = message.get_rect()
            message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
            screen.blit(message, message_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            break
        pygame.display.flip()

        screen.fill(blank) #Sets the background to black

        #Lines 240 through 243 render text the same way as previously shown.
        message = font.render(text, True, (255, 255, 255), (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
        screen.blit(message, message_rect)

        #The loop checks for any events that pygame detects. Events are any key press, mouse movement, or mouse press.
        for event in pygame.event.get():
            #If the user tries to exit the game, the conditional on line 248 detects it, and ends the program with the "running" variable.
            if event.type == pygame.QUIT:
                running = False

            #Lines 252 through 258 are used to detect where the mouse was clicked. For every row in the grid, the algorithm checks if the pixel coordinates of the click were within the row's range and calls the moves2() function to try to place a "chip" there.
            counter = 0
            for i in range(7):
                if (event.type == pygame.MOUSEBUTTONUP) and (0 + counter < pygame.mouse.get_pos()[0] < (52 * scaling) + counter):
                    #text = (f"click in row({i}).")
                    moves2(i)
                    #text = (get_grid())
                counter += 50 * scaling

        #Lines 261 through 267 draw the grid using the grid_lines() function
        tracker = 50 * scaling
        for i in range(6):
            pygame.draw.line(*grid_lines(tracker, 0, tracker, max_height))
            pygame.draw.line(*grid_lines(0, tracker, max_width, tracker))
            if i == 5:
                pygame.draw.line(*grid_lines(0, 0, max_width, 0))
            tracker += 50 * scaling
        
        #Lines 270 through 277 draw the "chips" on the grid using the dictionaries at the start of the file and the chip() function
        h_counter = 25 * scaling
        for h in range(7):
            v_counter = max_height - 25 * scaling
            for v in range(1, 7):
                pygame.draw.circle(*chip(h_counter, v_counter, get_grid()[h][v]))
                #text = (f"{h_counter}, {v_counter}")
                v_counter -= 50 * scaling
            h_counter += 50 * scaling
        
        #The conditional in line 280 calls both the draw_check() and the win_check() functions. If either of them return true, the program will update the screen with the game results, and end the game.
        if draw_check() or win_check():
            win = True
    pygame.quit()

#The temp_game() function is called in an infinite loop, so the game resets if the user wants to play again, they don't have to go through the menu again. The loop is inside a function so it can be called from the GraphicalMenu file.
def game():
    while True:
        tempGame()
        #Once the game ends, the program asks the user if they want to play again. If they don't the GraphicalLocal file ends, and the user is returned to the menu.
        if getText("Play Again? (Y/N)", xpos=50, boxHeight=40, boxWidth=205).upper() == "Y":
            continue
        else:
            break