from lib import *

# Game loop
while True:
    for event in pygame.event.get():
        action_quit(event)
        switch_state(event)
        next_card(event)

    game.screen.fill(colors.bg)

    if game.state is "pick_mode":
        draw_menu(game.screen)
    elif game.state is "card_back":
        draw_card_back(game.screen)
    elif game.state is "view_card":
        draw_card(game.screen, game.card)

    next_frame()

