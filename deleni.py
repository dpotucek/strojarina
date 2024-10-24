#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 29, 2015
Vypocty k delici hlave

@author: david
'''

__RATIO = 40.0  # delici hlava otoci kotoucem 40x nez udela jednu otocku
__RATIO_TABLE = 120 # stul otoci packou 120x nez udela jednu otocku
__DIRY = (43, 42, 41, 39, 38, 37, 34, 30, 28, 25, 24)  # muj kotouc na delici hlave
__DIRY2 = (46, 47, 49, 51, 53, 54, 57, 58, 59, 62, 66)  # muj kotouc druha strana
__DIRY_CINA_1 = (61, 55, 47, 41, 33, 30, 27, 19)    # kotouc k ot. stolu
__DIRY_CINA_2 = (59, 51, 43, 39, 31, 28, 25, 23)    # kotouc k ot. stolu zezadu
__POCTY_DER = False
__VYPOCET_KOTOUCE = True


def prozkoumej_deleni(pocet_der, ratio=__RATIO):
    """Vypocte z pomeru delici hlavy a z poctu der v kotouci dosazitelna celociselna deleni.
    :param pocet_der - pocet der v kotouci
    :param ratio  pomer delici hlavy - nastaveno na default __RATIO
    :return tuple celociselnych deleni"""
    max_num = pocet_der * ratio
    out = []
    for iterator in range(1, int(max_num)):
        num = max_num / iterator
        if num.is_integer():
            out.append(int(num))

        if iterator > max_num:
            break
    return tuple(out)


def vypocti_pocet_der(deleni, ratio=__RATIO):
    """Vypocte z pozadovaneho deleni pri danem pomeru hlavy pocet der.
    :param deleni pozadovane deleni
    :param ratio pomer delici hlavy - nastaveno na default __RATIO  """
    base = ratio / deleni
    prubezne = 1
    while True:
        check_num = base * prubezne
        if check_num.is_integer():
            break
        else:
            prubezne += 1
        if prubezne > 150:
            print("too much holes, aborting")
            prubezne = 0
            break
    return prubezne


if __name__ == '__main__':
    from daptools.myTools import numUsrIn, strEnumUsrIn
    print('co chces vypocitat - pocty der v kotoucich nebo vypocist diry pro dosazeni deleni?')
    coChci = strEnumUsrIn('zadej bud p (pocty) nebo d (diry pro deleni? [d]', ('d', 'p'), 'd')
    if coChci == 'p':
        for dira in __DIRY2:
            deleni = prozkoumej_deleni(dira)
            print('pro pocet der: {} (max: {}) \n {}'.format(dira, dira*__RATIO, deleni))

    if coChci == 'd':
        pozadDeleni = numUsrIn('zadej pozadovane deleni: ', 26)
        pocetDer = vypocti_pocet_der(pozadDeleni)
        if pocetDer > 0:
            print('pro deleni {} je nutne mit pri pomeru hlavy {} obsazenych {} der v kotouci, '
                  'nebo celociselne nasobky tohoto cisla.'.format(pozadDeleni, __RATIO, pocetDer))
        else:
            print("ERROR occured...")
