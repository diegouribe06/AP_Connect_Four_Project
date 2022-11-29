from update_stats import update_stats


def temp_game():
    import socket

    player1 = input("What is your name? ")
    #This socket is used to get the host's ip address
    temp_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.setdefaulttimeout(0)
    try:
        temp_ip.connect(('1.2.3.4', 1))
        temp_ip2 = temp_ip.getsockname()[0]
    except Exception:
        temp_ip2 = "127.0.0.1"
    finally:
        temp_ip.close()
        host_ip = temp_ip2
    socket.setdefaulttimeout(None)
    #Initializing the server
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Give this IP to the other player: {host_ip}")
    while True:
        while True:
            port = int(input("Choose a port: (Number between 1024 and 65536) "))
            if port > 1024 and port < 65536:
                break
            else:
                print("Please select a valid port number.")
        try:
            host.bind((host_ip, port))
            break
        except:
            print("The port is currently in use. Please select another port.")
            
    print("...Connecting...")
    host.listen()
    connection, address = host.accept()
    print("Connected Successfully!")
    #Host initialized
    connection.sendall(bytes(player1, "utf-8"))
    player2 = connection.recv(1024)
    player2 = player2.decode("utf-8")
    print(f"Playing against {player2}")

    #Defining the board
    blank = "\033[1;37;40mO\033[1;34;40m"
    yellow = "\033[1;33;40mO\033[1;34;40m"
    red = "\033[1;31;40mO\033[1;34;40m"
    row_a = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_b = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_c = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_d = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_e = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_f = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}
    row_g = {1:blank, 2:blank, 3:blank, 4:blank, 5:blank, 6:blank}

    player_turn = 0 #Used to determine turn

    #This function is used to update the board
    def print_board(row_a = row_a, row_b = row_b, row_c = row_c, row_d = row_d, row_e = row_e, row_f = row_f, row_g = row_g, draw = True):
            #The "draw" variable is used to make sure the grid doesn't print multiple times.
            board = '''
            \033[1;34;40m|A|B|C|D|E|F|G|
            |{a6}|{b6}|{c6}|{d6}|{e6}|{f6}|{g6}|
            ---------------
            |{a5}|{b5}|{c5}|{d5}|{e5}|{f5}|{g5}|
            ---------------
            |{a4}|{b4}|{c4}|{d4}|{e4}|{f4}|{g4}|
            ---------------
            |{a3}|{b3}|{c3}|{d3}|{e3}|{f3}|{g3}|
            ---------------
            |{a2}|{b2}|{c2}|{d2}|{e2}|{f2}|{g2}|
            ---------------
            |{a1}|{b1}|{c1}|{d1}|{e1}|{f1}|{g1}|
            ---------------
            '''.format(a1 = row_a[1], a2 = row_a[2],a3 = row_a[3],a4 = row_a[4],a5 = row_a[5],a6 = row_a[6], b1 = row_b[1],b2 = row_b[2],b3 = row_b[3],b4 = row_b[4],b5 = row_b[5],b6 = row_b[6], c1 = row_c[1],c2 = row_c[2],c3 = row_c[3],c4 = row_c[4],c5 = row_c[5],c6 = row_c[6], d1 = row_d[1],d2 = row_d[2],d3 = row_d[3],d4 = row_d[4],d5 = row_d[5],d6 = row_d[6], e1 = row_e[1],e2 = row_e[2],e3 = row_e[3],e4 = row_e[4],e5 = row_e[5],e6 = row_e[6], f1 = row_f[1],f2 = row_f[2],f3 = row_f[3],f4 = row_f[4],f5 = row_f[5],f6 = row_f[6], g1 = row_g[1],g2 = row_g[2],g3 = row_g[3],g4 = row_g[4],g5 = row_g[5],g6 = row_g[6])
            if draw == True: #When "draw" is set to false, the function won't print the grid. This is important for the move check in the "moves()" function.
                print(board)
            return board

    def moves2():
            nonlocal player_turn
            nonlocal yellow
            nonlocal red
            nonlocal blank
            rows = {"A":row_a, "B":row_b, "C":row_c, "D":row_d, "E":row_e, "F":row_f, "G":row_g}
            precheck = print_board(draw = False)
            while True:
                #Code to make sure that the player chose a valid spot to go in
                while True:
                    if player_turn == 0:
                        desired_row = (input(f"Which row does the {player1} want to go in?")).upper()
                        connection.sendall(bytes(desired_row, "utf-8"))
                    elif player_turn == 1:
                        print(f"It's {player2}'s turn.")
                        desired_row = (connection.recv(1024)).decode("utf-8")
                        if len(desired_row) == 0: return True
                    if (desired_row == "A") or (desired_row == "B") or (desired_row == "C") or (desired_row == "D") or (desired_row == "E") or (desired_row == "F") or (desired_row == "G"):
                        break
                    else:
                        if player_turn == 0:
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
                
                if precheck != print_board(draw = False):
                    break #This if block checks to make sure there was a change in the board. "precheck" was initiallized earlier to check for a change before the move is made.
                #Once the change is detected, it breaks out of the while true loop, to make sure that the same player doesn't get locked making all the moves.
                else:
                    if player_turn == 0:
                        print("That row is full. Please choose a different row.")
                    #Finally, no matter the turn, if the algorithm reaches the end, it'll ask the player to choose a different row since the chosen one is full.

            if player_turn == 0:
                player_turn = 1
            elif player_turn == 1:
                player_turn = 0
        #This function is the origional algorithm that places the players markers.

    def win_check():
            nonlocal yellow, red, blank, player_turn
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
            #End of diagonal up left checking

    def draw_check():
        nonlocal blank
        rows = [row_a, row_b, row_c, row_d, row_e, row_f, row_g]
        for row in rows:
            for spot in row:
                if row[spot] == blank:
                    return False
        print("It's a tie!")
        return True
        
    while True:
        print_board()
        if win_check() or draw_check():
            host.close()
            break
        if moves2(): 
            print(f"{player2} disconnected.")
            break

def game():
    while True:
        temp_game()
        if ((input("Play Again? (Y/N) ")).upper()) == "Y":
            continue
        else:
            break
if __name__ == "__updated_cf_host__":
    game()