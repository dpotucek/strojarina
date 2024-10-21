#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 2, 2015
Vypocet ruznych velicin pro strojarinu. Rizeno pomoci konstant na zacatku.

@author: david
'''
# -------- sine bar variables ---------------
__SINE_BAR = False
__DELKA = 100  # vzdalenost os valecku [mm]
__R1 = 30  # prvni (referencni) valecek
# -------- revolver variables ---------------
__REVOLVER = False
__NO_HOLES = 7  # pocet der v revolveru
__HOLE_DIAM = 12  # prumer der
__SPACING = 6  # vzdalenost mezi dirama [mm]
__TLOUSTKA_STENY = 6  # tloustka steny mezi dirou a okrajem disku
# ---- variable revolver variables ----------
__VREVOLVER = False
#__HOLES = (0.2656, 0.2656, 0.3281, 0.3281, 0.4063, 0.4063, 0.4063, 0.4844)
__HOLES = (8, 8, 8, 10, 10, 10, 12)     # prumer der [mm]
__SPACING_V = 6                         # vzdalenost mezi dirama [mm]
__TLOUSTKA_STENY_V = 6                  # tloustka steny mezi dirou a okrajem disku
# ---- drill allowance variables ----------
__DALLOW = True


def sineBarRadius(delka, r1, uhel):
    """Vypocet polomeru valcu pro nastaveni pozadovaneho uhlu.
    IN:
        delka = vzdalenost os valecku
        r1 = prumer prvniho valecku
        uhel = uhel ktery chci dostat, uhel mezi vodorovnou rovinou a rovinou valecku
    OUT:
        r2 = prumer druheho valecku
        -------------------------------------------------------------------------------
    VZOREC:     r2 = 2 * delka * sin(0.5 * uhel) + r1
    """
    import math
    import Python.misc.mathPhys as mfz
    return 2 * delka * math.sin(0.5 * mfz.deg2rad(uhel)) + r1


def revolverRegular(holes, diameter, spacing, wall):
    """ Spocita prumer materialu a radius na kterem se maji vrtat diry pro stejny prumer der.
    IN:
        holes       - pozadovany pocet der
        diameter    - pozadovany polomer der1 [mm]
        spacing     - pozadovana vzdalenost mezi dirama [mm]
        wall        - tloustka steny mezi dirou a okrajem disku [mm]
    OUT:
        tuple (radius pro vrtani der, min. prumer materialu)"""
    import math
    r = ((holes * diameter) + (holes * spacing)) / (2 * math.pi)  # polomer kruznice pro stredy
    rr = 2 * (r + diameter / 2 + wall)  # prumer materialu
    return (r, rr)


def variableRevolver(holes, spacing, wall):
    """Spocita prumer materialu a radius na kterem se maji vrtat diry pro pripad ruznych prumeru der.
    IN:
        holes       - pole prumeru der
        spacing     - pozadovana vzdalenost mezi dirama [mm]
        wall        - tloustka steny mezi dirou a okrajem disku [mm]
    OUT:
        tuple (radius pro vrtani der, min. prumer materialu)"""
    import math
    soucet = 0
    maxPrumer = 0
    for dira in holes:
        soucet = soucet + dira  # soucet prumeru der
        if dira > maxPrumer: maxPrumer = dira  # nalezeni max prumeru
    r = ((len(holes) * spacing) + soucet) / (2 * math.pi)  # polomer kruznice pro stredy
    rr = 2 * (r + (maxPrumer / 2) + wall)  # prumer materialu
    return (r, rr)


if __name__ == '__main__':
    if __SINE_BAR: print(sineBarRadius(__DELKA, __R1, 10))

    if __REVOLVER:
        import math as m
        print("!Revolver stejne diry!")
        v = revolverRegular(__NO_HOLES, __HOLE_DIAM, __SPACING, __TLOUSTKA_STENY)
        print("presny vysledek: ", v)
        vysledky = []
        for num in v:
            vysledky.append(m.ceil(num))
        vysledky = tuple(vysledky)
        print("radius pro navrtani der: %3.0f mm\nmin. prumer materialu: %3.0f mm" % vysledky)

    if __VREVOLVER:
        from math import ceil as c
        print("!Revolver nestejne diry!")
        v =(variableRevolver(__HOLES, __SPACING_V, __TLOUSTKA_STENY_V))
        print("presny vysledek: ", v)
        vysledky = []
        for num in v:
            vysledky.append(c(num))
        vysledky = tuple(vysledky)
        print("radius pro navrtani der: %3.0f mm\nmin. prumer materialu: %3.0f mm" % vysledky)

    if __DALLOW:
        import math
        import Python.misc.myTools as myTools
        import Python.misc.mathPhys as mfz
        """ Vypocte hloubku hrotu vrtaku na zaklade prumeru vrtaku a vrcholoveho uhlu."""

        print('Vypocet pridavku k hloubce diry pri vrtani.')
        uhel = myTools.numUsrIn('zadej uhel cela vrtaku: ', 118)
        prumer = myTools.numUsrIn('zadej prumer vrtaku: ', 10)
        hloubka = (prumer/2)/math.tan(mfz.deg2rad(uhel/2))
        print('hloubka hrotu vrtaku: {:.2f}'.format(hloubka))



