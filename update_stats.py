#Line one imports pygame, a graphics library not made by me.
import pygame

#This file contains functions used by multiple files.

#Update stats is used to update the stats.txt file
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

#getText is used to get a text input from the user, or to display a message.
def getText(message = "", color = (255,0,0), xpos = 100, boxWidth = 100, boxHeight = 25):
    pygame.init()
    text_screen = pygame.display.set_mode([300, 300])
    font = pygame.font.SysFont("comic_sans_ms", 25)
    text = ""
    text_bar = pygame.Rect(0, 250, 300, 100)
    message_bar = pygame.Rect(xpos, 50, boxWidth, boxHeight)
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
        text_screen.blit(message_surface, (xpos, 50))
        
        pygame.display.flip()

def show_stats():
    if __name__ == "update_stats":
        with open("stats.txt", "r") as stats:
            stats = stats.read().split("\n")
            getText(f"{stats[0][0]} wins, {stats[1][0]} losses", xpos=60, boxWidth=180, boxHeight=40)