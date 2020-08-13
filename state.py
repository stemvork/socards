from lib import *

# GAME STATE AND SETTINGS
game = DotDict({})

game.debug = True
game.states = [ "pick_mode"
              , "card_back"
              , "view_card"
              ]
game.state = game.states[0]

game.cards = cards
game.card_selected = 0
game.card = game.cards[game.card_selected]

game.menu_options = menu_options
game.menu_selected = 0

# The screen width and height are the maximum possible width and height.
screensize = (300, 420)
maxwidth, maxheight = screensize

# The following are not necessarily game state
# but in case of trouble with scope, these can
# be accessed through the game state as well.
game.maxwidth = maxwidth
game.maxheight = maxheight
game.screen = pygame.display.set_mode(screensize)
game.center = game.screen.get_rect().center

pygame.display.set_caption("Socards v0.2")
game.clock  = pygame.time.Clock()
game.colors = colors

