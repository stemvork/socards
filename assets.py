import pygame
from dotdict import *

pygame.init()

# In this file, the colors and fonts are configured.

# They require the pygame package. I prefer to interact with
# the colors as `colors.red` rather than `colors["red"]`
# as the usual dicationary implementation or  `colors[0]`
# as a list implementation.

# For now, 5 specific font-size combinations are chosen.
# However, it is possible to specify only the font name
# and specify the size upon rendering. Performance vs. usability?

# TODO: choose and implement fallback font for Savoye LET
sans        = pygame.font.SysFont("Arial Bold", 100)
sans_small  = pygame.font.SysFont("Arial Bold", 30)
serif       = pygame.font.SysFont("Times New Roman", 30)
serif_small = pygame.font.SysFont("Times New Roman", 15)
written     = pygame.font.SysFont("Savoye LET", 30)

# I am not sure if the colours match their words, oops.
# The white, black and gray are correct.

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
