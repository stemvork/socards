from lib import *

# All of the relevant assets and requirements are
# imported by importing everything mentioned in lib.

# assets.py defines the fonts and colours.

# dotdict.py allows for convenient dictionary access.
# Note that dictionary access is now colours.red
# rather than colors["red"] (standard dictionary)
# and also not colors[0] (standard list).

# state.py contains the game state object and inital values

# strings.py contains the language-specific strings.
# This will be useful for translating later.

# lib.py is imported by main.py. 
# For now, main.py contains an infinite loop that calls
# to the high-level update and draw functions specified here.

#-------- LOGIC FUNCTIONS

# High-level update function,
# keeps track of actions that respond to inputs.

def update(game):
    for event in pygame.event.get():
        handle_quit(event)
        switch_state(event)
        next_card(event)
        next_menu(event)

#-------- DRAW FUNCTIONS

# High-level draw function,
# delegates to the specific draw functions.

def draw(game):
    game.screen.fill(colors.bg)
    draw_border(game.screen)

    if game.state == "pick_mode":
        draw_menu(game.screen)
    elif game.state == "card_back":
        draw_card_back(game.screen)
    elif game.state == "view_card":
        draw_card(game.screen)

    next_frame()

# Draws a white rectangle as a pretty border.
def draw_border(screen):
    g = 5
    # Draw a rectangle border
    pygame.draw.rect(screen, colors.white, 
            (g, g, maxwidth - 2*g, maxheight - 2*g), 1)

# Draws the large "So"
def draw_title(screen):
    title_text = sans.render("So", True, colors.white)
    title_rect_position = (maxwidth//2, maxheight//2 -15)
    screen.blit(title_text, title_text.get_rect(bottomright=title_rect_position))

# Draws the text underneath So...
def draw_subtitle(screen):
    first_text = written.render("a collection of questions", True, colors.white)
    first_rect_center = (maxwidth//2, maxheight//2 + 15)
    screen.blit(first_text, first_text.get_rect(center=first_rect_center))

    second_text = written.render("for deeper discussions", True, colors.white)
    second_rect_center = (maxwidth//2, maxheight//2 + 15 +
            written.size("for deeper discussions")[1])
    screen.blit(second_text, second_text.get_rect(center=second_rect_center))

# Draws a text-wrapped list of strings to the screen
def draw_multi_line(maxwidth, lines, 
        font=written, color=colors.white, padding=0, center=True):

    linesurfaces = [font.render(line, True, color) for line in lines]
    totalheight = sum([surface.get_size()[1] for surface in linesurfaces])

    textsurface = pygame.Surface((maxwidth, totalheight))
    textsurface.set_colorkey(colors.black)
    textsurface_center = textsurface.get_rect().center

    next_height = 0
    for line in linesurfaces:
        if center:
            line_position = textsurface_center[0], next_height
            textsurface.blit(line, line.get_rect(midtop=line_position))
        else:
            textsurface.blit(line, line.get_rect(top=next_height))
        next_height += line.get_rect().height + padding
    return textsurface

# Draw a string to the screen that fits the screen without wrapping
def draw_single_line(maxwidth, text, 
        font=written, color=colors.white, center=True):

    lineheight = font.size(text)[1]

    textsurface = pygame.Surface((maxwidth, lineheight))
    textsurface.set_colorkey(colors.black)
    textsurface_center = textsurface.get_rect().center
    
    line_img  = font.render(text, True, color)

    if center:
        line_rect = line_img.get_rect(center = textsurface_center)
    else:
        line_rect = line_img.get_rect()

    textsurface.blit(line_img, line_rect)
    return textsurface

# Draw the menu state, strongly documented
def draw_menu(screen, padding=30):
    # Collect all surfaces that need to be drawn
    textsurfaces = []

    # Iterate over the menu options as specified in assets
    # and add the required surfaces to the textsurfaces list
    for i, option in enumerate(menu_options):
        if i is game.menu_selected: # white and with description
            textsurfaces.append(draw_single_line(maxwidth, option, 
                    font=sans_small, color=colors.white, center=False))

            description = textwrap.wrap(menu_options_desc[i], width=36)
            textsurfaces.append(draw_multi_line(maxwidth, description,
                    font=serif_small, color=colors.white, center=False))

        else: # gray and without description
            textsurfaces.append(draw_single_line(maxwidth, option, 
                    font=sans_small, color=colors.gray, center=False))

    # Calculate the total height of the textsurfaces
    totalheight = sum([surface.get_size()[1] 
        for surface in textsurfaces]) + padding * (len(menu_options) - 1)

    if totalheight > maxheight:
        print("warning: overflows screen drawing", "question")

    # Create a surface to contain then all
    # Make it transparent
    # Calculate the center based on specified padding (function argument)
    textsurface = pygame.Surface((maxwidth, totalheight))
    textsurface.set_colorkey(colors.black)
    textsurface_center = game.center[0] + padding, game.center[1]

    # Keep track of the height (relative to textsurface) that
    # the next surface needs to be drawn at, increment by the
    # height of the drawn surface, with padding for all except
    # the menu item that is followed by a description
    next_height = 0
    for i, surface in enumerate(textsurfaces):
        textsurface.blit(surface, surface.get_rect(top=next_height))
        if i is game.menu_selected:
            next_height += surface.get_rect().height
        else:
            next_height += surface.get_rect().height + padding

    # Draw the entire textsurface that contains all to the screen.
    screen.blit(textsurface, textsurface.get_rect(center=textsurface_center))

# Draw the back of a card
def draw_card_back(screen):
    draw_title(screen)
    draw_subtitle(screen)

    # Draw the coloured dots
    g = 5 # acts like a grid size
    title_center = pygame.Vector2(maxwidth//2, maxheight//2 - 3*g)
    circle_colors = [colors.red, colors.blue, colors.green]
    circle_offsets = [(20, -20), (50, -20), (80, -20)]
    [pygame.draw.circle(screen, color, title_center + offset, 2*g)
            for color, offset in zip(circle_colors, circle_offsets)]

# Draw the current game card
def draw_card(screen):
    lines = textwrap.wrap(game.card, 30)
    textsurface = draw_multi_line(maxwidth, lines)
    screen.blit(textsurface, textsurface.get_rect(center=game.center))

# Shortcut to display the buffer and await next game loop
def next_frame():
    pygame.display.flip()
    game.clock.tick(30)

#------- EVENT HANDLERS

# These are called from the update function
# and respond to user input by updating the game
# state object accordingly.

# Allows to exit using Esc, q and the OS-default way
def handle_quit(event):
    if event.type == pygame.QUIT:
        proper_exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            proper_exit()
        elif event.key == pygame.K_q:
            proper_exit()

# Switch to the next mode with `m` (debugging)
def switch_state(event):
    if event.type == pygame.KEYDOWN:
        if event.key is pygame.K_m:
            game.states.append(game.states.pop(0))
            game.state = game.states[0]

# Press space to show the next card in 
# the view_card mode.
def next_card(event):
    if game.state != "view_card":
        return
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if game.card_selected < len(game.cards) -1:
                game.card_selected += 1
                game.card = game.cards[game.card_selected]
            else:
                game.card_selected = 0
                game.card = game.cards[game.card_selected]
            return

# Press up and down arrow to browse the menu
def next_menu(event):
    if game.state == "pick_mode":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.menu_selected > 0:
                    game.menu_selected -= 1
                else:
                    game.menu_selected = len(menu_options)-1
            elif event.key == pygame.K_DOWN:
                if game.menu_selected < len(menu_options)-1:
                    game.menu_selected += 1
                else:
                    game.menu_selected = 0
