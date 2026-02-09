
from PyQt6 import QtWidgets, QtCore
from conexion import Conexion
from PyQt6.QtGui import QColor
import globals


class Products:
    def loadTableProd(self):
        try:
            listProd = Conexion.listProds(self)
            index = 0
            for record in listProd:
                globals.ui.tblProdlist.setRowCount(index + 1)
                globals.ui.tblProdlist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tblProdlist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tblProdlist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))
                globals.ui.tblProdlist.setItem(index, 3, QtWidgets.QTableWidgetItem(str(record[3])))
                globals.ui.tblProdlist.setItem(index, 4, QtWidgets.QTableWidgetItem(str(record[4])))

                if record[2] < 10:
                    item = QtWidgets.QTableWidgetItem(str(record[2]))
                    globals.ui.tblProdlist.setItem(index, 2, item)
                    font = item.font()
                    font.setBold(True)
                    item.setForeground(QtCore.Qt.GlobalColor.red)

                index += 1

        except Exception as e:
            print("Error en loadTableProd: ", e)


    def saveProd(self):
        try:
            newProd = [globals.ui.txtNameProd.text(), globals.ui.txtStock.text(), globals.ui.cmbFamily.currentText(), globals.ui.txtPrice.text()]
            if Conexion.addProd(newProd) and len(newProd) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The product has been added")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                Products.loadTableProd(self)
                Products.resetProduct(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Contact with the administrator")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)

        except Exception as error:
            print("error del save prod ", error)

    def resetProduct(self):
        try:
            globals.ui.lblCodeId.setText("")
            globals.ui.txtNameProd.setText("")
            globals.ui.txtStock.setText("")
            globals.ui.txtPrice.setText("")

        except Exception as error:
            print("error emptyCustomers ", error)

    def selectProd(self):
        try:
           row = globals.ui.tblProdlist.selectedItems()
           id = row[0].text()
           record = Conexion.dataOneProduct(id)
           boxes = [globals.ui.lblCodeId, globals.ui.txtNameProd, globals.ui.txtStock, globals.ui.txtPrice, globals.ui.txtPrice]
           for i in range(len(boxes)):
               boxes[i].setText(str(record[i]))

           globals.ui.cmbFamily.setCurrentText(str(record[3]))
        except Exception as e:
            print("error en selectProd ", e)

    @staticmethod
    def delProd(self):
        try:
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Warning")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setText("Delete Product?")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            if mbox.exec():
                id = globals.ui.lblCodeId.text()
                if Conexion.deleteProd(id):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("The product has been deleted")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    Products.loadTableProd(self)
                    Products.resetProduct(self)
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Contact with the administrator")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
        except Exception as error:
            print("error al eliminar el cliente", error)



    def modifProd(self):
        try:
            if globals.ui.lblCodeId.text() != "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Question")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
                mbox.setText("Are you sure you want to modify this product?")
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
                if mbox.exec():
                    id = globals.ui.lblCodeId.text()
                    modifProd = [globals.ui.txtNameProd.text(), globals.ui.txtStock.text(), globals.ui.cmbFamily.currentText(), globals.ui.txtPrice.text()]
                    if Conexion.modifProd(id, modifProd):
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Information")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                        mbox.setText("The product has been modified")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setWindowTitle("Warning")
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setText("Error modifying the product.")
                        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                        if mbox.exec():
                            mbox.hide

            Products.loadTableProd(self)
            Products.resetProduct(self)
        except Exception as error:
            print("error en modifCli ", error)

    @staticmethod
    def capitalizar(widget):
        try:
            text= widget.text()
            widget.setText(text.capitalize())
        except Exception as error:
            print("error en capitalizar texto ", error)

    @staticmethod
    def comaPunto(valor):
        valor = str(valor.replace(",", "."))
        globals.ui.txtPrice.setText(valor)
