import pygame
from dotdict import *

pygame.init()

# TODO: choose and implement fallback font
sans        = pygame.font.SysFont("Arial Bold", 100)
sans_small  = pygame.font.SysFont("Arial Bold", 30)
serif       = pygame.font.SysFont("Times New Roman", 30)
serif_small = pygame.font.SysFont("Times New Roman", 15)
written     = pygame.font.SysFont("Savoye LET", 30)


colors = DotDict({ k: pygame.Color(c) for k, c in {
    "white": "#ffffff",
    "black": "#000000",
    "gray": "#777777",
    "red": "#f4a586",
    "blue": "#baddab",
    "green": "#8bbbe0",
    "pink": "#f8f490",
    "purple": "#b5b3dd"}.items()})
colors.bg = (20, 40, 60)
