import pygame
import sys
import random
import textwrap

from dotdict import *
from strings import * 
from assets import *
from state import *

def proper_exit():
    pygame.quit()
    sys.exit()

def isstring(obj):
    return isinstance(obj, str)
