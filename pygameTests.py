import copy
from time import sleep
import pygame
from update_stats import update_stats

pygame.init()
# Alt + Z turns text wrap on and off. Use this to make the comments easier to read since python does not support multi-line comments.

#IDEA
#Make the circles always there, but black, and get the color values from the moves2 and get_grid functions.
# Chips will be 100 * 100
# Lines are currently 20 thick
player1 = input("Player 1: ")
player2 = input("Player 2:")
player_turn = 0

blank = (0,0,0)
yellow = (255, 255, 0)
red = (255, 0, 0)

row_a = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
row_b = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
row_c = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
row_d = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
row_e = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
row_f = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
row_g = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}

while True:
    scaling = round(float(input("Enter the scale factor. If the game does not need to be up/downscaled enter 1.")))
    if isinstance(scaling, int):
        break
    else:
        print("Please enter a valid number.")
max_height = 300 * scaling
max_width = 350 * scaling

running = True
screen = pygame.display.set_mode([max_width, max_height])

def grid_lines(x1, y1, x2, y2):
    return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

def chip(x, y, color):
    return [screen, color, (x, y), 20 * scaling, 25 * scaling]

def get_grid():
    return [row_a, row_b, row_c, row_d, row_e, row_f, row_g]

def moves2(row):
        global player_turn
        rows = get_grid()
        precheck = copy.deepcopy(rows)

        while True:
            #Code to make sure that the player chose a valid spot to go in
            while True:
                if player_turn == 0:
                    desired_row = row
                elif player_turn == 1:
                    desired_row = row
                if (desired_row == 0) or (desired_row == 1) or (desired_row == 2) or (desired_row == 3) or (desired_row == 4) or (desired_row == 5) or (desired_row == 6):
                    break
                else:
                    print("That is an invalid selection.")
            #End of row check section
            #for row in rows:#This loop is to check in every row
            for spot in rows[desired_row]: #For every spot in the row, the algoritm checks if there is anything but an empty chip already occupying the spot.
                if player_turn == 0 and rows[desired_row][spot] == blank:#If it's player one's turn, the algorithm places an empty chip in the first empty spot
                    rows[desired_row][spot] = yellow
                    break
                elif player_turn == 1 and rows[desired_row][spot] == blank:#If it's player two's turn, it'll place a red chip instead.
                    rows[desired_row][spot] = red
                    break
            
            if list(precheck) != get_grid(): #Bug: when the conditional calls precheck, precheck calls the "get_grid()" function again inside the conditional. When this happens, a condition that is always true occurs, and that breaks the logic that checks for a difference in the grid before a turn was made.

                if player_turn == 0:
                    player_turn = 1
                elif player_turn == 1:
                    player_turn = 0

                break #This if block checks to make sure there was a change in the board. "precheck" was initiallized earlier to check for a change before the move is made.

            #Once the change is detected, it breaks out of the while true loop, to make sure that the same player doesn't get locked making all the moves.
            else:
                print("That row is full. Please choose a different row.")
                break
                #Finally, no matter the turn, if the algorithm reaches the end, it'll ask the player to choose a different row since the chosen one is full.

def draw_check():
        global row_a, row_b, row_c, row_d, row_e, row_f, row_g, blank
        rows = [row_a, row_b, row_c, row_d, row_e, row_f, row_g]
        for row in rows:
            for spot in row:
                if row[spot] == blank:
                    return False
        print("It's a tie!")
        return True

