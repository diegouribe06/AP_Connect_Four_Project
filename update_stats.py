def update_stats(check, debug = False):
    if check == "win":
        with open("stats.txt") as stats:
            current_stats = stats.read()

        current_stats = current_stats.split("\n")
        if debug: print(current_stats)
        current_stats[0] = f"{int(current_stats[0][0]) + 1} wins"
    elif check == "lose":
        with open("stats.txt") as stats:
            current_stats = stats.read()

        if debug: print(current_stats)
        current_stats = current_stats.split("\n")
        current_stats[-1] = f"{int(current_stats[1][0]) + 1} losses"
    rewrite = f"{current_stats[0]}\n{current_stats[-1]}"
    with open("stats.txt", "w") as stats:
        stats.write(rewrite)

    if debug:
        with open("stats.txt", "w") as stats:
            reset = "0 wins\n0losses"
            stats.write(reset)