#!/usr/bin/python 3
# -*- coding: utf-8 -*-
'''
Spocita parametry dvou remenic a delku remene.
Poskytuje dve metody: calculate2Pulleys() a findDrivenDiameter().

calculate2Pulleys() na zaklade dodanych RMP, prumeru obou remenic a vzdalenosti stredu
vrati otacky hnane remenice a celkovou delku remenu.

findDrivenDiameter() na zaklade dodanych otacek a prumeru hnaci remenice a pozadovanych otacek
hnane remenice vrati prumer hnane tak aby mela pozadovane otacky.

Created on 28/06/2018, 10:38

@author: David Potucek
'''

from math import pi as pi

driverRPM = 1450
driverDia = 10
drivenDia = 18
distance = 65


def calculate2Pulleys(RPM, driverDia, drivenDia, distance):
    rpm = RPM * (driverDia/drivenDia)
    length = ((pi * driverDia)/2) + ((pi * drivenDia)/2 + (2*distance))
    return (rpm, length)

def findDrivenDiameter(RPMDriver, RPMRequest, driverDia):
    if RPMDriver == RPMRequest:
        return driverDia
    else:
        return RPMDriver * driverDia / RPMRequest

def testPulley():
    print('\n******************** testovaci run ********************')
    print('pro prumer hnaci remenice o prumeru {} cm, otacky {} RPM,'.format(driverDia, driverRPM))
    print('prumeru hnane remenice {} cm a vzdalenosti stredu remenic od sebe {} cm'.format(drivenDia, distance))
    otacky, delka = calculate2Pulleys(driverRPM, driverDia, drivenDia, distance)
    print('vychazi: otacky hnane remenice: {:.2f} RPM, delka remene: {:.2f} cm'.format(otacky, delka))
    print('')
    print('******************** zpetne ********************')
    prumer = findDrivenDiameter(driverRPM, 805, driverDia)
    print('pro remenici o prumeru {} a otackach {} hledame prumer hnane remenice abychom dosahli otacek 805 RPM'.
          format(driverDia, driverRPM))
    print('melo by vyjit neco kolem 18 cm viz vyse, vychazi {:.2f} cm.'.format(prumer))




if __name__ == "__main__":

    testPulley()

