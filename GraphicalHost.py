#More in detail explanations for algorithms can be found in GraphicalLocal as they work the same way here. The only difference is that code for socket functionality is added here. 

#Lines 4 through 6 import libraries not made by me.
import copy
import pygame
import socket
#Lines 8 and 9 import custom functions from a seperate file that I created.
from update_stats import update_stats
from update_stats import getText

#Same as before, the game is in a function so it can be placed in a loop for instat replayability.
def tempGame():
    player1 = getText("Player 1:")

    #Same code to get the scale factor from the user
    while True:
        try:
            scaling = round(float(getText("Scale: ", (0, 0, 255))))
            break
        except:
            pass

    #Lines 24 through 38 get the computer's LAN ip address. This is used so the client can connect to it.
    #Line 25 creates a "dummy" socket. The computer's IP address will be read from the logs of the socket.
    temp_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #Line 27 sets socket's timeout to 0, so the computer doesn't waste resources actually trying to connect to an IP address that won't be used.
    socket.setdefaulttimeout(0)
    #In lines 29 through 31, the socket attempts to connect to the fake IP. If there's a connection available, temp_ip2 will be set to the IP of the socket name of the IPs used, which will be the computer's LAN IP.
    try:
        temp_ip.connect(('1.2.3.4', 1))
        temp_ip2 = temp_ip.getsockname()[0]
    #If no connection is availabe, lines 33 and 34 will default the IP to localhost
    except Exception:
        temp_ip2 = "127.0.0.1"
    #If there was a connection available, the socket will close, and set the host IP to the computer's LAN IP in lines 36 through 39.
    finally:
        temp_ip.close()
        host_ip = temp_ip2

    #Line 41 sets the timeout back to None, so the socket doesn't close when the player attempts to use it.
    socket.setdefaulttimeout(None)

    #Line 44 initializes the host variable as a socket
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Line 47 displays the IP to the user, so they can give it to the second player ot connect.
    getText(f"IP: {host_ip}", xpos=50, boxWidth=200)

    #Lines 50 through _ are in an infinite loop to insure that a valid, unused port is chosen.
    while True:
        #Lines 52 through _ are in an infinite loop to insure that a port in the correct range is chosen.
        while True:
            #Line 55 will try to get a port number from the user.
            try:
                port = int(getText("Port?"))
            #If the user does not enter a number for the port, the program will prompt them to enter a valid number in line 58
            except:
                getText("Invalid Port")

            #If the user entered a number for the port, the program will then check if the port is within the valid range in line 61.
            if port > 1024 and port < 65536:
                #If the port is valid, the program will exit the first loop and continue (Line 63)
                break
            else:
                #If the user did not enter a port in the valid range, the program will prompt them to try again (Line 66)
                getText("Invalid Port")

        #In lines 69 through 73, the program will attempt to create a socket on the specified port.
        try:
            #If the port is successfully created, the program wil exit the infinite loop (Lines 71 and 72)
            host.bind((host_ip, port))
            break
        except:
            #If the port could not be created, that means that the port the user chose is currently in use by a different program. The program will then tell the user to choose a different port. (Line 75)
            getText("Invalid Port")

    #In lines 78 through 80, the server will listen for incoming connections. When a connection is found, the program will tell the user that the server was able to connect.
    host.listen()
    connection, address = host.accept()
    getText("Connected!", xpos=85, boxWidth=130)

    #The program will send the user's name to the client in line 83
    connection.sendall(bytes(player1, "utf-8"))
    #In lines 85 and 86, the program will wait for the client program to send a name back, and decode the information.
    player2 = connection.recv(1024)
    player2 = player2.decode("utf-8")
    #Line 88 will tell the user who they're playing against
    getText(f"Playing against: {player2}", xpos=20, boxWidth=260)

    #Same as in GraphicalLocal, lines 91 through 113 set the player's turn, the colors, the grid, the screen size, and the font to be used
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

    #Because the functions in lines 116 through 122 are within another function, they cannot be imported. Instead the functions are recreated and work the same as the functions of the same name found in GraphicalLocal.
    def grid_lines(x1, y1, x2, y2):
        return [screen, (0,0,255), (x1, y1), (x2, y2), 5]

    def chip(x, y, color):
        return [screen, color, (x, y), 20 * scaling, 25 * scaling]

    def get_grid():
        return [row_a, row_b, row_c, row_d, row_e, row_f, row_g]

    #The function moves2 works almost the same as the one in GraphicalLocal. The algorithms are almost the same, withchanges only being made to work in a client-server manner.
    def moves2(row):
            nonlocal player_turn
            nonlocal text
            nonlocal red
            nonlocal yellow
            nonlocal blank
            rows = get_grid()
            precheck = copy.deepcopy(rows)

            #Lines 136 through _ are in an infinite loop to make sure that a valid spot is chosen
            while True:
                #If it is player one's turn, the program will let the user choose a spot to go in (Lines 139 and 140) and then send that information to player two (Line 141)
                if player_turn == 0:
                    text = f'{player2}\'s turn'
                    desired_row = row
                    connection.sendall(bytes(str(desired_row), "utf-8"))
                elif player_turn == 1:
                    #If it's player two's turn, the progtam will not allow player one to make a move.
                    text = f'{player1}\'s turn'
                    desired_row = row

                #The loop in line 148 will loop through the row that the user chose.
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
                
                #The turn logic in lines 160 through 167 works the same as the logic found in GraphicalLocal.
                if list(precheck) != get_grid(): 

                    if player_turn == 0:
                        player_turn = 1
                    elif player_turn == 1:
                        player_turn = 0
                    break 
                #Once the change is detected, it breaks out of the while true loop, to make sure that the same player doesn't get locked making all the moves.
                else:
                    text = "Invalid Choice"
                    break
                    #Finally, no matter the turn, if the algorithm reaches the end, it'll ask the player to choose a different row since the chosen one is full.

    #The draw_check function works the same way as the one found in GraphicalLocal.
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
    #Win check the same way as the one in GraphicalLocal
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

    #The win variable is used to update the screen one final time after one of the players wins.
    win = False

    while running:
        if win:
            #Like in GraphicalLocal, when someone wins, the screen will be updated one last time to display the results.
            message = font.render(text, True, (255, 255, 255), (0, 0, 0))
            message_rect = message.get_rect()
            message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
            screen.blit(message, message_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            break
        pygame.display.flip()

        screen.fill((0,0,0)) #Sets the background

        #Lines 282 through 285 display text on the bottom bar of the game. 
        message = font.render(text, True, (255, 255, 255), (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.center = (((max_width / 2)), (max_height + 25 * scaling))
        screen.blit(message, message_rect)

        #If it's player one's turn, the program will monitor for any events
        if player_turn == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                #The loop in lines 295 through 298 work the same way as the one found in GraphicalLocal. The user's move is sent to the client inside the moves2 function.
                counter = 0
                for i in range(7):
                    if (event.type == pygame.MOUSEBUTTONUP) and (0 + counter < pygame.mouse.get_pos()[0] < (52 * scaling) + counter):
                        moves2(i)
                    counter += 50 * scaling
        #If it;s player two's turn, the program will wait for the move to be sent from the client
        elif player_turn == 1:
            moves2(int((connection.recv(1024)).decode("utf-8")))

        #Lines 304 through 321 draw the board the in the same way as GraphicalLocal does.
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

        #The conditional to check for wins works the same way as it does in GraphicalLocal. The addition in line 326 closes the server, to conserve resournces.
        if draw_check() or win_check():
            win = True
            connection.close()

    #When the game is over, line 329 closes the graphics module to preserve resources.
    pygame.quit()

#Like in GraphicalLocal, the tempGame function is called inside a different function, so it can be placed inside a loop for instant replayability.
def game():
    import pygame
    while True:
        tempGame()
        if getText("Play Again? (Y/N)", xpos=50, boxHeight=40, boxWidth=205).upper() == "Y":
            continue
        else:
            break