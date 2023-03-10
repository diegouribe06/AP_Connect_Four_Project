import copy
import pygame
from update_stats import update_stats
import socket

# Alt + Z turns text wrap on and off. Use this to make the comments easier to read since python does not support multi-line comments.

#player1 = ''
#player2 = ''
#scaling = ''
def tempGame():
    def getText(message = "", color = (255,0,0)):
        pygame.init()
        text_screen = pygame.display.set_mode([300, 300])
        font = pygame.font.SysFont("comic_sans_ms", 25)
        text = ""
        text_bar = pygame.Rect(0, 250, 300, 100)
        message_bar = pygame.Rect(100, 50, 100, 25)
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
            text_screen.blit(message_surface, (100, 50))
            
            pygame.display.flip()

    socket.setdefaulttimeout(45000)

    player2 = getText("Player 2:")

    #Scaling
    while True:
        try:
            scaling = round(float(getText("Scale: ", (0, 0, 255))))
            break
        except:
            text = ("Please enter a valid number.")


    while True:
        host_ip = getText("What is the host IP?")
        host_port = int(getText("What is the host port?"))
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print("...Connecting...")
        try:
            client.connect((host_ip, host_port))
            getText("Connected Successfully!")
            break
        except:
            getText("Host took too long to respond. Please check the IP and Port and try again.")


    socket.setdefaulttimeout(None)
    #Initializing the server
    player1 = client.recv(1024)
    player1 = player1.decode()
    getText(f"Playing against: {player1}")
    client.sendall(bytes(player2, "utf-8"))

    player_turn = 0
    text = f"{player1}'s Turn"


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


    max_height = 300 * scaling
    max_width = 350 * scaling
    pygame.init()
    font = pygame.font.SysFont("comic_sans_ms", 25 * scaling)

    running = True
    screen = pygame.display.set_mode([max_width, max_height + 50 * scaling])

    def grid_lines(x1, y1, x2, y2):
        return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

    def chip(x, y, color):
        return [screen, color, (x, y), 20 * scaling, 25 * scaling]

    def get_grid():
        return [row_a, row_b, row_c, row_d, row_e, row_f, row_g]

    def moves2(row):
            global player_turn
            global text
            global red
            global yellow
            global blank
            rows = get_grid()
            precheck = copy.deepcopy(rows)

            while True:
                #Code to make sure that the player chose a valid spot to go in
                while True:
                    if player_turn == 0:
                        text = f"{player2}'s turn"
                        desired_row = row
                    elif player_turn == 1:
                        text = f"{player1}'s turn"
                        desired_row = row
                        client.sendall(bytes(str(desired_row), "utf-8"))
                    if (desired_row == 0) or (desired_row == 1) or (desired_row == 2) or (desired_row == 3) or (desired_row == 4) or (desired_row == 5) or (desired_row == 6):
                        break
                    else:
                        text = ("Invalid Choice")
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
                    text = "Invalid Choice"
                    break
                    #Finally, no matter the turn, if the algorithm reaches the end, it'll ask the player to choose a different row since the chosen one is full.

    def draw_check():
            global row_a, row_b, row_c, row_d, row_e, row_f, row_g, blank
            global text
            rows = [row_a, row_b, row_c, row_d, row_e, row_f, row_g]
            for row in rows:
                for spot in row:
                    if row[spot] == blank:
                        return False
            text = "   It's a tie!    "
            return True

    def win_check():
            global player_turn
            global text
            global yellow
            global red
            global blank

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
                        text = f'{player1} Wins!'
                        update_stats("win")
                        return True
                    elif vert_check(row, additional) and player_turn == 0:
                        text = f'{player2} Wins!'
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
                        text = (f'{player1} Wins!')
                        update_stats("win")
                        return True
                    elif horiz_check(additional, horizontal) and player_turn == 0:
                        text = (f'{player2} Wins!')
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
                        text = (f'{player1} Wins!')
                        update_stats("win")
                        return True
                    elif diag_ur_checking(additional, horizontal) and player_turn == 0:
                        text = (f'{player2} Wins!')
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
                        text = (f'{player1} Wins!')
                        update_stats("win")
                        return True
                    elif diag_ul_checking(additional, horizontal) and player_turn == 0:
                        text = (f'{player2} Wins!')
                        update_stats("lose")
                        return True

    win = False

    while running:
        if win:
            message = font.render(text, True, (255, 255, 255), (0, 0, 0))
            message_rect = message.get_rect()
            message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
            screen.blit(message, message_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            break
        pygame.display.flip()

        screen.fill((0,0,0)) #Sets the background

        message = font.render(text, True, (255, 255, 255), (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
        screen.blit(message, message_rect)
        
        if player_turn == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                counter = 0
                for i in range(7):
                    if (event.type == pygame.MOUSEBUTTONUP) and (0 + counter < pygame.mouse.get_pos()[0] < (52 * scaling) + counter):
                        #text = (f"click in row({i}).")
                        moves2(i)
                        #text = (get_grid())
                    counter += 50 * scaling
        elif player_turn == 0:
            moves2(int((client.recv(1024)).decode("utf-8")))




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
                #text = (f"{h_counter}, {v_counter}")
                v_counter -= 50 * scaling
            h_counter += 50 * scaling
        



        if draw_check() or win_check():
            win = True
            client.close()
    pygame.quit()

def game():
    import pygame
    from GraphicalMenu import getText
    while True:
        tempGame()
        if getText("Play Again? (Y/N)", xpos=50, boxHeight=40, boxWidth=205).upper() == "Y":
            continue
        else:
            break

if __name__ == "__GraphicalClient__":
        game()