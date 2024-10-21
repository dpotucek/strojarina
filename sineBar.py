#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 3.11.2016

@author: David Potucek
'''

import Python.misc.myTools as tools
import math

def getUserInput():
    m = 'c'
    a = 15
    cyl = 20
    m = tools.strEnumUsrIn('do you want to use link method or method of contacting cylinders?: ', ('l', 'c'), m)
    a = tools.numUsrIn("required angle?: ", a)
    cyl = tools.numUsrIn('size of the bigger cylinder?: ', cyl)
    return m, a, cyl

def calculateLinkSineBar(angle, cyl):
    rozvor = tools.numUsrIn('cylinder center distance?:', 3)
    prumer = 2 * rozvor * math.sin(0.5 * math.radians(angle)) + cyl
    print('size of bigger cylinder {} and distance between centers of {}'.format(cyl, rozvor))
    print('smaller cylinder diameter to obtain angle of {} is {}.'.format(angle, prumer))
    return prumer


def calculateContactSineBar(angle, cyl):
    vyrazSinu = math.sin(0.5 * math.radians(angle))
    prumer = cyl * (1 - vyrazSinu)/(1 + vyrazSinu)
    print('smaller cylinder diameter to obtain angle of {} deg is {}.'.format(angle, prumer))
    print('with diameter of bigger cylinder of {}'.format(cyl))
    return prumer

def testLinkMethod():
    dist = calculateLinkSineBar(10, 0.375)
    print('\n\nTEST Result: with default value of link [3], result shall be {}, is {}'.format(0.8979, dist))
    import sys
    sys.exit()

def testContactMethod():
    dist = calculateContactSineBar(1.5, 0.75)
    print('\n\nTEST Result: result shall be {}, is {}'.format(0.7306, dist))
    import sys
    sys.exit()


if __name__ == "__main__":
    print('Program to calculate sine bar cylinders.')
    # testLinkMethod()
    # testContactMethod()
    method, angle, cSize = getUserInput()

    if method == 'l':
        calculateLinkSineBar(angle, cSize)
    else:
        calculateContactSineBar(angle, cSize)