import re

import globals
from events import *
from invoice import *
from conexion import *
from PyQt6 import QtWidgets, QtCore, QtGui

class Customers:

    @staticmethod
    def checkDni(self=None):
        try:
            globals.ui.txtDnicli.editingFinished.disconnect(Customers.checkDni)
            dni = globals.ui.txtDnicli.text()
            dni = str(dni).upper()

            if globals.ui.txtDnicli.text() != dni:
                globals.ui.txtDnicli.setText(dni)

            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')
                else:
                    globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                    globals.ui.txtDnicli.setText(None)
                    globals.ui.txtDnicli.setFocus()
            else:
                globals.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtDnicli.setText(None)
                globals.ui.txtDnicli.setFocus()
        finally:
            globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)

    def capitalizar(texto, widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error capitalizing text", error)

    @staticmethod
    def checkMail(email):
        try:
            patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(patron, email):
                globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
            else:
                globals.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB;')
                globals.ui.txtEmailcli.setText(None)
                globals.ui.txtEmailcli.setPlaceholderText('Invalid Email')
                globals.ui.txtEmailcli.setFocus()
        except Exception as error:
            print("error validating email ", error)

    @staticmethod
    def checkMobil(numero):
        patron = r'^[67]\d{8}$'
        if re.match(patron, numero):
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobilecli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobilecli.setText(None)
            globals.ui.txtMobilecli.setPlaceholderText('Invalid Mobile')
            globals.ui.txtMobilecli.setFocus()

    @staticmethod
    def cleanCli(self=None):
        try:
            formcli = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli,
                       globals.ui.txtNomecli, globals.ui.txtEmailcli, globals.ui.txtMobilecli,
                       globals.ui.txtDircli]
            for i, dato in enumerate(formcli):
                formcli[i] = dato.setText("")

            Events.loadProv(self)
            globals.ui.cmbMunicli.clear()
            globals.ui.rbtFacemail.setChecked(True)
            globals.ui.txtDnicli.setEnabled(True)
            globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.txtMobilecli.setStyleSheet('background-color: rgb(255, 255, 255);')
            globals.ui.lblWarning.setText("")
            globals.ui.txtEmailcli.setPlaceholderText("")
            globals.ui.txtMobilecli.setPlaceholderText("")
            globals.ui.lblWarning.setStyleSheet('background-color: none;')

        except Exception as error:
            print("error in clean ", error)

    @staticmethod
    def loadTablecli(globalscli):
        try:
            listTabCustomers = Conexion.listTabCustomers(globalscli)
            index = 0
            for record in listTabCustomers:
                globals.ui.tableCustomerlist.setRowCount(index + 1)
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str("  " + str(record[5]) + "  ")))
                globals.ui.tableCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                if str(record[10]) == "True":
                    globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Alta")))
                else:
                    globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Baja")))
                globals.ui.tableCustomerlist.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                index += 1
        except Exception as error:
            print("error in loadTablecli ", error)

    @staticmethod
    def Historicocli(self):
        try:
            if globals.ui.chkHistoricocli.isChecked():
                globalscli = False
            else:
                globalscli = True
            Customers.loadTablecli(globalscli)
        except Exception as error:
            print("error en historicocli ", error)

    @staticmethod
    def selectCustomer(self=None):
        try:
            row = globals.ui.tableCustomerlist.selectedItems()
            data = [dato.text() for dato in row]
            record = Conexion.dataOneCustomer(str(data[2]))
            boxes = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNomecli, globals.ui.txtEmailcli, globals.ui.txtMobilecli, globals.ui.txtDircli]
            for i in range(len(boxes)):
                boxes[i].setText(record[i])

            globals.ui.cmbProvcli.setCurrentText(str(record[7]))
            globals.ui.cmbMunicli.setCurrentText(str(record[8]))
            if str(record[9]) == 'paper':
                globals.ui.rbtFacpapel.setChecked(True)
            else:
                globals.ui.rbtFacemail.setChecked(True)
            globals.estado = str(record[10])
            globals.ui.txtDnicli.setEnabled(False)
        except Exception as error:
            print("error en selecting customer ", error)

    @staticmethod
    def delCliente(self=None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("WARNING")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:

                dni = globals.ui.txtDnicli.text()
                if Conexion.deleteCli(dni):

                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Client?")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

                else:
                    print("Something went wrong")
                Customers.loadTablecli(self)
                globals.ui.chkHistoricocli.setChecked(True)
            else:
                pass

        except Exception as error:
            print("error en deleting customer ", error)

    @staticmethod
    def saveCli(self=None):
        try:
            newcli = [globals.ui.txtDnicli.text(), globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(), globals.ui.txtNomecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(), globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText()]
            if globals.ui.rbtFacpapel.isChecked():
                fact = "paper"
            elif globals.ui.rbtFacemail.isChecked():
                fact = "electronic"
            newcli.append(fact)
            if Conexion.addCli(newcli) and len(newcli) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)

                if mbox.exec():
                    mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, no Client added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes)

                if mbox.exec():
                    mbox.hide()
            globalscli = True
            Customers.loadTablecli(globalscli)
        except Exception as error:
            print("Error  saving customer ", error)

    @staticmethod
    def modifcli(self=None):
        try:
            globalscli = "True"
            if globals.estado == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client non activated. DO you want activated?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                reply = mbox.exec()
                if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                    globals.estado = str("True")

            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Modify")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
            mbox.setText("Modify Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                dni = globals.ui.txtDnicli.text()
                modifcli = [globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(),
                            globals.ui.txtNomecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                            globals.ui.txtDircli.text(), globals.ui.cmbProvcli.currentText(),
                            globals.ui.cmbMunicli.currentText(), globals.estado]
                if globals.ui.rbtFacpapel.isChecked():
                    fact = "paper"
                elif globals.ui.rbtFacemail.isChecked():
                    fact = "electronic"
                modifcli.append(fact)
                if Conexion.modifyCli(dni, modifcli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client modified")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide()
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Warning, no Client modified")
                    if mbox.exec():
                        mbox.hide()
            else:
                mbox.hide()

            Customers.loadTablecli(globalscli)
            globals.ui.chkHistoricocli.setChecked(False)
        except Exception as error:
            print("error en modifing customer ", error)

    @staticmethod
    def searchCli(self=None):
        try:
            record = []
            dni = globals.ui.txtDnicli.text()
            record = Conexion.dataOneCustomer(str(dni))
            if not record:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client does not exists")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide()
            else:
                box = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNomecli, globals.ui.txtEmailcli, globals.ui.txtMobilecli, globals.ui.txtDircli]
                for i in range(len(box)):
                    box[i].setText(record[i])

                globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                globals.ui.cmbMunicli.setCurrentText(str(record[8]))
                Invoice.selectDniInvoice()
                if str(record[9]) == 'paper':
                    globals.ui.rbtFacpapel.setChecked(True)
                else:
                    globals.ui.rbtFacemail.setChecked(True)
                if str(record[10]) == 'False':
                    globals.ui.lblWarning.setText("Hystorical Client")
                    globals.ui.lblWarning.setStyleSheet("background-color:rgb(255,255,200); color:red;")

        except:
            print("error in searching customer ")

    @staticmethod
    def cargaTablaClientes(self):
        try:
            import conexion
            listadocli = conexion.Conexion.listTabCustomers(self)
            globals.longcli = len(listadocli)
            start_index = globals.paginacli * globals.clientesxpagina
            end_index = start_index + globals.clientesxpagina
            listado_pagina = listadocli[start_index:end_index]
            index = 0
            for registro in listado_pagina:
                globals.ui.tableCustomerlist.setRowCount(index + 1)
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[2])))
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[3])))
                globals.ui.tableCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str("  " + registro[5] + "  ")))
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(registro[7])))
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(registro[8])))
                globals.ui.tableCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[9]))
                globals.ui.tableCustomerlist.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignVCenter)
                index += 1
        except Exception as e:
            print("error cargaTablaCientes", e)
