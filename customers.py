import re

from PyQt6 import QtWidgets, QtCore

import conexion
import globals

class Customers:
    @staticmethod
    def checkDni(self=None):
        try:
            dni = globals.ui.txtDnicli.text()
            dni = str(dni).upper()
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
        except Exception as error:
            print("error en validar dni ", error)

    def capitalizar(texto, widget):
        try:
            texto = texto.title()
            widget.setText(texto)
        except Exception as error:
            print("error en capitalizar texto ", error)

    def checkEmail(email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(patron, email):
            globals.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtEmailcli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtEmailcli.setText(None)
            globals.ui.txtEmailcli.setPlaceholderText("Invalid Email")
            globals.ui.txtEmailcli.setFocus()

    def checkMobil(numero):
        patron = r'^[67]\d{8}$'
        if re.match(patron, numero):
            globals.ui.txtMobilcli.setStyleSheet('background-color: rgb(255, 255, 220);')
        else:
            globals.ui.txtMobilcli.setStyleSheet('background-color: #FFC0CB;')
            globals.ui.txtMobilcli.setText(None)
            globals.ui.txtMobilcli.setPlaceholderText("Invalid Mobile")
            globals.ui.txtMobilcli.setFocus()

    @staticmethod
    def loadTablecli(varcli):
        try:
            listTabCustomers = conexion.Conexion.listCustomers(varcli)
            print(listTabCustomers)
            index = 0
            for record in listTabCustomers:
                globals.ui.tableCustomerlist.setRowCount(index + 1)
                globals.ui.tableCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tableCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tableCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[5])))
                globals.ui.tableCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.tableCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tableCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                globals.ui.tableCustomerlist.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tableCustomerlist.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 4).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tableCustomerlist.item(index, 5).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                index += 1
        except Exception as error:
            print("error en loadTablecli ", error)

    @staticmethod
    def selectCustomer(self):
        try:
            row = globals.ui.tableCustomerlist.selectedItems()
            data = [dato.text() for dato in row]
            record = conexion.Conexion.dataOneCustomer(data[2])
            boxes = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNomecli ,globals.ui.txtEmailcli, globals.ui.txtMobilcli, globals.ui.txtDircli]
            print(data)
            for i in range (len(boxes)):
                boxes[i].setText(str(record[i]))

            globals.ui.cmbProvcli.setCurrentText(str(record[7]))
            globals.ui.cmbMunicli.setCurrentText(str(record[8]))

            if str(record[9]) == 'paper':
                globals.ui.rbtFacpaper.setChecked(True)
            else:
                globals.ui.rbtFacemail.setChecked(False)

            globals.ui.txtDnicli.setEnabled(True)
            globals.ui.txtDnicli.setStyleSheet("background-color: rgb(255, 255, 197);")
        except Exception as error:
            print("error en selectCustomer ", error)

    @staticmethod
    def delCliente():
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():
                dni = globals.ui.txtDnicli.text()
                if conexion.Conexion.deleteCli(dni):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Client")
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Something went wrong, contact with administrator")
                Customers.loadTablecli()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Error. Contact with the administrator or try again later.")
        except Exception as error:
            print("error delete cliente ", error)

    @staticmethod
    def Historicocli(self):
        try:
            if globals.ui.chkHistoricocli.isChecked():
                varcli = False
            else:
                varcli = True
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error en historicocli ", error)

    @staticmethod
    def saveCli(self):
            try:
                newcli = [globals.ui.txtDnicli.text(), globals.ui.txtDnicli.text(), globals.ui.txtApelcli.text(),
                          globals.ui.txtNamecli.text(), globals.ui.txtEmailcli.text(), globals.ui.txtMobilecli.text(),
                          globals.ui.txtDircli.text, globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText()]

                if globals.ui.rbtFacpaper.isChecked():
                    fact = "paper"
                elif globals.ui.rbtFacmail.isChecked():
                    fact = "electronic"

                newcli.append(fact)
                if conexion.Conexion.addCli(newcli):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Client added")
                    varcli = True
                    Customers.loadTablecli(varcli)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Client not added")
            except Exception as e:
                print("Error data", e)

    # @staticmethod
    # def buscaCli():
    #     try:
    #         for i in range(len(box)):
    #             box[i].setText(record([i]))
    #         globals.ui.cmbProvcli.setCurrentText(str(record[7]))
    #         globals.ui.cmbMunicli.setCurrentText(str(record[8]))
    #         if str(record[])
    #     except Exception as error:
    #         print("error buscaCli ", error)
