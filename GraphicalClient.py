#Lines 2 through 4 import modules not made by me
import copy
import pygame
import socket
#Lines 6 and 7 import custom function from update_stats.
from update_stats import update_stats
from update_stats import getText
#More detailed explanations for algorithms are in GraphicalLocal, as they work the same way here. The diferences are to allow the game to work in a server-client model

def tempGame():
    #Line 12 sets the default socket timeout to 45 seconds, so if the user makes a mistake when entering the IP or port, the program will let them try again.
    socket.setdefaulttimeout(45000)

    #line 15 gets the user's name
    player2 = getText("Player 2:")

    #Lines 18 through 23 get a scale factor like in GraphicalLocal
    while True:
        try:
            scaling = round(float(getText("Scale: ", (0, 0, 255))))
            break
        except:
            text = ("Please enter a valid number.")

    #Line 26 initializes the client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Lines 29 through 47 are in an infinite loop to make sure that the client successfully connects to a game/.
    while True:
        #Line 31 gets the client IP from the user. The IP is generated in the host game.
        host_ip = getText("What is the host IP?")
        #Lines 33 through 38 try to get the client port number from the user. The lines are in an infinite loop to make sure that a valid port is entered.
        while True:
            try:
                host_port = int(getText("What is the host port?"))
                break
            except:
                getText("Invalid Port")
        #Lines 40 through 47 attempt to connect to the IP and port given to the program.
        try:
            #If the client successfully connects, the program exits the loop and continues with the game.
            client.connect((host_ip, host_port))
            getText("Connected Successfully!")
            break
        except:
            #If the client can't connect in 45 seconds, the program will prompt the user to re-enter the IP and port to try again.
            getText("Host took too long to respond. Please check the IP and Port and try again.")

    #Line 50 resets the server timeout to None, so the game doesn't close due to inactivity.
    socket.setdefaulttimeout(None)

    #Lines 53 and 54 recieve and decode the opponents name.
    player1 = client.recv(1024)
    player1 = player1.decode()
    getText(f"Playing against: {player1}")
    #Line 57 sends the user's name to the opponent.
    client.sendall(bytes(player2, "utf-8"))

    #Lines 60 through 83 create the grid, colors, player turn, and font in the same way as GraphicalLocal.
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

    #The functions in lines 86 through 93 work the same way as the functions of the same name in GraphicalLocal.
    def grid_lines(x1, y1, x2, y2):
        return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

    def chip(x, y, color):
        return [screen, color, (x, y), 20 * scaling, 25 * scaling]

    def get_grid():
        return [row_a, row_b, row_c, row_d, row_e, row_f, row_g]

    #The algorithms for moves2 work the same way as the ones in GraphicalLocal. A couple of lines have been added to work with the server-client model
    def moves2(row):
            nonlocal player_turn
            nonlocal text
            nonlocal red
            nonlocal yellow
            nonlocal blank
            rows = get_grid()
            precheck = copy.deepcopy(rows)

            while True:
                while True:
                    #If it's player one's turn, the program does not allow the user to make a move, as it is not their turn
                    if player_turn == 0:
                        text = f"{player2}'s turn"
                        desired_row = row
                    #If it's player two's turn, the game allows the player to make a move, and then sends the move to the host (Line 115)
                    elif player_turn == 1:
                        text = f"{player1}'s turn"
                        desired_row = row
                        client.sendall(bytes(str(desired_row), "utf-8"))
                    if (desired_row == 0) or (desired_row == 1) or (desired_row == 2) or (desired_row == 3) or (desired_row == 4) or (desired_row == 5) or (desired_row == 6):
                        break
                    else:
                        text = ("Invalid Choice")
                
                for spot in rows[desired_row]: 
                    #For every spot in the row, the algoritm checks if there is anything but an empty chip already occupying the spot.
                    if player_turn == 0 and rows[desired_row][spot] == blank:
                        #If it's player one's turn, the algorithm places an empty chip in the first empty spot
                        rows[desired_row][spot] = yellow
                        break
                    elif player_turn == 1 and rows[desired_row][spot] == blank:
                        #If it's player two's turn, it'll place a red chip instead.
                        rows[desired_row][spot] = red
                        break
                
                if list(precheck) != get_grid():

                    if player_turn == 0:
                        player_turn = 1
                    elif player_turn == 1:
                        player_turn = 0

                    break 
                else:
                    text = "Invalid Choice"
                    break
                    #Finally, no matter the turn, if the algorithm reaches the end, it'll ask the player to choose a different row since the chosen one is full.
    #The draw_check and win_check functions work the same way as the functions found in GraphicalLocal
    def draw_check():
            nonlocal row_a, row_b, row_c, row_d, row_e, row_f, row_g, blank
            nonlocal text
            rows = [row_a, row_b, row_c, row_d, row_e, row_f, row_g]
            for row in rows:
                for spot in row:
                    if row[spot] == blank:
                        return False
            text = "   It's a tie!    "
            return True

    def win_check():
            nonlocal player_turn
            nonlocal text
            nonlocal yellow
            nonlocal red
            nonlocal blank

            def vert_check(row, additional):
                if((row[1 + additional] == yellow) or (row[1 + additional] == red)) and (row[1 + additional] == row[2 + additional]) and (row[2 + additional] == row[3 + additional]) and (row[3 + additional] == row[4 + additional]):
                    return True
                else:
                    return False

            for row in get_grid():
                for additional in range(3):
                    if vert_check(row, additional) and player_turn == 1:
                        text = f'{player1} Wins!'
                        update_stats("win")
                        return True
                    elif vert_check(row, additional) and player_turn == 0:
                        text = f'{player2} Wins!'
                        update_stats("lose")
                        return True

            def horiz_check(additional, horizontal):
                if additional == 0:
                    check = get_grid()[0:4]
                elif additional == 1:
                    check = get_grid()[1:5]
                elif additional == 2:
                    check = get_grid()[2:6]
                elif additional == 3:
                    check = get_grid()[3:7]
                if ((check[0][horizontal] == yellow) or (check[0][horizontal] == red)) and ((check[0][horizontal] == check[1][horizontal]) and (check[1][horizontal] == check[2][horizontal]) and (check[2][horizontal] == check[3][horizontal])):
                    return True
            
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

            def diag_ur_checking(additional, horizontal):
                rows = get_grid()
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

            def diag_ul_checking(additional, horizontal):
                rows = get_grid()
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
    
    #The win variable is used to update the screen a final time after a player wins.
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

        #Lines 252 through 255 set the text in the bottom bar
        message = font.render(text, True, (255, 255, 255), (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
        screen.blit(message, message_rect)
        
        #If it's player two's turn, the program will allow the user to make a move, and then send it to the host in moves2
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
        #If it's player one's turn, the program will not allow the user to make a move, as it is not their turn. The program will also wait for the host program to send its move (Line 272)
        elif player_turn == 0:
            moves2(int((client.recv(1024)).decode("utf-8")))

        #Lines 275 through 292 draw the grid the same way as in GraphicalLocal.
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
        
        #The conditional to detect wins or draws also works the same way as the one in GraphicalLocal. The additional line (Line 297) closes the socket to preserve resources.
        if draw_check() or win_check():
            win = True
            client.close()
    #Finally, when the game is over, the program closes the graphics module to preserve resources.
    pygame.quit()

#The tempGame function is placed inside a seperate function for instant replayability, like in GraphicalLocal.
def game():
    import pygame
    while True:
        tempGame()
        if getText("Play Again? (Y/N)", xpos=50, boxHeight=40, boxWidth=205).upper() == "Y":
            continue
        else:
            break