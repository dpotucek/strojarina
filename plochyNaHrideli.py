#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Spočítá hloubku, kterou musi mit ploška na hřídeli, pokud znám průměr hřídele a žádanou
šířku plošky.
Umí spočítat i čtverec na hřídeli, přepínač je v prvním parametru.
Created on 22/02/2021, 14:03

@author: David Potucek
"""

from math import sqrt
from daptools.myTools import strEnumUsrIn, numUsrIn

def hloubka_plosky(prumer, sirka_plosky):
    h = prumer - sqrt((prumer/2) ** 2 - (sirka_plosky / 2) ** 2)
    return h

def hloubka_ctverce(prumer):
    return 0.125 * prumer

if __name__ == "__main__":
    defaultPrumer = 25
    defaultSirkaPlosky = 7
    varianty = ('c', 'p')
    choice = strEnumUsrIn('chces spocitat ctverec {zadej c, nebo nic}, nebo plošku na hřídeli {zadej p}', varianty, 'c')
    if choice == 'c':           # pocitame ctverec
        print('počítáme čtverec na hřídeli.')
        prumer = numUsrIn('Zadej průměr hřídele: ', defaultPrumer)
        hloubkaRezu = hloubka_ctverce(prumer)
        print('Pro průměr hřídele {}mm je hloubka řezu čtverce {:3.2f}mm'.format(prumer, hloubkaRezu))
    else:
        print('počítáme plošku na hřídeli.')
        prumer = numUsrIn('Zadej průměr hřídele: ', defaultPrumer)
        sirkaPlosky = numUsrIn('Zadej šířku plošky: ', defaultSirkaPlosky)
        hloubkaRezu = hloubka_plosky(prumer, sirkaPlosky)
        print('Pro průměr hřídele {}mm a šířku plošky {}mm je hloubka řezu {:3.2f}'.
              format(prumer, sirkaPlosky, hloubkaRezu))




