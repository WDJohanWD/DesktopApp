import sys
import time

import conexion
import globals

from PyQt6 import  QtCore, QtGui, QtWidgets

class Events:
    @staticmethod
    def messageExit():
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowIcon(QtGui.QIcon('./img/logo.png'))
        mbox.setWindowTitle('Exit')
        mbox.setText('Are you sure you want to exit?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.resize(600, 800)
        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def openCalendar(self):
        try:
            globals.vencal.show()

        except Exception as e:
            print("Error en calendario", e)

    def loadData(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if globals.ui.panPrincipal.currentIndex() == 0:
                globals.ui.txtAltacli.setText(data)
            time.sleep(0.3)
            globals.vencal.hide()

        except Exception as e:
            print("error en cargar Data", e)

    def loadProv(self):
        try:
            globals.ui.cmbProvcli.clear()
            list = conexion.Conexion().listProv()
            globals.ui.cmbProvcli.addItems(list)
        except Exception as e:
            print("Error en cargar Provincias", e)

    def loadMunicli(self):
        try:
            province = globals.ui.cmbProvcli.currentText()
            list = conexion.Conexion.listMuniProv(province)
            globals.ui.cmbMunicli.clear()
            globals.ui.cmbMunicli.addItems(list)

        except Exception as e:
            print("Error en cargar Municipios", e)


