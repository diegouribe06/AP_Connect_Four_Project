import pygame
pygame.init()
#IDEA
#Make the circles always there, but black, and get the color values from the moves2 and get_grid functions.
# Chips will be 100 * 100
# Lines are currently 20 thick

running = True

def grid_lines(x1, y1, x2, y2):
    return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

def chip(x, y, color):
    if color == "red":
        return [screen, (255, 0, 0), (x, y), 25, 25]
    elif color == "yellow":
        return [screen, (255, 0, 0), (x, y), 25, 25]
    elif color == "black":
        return [screen, (0, 0, 0), (x,y), 25, 25]

player_turn = 0

def get_grid():
    return [row_a, row_b, row_c, row_d, row_e, row_f, row_g]

def moves2(row):
        global player_turn
        rows = {0:row_a, 1:row_b, 2:row_c, 3:row_d, 4:row_e, 5:row_f, 6:row_g}
        precheck = get_grid
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
            
            if precheck != get_grid():
                break #This if block checks to make sure there was a change in the board. "precheck" was initiallized earlier to check for a change before the move is made.
            #Once the change is detected, it breaks out of the while true loop, to make sure that the same player doesn't get locked making all the moves.
            else:
                print("That row is full. Please choose a different row.")
                #Finally, no matter the turn, if the algorithm reaches the end, it'll ask the player to choose a different row since the chosen one is full.

        if player_turn == 0:
            player_turn = 1
        elif player_turn == 1:
            player_turn = 0

blank = None
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
    scaling = float(input("Enter the scale factor. If the game does not need to be up/downscaled enter 1."))
    if isinstance(scaling, float):
        break
    else:
        print("Please enter a valid number.")

max_height = 300 * scaling
max_width = 350 * scaling

screen = pygame.display.set_mode([max_width, max_height])

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        counter = 0
        for i in range(7):
            if (event.type == pygame.MOUSEBUTTONUP) and (0 + counter < pygame.mouse.get_pos()[0] < (52 * scaling) + counter):
                print(f"click in row({i}).")
                moves2(i)
                print(get_grid())
            counter += 50 * scaling

    screen.fill((0,0,0)) #Sets the background

    tracker = 50 * scaling
    for i in range(6):
        pygame.draw.line(*grid_lines(tracker, 0, tracker, max_height))
        pygame.draw.line(*grid_lines(0, tracker, max_width, tracker))
        if i == 5:
            pygame.draw.line(*grid_lines(0, 0, max_width, 0))
        tracker += 50 * scaling
    spacing = 50 * scaling
    pygame.draw.circle(*chip((1/2) * spacing, max_height - (1/2) * spacing, "red"))
    pygame.display.flip()
    
pygame.quit()