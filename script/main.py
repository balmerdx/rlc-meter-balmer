# -*- coding: UTF-8 -*-
# balmer@inbox.ru 2014 RLC Meter
import sys, os, csv
from PyQt4 import QtCore, QtGui

import matplotlib
import time
import datetime
import threading
import json
import os.path

import usb_commands
import plot
import jplot

TITLE = 'RLC Meter "Balmer 303" (R) 2014'


class FormMain(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(FormMain, self).__init__(parent)

        self.setWindowTitle(TITLE)
        self.CreateMainFrame()
        pass        
        
    def CreateMainFrame(self):
        self.main_frame = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout()

        header_label = QtGui.QLabel('Измеритель комплексного сопротивления')

        vbox.addWidget(header_label)

        scan_button = QtGui.QPushButton('Просканировать диапазон')
        scan_button.clicked.connect(self.OnScan)
        vbox.addWidget(scan_button)

        scan_button = QtGui.QPushButton('Измерить')
        scan_button.clicked.connect(self.OnMeasure)
        vbox.addWidget(scan_button)

        graph_button = QtGui.QPushButton('Просмотреть последний график')
        graph_button.clicked.connect(self.OnGraph)
        vbox.addWidget(graph_button)

        graph_button = QtGui.QPushButton('Просмотреть график...')
        graph_button.clicked.connect(self.OnGraphOpen)
        vbox.addWidget(graph_button)

        cal_button = QtGui.QPushButton('Калибровка')
        cal_button.clicked.connect(self.OnCalibration)
        vbox.addWidget(cal_button)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        pass

    def initDevice(self):
        if not usb_commands.initDevice():
            QtGui.QMessageBox.about(self, TITLE, "Устройство не найдено.")
            return False
        return True

    def OnMeasure(self):
        if not self.initDevice():
            return
        form = plot.FormMeasure(TITLE, self)
        form.show()
        pass

    def OnScan(self):
        if not self.initDevice():
            return
        form = FormScan(self)
        form.setMaxAmplitude(jplot.MaxAmplitude())
        form.startDefault()
        form.show()
        pass

    def OnGraph(self):
        form = plot.FormDrawData(TITLE, self)
        form.setData('freq.json')
        form.show()
        pass

    def OnGraphOpen(self):
        fileName = QtGui.QFileDialog.getOpenFileName(filter='freq json (*.json)', caption=TITLE+' - Open freq.json')
        if len(fileName)==0:
            return
        form = plot.FormDrawData(TITLE, self)
        form.setData(fileName)
        form.show()
        pass

    def OnCalibration(self):
        if not self.initDevice():
            return
        form = FormCalibrationResistor(self)
        form.show()
        pass

def getCorrName(resistorData, Rname):
    return 'cor/R'+str(resistorData['resistorIndex'])+'V'+str(resistorData['VIndex'])+'I'+str(resistorData['IIndex'])+'_'+Rname+'.json'

#DX_KY_R
#X - индекс резистора 0..3
#Y - крэффициэнт усиления в канале I
#R - имя резистора, который измеряется

class FormScan(QtGui.QMainWindow):
    signalComplete = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(FormScan, self).__init__(parent)
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.end_thread = False

        dir = "cor"
        if not os.path.isdir(dir):
            print("mkdir=", os.mkdir(dir))
            
        self.setWindowTitle(TITLE)
        self.CreateMainFrame()
        self.maxAmplitude = None

        self.signalComplete.connect(self.ThClose)
        pass

    def generatorQuant(self):
        ok = next(self.generator, False)
        if not ok:
            self.timer.stop()
            self.signalComplete.emit()
        pass

    def generatorStart(self, gen):
        self.generator = gen
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.generatorQuant)
        self.timer.start(100)
        pass


    def startDefault(self, filename='freq.json'):
        self.scan_freq = usb_commands.ScanFreq()
        self.scan_freq.init(fileName=filename)

        self.progress_bar.setRange(0, self.scan_freq.count())
        self.progress_bar.setValue(0)

        self.generatorStart(self.UsbThread())
        pass

    def startCalibrateR(self, R, resistorData, Rname):
        '''
        resistorData - диапазоны на котором производится измерение
            [
            {
            'resistorIndex':1..3,
            'VIndex':0..7,
            'IIndex':0..7,
            },
            ...
            ]
        Rindex - индекс резистора для getCorrName
        '''
        self.generatorStart(self.CalibrateThreadR(R, resistorData, Rname))
        pass

    def setMaxAmplitude(self, maxAmplitude):
        self.maxAmplitude = maxAmplitude
        pass

    def CreateMainFrame(self):
        self.main_frame = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout()

        self.header_label = QtGui.QLabel('Сканирование диапазона.')
        vbox.addWidget(self.header_label)

        self.progress_bar = QtGui.QProgressBar()

        vbox.addWidget(self.progress_bar)

        self.info_label = QtGui.QLabel('info');
        vbox.addWidget(self.info_label);

        button_close = QtGui.QPushButton('Отменить.')
        button_close.clicked.connect(self.close)
        vbox.addWidget(button_close)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        pass

    def ThClose(self):#close from anntoer thread
        self.close()
        pass

    def closeEvent(self, event):
        self.end_thread = True
        event.accept()
        pass

    def UsbThread(self):
        while next(self.scan_freq):
            if self.end_thread:
                return
            self.SetInfo()
            yield True

        self.SetInfo()
        self.scan_freq.save()
        pass

    def CalibrateThreadR(self, R, resistorDatas, Rname):

        for resistorData in resistorDatas:            
            fileName = getCorrName(resistorData, Rname)
            self.header_label.setText(fileName)
            self.scan_freq = usb_commands.ScanFreq()

            VIndex=resistorData['VIndex']
            IIndex=resistorData['IIndex']
            div = resistorData['div']

            amplitude = usb_commands.DEFAULT_DAC_AMPLITUDE // div

            print("resistorIndex="+str(resistorData['resistorIndex']))
            print("VIndex="+str(VIndex), "IIndex="+str(IIndex), "amplitude="+str(amplitude))

            self.scan_freq.init(resistorIndex=resistorData['resistorIndex'],
                            VIndex=VIndex, IIndex=IIndex,
                            amplitude=amplitude, fileName=fileName,
                            maxAmplitude=self.maxAmplitude)

            self.progress_bar.setRange(0, self.scan_freq.count())
            self.progress_bar.setValue(0)

            while next(self.scan_freq):
                if self.end_thread:
                    return
                self.SetInfo()
                yield True

            self.SetInfo()
            self.scan_freq.jout['R'] = R
            self.scan_freq.save()

        pass

    def SetInfo(self):
        s = self
        s.progress_bar.setValue(s.scan_freq.current())
        jout = s.scan_freq.jfreq[-1]
        data = jplot.calculateJson(jout)
        info = ''
        info += 'F=' + str(int(data['F']))
        info += '\n' + 'R='+usb_commands.getResistorValueStr(usb_commands.resistorIdx)
        info += '\n' + 'KU='+str(usb_commands.getGainValueV(usb_commands.gainVoltageIdx))+'x'
        info += ' KI='+str(usb_commands.getGainValueI(usb_commands.gainCurrentIdx))+'x'
        info += '\n' + 'Rre='+str(jplot.formatR(data['R'].real))
        info += '\n' + 'Rim='+str(jplot.formatR(data['R'].imag))

        s.info_label.setText(info)
        pass

