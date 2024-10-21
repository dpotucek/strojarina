#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
program pro vypocet parametru vroubkovani.
Created on 20/02/2020, 11:27

@author: David Potucek
'''

from math import pi, floor

# pouzivam prumer kolecek 20 mm.
WHEEL_DIAMETER = 20
# pitches definuji jake mam kolecka a jakeho typu. Typy dodeleny ':'
# typy: P = pair, S = straigt, D = diagonal
PITCHES = {2.0: 'P', 1.6:'D', 1.2:'P', 1.0: 'P', 0.8: 'P', 0.4:'S'}

EPSILON = 0.01

def countKnurlingAmerican(wheelDia, numOfTeeth, pieceDia):
    deltaK = pi * wheelDia / numOfTeeth       # roztec zubu kolecka
    crestNum = floor(pi * pieceDia / deltaK)
    return deltaK, crestNum

def countCrestNum4Dia(roztecKolecka, prumerKusu):
    pocetVrypu = floor(pi * prumerKusu / roztecKolecka)
    potrebnyObvodKusu = pocetVrypu * roztecKolecka
    idealniOradlovani = potrebnyObvodKusu / pi
    return(pocetVrypu, potrebnyObvodKusu, idealniOradlovani)

if __name__ == "__main__":
    # for polozka in PITCHES:
    #     print('polozka = {}: {}'.format(polozka, PITCHES[polozka]))

    roztec = 2

    # pieceDia = MTools.numUsrIn('zadej nominalni prumer kusu k radlovani: ', 30)
    pieceDia = 30
    pocetVrypu, potrebnyObvod, idealniObvod = countCrestNum4Dia(roztec, pieceDia)

    print('----------------- Vysledky --------------------')
    print('Pro kus o prumeru: {} mm'. format(pieceDia))
    print('celociselny pocet vrypu na kusu: {}'.format(pocetVrypu))
    print('potrebny obvod kusu: {:.3f} mm'.format(potrebnyObvod))
    print('pro perfektni oradlovani je potreba mit prumer kusu: {:.2f} mm'.format(idealniObvod))