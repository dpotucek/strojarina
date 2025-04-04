#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on 3.11.2016

@author: David Potucek
"""

import daptools.myTools as tools
import math

def get_user_input():
    m = 'c'
    a = 15
    cyl = 20
    m = tools.str_enum_usr_in('do you want to use link method or method of contacting cylinders?: ', ('l', 'c'), m)
    a = tools.num_usr_in("required angle?: ", a)
    cyl = tools.num_usr_in('size of the bigger cylinder?: ', cyl)
    return m, a, cyl

def calculate_link_sine_bar(angle, cyl):
    rozvor = tools.num_usr_in('cylinder center distance?:', 3)
    prumer = 2 * rozvor * math.sin(0.5 * math.radians(angle)) + cyl
    print('size of bigger cylinder {} and distance between centers of {}'.format(cyl, rozvor))
    print('smaller cylinder diameter to obtain angle of {} is {}.'.format(angle, prumer))
    return prumer


def calculate_contact_sine_bar(angle, cyl):
    vyraz_sinu = math.sin(0.5 * math.radians(angle))
    prumer = cyl * (1 - vyraz_sinu)/(1 + vyraz_sinu)
    print('smaller cylinder diameter to obtain angle of {} deg is {}.'.format(angle, prumer))
    print('with diameter of bigger cylinder of {}'.format(cyl))
    return prumer

def test_link_method():
    dist = calculate_link_sine_bar(10, 0.375)
    print('\n\nTEST Result: with default value of link [3], result shall be {}, is {}'.format(0.8979, dist))
    import sys
    sys.exit()

def test_contact_method():
    dist = calculate_contact_sine_bar(1.5, 0.75)
    print('\n\nTEST Result: result shall be {}, is {}'.format(0.7306, dist))
    import sys
    sys.exit()


if __name__ == "__main__":
    print('Program to calculate sine bar cylinders.')
    method, angle, cSize = get_user_input()

    if method == 'l':
        calculate_link_sine_bar(angle, cSize)
    else:
        calculate_contact_sine_bar(angle, cSize)