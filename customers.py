import re


from PyQt6 import QtWidgets, QtCore

import globals
from conexion import Conexion
from events import Events


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

    def loadTablecli(varcli):
        try:
            listTabCustomers = Conexion.listCustomers(varcli)
            index = 0
            for record in listTabCustomers:
                globals.ui.tblCustomerlist.setRowCount(index + 1)
                globals.ui.tblCustomerlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tblCustomerlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tblCustomerlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str("  " + str(record[5]) + "  ")))
                globals.ui.tblCustomerlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[7])))
                globals.ui.tblCustomerlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[8])))
                globals.ui.tblCustomerlist.setItem(index, 5, QtWidgets.QTableWidgetItem(str(record[9])))
                if str(record[10]) == "True":
                    globals.ui.tblCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Alta")))
                else:
                    globals.ui.tblCustomerlist.setItem(index, 6, QtWidgets.QTableWidgetItem(str("Baja")))

                globals.ui.tblCustomerlist.item(index, 0).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblCustomerlist.item(index, 1).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblCustomerlist.item(index, 2).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerlist.item(index, 3).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerlist.item(index, 4).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerlist.item(index, 5).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblCustomerlist.item(index, 6).setTextAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                index += 1
        except Exception as error:
            print("error en loadTablecli ", error)

    def selectCustomer(self):
        try:
            row = globals.ui.tblCustomerlist.selectedItems()
            data = [data.text() for data in row]
            record = Conexion.dataOneCustomer(str(data[2]))
            boxes = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNomecli,
                     globals.ui.txtEmailcli, globals.ui.txtMobilcli, globals.ui.txtDircli]
            for i in range(len(boxes)):
                boxes[i].setText(str(record[i]))
            globals.ui.cmbProvcli.setCurrentText(str(record[7]))
            globals.ui.cmbMunicli.setCurrentText(str(record[8]))
            if str(record[9]) == "paper":
                globals.ui.rbtFacpaper.setChecked(True)
            else:
                globals.ui.rbtFacmail.setChecked(True)

            if str(record[10]) == "True":
                globals.estado = str("True")
            else:
                globals.estado = str("False")

            globals.ui.txtDnicli.setEnabled(False)
            globals.ui.txtDnicli.setStyleSheet("background-color: rgb(255, 255, 197);")


        except Exception as error:
            print("error en selectCustomer ", error)


    @staticmethod
    def delCliente(self):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Client?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No )
            if mbox.exec():
                dni = globals.ui.txtDnicli.text()
                if Conexion.deleteCli(dni):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("The client has been deleted")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                varcli = True
                Customers.loadTablecli(varcli)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Contact with the administrator")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        except Exception as error:
            print("error del cliente ", error)

    def HistoricoCli(self):
        try:
            if globals.ui.chkHistoricocli.isChecked():
                varcli = False;
            else:
                varcli = True;
            Customers.loadTablecli(varcli)
        except Exception as error:
            print("error del historico cliente ", error)

    def saveCli(self):
        try:
            newCli = [globals.ui.txtDnicli.text(), globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(), globals.ui.txtNomecli.text(),
                      globals.ui.txtEmailcli.text(), globals.ui.txtMobilcli.text(), globals.ui.txtDircli.text(),
                      globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText()]
            if globals.ui.rbtFacpaper.isChecked():
                fact = "paper"
            elif globals.ui.rbtFacmail.isChecked():
                fact = "electronic"
            newCli.append(fact)
            if Conexion.addCli(newCli) and len(newCli) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The client has been added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                varcli = True
                Customers.loadTablecli(varcli)
                Customers.resetCustomer()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Contact with the administrator")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        except Exception as error:
            print("error del save cliente ", error)

    def resetCustomer(self):
        try:
            globals.ui.txtDnicli.setText("")
            globals.ui.txtDnicli.setStyleSheet('background-color: none;')
            globals.ui.txtDnicli.setEnabled(True)
            globals.ui.txtAltacli.setText("")
            globals.ui.txtNomecli.setText("")
            globals.ui.txtApelcli.setText("")
            globals.ui.txtEmailcli.setText("")
            globals.ui.txtEmailcli.setStyleSheet('background-color: none;')
            globals.ui.txtMobilcli.setText("")
            globals.ui.txtMobilcli.setStyleSheet('background-color: none;')
            globals.ui.txtDircli.setText("")
            Events.loadProv(self)
            globals.ui.cmbMunicli.clear()
            globals.ui.rbtFacmail.setChecked(True)
            globals.ui.lblWarning.setText("")
            globals.ui.lblWarning.setStyleSheet("background-color: none")


        except Exception as error:
            print("error emptyCustomers ", error)

    def modifCli(self):
        try:
            print(globals.estado)
            if globals.estado == str("False"):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Question")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
                mbox.setText("Cliente not activated. Doy tou want it activated?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec():
                    globals.estado = str("True")

            if globals.ui.txtDnicli.text() != "":
                dni = globals.ui.txtDnicli.text()
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Question")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
                mbox.setText("Are you sure you want to modify this client?")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec():
                    dni = globals.ui.txtDnicli.text()
                    modifCli = [globals.ui.txtAltacli.text(), globals.ui.txtApelcli.text(), globals.ui.txtNomecli.text(),
                                globals.ui.txtEmailcli.text(), globals.ui.txtMobilcli.text(), globals.ui.txtDircli.text(),
                                globals.ui.cmbProvcli.currentText(), globals.ui.cmbMunicli.currentText()]
                    if globals.ui.rbtFacpaper.isChecked():
                        fact = "paper"
                    elif globals.ui.rbtFacmail.isChecked():
                        fact = "electronic"
                    modifCli.append(fact)
                    print(modifCli)
                    if Conexion.modifCli(dni, modifCli):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Information")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setText("The client has been modified")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Warning")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setText("Error modifying the client.")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide

            Customers.loadTablecli(True)
        except Exception as error:
            print("error en modifCli ", error)


    @staticmethod
    def buscaCli(self):
        try:
            record = []
            dni = globals.ui.txtDnicli.text()
            record = Conexion.dataOneCustomer(dni)
            if not record:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Client does not exist")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide
            else:
                box = [globals.ui.txtDnicli, globals.ui.txtAltacli, globals.ui.txtApelcli, globals.ui.txtNomecli,
                       globals.ui.txtEmailcli, globals.ui.txtMobilcli, globals.ui.txtDircli]
                for i in range(len(box)):
                    box[i].setText(str(record[i]))
                globals.ui.cmbProvcli.setCurrentText(str(record[7]))
                globals.ui.cmbMunicli.setCurrentText(str(record[8]))
                if str(record[9]) == "paper":
                    globals.ui.rbtFacpaper.setChecked(True)
                else:
                    globals.ui.rbtFacmail.setChecked(True)
                if str(record[10]) == "False":
                    globals.ui.lblWarning.setText("Historical Client")
                    globals.ui.lblWarning.setStyleSheet("background-color: rgb(255, 255, 200); color: red;")

        except Exception as error:
            print("error buscaCli ", error)