def win_check():
        global player_turn
        #Vertical checking from down up, and left to right
        def update_rows(r = True): #Used to make sure that the rows in the function are accurate.
            rows = [row_a, row_b, row_c, row_d, row_e, row_f, row_g]
            if r == True:
                return rows
            
        def vert_check(row, additional): #Checks the verticals. The "... == yellow" and "...== red" is to make sure that the algorithm isn't set off by the blank pieces.
            if((row[1 + additional] == yellow) or (row[1 + additional] == red)) and (row[1 + additional] == row[2 + additional]) and (row[2 + additional] == row[3 + additional]) and (row[3 + additional] == row[4 + additional]):
                return True
            else:
                return False

        for row in update_rows(): #7 left and right
            for additional in range(3): #2 added for all up and down
                if vert_check(row, additional) and player_turn == 1: #Player turn has to be reversed for this conditional, because a previous function changes it before the program can check for wins.
                    print(f'{player1} Wins!')
                    update_stats("win")
                    return True
                elif vert_check(row, additional) and player_turn == 0:
                    print(f'{player2} Wins!')
                    update_stats("lose")
                    return True
        #End of vertical checking
        #Start of horizontal checking
        def horiz_check(additional, horizontal):
            #Saves the rows that will be checked as "check"
            if additional == 0:
                check = update_rows()[0:4]
            elif additional == 1:
                check = update_rows()[1:5]
            elif additional == 2:
                check = update_rows()[2:6]
            elif additional == 3:
                check = update_rows()[3:7]
            if ((check[0][horizontal] == yellow) or (check[0][horizontal] == red)) and ((check[0][horizontal] == check[1][horizontal]) and (check[1][horizontal] == check[2][horizontal]) and (check[2][horizontal] == check[3][horizontal])):
                return True #This checks to make sure that everything in the check list is the same. Horizantal is used to move the selection band up.
        
        for additional in range(4):
            for horizontal in range(1, 7):
                if horiz_check(additional, horizontal) and player_turn == 1:
                    print(f'{player1} Wins!')
                    update_stats("win")
                    return True
                elif horiz_check(additional, horizontal) and player_turn == 0:
                    print(f'{player2} Wins!')
                    update_stats("lose")
                    return True
        #End of horizontal checking
        #Start of diagonal up,right checking
        def diag_ur_checking(additional, horizontal):
            rows = update_rows()
            check = [rows[additional][horizontal], rows[additional + 1][horizontal + 1], rows[additional + 2][horizontal + 2], rows[additional + 3][horizontal + 3]]
            if ((check[0] == red) or (check[0] == yellow)) and ((check[0] == check[1]) and (check[1] == check[2]) and (check[2] == check[3])):
                return True
        for additional in range(4):
            for horizontal in range(1, 4):
                if diag_ur_checking(additional, horizontal) and player_turn == 1:
                    print(f'{player1} Wins!')
                    update_stats("win")
                    return True
                elif diag_ur_checking(additional, horizontal) and player_turn == 0:
                    print(f'{player2} Wins!')
                    update_stats("lose")
                    return True
        #End of diagonal up,right checking
        #Start of diagonal up left checking
        def diag_ul_checking(additional, horizontal):
            rows = update_rows()
            check = [rows[additional][horizontal + 3], rows[additional + 1][horizontal + 2], rows[additional + 2][horizontal + 1], rows[additional + 3][horizontal]]
            if ((check[0] == red) or (check[0] == yellow)) and ((check[0] == check[1]) and (check[1] == check[2]) and (check[2] == check[3])):
                return True
        for additional in range(4):
            for horizontal in range(1, 4):
                if diag_ul_checking(additional, horizontal) and player_turn == 1:
                    print(f'{player1} Wins!')
                    update_stats("win")
                    return True
                elif diag_ul_checking(additional, horizontal) and player_turn == 0:
                    print(f'{player2} Wins!')
                    update_stats("lose")
                    return True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        counter = 0
        for i in range(7):
            if (event.type == pygame.MOUSEBUTTONUP) and (0 + counter < pygame.mouse.get_pos()[0] < (52 * scaling) + counter):
                #print(f"click in row({i}).")
                moves2(i)
                #print(get_grid())
            counter += 50 * scaling

    screen.fill((0,0,0)) #Sets the background


    tracker = 50 * scaling
    for i in range(6):
        pygame.draw.line(*grid_lines(tracker, 0, tracker, max_height))
        pygame.draw.line(*grid_lines(0, tracker, max_width, tracker))
        if i == 5:
            pygame.draw.line(*grid_lines(0, 0, max_width, 0))
        tracker += 50 * scaling

    grid = get_grid()
    
    h_counter = 25 * scaling
    for h in range(7):
        v_counter = max_height - 25 * scaling
        for v in range(1, 7):
            pygame.draw.circle(*chip(h_counter, v_counter, grid[h][v]))
            #print(f"{h_counter}, {v_counter}")
            v_counter -= 50 * scaling
        h_counter += 50 * scaling

    pygame.display.flip()
    
    if draw_check() or win_check():
        running = False
        break
sleep(5)
pygame.quit()