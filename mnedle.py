#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle

import sys, random
from pick import pick                   # rozhodovaci menu (https://github.com/wong2/pick), pip install pick
import numpy as np                      # knihovna s 2d polem, pip install numpy
from termcolor import colored, cprint   # ANSII Color formatting for output in terminal, pip install termcolor

# nacteni vlastni knihovny 5 mistnich ceskych slov
import slova5 # promenna words5

# globalni promenna, celkovy pocet dosazenych bodu
score = 0

def print_logo():
    logo = '███╗   ███╗███╗   ██╗███████╗██████╗ ██╗     ███████╗\n'
    logo +='████╗ ████║████╗  ██║██╔════╝██╔══██╗██║     ██╔════╝\n'
    logo +='██╔████╔██║██╔██╗ ██║█████╗  ██║  ██║██║     █████╗  \n'
    logo +='██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║  ██║██║     ██╔══╝  \n'
    logo +='██║ ╚═╝ ██║██║ ╚████║███████╗██████╔╝███████╗███████╗\n'
    logo +='╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚══════╝\n'
    logo +='         CZ Wordle - hádej pětimístné slovo          \n'
    logo +='         (https://github.com/kralik/Mnedle)          '
    return logo

# menu moznosti
options = ['Začni hru', 'Konec']
title = print_logo()

# barvicky
colors = {
    'default': 'blue',
    'bad_input': 'red',
    'actual_row': 'magenta',
    'with_pos': 'green',
    'without_pos': 'yellow'
}

# 2D hraci pole 5x5 (resp. 6x5 s popiskem), pet pokusu petimistnych slov
class GameField(object):
    
    matrix = []
    defaultChar = '⏺'
    badChar = 'ᳵ'
    gapChar = ' '
    colon = ':'
    word = ''

    def __init__(self, w, h):

        self.w = int(w)
        self.h = int(h)

        self.word = random.choice(list(slova5.words5.items()))[1]

        self.matrix = np.array([[self.defaultChar]*self.w]*self.h)

        for i in range(0, len(self.matrix)):
            self.matrix[i,0] = str(self.h-((i+1)-1))

    def listingGameField(self):
        
        view = ''
        
        for r in range(0, len(self.matrix)):
            row = ''
            first = True
            for item in self.matrix[r]:
                if (first):
                    row += item + self.colon
                    first = False
                else:
                    row += self.gapChar + item + self.gapChar
            view += row + '\n'
        
        return colored(view,colors['default'])


# sklonovani slova bod
def inflection(score):
    switcher = {
        1: '',
        2: 'y',
        3: 'y',
        4: 'y'
    }
    return 'bod' + str(switcher.get(abs(score), 'ů'))

def start():
    global score
    print('Celkové skóre: ' + str(score) + ' ' + inflection(score) + '\n')
    gf = GameField(6,5)
    print(gf.listingGameField())

# Main
if __name__ == "__main__":

    option, index = pick(options, title, indicator = '->')
    if (index == 0):
        start()
    if (index == 1):
        exit()