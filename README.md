# Mnedle
CZ Wordle - hádání pětimístních, českých slov v consoli https://github.com/kralik/Mnedle.

- Autor: Martin Vodráška
- Student AIK2 (2020)

## Proč mnedle?
České "IMHO", viz [https://twitter.com/jazykovedma/status/1321074628236873730?lang=cs].

## Zdroj dat

Původní cz_words.txt databáze českých podstatných jmen stažena z [https://pastebin.com/7uPetKWh]. Upraveno pomocí příkazu: 
> grep -o -w "^\w\{5\}" cz_words.txt >> cz_words_5.txt

Dále upraveno v LibreOffice Calc do podoby slovníku pro python a uloženo v slova5.py

## TODO

- zlepšit slovník slov
- problém s ď, ť, ň kombinace se shiftem
- ověření vstupu např. při zadávaní čísel, které ve vstupu nemají co dělat