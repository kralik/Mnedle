#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle

import sys
from os import system, name

# nacteni vlastni knihovny 5 mistnich ceskych slov
import slova5 # promenna words5

# globalni promenna, celkovy pocet dosazenych bodu
score = 0

# menu moznosti
menu_options = {
    1: 'Pokračovat',
    2: 'Konec'
}

def print_logo():
    print('                                                     ')
    print('███╗   ███╗███╗   ██╗███████╗██████╗ ██╗     ███████╗')
    print('████╗ ████║████╗  ██║██╔════╝██╔══██╗██║     ██╔════╝')
    print('██╔████╔██║██╔██╗ ██║█████╗  ██║  ██║██║     █████╗  ')
    print('██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║  ██║██║     ██╔══╝  ')
    print('██║ ╚═╝ ██║██║ ╚████║███████╗██████╔╝███████╗███████╗')
    print('╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚══════╝')
    print('                                                     ')

def print_hr():
    print('----------------')

def clear():
    # win
    if name == 'nt':
        _ = system('cls')
    # mac, linux (posix)
    else:
        _ = system('clear')

def print_menu():
    for key in menu_options.keys():
        print (key, '=', menu_options[key])

# sklonovani slova bod, program match zde nepouzivam kvuli kompatibilite se starsimi verzemi pythonu
def inflection(score):
    infl = ' bod'
    switcher = {
        1: '',
        2: 'y',
        3: 'y',
        4: 'y'
    }
    return infl + str(switcher.get(abs(score), 'ů'))

def start():
    global score
    print('Celkové skóre: ' + str(score) + inflection(4))



# Main
if __name__ == "__main__":

    while(True):
        clear()
        print_logo()
        print_menu()
        print_hr()
        option = ''
        try:
            option = int(input('Napiš možnost: '))
        except:
            print('Musí být pouze číslo ...')
        if option == 1:
            start()
        elif option == 2:
            exit()
        else:
            print('Pouze čísla 1 pro pokračování a 2 pro konec')
        print_hr()