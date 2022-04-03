#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle
# Date: 2022/04/03
# Author: Martin Vodráška
# Student: AIK2 (2020)
# School: (https://www.vosplzen.cz/)
# City, Country: Pilsen, Czechia

import sys, os, random, threading           # zakladni knihovna, knihovna operacniho systemu, knihovna pro nahodnost, knihovna pro vlakna
from os import system, name                 # vymaz console
from pick import pick                       # rozhodovaci menu (https://github.com/wong2/pick), pip install pick
import numpy as np                          # knihovna s 2d polem, pip install numpy
from termcolor import colored, cprint       # ANSII Color formatting for output in terminal, pip install termcolor
from pynput.keyboard import Listener, Key   # cteni stiknutych klaves z klavesnice, pip install pynput


import slova5                               # nacteni vlastni knihovny 5 mistnich ceskych slov, promenna words5

score = 0                                   # globalni promenna, celkovy pocet dosazenych bodu
gf = None                                   # globalni promenna pro objekt GameField hraciho pole
output = ''                                 # globalni promenna pro ulozeni vystupu z klavesnice

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
options = ['Hraj', 'Konec']
title = print_logo()

# 2D hraci pole
class GameField(object):
    
    global score
    global output
    
    matrix = []
    colors = []
    defaultChar = '⏺'
    badChar = 'ᳵ'
    gapChar = ' '
    colon = ':'
    word = ''
    actualpos = [0,0]
    border = 0

    # barvicky - color name
    cn = {
        'default': 'blue',
        'correct': 'gray',
        'bad_input': 'red',
        'actual_row': 'cyan',
        'with_pos': 'green',
        'without_pos': 'yellow'
    }

    def __init__(self, w, h):

        self.w = int(w)
        self.h = int(h)

        self.border = self.w-2

        self.word = random.choice(list(slova5.words5.items()))[1]

        self.matrix = np.array([[self.defaultChar]*self.w]*self.h, dtype='<U100')
        self.colors = np.array([[self.cn['default']]*self.w]*self.h, dtype='<U100')

        for i in range(0, len(self.matrix)):
            self.matrix[i,0] = str(self.h-((i+1)-1))
            self.matrix[i,self.w-1] = self.gapChar

    def colorColored(self, txt, x, y):

        self.txt = txt
        self.x = int(x)
        self.y = int(y)

        return colored(self.txt, self.colors[x,y])
    
    def colorChangeCell(self, name, x, y):

        self.name = name
        self.x = int(x)
        self.y = int(y)

        self.colors[self.x,self.y] = self.cn[self.name]
    
    def colorChangeRow(self, name, r):

        self.name = name
        self.r = int(r)

        for r in range(0, len(self.colors)):
            for i in range(0, len(self.colors[r])):
                if (r == self.r):
                    self.colors[r,i] = self.cn[self.name]
    
    def valueChangeCell(self, val, x, y):

        self.val = val
        self.x = int(x)
        self.y = int(y)

        self.matrix[self.x,self.y] = self.val

    def listingGameField(self):
        
        #view = ''
        view = 'slovo: ' + self.word + ', output: ' + output + ', pozice [' + str(self.actualpos[0]) + ',' + str(self.actualpos[1]) + '], border: ' + str(self.border) + '\n\n'
        
        for r in range(0, len(self.matrix)):
            row = ''
            for i in range(0, len(self.matrix[r])):
                prefix = suffix = ''
                if (i == 0):
                    prefix = ''
                    suffix = self.colon
                else:
                    prefix = suffix = self.gapChar
                row += self.colorColored(prefix + self.matrix[r,i] + suffix, r, i)
            view += row + '\n'
        
        return view + '\nCelkové skóre: ' + str(score) + ' ' + inflection(score) + '\n'


# sklonovani slova bod
def inflection(score):
    switcher = {
        1: '',
        2: 'y',
        3: 'y',
        4: 'y'
    }
    return 'bod' + str(switcher.get(abs(score), 'ů'))

def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # mac, linux
    else:
        _ = system('clear')

def introductory_text():
    print('\nklávesa delete = konec hry')
    print(colored('žluté písmeno  = nachází se někde ve slově .. +1 bod','yellow'))
    print(colored('zelené písmeno = nachází se v přesné pozici slova .. +2 body','green'))
    print('\nhádej pětimístné české slovo\nv maximálně pěti pokusech:\n')

def printPlayListing():
    global gf
    return print(gf.listingGameField())

def play(ch):
    
    global gf
    global output

    if (len(output) < gf.border):
        output += ch

    if (len(output) > 0 and gf.actualpos[1] < gf.border):
        gf.actualpos[1] += 1
        gf.valueChangeCell(ch.upper(), gf.actualpos[0], gf.actualpos[1])
    
        if (gf.actualpos[1] == gf.border):
            # na psoledni pozici hadaneho slova
            gf.valueChangeCell("Stiskni enter pro vyhodnocení", gf.actualpos[0], int(gf.border+1))
            #TODO zde probehne kontrola outputu

    clear()
    introductory_text()
    printPlayListing()

def playBackspace():

    global gf
    global output

    output = output[:-1]
    lenput = len(output)

    gf.valueChangeCell(gf.gapChar, gf.actualpos[0], 6)

    if (lenput >= 0 and gf.actualpos[1] > 0):
        gf.valueChangeCell(gf.defaultChar, gf.actualpos[0], gf.actualpos[1])
        gf.actualpos[1] -= 1
    

    clear()
    introductory_text()
    printPlayListing()
    
def playEnter():

    global gf
    global output

    output = '';
    gf.actualpos[0] += 1
    gf.actualpos[1] = 0
    gf.colorChangeRow('actual_row', gf.actualpos[0])



def start():

    global gf

    # vytvoreni hraciho pole 5x5 (resp. 7x5 s popiskama na 0 sloupci a poslednim sloupci), pet pokusu petimistnych slov
    gf = GameField(int(5+2),int(5))
    gf.colorChangeRow('actual_row', 0)
    
    #gf.colorChangeCell('bad_input', 1, 4)
    #gf.valueChangeCell(gf.badChar, 1, 4)

    play('')


def on_press(key):
    global gf;
    if (hasattr(key, 'char')):
        # bezne klavesy
        play(key.char)
    elif key == Key.enter:
        pass # enter
    elif key == Key.backspace:
        # backspace
        playBackspace()
    elif key == Key.space:
        pass # space
    elif key == Key.delete:
        # stop listener
        return False
    else:
        pass #key.name

# Main
if __name__ == "__main__":

    option, index = pick(options, title, indicator = '->')
    if (index == 0):
        introductory_text()
        start()
        with Listener(on_press=on_press, suppress=True) as listener:
            listener.join()
    if (index == 1):
        exit()
    
    