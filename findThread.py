#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Oct 29, 2016

@author: David Potucek
"""

__FILE__ = "FINDTHRD.DAT"

class Thread():
    """Represents thread with parameters. Works with all threads. For metric threads only see
    tappingDrills.py file, includes super class of Thread -> MetricThread.
    Created by David on 29/10/2016
    """

    def __init__(self, nom, dI, dM, pTPI, pMM, cdi='N/A', cmm='N/A', deI='N/A', dmm='N/A'):
        """Constructor for Thread, core diameters and depths are not mandatory."""
        self.name = nom
        self.diaInch = dI
        self.diaMM = dM
        self.pitchTPI = pTPI
        self.pitchMM = pMM
        self.coreDia = cdi
        self.coreMM = cmm
        self.depthInch = deI
        self.depthMM = dmm

    def get_pitch(self, mm = True):
        """returns pitch of the thread, default in mm."""
        if mm: return self.pitchMM
        else: return self.pitchTPI

    def get_diameter(self, mm = True):
        """returns major diameter of the thread, default in mm."""
        if mm: return self.diaMM
        else: return self.diaInch

    def get_param_all(self):
        """Returns all the parameters of the thread in touple.
        Sequence: name, major diameter[in], major diameter[mm], pitch[in], itch[mm],
        core diameter[in], core diameter[mm], depth[in], depth[mm].
        Last 4 parameters might not be available (N/A)."""
        return (self.name, self.diaInch, self.diaMM, self.pitchTPI, self.pitchMM, self.coreDia, self.coreMM, self.depthInch, self.coreMM)

    def fits_dimension(self, cislo):
        """Returns True iff any of major diameter or pitch in both mm or inch fits given dimension.
        :param cislo: number to compare thread with
        :return: True or False
        """
        if self.diaInch == cislo:
            return True
        elif self.diaMM == cislo:
            return True
        elif self.pitchMM == cislo:
            return True
        elif self.pitchTPI == cislo:
            return True
        else:
            return False

    def fits_major_diameter(self, cislo):
        """Returns True iff major diameter (mm or in) fits given dimension.
        :param cislo: number to compare thread with
        :return: True or False
        """
        if self.diaMM == cislo:
            return True
        elif self.diaInch == cislo:
            return True
        else:
            return False

    def fits_pitch(self, cislo):
        """ Returns True iff pitch (mm or in) fits given dimension.
        :param cislo: number to compare thread with
        :return: True or False
        """
        if self.pitchMM == cislo:
            return True
        elif self.pitchTPI == cislo:
            return True
        else:
            return False

    def fits_major_diameter_mm(self, cislo):
        """Returns True iff true diameter in mm fits given dimension.
        :param cislo: number to compare thread with
        :return: True or False"""
        if self.diaMM == cislo:
            return True
        else:
            return False

    def fits_major_diameter_in(self, cislo):
        """Returns True iff true diameter in in fits given dimension.
        :param cislo: number to compare thread with
        :return: True or False
        """
        if self.diaInch == cislo:
            return True
        else:
            return False

    def fits_pitch_mm(self, cislo):
        """Returns True iff pitch in mm fits given dimension.
        :param cislo:
        :return: True/False
        """
        if self.pitchMM == cislo:
            return True
        else:
            return False

    def fits_pitch_tpi(self, cislo):
        """Returns True iff pitch in mm fits given dimension.
        :param cislo:
        :return: True/False
        """
        if self.pitchTPI == cislo:
            return True
        else:
            return False

    def is_metric(self):
        """Returns true if thread is metric."""
        if self.name[0] == 'M':
            return True
        else:
            return False


    def __str__(self):
        strX = ("Thread name = " + str(self.name) + "\nmajor diameter =\t" + str(self.diaMM) + ' mm;\t' + str(self.diaInch) + ' in\n' +
        "pitch = \t\t\t" + str(self.pitchMM) + ' mm;\t' + str(self.pitchTPI) + ' TPI\n' + "core diameter =\t\t" + str(self.coreMM) +
        ' mm;\t' + str(self.coreDia) + ' in\n' + 'depth =\t\t\t\t' + str(self.depthMM) + ' mm;\t' + str(self.depthInch) + ' in\n')
        return str(strX)

class ThreadPool:
    """Reads all threads from source file FINDTHRD.TXT and allows operations on this collection."""

    def __init__(self):
        self.threadBin, self.threadData = self.read_up_data()  # fill the bin with threads from the file

    def search_threads(self, cislo, units ='mm', kriterium='pitch'):
        """Searches threads in kos container for cislo."""
        fit = []
        if units == 'mm' or units == 'tpi' or kriterium == 'pitch' or kriterium == 'diameter':
            if kriterium == 'diameter':
                if units == 'mm':
                    for t in self.threadBin:
                        if t.fits_major_diameter_mm(cislo):
                            fit.append(t)
                else:
                    for t in self.threadBin:
                        if t.fits_major_diameter_in(cislo):
                            fit.append(t)
            else:           # kriterium == 'pitch'
                if units == 'mm':
                    for t in self.threadBin:
                        if t.fits_pitch_mm(cislo):
                            fit.append(t)
                else:
                    for t in self.threadBin:
                        if t.fits_pitch_tpi(cislo):
                            fit.append(t)
        else:
            raise ValueError("expected diameter or pitch in mm or in, got: " + kriterium + ' ' + units)
        return fit

    def read_up_data(self):
        """Reads data from file, creates threads and returns thread tuple."""
        threads, data = self.open_data_file()  # v threads jsou jmena zavitu, v data jsou data zavitu
        seznam = []
        for t in data:
            if t == '\n': continue
            thread = self.extract_thread(t)
            seznam.append(thread)  # naplneny list threadu
        return tuple(seznam), threads

    def open_data_file(self):
        """Reads file FINDTHRD.TXT."""
        dataLines = []
        types = []
        with open(__FILE__) as file:
            counter = 0
            for line in file:
                if counter > 4 and counter < 27:
                    types.append(line)
                if (counter > 27) and (counter < 36):
                    pass
                if counter >= 32 and not line.startswith("ENDOFDATA"):
                    if line.startswith(';'): pass
                    else: dataLines.append(line)
                if line.startswith("ENDOFDATA"):
                    break
                counter += 1
        return tuple(types), tuple(dataLines)

    def extract_thread(self, t):
        """extracts information from file line and returns new Thread"""
        n = t[0:11].strip()         # thread name
        di = t[12:19].strip()       # diameter [in]
        dmm = t[20:27].strip()      # diameter [mm]
        ptp = t[28:34].strip()      # pitch [tpi]
        pmm = t[35:42].strip()      # pitch [mm]
        cd = t[43:50]               # core diameter [in]
        cmm = t[51:58]              # core diameter [mm]
        din = t[59:66]              # depth [in]
        dmmd = t[67:72]             # depth [mm]

        # korekce kvuli moznym chybejicim cislum
        if di.isspace() or di == '': di = 'N/A'     # metricke zavity nemaji inch diam
        else: di.strip()
        if ptp.isspace() or ptp == '': ptp = 'N/A'     # metricke zavity nemaji TPI pitch
        else: ptp.strip()
        if cd.isspace() or cd == '': cd = 'N/A'
        else: cd.strip()
        if cmm.isspace() or cmm == '': cmm = 'N/A'
        else: cmm.strip()
        if din.isspace() or din == '': din = 'N/A'
        else: din.strip()
        if dmmd.isspace() or dmmd == '': dmmd = 'N/A'
        else: dmmd.strip()
        if (di == 'N/A'):               # metric thread
            return Thread(n, di, float(dmm), ptp, float(pmm), cd, cmm, din, dmmd)
        else:                           # all other threads
            return Thread(n, float(di), float(dmm), float(ptp), float(pmm), cd, cmm, din, dmmd)

    def list_threads(self):
        for th in self.threadData:
            print(th)

    def list_metric_threads(self):
        """Vrati metricke zavity v tuple."""
        from daptools.myTools import contains as contain
        metric = []
        for t in self.threadBin:
            if t.is_metric() and not contain(t.name, 'HOLTZ'):   # vyhazuji jine nez metricke a Holtzapfels zavity
                metric.append(t)
        return tuple(metric)

def ui_inint():
    from daptools.myTools import str_enum_usr_in, num_usr_in
    unit = 'N/A'
    kriterium = 'N/A'

    unit = str_enum_usr_in("would you like to search for in or mm values? Enter in or mm.",
                        ('mm', 'in'), 'mm')
    kriterium = str_enum_usr_in("would you like to search for diameter of pitch? Enter d or p:",
                             ('d', 'p'), 'd')
    cislo = num_usr_in("please type value of the thread to search for", 10)
    return cislo, unit, kriterium


if __name__ == "__main__":


    cislo, units, kriterium = ui_inint()

    if units == 'mm':
        print('looking for metric threads', end="")
        if kriterium == 'd':
            print(' with diameter: ' + str(cislo))
        else:
            print(' with pitch: ' + str(cislo))
    else:
        print('looking for inch threads', end="")
        if kriterium == 'd':
            print(' with diameter: ' + str(cislo))
        else:
            print(' with pitch: ' + str(cislo))

    if kriterium == 'd':
        kriterium = 'diameter'
    else:
        kriterium = 'pitch'

    threads = ThreadPool()    # fill the bin with threads from the file
    vysl = threads.search_threads(cislo, units, kriterium)

    if vysl:
        for v in vysl:
            print(v.name)
    else:
        print("None found!")
    from daptools.myTools import str_enum_usr_in as userInput
    vypis = userInput('would you like to display list of thread descriptions? \nIf so, input y, otherwise anything else:\n',
                      ('y', '?'), 'n')
    if vypis == 'y':
        threads.list_threads()