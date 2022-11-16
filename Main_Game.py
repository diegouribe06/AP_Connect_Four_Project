#This import statement is for the local multiplayer version of the game.
from cf_client import game as multiplayerClient
from cf_local import game as localGame
from updated_cf_host import game as multiplayerHost


while True:
    while True:
        game_mode = (input("Local, LAN or Stats? ")).upper()
        if game_mode not in ["LOCAL", "LAN", "STATS"]:
            print("That is an invalid game selection. Please try again.")
        else:
            break
    if  game_mode == "LOCAL":
        local_game = localGame()
    elif game_mode == "LAN":
        mode = (input("Host or Join? ")).upper()
        if mode == "HOST":
            multiplayerHost()
        elif mode == "JOIN":
            multiplayerClient()
    elif game_mode == "STATS":
        with open("stats.txt") as stats:
            print(stats.read())
            #Add the code to add to the stats file to the rest of the files
    if (input("Play a different mode? (Y/N) ")).upper() == "Y":
        continue
    else:
        print("Thank you for playing!")
        break