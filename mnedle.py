#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle
# Date: 2022/04/03
# Author: Martin Vodráška
# E-mail: mvodraska@seznam.cz
# Student: AIK2 (2020)
# School: (https://www.vosplzen.cz/)
# City, Country: Pilsen, Czechia

import sys, os, random, threading           # zakladni knihovna, knihovna operacniho systemu, knihovna pro nahodnost, knihovna pro vlakna
from pick import pick                       # rozhodovaci menu (https://github.com/wong2/pick), pip install pick
import numpy as np                          # knihovna s 2d polem, pip install numpy
from termcolor import colored, cprint       # ANSII Color formatting for output in terminal, pip install termcolor
from pynput.keyboard import Listener, Key   # cteni stiknutych klaves z klavesnice, pip install pynput


import slova5                               # nacteni vlastni knihovny 5 mistnich ceskych slov, promenna words5

score = 0                                   # globalni promenna, celkovy pocet dosazenych bodu
gf = None                                   # globalni promenna pro objekt GameField hraciho pole
history = ''                                # globalni promenna pro ukladani predeslych radku
output = ''                                 # globalni promenna pro ulozeni vystupu z klavesnice

def print_logo():
    logo = '███╗   ███╗███╗   ██╗███████╗██████╗ ██╗     ███████╗\n'
    logo +='████╗ ████║████╗  ██║██╔════╝██╔══██╗██║     ██╔════╝\n'
    logo +='██╔████╔██║██╔██╗ ██║█████╗  ██║  ██║██║     █████╗  \n'
    logo +='██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║  ██║██║     ██╔══╝  \n'
    logo +='██║ ╚═╝ ██║██║ ╚████║███████╗██████╔╝███████╗███████╗\n'
    logo +='╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚══════╝\n'
    logo +='         CZ Wordle - hádej pětimístné slovo          \n'
    logo +='       Dobrovolná podpora (Donation), BTC (₿):       \n'
    logo +='      bc1qy8cflws9zufqcty7f6hpewnywty3uwcaugy6vc     '
    return logo

# menu moznosti
options = ['Hraj', 'Konec']
title = print_logo()

def introductory_text():
    txt  = '\nklávesa delete = konec hry, CH se bere jako dvoupísmenné\n'
    txt += colored('žluté písmeno  = nachází se někde ve slově .. +1 bod','yellow') + '\n'
    txt += colored('zelené písmeno = nachází se v přesné pozici slova .. +2 body','green') + '\n'
    txt += '\nhádej pětimístné české slovo\nv maximálně pěti pokusech:'
    return txt

# sklonovani slova bod
def inflection(score):
    switcher = {
        1: '',
        2: 'y',
        3: 'y',
        4: 'y'
    }
    return 'bod' + str(switcher.get(abs(score), 'ů'))

def plusScore(s):
    global score
    score = score + s
    return int(score)

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
        'correct': 'white',
        'bad_input': 'red',
        'actual_row': 'cyan',
        'with_pos': 'green',
        'without_pos': 'yellow'
    }

    def __init__(self, w, h):

        self.w = int(w)
        self.h = int(h)

        self.border = self.w-2

        self.word = random.choice(list(slova5.words5.items()))[1].lower()

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
                row += self.colorColored(prefix + self.matrix[r,i] + suffix, r, i)
            view += row + '\n'
        
        return view

    def listingGameActualRow(self, r):

        self.r = r
        row = ''

        for i in range(0, len(self.matrix[self.r])):
            prefix = suffix = ''
            if (i == 0):
                prefix = ''
                suffix = self.colon
            else:
                prefix = suffix = self.gapChar
            row += self.colorColored(prefix + self.matrix[self.r,i] + suffix, self.r, i)
        
        return row
        #return self.word + ', [' + str(self.actualpos[0]) + ',' + str(self.actualpos[1]) + '] ' +  row

    def searchWord(self):
        bl = False
        global output
        if output in slova5.words5.values():
            bl = True
        else:
            bl = False
        return bl

    def infoReportRow(self, txt, color):
        
        self.txt = txt
        self.color = color
        
        gf.valueChangeCell(self.txt + gf.gapChar*100, gf.actualpos[0], int(gf.border+1))
        gf.colorChangeCell(self.color, gf.actualpos[0], int(gf.border+1))

    def listingScore(self):
        return 'Skóre: ' + str(score) + ' ' + inflection(score)

    def evaluation(self, row):
        
        global output
        global gf
        self.row = row
        subscore = [0,0,0,0,0]

        i = 0

        for char in output:

            # defaultni zbarveni vyhodnoceneho slova
            gf.colorChangeCell('correct', self.row, i+1)

            if char in self.word:
                # nachazi se znak ve slove
                subscore[i] = 1
                gf.colorChangeCell('without_pos', self.row, i+1)
            
            if char == self.word[i]:
                # nachazi se znak na presne pozici
                subscore[i] = 2
                gf.colorChangeCell('with_pos', self.row, i+1)

            i += 1

        return sum(subscore)

    def done(self, row):
        
        self.row = row+1

        rscore = {
            1: 100,
            2: 50,
            3: 30,
            4: 25,
            5: 20
        }

        return int(rscore.get(self.row, 0))





