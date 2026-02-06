
from conexion import *
from PyQt6 import QtWidgets, QtCore, QtGui


class Products:
    @staticmethod
    def loadTableProducts(self=None):
        try:
            listTabProducts = Conexion.listProducts()
            index = 0
            for record in listTabProducts:
                globals.ui.tblProducts.setRowCount(index + 1)
                globals.ui.tblProducts.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tblProducts.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tblProducts.setItem(index, 2, QtWidgets.QTableWidgetItem(str("  " + str(record[2]) + "  ")))
                globals.ui.tblProducts.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tblProducts.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[4]) + " €"))

                stock = float(record[2])
                if stock < 5:
                    pale_red = QtGui.QColor(255, 200, 200)

                    for i in range(5):
                        item = globals.ui.tblProducts.item(index, i)
                        if item:
                            item.setBackground(pale_red)

                globals.ui.tblProducts.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblProducts.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                globals.ui.tblProducts.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter.AlignCenter)
                globals.ui.tblProducts.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight.AlignRight)
                globals.ui.tblProducts.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight.AlignRight)

                index += 1

        except Exception as error:
            print("error en loadTableProducts ", error)

    def comaPunto(valor):
        valor = valor.replace(',', '.')
        globals.ui.txtPrice.setText(str(valor))

    def savePro(self=None):
        try:
            newpro = [globals.ui.txtName.text(), globals.ui.txtStock.text(), globals.ui.comboBox.currentText(), globals.ui.txtPrice.text()]

            if Conexion.addPro(newpro) and len(newpro) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("Product added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

                if mbox.exec():
                    mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Warning, no Product added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

                if mbox.exec():
                    mbox.hide()

            Products.loadTableProducts(self=None)
        except Exception as error:
            print("Error  saving product ", error)

    @staticmethod
    def cleanPro():
        try:
            boxes = [globals.ui.txtCode, globals.ui.txtName,
                     globals.ui.txtStock, globals.ui.txtPrice
                     ]
            for i in range(len(boxes)):
                boxes[i].setText("")
            globals.ui.comboBox.setCurrentText("")
        except Exception as error:
            print("error clean pro ", error)

    def selectPro(self):
        try:
            row = globals.ui.tblProducts.selectedItems()
            data = [dato.text() for dato in row]
            data[4] = data[4].replace("€", "").strip()
            boxes = [globals.ui.txtCode, globals.ui.txtName, globals.ui.txtStock, globals.ui.comboBox,
                     globals.ui.txtPrice]
            for i in range(len(boxes)):
                if i == 3:
                    boxes[i].setCurrentText(str(data[3]).strip())
                else:
                    boxes[i].setText(str(data[i]))

            globals.ui.txtName.setStyleSheet("background-color: rgb(255, 255, 202);")
            globals.ui.tblProducts.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: rgb(255, 255, 202);
                color: black;
            }
            QTableWidget::item:hover {
                background-color: rgb(220, 240, 255);
                color: black;
            }
            """)
        except Exception as error:
            print("error en selecting product ", error)

    def delPro(self=None):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("WARNING")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Cancel)
            if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:

                name = globals.ui.txtName.text()
                if Conexion.deletePro(name):

                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("Delete Product?")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                    mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)

                else:
                    print("Something went wrong")
                Products.loadTableProducts(self=None)

            else:
                pass

        except Exception as error:
            print("error en deleting product ", error)

    @staticmethod
    def modifyPro():
        try:
            if globals.ui.txtCode.text() != "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Modify Data")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
                mbox.setText("Are you sure modify all data?")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                    id = globals.ui.txtCode.text()
                    modpro = [globals.ui.txtName.text(), globals.ui.comboBox.currentText(),
                              globals.ui.txtStock.text(), globals.ui.txtPrice.text()
                              ]

                    if Conexion.modifyPro(id, modpro):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Information")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setText("Product modified")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText("Error modifying data. Empty Data? ")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
            Products.loadTableProducts(self=None)
        except Exception as error:
            print("error modify pro ", error)
