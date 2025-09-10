#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 29, 2015
Vypocty k delici hlave

@author: david
'''


class DeliciHlava:
    """Trida pro vypocty delici hlavy."""
    
    def __init__(self, ratio=40.0, ratio_table=120):
        self.ratio = ratio
        self.ratio_table = ratio_table
        self.diry = (43, 42, 41, 39, 38, 37, 34, 30, 28, 25, 24)
        self.diry2 = (46, 47, 49, 51, 53, 54, 57, 58, 59, 62, 66)
        self.diry_cina_1 = (61, 55, 47, 41, 33, 30, 27, 19)
        self.diry_cina_2 = (59, 51, 43, 39, 31, 28, 25, 23)

    def prozkoumej_deleni(self, pocet_der):
        """Vypocte z pomeru delici hlavy a z poctu der v kotouci dosazitelna celociselna deleni.
        :param pocet_der - pocet der v kotouci
        :return tuple celociselnych deleni"""
        max_num = pocet_der * self.ratio
        out = []
        for iterator in range(1, int(max_num)):
            num = max_num / iterator
            if num.is_integer():
                out.append(int(num))
            if iterator > max_num:
                break
        return tuple(out)

    def vypocti_pocet_der(self, deleni, use_table=False):
        """Vypocte z pozadovaneho deleni pri danem pomeru hlavy pocet der.
        :param deleni pozadovane deleni
        :param use_table pokud True, pouzije ratio_table misto ratio
        :return pocet der"""
        # Vybere spravny pomer podle parametru
        active_ratio = self.ratio_table if use_table else self.ratio
        base = active_ratio / deleni
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


# Zachovani zpetne kompatibility
def prozkoumej_deleni(pocet_der, ratio=40.0):
    hlava = DeliciHlava(ratio)
    return hlava.prozkoumej_deleni(pocet_der)


def vypocti_pocet_der(deleni, ratio=40.0):
    hlava = DeliciHlava(ratio)
    return hlava.vypocti_pocet_der(deleni)


if __name__ == '__main__':
    from daptools.myTools import num_usr_in, str_enum_usr_in
    
    hlava = DeliciHlava()
    print('co chces vypocitat - pocty der v kotoucich nebo vypocist diry pro dosazeni deleni?')
    coChci = str_enum_usr_in('zadej bud p (pocty) nebo d (diry pro deleni? [d]', ('d', 'p'), 'd')
    if coChci == 'p':
        for dira in hlava.diry2:
            deleni = hlava.prozkoumej_deleni(dira)
            print('pro pocet der: {} (max: {}) \n {}'.format(dira, dira*hlava.ratio, deleni))

    if coChci == 'd':
        pozadDeleni = num_usr_in('zadej pozadovane deleni: ', 26)
        pocetDer = hlava.vypocti_pocet_der(pozadDeleni)
        if pocetDer > 0:
            print('pro deleni {} je nutne mit pri pomeru hlavy {} obsazenych {} der v kotouci, '
                  'nebo celociselne nasobky tohoto cisla.'.format(pozadDeleni, hlava.ratio, pocetDer))
        else:
            print("ERROR occured...")