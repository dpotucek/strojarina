#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
tappingDrills produkuje soubor zavitu a vrtaku k zahrnuti do LaTeX tabulky.
Soubor obsahuje udaje o zavitu a vrtaky pro ruzne sily zavitu.
Created on 05/10/2017, 13:39

@author: David Potucek
"""
from findThread import ThreadPool


class TappingDrills:
    """Trida pro vypocty vrtaku pro zavity."""
    
    def __init__(self, output_file='/home/david/Downloads/ThreadOutput.txt', debug=False):
        self.output_file = output_file
        self.debug = debug
        
    def test_count_drill(self):
        print('test spravnosti funkce')
        prcnt = 60
        prum = 4.0
        stoup = 0.7
        vrtak = MetricThread.countTapDrillSingle(prum, stoup, prcnt)
        print('pro zavit {0} se stroupanim {1} a silou zavitu {2}% pouzij vrtak {3:.2f}'.format(prum, stoup, prcnt, vrtak))
        print('spravny vysledek je: 3.55 mm')
        
    def put_header(self, file):
        file.write('Soubor k zahrnuti do LaTeX tabulky. Use copy/paste.\n')
        
    def generate_output(self):
        pool = ThreadPool()
        metric = pool.list_metric_threads()
        depth_threads = []
        for t in metric:
            depth_threads.append(MetricThread(t))

        depth_threads.sort()
        with open(self.output_file, 'w+') as file:
            self.put_header(file)
            for d in depth_threads:
                if self.debug:
                    print('{} & {:.2f} & {} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f}\\\\\\\\'.format(d.name,
                        float(d.pitchMM), d.coreMM, float(d.getDrill(60)), float(d.getDrill(65)),
                        float(d.getDrill(70)), float(d.getDrill(75)), float(d.getDrill(80)), float(d.getDrill(85))))

                file.write('{} & {:.2f} & {} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f} & {:.2f}\\\\\\\\\n'.format(d.name,
                    float(d.pitchMM), d.coreMM, float(d.getDrill(60)), float(d.getDrill(65)),
                    float(d.getDrill(70)), float(d.getDrill(75)), float(d.getDrill(80)), float(d.getDrill(85))))
            print('file {} written!'.format(self.output_file))


class MetricThread:

    sily = (60, 65, 70, 75, 80, 85)

    def __init__(self, thread):
        self.vrtaky = []
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

    @staticmethod
    def countTapDrillSingle(prumer, stoupani, procenta=75):
        """Stejna metoda jako countTapDrill(), ale urcena k pouziti bez konstrukce objektu MetricThread."""
        dia = prumer - (stoupani * 1.083 * procenta / 100)
        return dia

    def __lt__(self, other):
        return self.diaMM < other.diaMM

def putHeader(file):
    td = TappingDrills()
    td.put_header(file)


if __name__ == "__main__":
    td = TappingDrills()
    td.generate_output()