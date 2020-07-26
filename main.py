import pygame
import sys
import random

# create a window of reasonable size
# note that the font size is independent
# of the screen size and was chosen for
# the current screen size
# TODO: make font size dependent on screen size
# also note that the ratio between with and height
# is width : height = 1 : 1.4
# then set the screen caption to something
screen = pygame.display.set_mode((300, 420))
pygame.display.set_caption("Socards v0.1")

# to set a fixed framerate
# as it is silly to draw 100+ frames per second
# when the visuals barely change
clock  = pygame.time.Clock()

# this is needed for the font engine to start
pygame.init()

# define two main fonts with their size
# Savoye LET is not common...
# TODO: choose and implement fallback font
title_font    = pygame.font.SysFont("Arial Bold", 100)
subtitle_font = pygame.font.SysFont("Savoye LET", 30)

# define some shorthands for color tuples
# a tuple is an (immutable) list of values
# in this case, color is a tuple of RGB values
BG    = (1, 6, 3)
WHITE = (255, 255, 255)
# found some pastels on internet as hex codes
# so convert them to RGB tuples with the
# pygame.Color(..) function that takes
# hex string as an input
PASTELS = [pygame.Color(c) for c in [
    "#f4a586",
    "#baddab",
    "#8bbbe0",
    "#f8f490",
    "#b5b3dd"]]

# the proper exit function :)
def proper_exit():
    pygame.quit()
    sys.exit()

# general draw_text function, not currently used
def draw_text(_s, text, position, color=WHITE, align="c"):
   _i = title_font.render(text, True, color)
   if align == "br":
       _r = _i.get_rect(bottomright = position)
   elif align == "c":
       _r = _i.get_rect(center = position)
   elif align == "tl":
       _r = _i.get_rect(topleft = position)
   _s.blit(_i, _r)

# draw title takes the screen object as _s
# and renders the text "So" to a pygame.Surface
# with font title_font in WHITE. store as _i
# get the dimensions of the screen object as _sr
# then get the dimensions of this Surface as _r
# lastly draw _i to position _r on screen _s
def draw_title(_s):
    _i = title_font.render("So", True, WHITE)
    _sr = _s.get_rect()
    _r = _i.get_rect(bottomright = (_sr.width//2, _sr.height//2 - 15))
    _s.blit(_i, _r)

# similar to draw_title, but two seperate Surfaces
# one for each line of text
def draw_subtitle(_s):
    _i = subtitle_font.render(
            "a collection of questions", True, WHITE)
    _j = subtitle_font.render(
            "for deeper discussions", True, WHITE)
    _sr = _s.get_rect()
    _ri = _i.get_rect(center = (_sr.width//2, _sr.height//2 + 15))
    _rj = _j.get_rect(center = (_sr.width//2, _sr.height//2 + 15 +
        subtitle_font.size("for deeper discussions")[1]))
    _s.blit(_i, _ri)
    _s.blit(_j, _rj)

# collecting the logic to draw a card-back to screen _s
def draw_card_back(_s):
    # fill the screen surface _s with the BG colour
    # and get the dimensions of the surface as _r
    _s.fill(BG)
    _r = _s.get_rect()
    # draw the white rectangle of width 1 to the screen _s
    # at an offset from the left, top and right and bottom
    pygame.draw.rect(_s, WHITE, (5, 5, _r.width - 10, _r.height - 10), 1)

    # make use of the functions defined above
    draw_title(_s)
    draw_subtitle(_s)

    # draw the three coloured dots
    # TODO: play with the different pastel colours
    # PASTEL has elements 0, 1, 2, 3, 4
    # calculate title_center to position relative to...
    title_center = pygame.Vector2(_r.width//2, _r.height//2 - 15)
    pygame.draw.circle(_s, PASTELS[0], 
            title_center + (20,-20) , 10)
    pygame.draw.circle(_s, PASTELS[1], 
            title_center + (50,-20), 10)
    pygame.draw.circle(_s, PASTELS[2], 
            title_center + (80,-20), 10)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            proper_exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                proper_exit()

    
    # following line not relevant, since the card covers the screen
    screen.fill((20, 50, 80))

    # draw a card back to the screen, as defined above
    draw_card_back(screen)

    # flip the current screen surface to the user
    pygame.display.flip()
    # make sure that the next loop finishes 1/30th of a second later
    clock.tick(30)

