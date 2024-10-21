#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
tappingDrills produkuje soubor zavitu a vrtaku k zahrnuti do LaTeX tabulky.
Soubor obsahuje udaje o zavitu a vrtaky pro ruzne sily zavitu.
Created on 05/10/2017, 13:39

@author: David Potucek
'''
from findThread import ThreadPool

__outputFile__ = '/home/david/Downloads/ThreadOutput.txt'
__DEBUG__ = False


class MetricThread():

    sily = (60, 65, 70, 75, 80, 85)

    def __init__(self, thread):
        self.vrtaky = []        # vrtaky pro standardni sily zavitu - predpocitane
        self.thread = thread
        self.name = thread.name
        self.diaInch = thread.diaInch
        self.diaMM = thread.diaMM
        self.pitchTPI = thread.pitchTPI
        self.pitchMM = thread.pitchMM
        self.coreDia = thread.coreDia
        self.coreMM = thread.coreMM
        self.depthInch = thread.depthInch
        self.depthMM = thread.depthMM
        for s in self.sily:
            self.vrtaky.append(self.countTapDrill(thread.diaMM, thread.pitchMM, s))

    def getDrill(self, strength):
        if strength <= 20 or strength > 100:
            raise ValueError('value of the strength is out of reasonable range. Range (20 - 100>')
        if strength == 60:
            return self.vrtaky[0]
        elif strength == 65:
            return self.vrtaky[1]
        elif strength == 70:
            return self.vrtaky[2]
        elif strength == 75:
            return self.vrtaky[3]
        elif strength == 80:
            return self.vrtaky[4]
        elif strength == 85:
            return self.vrtaky[5]
        else:
            return self.countTapDrill(self.thread.diaMM, self.thread.pitchMM, strength)

    def countTapDrill(self, prumer, stoupani, procenta=75):
        """spocita prumer vrtaku pro dany prumer, stoupani a pokud je dodan tak procento sily
        zavitu. Procento je nastaveno standardne na 75.
        Interni metoda klasy MetricThread
        :param prumer    core diameter
        :param stoupani stoupani zavitu
        :param procenta pozadovana sila zavitu

        Nedoporucuje se jit nad 80%, standardne jsou zavity delany na 75%
        """
        dia = prumer - (stoupani * 1.083 * procenta / 100)
        return dia

    def countTapDrillSingle(self, prumer, stoupani, procenta=75):         # static method class MetricThread
        """Stejna metoda jako countTapDrill(), ale urcena k pouziti bez konstrukce objektu MetricThread."""
        dia = prumer - (stoupani * 1.083 * procenta / 100)
        return dia

    def __lt__(self, other):        # metoda less then. Pouzivano pro porovnavani instanci Thread
        return self.diaMM < other.diaMM

def testCountDrill():
    print('test spravnosti funkce')
    prcnt = 60
    prum = 4.0
    stoup = 0.7
    vrtak = MetricThread.countTapDrillSingle(prum, stoup, prcnt)       # vysledek 3.55
    print('pro zavit {0} se stroupanim {1} a silou zavitu {2}% pouzij vrtak {3:.2f}'.format(prum, stoup, prcnt, vrtak))
    print('spravny vysledek je: 3.55 mm')

def putHeader(file):
    file.write('Soubor k zahrnuti do LaTeX tabulky. Use copy/paste.\n')

if __name__ == "__main__":
    # from misc.LaTeXHelper import generateTableRow
    # testCountDrill()      # overeni funkcnosti vypoctu

    pool = ThreadPool()
    metric = pool.listMetricThreads()
    depthThreads = []
    for t in metric:
        depthThreads.append(MetricThread(t))

    depthThreads.sort()         # setrideni zavitu podle prumeru
    with open(__outputFile__, 'w+') as file:
        putHeader(file)
        for d in depthThreads:      # generovani polozek zavitu do tabulky v LaTexu
            # urceno pro testovani outputu bez nutnosti psat do file
            if (__DEBUG__):
                print('{} & {:.2f} & {} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f}\\\\'.format(d.name,
                    float(d.pitchMM), d.coreMM, float(d.getDrill(60)), float(d.getDrill(65)),
                    float(d.getDrill(70)), float(d.getDrill(75)), float(d.getDrill(80)), float(d.getDrill(85))))

            # samotne psani do souboru.
            file.write('{} & {:.2f} & {} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f}\\\\\n'.format(d.name,
                float(d.pitchMM), d.coreMM, float(d.getDrill(60)), float(d.getDrill(65)),
                float(d.getDrill(70)), float(d.getDrill(75)), float(d.getDrill(80)), float(d.getDrill(85))))
        print('file {} written!'.format(__outputFile__))
    file.close()
