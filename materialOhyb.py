#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
materialOhyb - jak dlouhy material o dane tloustce budu potrebovat na
ohyb o polomeru x? Quick & dirty solution!! Funguje pro ocel, ostatni jsem nezkousel.

Created on 01/06/2017, 09:26

@author: David Potucek
'''

import Python.misc.mathPhys as mathPhys
import Python.misc.myTools as myTools

if __name__ == "__main__":
    print('Zadej nasledující údaje pro výpočet materiálu na ohyb.')
    print('je to quick & dirty, ale chodi to + - dobře pro ocelove plechy.')
    tloustka = myTools.numUsrIn('Tloušťka materiálu: ', 3)  # 0.125
    radius = myTools.numUsrIn('Radius ohybu[mm]: ', 76)        # 3.0
    uhel = myTools.numUsrIn('Úhel ohybu[]', 90.0)

    tloustka = myTools.convertMm2In(tloustka)
    radius = myTools.convertMm2In(radius)

    ang = mathPhys.deg2rad(uhel)

    x = 0.4 * tloustka

    if (radius < (2 * tloustka)):
        x = 0.3333 * tloustka
    if (radius > (4 * tloustka)):
        x = 0.5 * tloustka

    pridavek = ang * (radius + x)

    lvnejsi = ang*(radius + tloustka)
    lvnitrni = ang * radius

    print('délka vnějšku ohybu: {:.2f}'.format(myTools.convertIn2Mm(lvnejsi)))
    print('délka vnitřku ohybu: {:.2f}'.format(myTools.convertIn2Mm(lvnitrni)))
    print('délka materiálu nutná pro ohyb: {:.2f}'.format(myTools.convertIn2Mm(pridavek)))
