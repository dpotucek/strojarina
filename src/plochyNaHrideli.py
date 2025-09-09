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
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../DaPTools/src'))
from daptools.myTools import str_enum_usr_in, num_usr_in


class PlochyNaHrideli:
    """Trida pro vypocet hloubky plosky a ctverce na hrideli."""
    
    def hloubka_plosky(self, prumer, sirka_plosky):
        """Vypocte hloubku plosky na hrideli.
        :param prumer: prumer hridele v mm
        :param sirka_plosky: sirka plosky v mm
        :return: hloubka rezu v mm
        """
        h = prumer - sqrt((prumer/2) ** 2 - (sirka_plosky / 2) ** 2)
        return h

    def hloubka_ctverce(self, prumer):
        """Vypocte hloubku ctverce na hrideli.
        :param prumer: prumer hridele v mm
        :return: hloubka rezu v mm
        """
        return 0.125 * prumer


# Zachovani zpetne kompatibility
def hloubka_plosky(prumer, sirka_plosky):
    pnh = PlochyNaHrideli()
    return pnh.hloubka_plosky(prumer, sirka_plosky)

def hloubka_ctverce(prumer):
    pnh = PlochyNaHrideli()
    return pnh.hloubka_ctverce(prumer)


if __name__ == "__main__":
    pnh = PlochyNaHrideli()
    defaultPrumer = 25
    defaultSirkaPlosky = 7
    varianty = ('c', 'p')
    choice = str_enum_usr_in('chces spocitat ctverec {zadej c, nebo nic}, nebo plošku na hřídeli {zadej p}', varianty, 'c')
    if choice == 'c':           # pocitame ctverec
        print('počítáme čtverec na hřídeli.')
        prumer = num_usr_in('Zadej průměr hřídele: ', defaultPrumer)
        hloubkaRezu = pnh.hloubka_ctverce(prumer)
        print('Pro průměr hřídele {}mm je hloubka řezu čtverce {:3.2f}mm'.format(prumer, hloubkaRezu))
    else:
        print('počítáme plošku na hřídeli.')
        prumer = num_usr_in('Zadej průměr hřídele: ', defaultPrumer)
        sirkaPlosky = num_usr_in('Zadej šířku plošky: ', defaultSirkaPlosky)
        hloubkaRezu = pnh.hloubka_plosky(prumer, sirkaPlosky)
        print('Pro průměr hřídele {}mm a šířku plošky {}mm je hloubka řezu {:3.2f}'.
              format(prumer, sirkaPlosky, hloubkaRezu))