class FormCalibrationResistor(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(FormCalibrationResistor, self).__init__(parent)

        self.setWindowModality(QtCore.Qt.WindowModal)

        self.diapazon = []
        self.diapazon.append({'diapazon':0, 'value':1e2})
        self.diapazon.append({'diapazon':1, 'value':1e3})
        self.diapazon.append({'diapazon':2, 'value':1e4})
        self.diapazon.append({'diapazon':3, 'value':1e5})
        self.lines  = []
        self.labelOS = {}

        self.setWindowTitle(TITLE)
        self.CreateMainFrame()
        self.checkComplete()
        pass

    def CreateMainFrame(self):
        self.main_frame = QtGui.QWidget()
        vbox = QtGui.QVBoxLayout()

        header_label = QtGui.QLabel('Калибровка')

        vbox.addWidget(header_label)

        self.AddLine(vbox, '1 Ом', '1Om', 1.0, [
            {'resistorIndex': 0, 'VIndex':7, 'IIndex':0, 'div': 1},
            ])

        self.AddLine(vbox, '100 Ом', '100Om', 1e2, [
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':1, 'div': 2},
            #{'resistorIndex': 0, 'VIndex':0, 'IIndex':2, 'div': 4},

            {'resistorIndex': 0, 'VIndex':1, 'IIndex':0, 'div': 2},
            {'resistorIndex': 0, 'VIndex':2, 'IIndex':0, 'div': 4},
            {'resistorIndex': 0, 'VIndex':4, 'IIndex':0, 'div': 8},
            {'resistorIndex': 0, 'VIndex':6, 'IIndex':0, 'div': 16},
            #{'resistorIndex': 0, 'VIndex':7, 'IIndex':0, 'div': 32},
            ])

        self.AddLine(vbox, '1 KОм', '1KOm', 1e3, [
            #{'resistorIndex': 0, 'VIndex':0, 'IIndex':0, 'div': 1},
            #{'resistorIndex': 0, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':2, 'div': 1},

            {'resistorIndex': 1, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 1, 'VIndex':0, 'IIndex':1, 'div': 2},
            #{'resistorIndex': 1, 'VIndex':0, 'IIndex':2, 'div': 4},
            ])

        self.AddLine(vbox, '10 KОм', '10KOm', 1e4, [
            #{'resistorIndex': 1, 'VIndex':0, 'IIndex':0, 'div': 1},
            #{'resistorIndex': 1, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 1, 'VIndex':0, 'IIndex':2, 'div': 1},

            {'resistorIndex': 2, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 2, 'VIndex':0, 'IIndex':1, 'div': 2},
            #{'resistorIndex': 2, 'VIndex':0, 'IIndex':2, 'div': 4},
            ])

        self.AddLine(vbox, '100 KОм', '100KOm', 1e5, [
            #{'resistorIndex': 2, 'VIndex':0, 'IIndex':0, 'div': 1},
            #{'resistorIndex': 2, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 2, 'VIndex':0, 'IIndex':2, 'div': 1},

            {'resistorIndex': 3, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':1, 'div': 2},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':2, 'div': 4},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':4, 'div': 8},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':6, 'div': 16},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':7, 'div': 32},
            ])

        self.AddLineShort(vbox, [
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':1, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':2, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':4, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':6, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':7, 'IIndex':0, 'div': 1},
            ])

        self.AddLineOpen(vbox, [
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 0, 'VIndex':0, 'IIndex':2, 'div': 1},

            {'resistorIndex': 1, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 1, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 1, 'VIndex':0, 'IIndex':2, 'div': 1},

            {'resistorIndex': 2, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 2, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 2, 'VIndex':0, 'IIndex':2, 'div': 1},

            {'resistorIndex': 3, 'VIndex':0, 'IIndex':0, 'div': 1},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':1, 'div': 1},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':2, 'div': 1},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':4, 'div': 1},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':6, 'div': 1},
            {'resistorIndex': 3, 'VIndex':0, 'IIndex':7, 'div': 1},

            ])

        button_close = QtGui.QPushButton('Записать в FLASH')
        button_close.clicked.connect(self.OnWriteFlash)
        vbox.addWidget(button_close)


        button_close = QtGui.QPushButton('Закрыть')
        button_close.clicked.connect(self.close)
        vbox.addWidget(button_close)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)
        pass

    def AddLine(self, vbox, name, nameShort, value, data):
        line = { 'data': data, 'name': nameShort }
        hbox = QtGui.QHBoxLayout()

        label1 = QtGui.QLabel('Точное значение сопротивления ' + name + '=')
        hbox.addWidget(label1)
        edit = QtGui.QLineEdit()
        #validator = QtGui.QDoubleValidator()
        #validator.setRange(90, 250)
        #edit.setValidator(validator)

        edit.setText(str(value))
        hbox.addWidget(edit)
        line['edit'] = edit

        button = QtGui.QPushButton(name)
        button.clicked.connect(lambda: self.process(line) )
        hbox.addWidget(button)

        label = QtGui.QLabel('Не пройден')
        line['label'] = label
        label.setStyleSheet("QLabel { color : red; }");
        hbox.addWidget(label)

        vbox.addLayout(hbox)
        self.lines.append(line)
        pass

    def AddLineShort(self, vbox, data):
        title = 'Замкнутые щупы'
        name = 'short'
        line = { 'data': data, 'name': name }        
        hbox = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel(title)
        hbox.addWidget(label1)
        button = QtGui.QPushButton('Пуск.')
        button.clicked.connect(lambda: self.processShort(line))
        hbox.addWidget(button)
        label = QtGui.QLabel('XXX')
        line['label'] = label
        hbox.addWidget(label)
        vbox.addLayout(hbox)

        self.lines.append(line)
        pass

    def AddLineOpen(self, vbox, data):
        title = 'Открытые щупы'
        name = 'open'
        line = { 'data': data, 'name': name }        
        hbox = QtGui.QHBoxLayout()
        label1 = QtGui.QLabel(title)
        hbox.addWidget(label1)
        button = QtGui.QPushButton('Пуск.')
        button.clicked.connect(lambda: self.processOpen(line))
        #button.clicked.connect(lambda: self.OnCompleteOpenPass(line))
        
        hbox.addWidget(button)
        label = QtGui.QLabel('XXX')
        line['label'] = label
        hbox.addWidget(label)
        vbox.addLayout(hbox)

        self.lines.append(line)
        pass

    def process(self, line):
        R = float(line['edit'].text())
        form = FormScan(self)
        form.signalComplete.connect(self.OnCompleteProcess)
        form.startCalibrateR(R, line['data'], line['name'])
        form.show()
        pass

    def processShort(self, line):
        R = 0
        form = FormScan(self)
        form.signalComplete.connect(self.OnCompleteProcess)
        form.startCalibrateR(R, line['data'], line['name'])
        form.show()

    def processOpen(self, line):
        form = FormScan(self)
        form.signalComplete.connect(lambda:self.OnCompleteOpenPass(line))
        form.startDefault(filename='cor/R3AUTO_open.json')
        form.show()

    def OnCompleteOpenPass(self, line):
        R = 1e9
        form = FormScan(self)
        form.setMaxAmplitude(jplot.MaxAmplitude())
        form.signalComplete.connect(lambda:self.OnCompleteProcess())
        form.startCalibrateR(R, line['data'], line['name'])
        form.show()


    def OnCompleteProcess(self):
        self.checkComplete()
        pass

    def OnWriteFlash(self):
        corrector = jplot.Corrector()
        maxAmplitude = jplot.MaxAmplitude()
        usb_commands.FlashCorrector(corrector, maxAmplitude)
        QtGui.QMessageBox.about(self, TITLE, "Запись корректирующих коэффициэнтов окончена.")
        pass

    def setComplete(self, label, ok):
        if ok:
            label.setText("Пройден.")
            label.setStyleSheet("QLabel { color : green; }");
        else:
            label.setText('Не пройден')
            label.setStyleSheet("QLabel { color : red; }");
        pass

    def checkCompleteOne(self, line):
        ok = True
        Rname = line['name']
        diapasons = line['data']
        for diapason in diapasons:
            filename = getCorrName(diapason, Rname)
            if not os.path.isfile(filename):
                ok = False
                break

        label = line['label']
        self.setComplete(label, ok)
        pass

    def checkCompleteOpenShort(self, name):
        ok = os.path.isfile('cor/K_'+name+'.json')
        label = self.labelOS[name]
        self.setComplete(label, ok)
        pass

    def checkComplete(self):
        for line in self.lines:
            self.checkCompleteOne(line)

        #self.checkCompleteOpenShort('open')
        pass

def main():
    app = QtGui.QApplication(sys.argv)
    form = FormMain()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
    
