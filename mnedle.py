#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Mnedle: CZ Wordle

import sys
from pick import pick   # rozhodovaci menu (https://github.com/wong2/pick), pip install pick

# nacteni vlastni knihovny 5 mistnich ceskych slov
import slova5 # promenna words5

# globalni promenna, celkovy pocet dosazenych bodu
score = 0

# menu moznosti
options = ['Začni hru', 'Konec']

def print_logo():
    logo = '                                                     \n'
    logo +='███╗   ███╗███╗   ██╗███████╗██████╗ ██╗     ███████╗\n'
    logo +='████╗ ████║████╗  ██║██╔════╝██╔══██╗██║     ██╔════╝\n'
    logo +='██╔████╔██║██╔██╗ ██║█████╗  ██║  ██║██║     █████╗  \n'
    logo +='██║╚██╔╝██║██║╚██╗██║██╔══╝  ██║  ██║██║     ██╔══╝  \n'
    logo +='██║ ╚═╝ ██║██║ ╚████║███████╗██████╔╝███████╗███████╗\n'
    logo +='╚═╝     ╚═╝╚═╝  ╚═══╝╚══════╝╚═════╝ ╚══════╝╚══════╝\n'
    return logo

title = print_logo()

# sklonovani slova bod, program match zde nepouzivam kvuli kompatibilite se starsimi verzemi pythonu
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

# Main
if __name__ == "__main__":

    option, index = pick(options, title, indicator = '->')
    if (index == 0):
        start()
    if (index == 1):
        exit()