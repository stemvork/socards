import pygame
import sys
import random
import textwrap

from cards import * 
from dotdict import *

game = DotDict({})
game.debug = True
game.states = [ "pick_mode"
              , "card_back"
              , "view_card"
              ]
game.state = game.states[0]
game.card = 2
game.cards = cards
game.menu_card = menu_card

game.screen = pygame.display.set_mode((300, 420))
pygame.display.set_caption("Socards v0.1")
game.clock  = pygame.time.Clock()
pygame.init()

# TODO: choose and implement fallback font
sans        = pygame.font.SysFont("Arial Bold", 100)
sans_small  = pygame.font.SysFont("Arial Bold", 30)
serif       = pygame.font.SysFont("Times New Roman", 15)
written     = pygame.font.SysFont("Savoye LET", 30)


colors = DotDict({ k: pygame.Color(c) for k, c in {
    "white": "#ffffff",
    "black": "#000000",
    "red": "#f4a586",
    "blue": "#baddab",
    "green": "#8bbbe0",
    "pink": "#f8f490",
    "purple": "#b5b3dd"}.items()})
colors.bg = (20, 40, 60)
game.colors = colors

def proper_exit():
    pygame.quit()
    sys.exit()

def draw_text(_s, text, position, color=colors.white, align="c"):
   _i = sans.render(text, True, color)
   if align == "br":
       _r = _i.get_rect(bottomright = position)
   elif align == "c":
       _r = _i.get_rect(center = position)
   elif align == "tl":
       _r = _i.get_rect(topleft = position)
   _s.blit(_i, _r)
def draw_title(_s):
    _i = sans.render("So", True, colors.white)
    _sr = _s.get_rect()
    _r = _i.get_rect(bottomright = (_sr.width//2, _sr.height//2 - 15))
    _s.blit(_i, _r)
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

def draw_questions(screen, questions):
    screen_rect = screen.get_rect()
    textheight = 200
    textsurface = pygame.Surface((screen_rect.width, textheight))
    textsurface.set_colorkey(colors.black)

    [draw_question(textsurface, i, question[0], sans_small) 
            for i, question in enumerate(questions)]
    screen.blit(textsurface, textsurface.get_rect(center =\
            (screen_rect.width//2, screen_rect.height//2)))

def draw_question(textsurface, i, question, font=written):
    lines = textwrap.wrap(question, width=30)
    if len(lines) is 1:
        lines = question
        line_img  = font.render(question, True, colors.white)
        lineheight = font.size(question)[1]
        line_rect = line_img.get_rect(center = \
                (textsurface.get_rect().width//2, lineheight * i + lineheight // 2))
        textsurface.blit(line_img, line_rect)
    else:
        for _i, line in enumerate(lines):
            line_img  = font.render(line, True, colors.white)
            lineheight = font.size(line)[1]
            line_rect = line_img.get_rect(center = \
                    (textsurface.get_rect().width//2, lineheight * (_i + i) + lineheight // 2))
            textsurface.blit(line_img, line_rect)

def draw_menu(_s):
    for _m in menu_card:
        draw_questions(_s, menu_card)

def draw_card(_s, card):
    draw_question(_s, 0, cards[card])

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
    if game.states[0] is not "view_card":
        return
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if game.card < len(game.cards) -1:
                game.card += 1
            else:
                game.card = 0
            return
