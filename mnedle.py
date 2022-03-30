#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle

import sys, random
from pick import pick   # rozhodovaci menu (https://github.com/wong2/pick), pip install pick

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

# 2D hraci pole 5x5 (resp. 6x5 s popiskem), pet pokusu petimistnych slov
class GameField(object):
    
    matrix = []
    defaultChar = '⏺'
    badChar = ' ᳵ '
    gapChar = ' '
    colon = ':'

    def __init__(self, w, h):

        self.w = int(w)
        self.h = int(h)
        
        for y in range(1, self.h):
            self.matrix.append([])
            for x in range(0, self.w):
                if (x == 0):
                    self.matrix[x].append(str(self.h-(y-1)) + self.colon + self.gapChar)
                else:
                    self.matrix[x].append(self.defaultChar)

    def listingGameField(self):
        
        view = ''
        
        for y in range(self.h):
            row = ''
            for x in range(self.w):
                row += self.matrix[x][y]
            view += row + '\n'
        
        return view


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
    print('Celkové skóre: ' + str(score) + ' ' + inflection(score))
    game = GameField(5,5)
    print(game.listingGameField())

# Main
if __name__ == "__main__":

    option, index = pick(options, title, indicator = '->')
    if (index == 0):
        start()
    if (index == 1):
        exit()