#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
DivisionPlatePlain
Created on 02/02/2017, 08:18
Program spocita prumer kotoucku ktere je potreba naskladat kolem disku daneho prumeru aby
se dosahlo potrebneho deleni bez pouziti delici hlavy nebo neceho podobneho. Stredy kotoucku
reprezentuji pozice bodu.

@author: David Potucek
"""


def calculate_disks_radius(div, diam):
    import math
    radius = 0.5 * diam
    theta = 360 / div
    si = math.sin(math.radians(theta * 0.5))
    ra = (radius * si)/(1 - si)
    return ra


if __name__ == "__main__":
    import daptools.myTools as tools
    divisions = 14
    diameter = 112
    print('Program spocita prumer kotoucku ktere je potreba naskladat kolem disku daneho prumeru \naby se '
          'dosahlo potrebneho deleni bez pouziti delici hlavy nebo neceho podobneho. \nStredy kotoucku '
          'reprezentuji pozice bodu.')

    divisions = tools.num_usr_in('pocet deleni: ', divisions)
    diameter = tools.num_usr_in('prumer disku k deleni: ', diameter)

    smallDisk = calculate_disks_radius(divisions, diameter)
    print('prumer {} malych disku = {:.4f} mm'.format(divisions, smallDisk * 2))
