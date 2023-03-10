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
