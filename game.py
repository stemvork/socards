from lib import *

game = DotDict({})
game.debug = True
game.states = [ "pick_mode"
              , "card_back"
              , "view_card"
              ]
game.state = game.states[0]
print(game.state)
game.cards = cards
game.card_selected = 0
game.card = game.cards[game.card_selected]
game.menu_options = menu_options
game.menu_selected = 0

game.screen = pygame.display.set_mode((300, 420))
maxwidth, maxheight = game.screen.get_size()
game.maxwidth = maxwidth
game.maxheight = maxheight
game.center = game.screen.get_rect().center
pygame.display.set_caption("Socards v0.2")
game.clock  = pygame.time.Clock()
pygame.init()

game.colors = colors

def update(game):
    # Handle pygame events
    [handle_event(event) for event in pygame.event.get()]

def handle_event(event):
    action_quit(event)
    switch_state(event)
    next_card(event)
    next_menu(event)

def draw(game):
    game.screen.fill(colors.bg)

    if game.state == "pick_mode":
        draw_menu(game.screen)
    elif game.state == "card_back":
        draw_card_back(game.screen)
    elif game.state == "view_card":
        draw_card(game.screen, game.card)

    next_frame()

def draw_text(surface, text, position, color=colors.white, font=sans):
   text_img  = font.render(text, True, color)
   text_rect = text_img.get_rect(topleft = position)
   screen.blit(text_img, text_rect)

# FIXME
def draw_title(_s):
    _i = sans.render("So", True, colors.white)
    _sr = _s.get_rect()
    _r = _i.get_rect(bottomright = (_sr.width//2, _sr.height//2 - 15))
    _s.blit(_i, _r)

# FIXME
def draw_subtitle(_s):
    _i = written.render(
            "a collection of questions", True, colors.white)
    _j = written.render(
            "for deeper discussions", True, colors.white)
    _sr = _s.get_rect()
    _ri = _i.get_rect(center = (_sr.width//2, _sr.height//2 + 15))
    _rj = _j.get_rect(center = (_sr.width//2, _sr.height//2 + 15 +
        written.size("for deeper discussions")[1]))
    _s.blit(_i, _ri)
    _s.blit(_j, _rj)

def draw_questions(screen, questions, font=written, padding=0, center=True):
    # print("question-multiple called with", questions)
    if isstring(questions):
        # print("questions called with single question")
        textsurface = draw_question(maxwidth, questions, font, padding=padding)
        screen.blit(textsurface, textsurface.get_rect(center=game.center))

def draw_question(maxwidth, question, font=written, padding=0, center=True):
    lines = textwrap.wrap(question, width=30)
    if len(lines) == 1:
        textsurface = draw_single_line(maxwidth, question, font, padding, center)
    else:
        textsurface = draw_multi_line(maxwidth, lines, font, padding, center)
    return textsurface

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

def draw_menu(screen, padding=30):
    textsurfaces = []

    for i, option in enumerate(menu_options):
        if i is game.menu_selected:
            textsurfaces.append(draw_single_line(maxwidth, option, 
                    font=sans_small, color=colors.white, center=False))

            description = textwrap.wrap(menu_options_desc[i], width=36)
            textsurfaces.append(draw_multi_line(maxwidth, description,
                    font=serif_small, color=colors.white, center=False))
        else:
            textsurfaces.append(draw_single_line(maxwidth, option, 
                    font=sans_small, color=colors.gray, center=False))

    totalheight = sum([surface.get_size()[1] 
        for surface in textsurfaces]) + padding * (len(menu_options) - 1)
    if totalheight > maxheight:
        print("warning: overflows screen drawing", "question")

    textsurface = pygame.Surface((maxwidth, totalheight))
    textsurface.set_colorkey(colors.black)
    textsurface_center = game.center[0] + padding, game.center[1]

    next_height = 0
    for i, surface in enumerate(textsurfaces):
        textsurface.blit(surface, surface.get_rect(top=next_height))
        if i is game.menu_selected:
            next_height += surface.get_rect().height
        else:
            next_height += surface.get_rect().height + padding
    screen.blit(textsurface, textsurface.get_rect(center=textsurface_center))

def draw_card(screen, card):
    lines = textwrap.wrap(game.card, 30)
    textsurface = draw_multi_line(maxwidth, lines)
    screen.blit(textsurface, textsurface.get_rect(center=game.center))

def draw_card_back(_s):
    # fill the screen surface _s with the BG colour
    # and get the dimensions of the surface as _r
    _s.fill(colors.bg)
    _r = _s.get_rect()
    # draw the white rectangle of width 1 to the screen _s
    # at an offset from the left, top and right and bottom
    pygame.draw.rect(_s, colors.white, (5, 5, _r.width - 10, _r.height - 10), 1)

    # make use of the functions defined above
    draw_title(_s)
    draw_subtitle(_s)

    # draw the three coloured dots
    # TODO: play with the different pastel colours
    # PASTEL has elements 0, 1, 2, 3, 4
    # calculate title_center to position relative to...
    title_center = pygame.Vector2(_r.width//2, _r.height//2 - 15)
    pygame.draw.circle(_s, colors.red,
            title_center + (20,-20) , 10)
    pygame.draw.circle(_s, colors.blue, 
            title_center + (50,-20), 10)
    pygame.draw.circle(_s, colors.green, 
            title_center + (80,-20), 10)

def next_frame():
    pygame.display.flip()
    game.clock.tick(30)

def action_quit(event):
    if event.type == pygame.QUIT:
        proper_exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            proper_exit()
        elif event.key == pygame.K_q:
            proper_exit()

def switch_state(event):
    if event.type == pygame.KEYDOWN:
        if event.key is pygame.K_m:
            game.states.append(game.states.pop(0))
            game.state = game.states[0]
            if game.debug:
                print(game.state)

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
