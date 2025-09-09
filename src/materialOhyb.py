#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
materialOhyb - jak dlouhy material o dane tloustce budu potrebovat na
ohyb o polomeru x? Quick & dirty solution!! Funguje pro ocel, ostatni jsem nezkousel.

Created on 01/06/2017, 09:26

@author: David Potucek
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../DaPTools/src'))
import daptools.mathPhys as mathPhys
import daptools.myTools as myTools

if __name__ == "__main__":
    print('Zadej nasledující údaje pro výpočet materiálu na ohyb.')
    print('je to quick & dirty, ale chodi to + - dobře pro ocelove plechy.')
    tloustka = myTools.num_usr_in('Tloušťka materiálu: ', 3)  # 0.125
    radius = myTools.num_usr_in('Radius ohybu[mm]: ', 76)        # 3.0
    uhel = myTools.num_usr_in('Úhel ohybu[]', 90.0)

    tloustka = myTools.convert_mm_2_in(tloustka)
    radius = myTools.convert_mm_2_in(radius)

    ang = mathPhys.deg2rad(uhel)

    x = 0.4 * tloustka

    if radius < (2 * tloustka):
        x = 0.3333 * tloustka
    if radius > (4 * tloustka):
        x = 0.5 * tloustka

    pridavek = ang * (radius + x)

    lvnejsi = ang*(radius + tloustka)
    lvnitrni = ang * radius

    print('délka vnějšku ohybu: {:.2f}'.format(myTools.convert_in_2_mm(lvnejsi)))
    print('délka vnitřku ohybu: {:.2f}'.format(myTools.convert_in_2_mm(lvnitrni)))
    print('délka materiálu nutná pro ohyb: {:.2f}'.format(myTools.convert_in_2_mm(pridavek)))