def printFlush():
    global gf
    print(gf.listingGameActualRow(gf.actualpos[0]), end='\r', flush=True)

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
            gf.infoReportRow('Stiskni enter pro vyhodnocení','actual_row')
            
    printFlush()

def playBackspace():

    global gf
    global output

    output = output[:-1]
    lenput = len(output)

    gf.valueChangeCell(gf.gapChar*100, gf.actualpos[0], 6)

    if (lenput >= 0 and gf.actualpos[1] > 0):
        gf.valueChangeCell(gf.defaultChar, gf.actualpos[0], gf.actualpos[1])
        gf.actualpos[1] -= 1
    
    printFlush()
    
def playEnter():

    global gf
    global output
    global score
    global history

    lenput = len(output)
    done = False

    if (lenput == gf.border):
        # spravna delka test slova
        if (gf.searchWord()):
            # slovo existuje v seznamu
            if (output == gf.word):
                # slovo se rovna hledanemu
                plusScore(gf.done(gf.actualpos[0]))
                gf.infoReportRow('!!! UHODLS !!! ' + gf.listingScore(), 'correct')
                done = True
            else:
                # slovo se nerovna hledanemu
                plusScore(gf.evaluation(gf.actualpos[0]))
                gf.infoReportRow(gf.listingScore(), 'correct')
        else:
            # slovo neexistuje v seznamu
            plusScore(-4)
            gf.infoReportRow('Takové slovo neexistuje, -4 ' + inflection(-4), 'bad_input')
        
    else:
        # test slovo nema pozadovanou delku
        gf.infoReportRow('Slovo nemá požadovanou délku', 'bad_input')

    if (lenput == gf.border):
        # jiz vyhodnoceno, prechod na dalsi slovo
        history = gf.listingGameActualRow(gf.actualpos[0])
        
        output = '';
        
        if (not done and gf.actualpos[0] == gf.border-1):
            # neuhodnuto a zaroven na posledni moznosti
            plusScore(-15)
            history += '\nNeuhodls, -15 bodů, slovo bylo ' + gf.word + ', ' + gf.gapChar + gf.listingScore()
            done = True

        if (gf.actualpos[0] < gf.border-1):
            gf.actualpos[0] += 1
            gf.actualpos[1] = 0
        
            gf.colorChangeRow('actual_row', gf.actualpos[0])
            play('')
        
        if (done):
            # uhodnuto
            history += '\nPokračuj ...'
        
        print(history)
    
    if (done):
        history = ''
        gf.actualpos[0] = 0
        gf.actualpos[1] = 0
        gf = None
        start()
    else:
        printFlush()



def start():

    global gf
    global history

    # vytvoreni hraciho pole 5x5 (resp. 7x5 s popiskama na 0 sloupci a poslednim sloupci)
    gf = GameField(int(5+2),int(5))
    gf.colorChangeRow('actual_row', 0)

    print(introductory_text())
    print(history)

    play('')


def on_press(key):
    global gf
    if (hasattr(key, 'char')):
        # bezne klavesy
        play(key.char)
    elif key == Key.enter:
        # enter
        playEnter()
    elif key == Key.backspace:
        # backspace
        playBackspace()
    elif key == Key.delete:
        # stop listener
        return False
    else:
        pass #key.name

# Main
if __name__ == "__main__":

    option, index = pick(options, title, indicator = '->')
    if (index == 0):
        #introductory_text()
        start()
        with Listener(on_press=on_press, suppress=True) as listener:
            listener.join()
    if (index == 1):
        exit()
    
    