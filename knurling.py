#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
program pro vypocet parametru vroubkovani.
Created on 20/02/2020, 11:27

@author: David Potucek
"""

from math import pi, floor

# pouzivam prumer kolecek 20 mm.
WHEEL_DIAMETER = 20
# pitches definuji jake mam kolecka a jakeho typu. Typy dodeleny ':'
# typy: P = pair, S = straigt, D = diagonal
PITCHES = {2.0: 'P', 1.6:'D', 1.2:'P', 1.0: 'P', 0.8: 'P', 0.4:'S'}

EPSILON = 0.01

def count_knurling_american(wheelDia, numOfTeeth, pieceDia):
    deltaK = pi * wheelDia / numOfTeeth       # roztec zubu kolecka
    crestNum = floor(pi * pieceDia / deltaK)
    return deltaK, crestNum

def count_crest_num4_dia(roztecKolecka, prumerKusu):
    pocetVrypu = floor(pi * prumerKusu / roztecKolecka)
    potrebnyObvodKusu = pocetVrypu * roztecKolecka
    idealniOradlovani = potrebnyObvodKusu / pi
    return(pocetVrypu, potrebnyObvodKusu, idealniOradlovani)

if __name__ == "__main__":
    roztec = 2
    pieceDia = 30
    pocetVrypu, potrebnyObvod, idealniObvod = count_crest_num4_dia(roztec, pieceDia)

    print('----------------- Vysledky --------------------')
    print('Pro kus o prumeru: {} mm'. format(pieceDia))
    print('celociselny pocet vrypu na kusu: {}'.format(pocetVrypu))
    print('potrebny obvod kusu: {:.3f} mm'.format(potrebnyObvod))
    print('pro perfektni oradlovani je potreba mit prumer kusu: {:.2f} mm'.format(idealniObvod))