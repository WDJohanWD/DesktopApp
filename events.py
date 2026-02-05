import csv
import os
import shutil
import sys
import time
import zipfile
from datetime import datetime


import conexion
import customers
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

    def messageAbout(self):
        try:
            globals.about.show()
        except Exception as e:
            print("Error en about", e)

    def closeAbout(self):
        try:
            globals.about.hide()
        except Exception as e:
            print("Error en about", e)

    def resizeTabCustomer(self):
        try:
            header = globals.ui.tblCustomerlist.horizontalHeader()
            for i in range(header.count()):
                if i == 6:
                    header.setSelectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                header_items = globals.ui.tblCustomerlist.horizontalHeaderItem(i)
                # negrita cabecera
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla clients: ", e)


    def saveBackup(self):
        try:
            data = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            fileName = str(data)+'_backup.zip'
            directory, file = globals.dlgopen.getSaveFileName(None, 'Save Backup file', fileName, 'zip')
            if globals.dlgopen.accept and file:
                fileZip = zipfile.ZipFile(file, "w")
                fileZip.write('./data/bbdd.sqlite', os.path.basename('bbdd.sqlite'), zipfile.ZIP_DEFLATED)
                fileZip.close()
                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.png'))
                mbox.setWindowTitle('Save Backup')
                mbox.setText('Save Backup Done')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

            print("HOLA")
        except Exception as e:
            print("Error en save backup", e)

    def restoreBackup(self):
        try:
            fileName = globals.dlgopen.getOpenFileName(None, 'Restore Backup file', '', '*.zip;;All Files (*)')
            file = fileName[0]
            if file:
                with zipfile.ZipFile(file, "r") as bbdd:
                    bbdd.extractall(path='./data', pwd=None)
                    bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.png'))
                mbox.setWindowTitle('Restore Backup')
                mbox.setText('Restore Backup Done')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                conexion.Conexion.db_conexion(self)
                Events.loadProv(self)
                customers.Customers.loadTablecli(True)

        except Exception as e:
            print("Error en restore backup", e)


    def exportXlsCustomers(self):
        try:
            data = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            fileName = str(data)+'_customers.csv'
            directory, file = globals.dlgopen.getSaveFileName(None, 'Save Customers file', fileName, 'csv')
            var = True
            if file:
                records = conexion.Conexion.listCustomers(var)
                with open(file, "w", newline= '', encoding= 'utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["DNI_NIE", "Fecha alta", "surname", "Name", "Mail", "Mobile", "Address", "Province", "City", "Invoice Type", "Active"])

                    for record in records:
                        writer.writerow(record)

                shutil.move(file, directory)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.png'))
                mbox.setWindowTitle('Export Customers')
                mbox.setText('The customer data has been exported')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon('./img/logo.png'))
                mbox.setWindowTitle('Error exporting')
                mbox.setText('There was an error exporting the customer data')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()



        except Exception as e:
            print("Error en export customers", e)

    def loadStatusBar(self):
        try:
            data = datetime.now().strftime('%d/%m/%y')
            self.labelstatus = QtWidgets.QLabel(self)
            self.labelstatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.labelstatus.setText(f'Date: {data}')
            self.labelstatus.setStyleSheet('color: white')
            globals.ui.statusbar.addWidget(self.labelstatus)
            self.labelversion = QtWidgets.QLabel(self)
            self.labelversion.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.labelversion.setText('Version 0.0.1')
            self.labelversion.setStyleSheet('color: white')
            globals.ui.statusbar.addWidget(self.labelversion)

        except Exception as e:
            print("Error en status bar", e)