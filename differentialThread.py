#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
differentialThread
Created on 3.11.2016
Program vybere kombinaci dvou dostupnych zavitu nutnuch pro pozadovane stoupani.
viz https://en.wikipedia.org/wiki/Differential_screw

@author: David Potucek
'''

# __dataFile__ = '/Users/david/MySmallProjects/experiments/strojarina/DIFFTHRD.DAT'
__dataFile__ = "DIFFTHRD.DAT"

def parseData(radky):
    tpi = []
    mm = []
    mms = False
    for radek in radky:
        if radek == '\n':
            continue
        if radek.startswith('tpi'):
            mms = False
            continue
        if radek.startswith('mm'):
            mms = True
            continue
        cislo = float(radek)
        if mms:
            mm.append(cislo)
        else:
            tpi.append(cislo)
    return tuple(tpi), tuple(mm)

def calculateDiffThread(stoupaniHrube, stoupaniJemne):
    """
    Counts real effective pitch of the thread based on 2 supplied standard pitches.
    :param stoupaniHrube: pitch of thread 1
    :param stoupaniJemne: pitch of thread 2
    :return: Pe: effective pitch of differential thread
    """
    if stoupaniHrube == 0 or stoupaniJemne == 0:
        raise ValueError('got zero argument')
    if stoupaniHrube == stoupaniJemne:
        raise ValueError('differential thread requires different pitches.')
    Pe = 1 / ((1 / stoupaniHrube) - (1 / stoupaniJemne))
    return abs(Pe)

def __combineVariants(cislo, values):
    vysledek = []
    best = 3e6

    for coarse in reversed(values):
        for fine in values:
            if coarse == fine or coarse < fine:
                continue
            pe = calculateDiffThread(coarse, fine)
            d = abs(cislo - pe)
            if d <= best:
                vysledek = (coarse, fine, pe)
                best = d
    return vysledek

def vyzkousejKombinace(cislo, tpi, mm, units = 'mm'):
    if units == 'mm':
        vysledek = __combineVariants(cislo, mm)
    elif units == 'in':
        vysledek = __combineVariants(cislo, tpi)
    else:
        vysledek = __combineVariants(cislo, mm + tpi)
    return vysledek



if __name__ == "__main__":
    from Python.misc.myTools import readDataFile
    import sys
    print('Program vybere kombinaci dvou dostupnych zavitu nutnuch pro pozadovane stoupani. \n'
          'viz https://en.wikipedia.org/wiki/Differential_screw')
    lines = readDataFile(__dataFile__)
    stoupaniTPI, stoupaniMM = parseData(lines)  # ve stoupanich jsou data pro palcova a metricka stoupani
    print('read {} items'.format(len(stoupaniTPI) + len(stoupaniMM)))

    zadanyZavit = 1.8
    jednotky = 'mm'
    kombinace = []
    try:
        zadanyZavit = float(input('zadej požadované stoupání: \n'))
        jednotky = input('hledat v mm, in, nebo obou [mm]\n')
    except ValueError:
        print('nezadal jsi požadované hodnoty, beru default stoupání závitu: {:2f}, jednotky {}'.format(zadanyZavit, jednotky))

    if zadanyZavit in stoupaniMM or zadanyZavit in stoupaniTPI:
        print('Tohle si můžeš vytočit sám, máš na to nástroje!.')
        sys.exit(0)
    if jednotky == 'mm' or jednotky == 'in':
        kombinace = vyzkousejKombinace(zadanyZavit, stoupaniTPI, stoupaniMM, jednotky)
    else:
        kombinace = vyzkousejKombinace(zadanyZavit, stoupaniTPI, stoupaniMM)

    cThread = kombinace[0]
    fThread = kombinace[1]
    ePitch = kombinace[2]

    aux = ''                # nastaveni jednotek pro vypis
    if jednotky == 'mm':
        aux = 'mm/zavit'
    else:
        aux = 'TPI'

    print('z dostupnych závitů je nejbližší kombinace k {:.2f} {}'.format(zadanyZavit, aux))
    print('hrubý závit: {:.2f}'.format(cThread))
    print('jemný závit: {:.2f}'.format(fThread))
    print('s efektivní hodnotou stoupání: {:.3f}'.format(ePitch))
    print('')

    cNutThic = 4
    fNutThic = 2
    motion = 15

    try:
        cNutThic = float(input('zadej tloušťku hrubé (fixní) matky:  \n'))
        fNutThic = float(input('zadej tloušťku jemné (pohyblivé) matky:  \n'))
        motion = float(input('zadej požadovaný pohyb :  \n'))
    except ValueError:
        print('nezadal jsi požadované údaje, beru default:\n',\
              'hrubá matka: ', cNutThic, ' ',jednotky, '\n',\
              'jemná matka: ', fNutThic, ' ', jednotky,'\n',\
              'požadovaný pohyb: ', motion, ' ', jednotky, '\n')

    print('efektivní stoupání: {:.2f} {}'.format(ePitch, jednotky))
    print('pohyb diferenciálního závitu na jednu otáčku: {:.2f} {}'.format(1/ePitch, jednotky))
    print('počet otáček k dosažení požadovaného posuvu: {:.2f}'.format(motion*ePitch))
    print('minimum délky hrubého závitu: {:.2f}'.format(cNutThic + motion * ePitch/fThread))
    print('minimum délky jemného závitu: {:.2f}'.format(fNutThic + motion * ePitch/cThread))
    print('maximum vzdálenosti mezi matkami: {:.2f}'.format(motion * ePitch/cThread))
    print('minimum vzdálenosti mezi matkami: {:.2f}'.format(motion * ePitch/fThread))