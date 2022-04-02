#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle
# Date: 2022/04/03
# Author: Martin Vodráška
# Student: AIK2 (2020)
# School: (https://www.vosplzen.cz/)
# City, Country: Pilsen, Czechia

import sys, os, random, threading           # zakladni knihovna, knihovna operacniho systemu, knihovna pro nahodnost, knihovna pro vlakna
from pick import pick                       # rozhodovaci menu (https://github.com/wong2/pick), pip install pick
import numpy as np                          # knihovna s 2d polem, pip install numpy
from termcolor import colored, cprint       # ANSII Color formatting for output in terminal, pip install termcolor
from pynput.keyboard import Key, Listener   # cteni stiknutych klaves z klavesnice, pip install pynput
from pynput import keyboard                 # cteni stiknutych klaves z klavesnice, pip install pynput

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
    logo +='         (https://github.com/kralik/Mnedle)          \n'
    logo +='       Dobrovolná podpora (Donation), BTC (₿):       \n'
    logo +=''
    return logo

# menu moznosti
options = ['Začni hru', 'Konec']
title = print_logo()

# 2D hraci pole 5x5 (resp. 7x5 s popiskama na 0 sloupci a poslednim sloupci), pet pokusu petimistnych slov
class GameField(object):
    
    matrix = []
    colors = []
    defaultChar = '⏺'
    badChar = 'ᳵ'
    gapChar = ' '
    colon = ':'
    word = ''

    # barvicky - color name
    cn = {
        'default': 'blue',
        'bad_input': 'red',
        'actual_row': 'cyan',
        'with_pos': 'green',
        'without_pos': 'yellow'
    }

    def __init__(self, w, h):

        self.w = int(w)
        self.h = int(h)

        self.word = random.choice(list(slova5.words5.items()))[1]

        self.matrix = np.array([[self.defaultChar]*self.w]*self.h)
        self.colors = np.array([[self.cn['default']]*self.w]*self.h)

        for i in range(0, len(self.matrix)):
            self.matrix[i,0] = str(self.h-((i+1)-1))
            self.matrix[i,self.w-1] = ''

    def colorColored(self, txt, x, y):

        self.txt = txt
        self.x = int(x)
        self.y = int(y)

        return colored(self.txt, self.colors[x][y])
    
    def colorChangeCell(self, name, x, y):

        self.name = name
        self.x = int(x)
        self.y = int(y)

        self.colors[self.x][self.y] = self.cn[self.name]
    
    def colorChangeRow(self, name, r):

        self.name = name
        self.r = int(r)

        for r in range(0, len(self.colors)):
            for i in range(0, len(self.colors[r])):
                if (r == self.r):
                    self.colors[r][i] = self.cn[self.name]
    
    def valueChangeCell(self, val, x, y):

        self.val = val
        self.x = int(x)
        self.y = int(y)

        self.matrix[self.x][self.y] = self.val

    def listingGameField(self):
        
        view = ''
        
        for r in range(0, len(self.matrix)):
            row = ''
            for i in range(0, len(self.matrix[r])):
                prefix = suffix = ''
                if (i == 0):
                    prefix = ''
                    suffix = self.colon
                else:
                    prefix = suffix = self.gapChar
                row += self.colorColored(prefix + self.matrix[r][i] + suffix, r, i)
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

    print('--------------')
    print('Celkové skóre: ' + str(score) + ' ' + inflection(score) + '\n')
    
    gf = GameField(7,5)
    gf.colorChangeRow('actual_row', 2)
    
    gf.colorChangeCell('bad_input', 1, 4)
    gf.valueChangeCell(gf.badChar, 1, 4)

    print(gf.listingGameField())

def onPress(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        if (key == Key.space):
            pass
        if (key == Key.enter):
            pass
        if (key == Key.esc):
            exit()

def pressKey():
    with Listener(on_press=onPress) as listener:
        listener.join()

# Main
if __name__ == "__main__":

    thread = threading.Thread(target=pressKey, args=())

    option, index = pick(options, title, indicator = '->')
    if (index == 0):
        start()
        thread.start()
    if (index == 1):
        exit()
    
    