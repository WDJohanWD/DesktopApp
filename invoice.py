from datetime import datetime

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon

from conexion import Conexion
import globals
from globals import linesales
from reports import Reports

class Invoice:

    @staticmethod
    def searchInvoice():
        try:
            dni = globals.ui.txtDniFac.text().upper().strip()

            if dni == "" or Conexion.searchClient(dni):
                if dni == "":
                    dni = "00000000T"
                    globals.ui.txtDniFac.setText(dni)

                record = Conexion.dataOneCustomer(dni)

                globals.ui.lblNamefac.setText(record[2] + " " + record[3])
                globals.ui.lblTipofac.setText(record[9])
                globals.ui.lblnumfac_3.setText(
                    record[6] + "   " + record[8] + "   " + record[7]
                )
                globals.ui.lblnumfac_4.setText(str(record[5]))

                if record[10] == "True":
                    globals.ui.lblStatusfac.setText("Activo")
                else:
                    globals.ui.lblStatusfac.setText("Inactivo")
            else:
                globals.ui.txtDniFac.setText("")
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Client not exists")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en searchInvoice", error)

    @staticmethod
    def reloadInvoice():
        try:
            formfact = [
                globals.ui.lblNamefac,
                globals.ui.lblnumfac_3,
                globals.ui.lblStatusfac,
                globals.ui.lblTipofac,
                globals.ui.lblnumfac_4,
                globals.ui.lblFechafac,
                globals.ui.lblnumfac,
                globals.ui.txtDniFac,
            ]

            for dato in formfact:
                dato.setText("")

            globals.ui.tabsales.setRowCount(0)

        except Exception as error:
            print("error en reloadInvoice", error)

    @staticmethod
    def saveInvoice():
        try:
            dni = globals.ui.txtDniFac.text()
            data = datetime.now().strftime("%d/%m/%Y")

            if dni != "" and data != "":
                if Conexion.insertInvoice(dni, data):
                    Invoice.loadTableInvoice()

                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Invoice")
                    mbox.setText("Invoice created successfully")
                    if mbox.exec():
                        mbox.hide()

                    Invoice.activeSales()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Warning")
                mbox.setText("Missing Fields or Data")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()

        except Exception as error:
            print("error en saveInvoice", error)

    @staticmethod
    def loadTableInvoice(self=None):
        try:
            records = Conexion.allInvoices(self)
            index = 0

            header = globals.ui.tablefacv.horizontalHeader()
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tablefacv.setColumnWidth(3, 36)
            globals.ui.tablefacv.setColumnWidth(0, 55)

            for record in records:
                globals.ui.tablefacv.setColumnWidth(3, 34)
                globals.ui.tablefacv.setRowCount(index + 1)
                globals.ui.tablefacv.setItem(index, 0, QtWidgets.QTableWidgetItem(record[0]))
                globals.ui.tablefacv.setItem(index, 1, QtWidgets.QTableWidgetItem(record[1]))
                globals.ui.tablefacv.setItem(index, 2, QtWidgets.QTableWidgetItem(record[2]))
                btn_del = QtWidgets.QPushButton()
                btn_del.setIcon(QIcon("./img/basura.png"))
                btn_del.setIconSize(QtCore.QSize(26, 26))
                btn_del.setFixedSize(32, 32)
                btn_del.setStyleSheet("border: none; background-color: transparent")
                btn_del.clicked.connect(Invoice.deleteInvoice)
                globals.ui.tablefacv.setCellWidget(index, 3, btn_del)
                globals.ui.tablefacv.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                globals.ui.tablefacv.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index = index + 1
            datos = records[0]
            globals.ui.lblnumfac.setText(str(datos[0]))
            globals.ui.txtDniFac.setText(str(datos[1]))
            globals.ui.lblFechafac.setText(str(datos[2]))
        except Exception as error:
            print("error load tablafac", error)

    @staticmethod
    def loadInvoiceirst():
        try:
            globals.ui.txtDniFac.setText("00000000T")
            globals.ui.lblnumfac.setText("")
            globals.ui.lblFechafac.setText("")
            Invoice.searchInvoice()
            header = globals.ui.tabsales.horizontalHeader()
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeMode.Fixed)
            globals.ui.tabsales.setColumnWidth(5, 36)

        except Exception as error:
            print("error en loadInvoiceirst", error)

    @staticmethod
    def selectInvoice():
        try:
            row = globals.ui.tablefacv.currentRow()
            if row == -1:
                return

            id_factura = globals.ui.tablefacv.item(row, 0).text()

            recordinvoice = Conexion.dataOneInvoice(id_factura)
            if not recordinvoice:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    f"No se encontraron datos para la factura con ID {id_factura}.",
                )
                return

            globals.ui.lblnumfac.setText(str(recordinvoice[0]))
            globals.ui.txtDniFac.setText(str(recordinvoice[1]))
            globals.ui.lblFechafac.setText(str(recordinvoice[2]))

            recordcustomer = Conexion.dataOneCustomer(recordinvoice[1])
            if recordcustomer:
                globals.ui.lblNamefac.setText(recordcustomer[2] + " " + recordcustomer[3])
                globals.ui.lblTipofac.setText(recordcustomer[9])
                globals.ui.lblnumfac_3.setText(
                    recordcustomer[6] + "   " + recordcustomer[8] + "   " + recordcustomer[7]
                )
                globals.ui.lblnumfac_4.setText(str(recordcustomer[5]))

                if recordcustomer[10] == "True":
                    globals.ui.lblStatusfac.setText("Activo")
                else:
                    globals.ui.lblStatusfac.setText("Inactivo")

            Invoice.cargarVentas(id_factura)

        except Exception as error:
            print("Error en selectInvoice:", error)

    @staticmethod
    def selectDniInvoice():
        try:
            dni = globals.ui.txtDnicli.text()

            recordinvoice = Conexion.dataOnlyOneInvoice(dni)
            if not recordinvoice:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Error",
                    f"No se encontraron datos para la factura con ID {dni}.",
                )
                return

            globals.ui.lblnumfac.setText(str(recordinvoice[0]))
            globals.ui.txtDniFac.setText(str(recordinvoice[1]))
            globals.ui.lblFechafac.setText(str(recordinvoice[2]))

            recordcustomer = Conexion.dataOneCustomer(recordinvoice[1])
            if recordcustomer:
                globals.ui.lblNamefac.setText(recordcustomer[2] + " " + recordcustomer[3])
                globals.ui.lblTipofac.setText(recordcustomer[9])
                globals.ui.lblnumfac_3.setText(
                    recordcustomer[6] + "   " + recordcustomer[8] + "   " + recordcustomer[7]
                )
                globals.ui.lblnumfac_4.setText(str(recordcustomer[5]))

                if recordcustomer[10] == "True":
                    globals.ui.lblStatusfac.setText("Activo")
                else:
                    globals.ui.lblStatusfac.setText("Inactivo")

        except Exception as error:
            print("Error en selectDniInvoice:", error)

    @staticmethod
    def activeSales(row=None):
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
                return

            table = globals.ui.tabsales
            if row is None:
                row = table.rowCount()

            if row >= globals.ui.tabsales.rowCount():
                globals.ui.tabsales.setRowCount(row + 1)

            center_align = QtCore.Qt.AlignmentFlag.AlignCenter

            item_code = QtWidgets.QTableWidgetItem("")
            item_code.setTextAlignment(center_align)
            globals.ui.tabsales.setItem(row, 0, item_code)

            globals.ui.tabsales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))

            item_price = QtWidgets.QTableWidgetItem("")
            item_price.setTextAlignment(center_align)
            globals.ui.tabsales.setItem(row, 2, item_price)

            item_qty = QtWidgets.QTableWidgetItem("")
            item_qty.setTextAlignment(center_align)
            globals.ui.tabsales.setItem(row, 3, item_qty)

            item_total = QtWidgets.QTableWidgetItem("")
            item_total.setTextAlignment(
                QtCore.Qt.AlignmentFlag.AlignRight |
                QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            globals.ui.tabsales.setItem(row, 4, item_total)

            btn_del = QtWidgets.QPushButton()
            btn_del.setIcon(QIcon("./img/basura.png"))
            btn_del.setIconSize(QtCore.QSize(26, 26))
            btn_del.setFixedSize(32, 32)
            btn_del.setStyleSheet("border: none; background-color: transparent")
            btn_del.clicked.connect(Invoice.deleteSales)
            globals.ui.tabsales.setCellWidget(row, 5, btn_del)

        except Exception as error:
            print("error en activeSales", error)

    @staticmethod
    def cellChangedSales(item):
        try:
            if item is None:
                return

            row = item.row()
            col = item.column()

            if col not in (0, 3):
                return

            globals.ui.tabsales.blockSignals(True)

            value = item.text().strip()

            if col == 0:
                if value == "":
                    globals.ui.tabsales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
                    globals.ui.tabsales.setItem(row, 2, QtWidgets.QTableWidgetItem(""))
                else:
                    data = Conexion.selectProduct(value)
                    if data:
                        globals.ui.tabsales.setItem(
                            row, 1, QtWidgets.QTableWidgetItem(str(data[0]))
                        )
                        globals.ui.tabsales.setItem(
                            row, 2, QtWidgets.QTableWidgetItem(str(data[1]))
                        )
                        globals.ui.tabsales.item(
                            row, 2
                        ).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    else:
                        mbox = QtWidgets.QMessageBox()
                        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        mbox.setWindowTitle("Warning")
                        mbox.setText("Product not exists")
                        mbox.setStandardButtons(
                            QtWidgets.QMessageBox.StandardButton.Ok
                        )
                        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                            mbox.hide()
                        globals.ui.tabsales.setItem(
                            row, 0, QtWidgets.QTableWidgetItem("")
                        )

            if col in (0, 3):
                item_qty = globals.ui.tabsales.item(row, 3)
                item_price = globals.ui.tabsales.item(row, 2)

                if item_qty and item_price:
                    try:
                        cantidad = float(item_qty.text())
                        precio = float(item_price.text())
                        tot = round(precio * cantidad, 2)

                        globals.ui.tabsales.setItem(
                            row, 4, QtWidgets.QTableWidgetItem(str(tot))
                        )
                        globals.ui.tabsales.item(
                            row, 4
                        ).setTextAlignment(
                            QtCore.Qt.AlignmentFlag.AlignRight |
                            QtCore.Qt.AlignmentFlag.AlignVCenter
                        )
                    except ValueError:
                        globals.ui.tabsales.setItem(
                            row, 4, QtWidgets.QTableWidgetItem("0.00")
                        )

            grand_subtotal = 0.0
            for r in range(globals.ui.tabsales.rowCount()):
                item_total = globals.ui.tabsales.item(r, 4)
                if item_total and item_total.text():
                    try:
                        grand_subtotal += float(item_total.text())
                    except ValueError:
                        pass

            globals.subtotal = grand_subtotal

            iva = 0.21
            totaliva = round(globals.subtotal * iva, 2)
            total = round(globals.subtotal + totaliva, 2)

            globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
            globals.ui.lblIVA.setText(f"{totaliva:.2f} €")
            globals.ui.lblTotal.setText(f"{total:.2f} €")

            row_items = [globals.ui.tabsales.item(row, i) for i in range(5)]
            is_row_complete = all(it and it.text().strip() for it in row_items)

            fact = globals.ui.lblnumfac.text().strip()

            if not fact.isdigit():
                return

            if is_row_complete:
                if not Conexion.existeFacturaSales(fact):
                    if row == globals.ui.tabsales.rowCount() - 1:
                        next_row = globals.ui.tabsales.rowCount()
                        QtCore.QTimer.singleShot(
                            0, lambda: Invoice.activeSales(next_row)
                        )

                    sale = [
                        int(globals.ui.lblnumfac.text()),
                        int(row_items[0].text()),
                        row_items[1].text(),
                        float(row_items[2].text()),
                        int(row_items[3].text()),
                        float(row_items[4].text()),
                    ]
                    globals.linesales.append(sale)

        except Exception as error:
            print("Error in cellChangedSales:", error)

        finally:
            globals.ui.tabsales.blockSignals(False)

    @staticmethod
    def saveSales(self=None):
        from products import Products
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
                Reports.ticket(self)
            else:
                correct = False
                for data in globals.linesales:
                    correct = Conexion.saveSales(data)
                    if correct:
                        Conexion.descontarStock(data[1], data[4])

                if globals.linesales[-1] and correct:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setWindowTitle("Sales Saved")
                    mbox.setText(
                        "Sales saved. Printing Invoice..."
                    )
                    mbox.setStandardButtons(
                        QtWidgets.QMessageBox.StandardButton.Ok
                    )
                    Reports.ticket(self)

                    if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                        Invoice.bloquearTablaSales()
                        globals.linesales.clear()
                        globals.ui.tabsales.setRowCount(0)
                        mbox.hide()

                        Products.loadTableProducts()

        except Exception as error:
            print("Error in saveSales:", error)

    @staticmethod
    def cargarVentas(idfac):
        try:
            data = Conexion.dataOneSale(idfac)
            table = globals.ui.tabsales

            table.setRowCount(0)

            if not data:
                Invoice.activeSales()
            else:
                table.setRowCount(len(data))

                for row_index, sale_row in enumerate(data):
                    for col_index, cell_value in enumerate(sale_row):
                        table_item = QtWidgets.QTableWidgetItem(str(cell_value))
                        table.setItem(row_index, col_index, table_item)

                    btn_del = QtWidgets.QPushButton()
                    btn_del.setIcon(QIcon("./img/basura.png"))
                    btn_del.setIconSize(QtCore.QSize(26, 26))
                    btn_del.setFixedSize(32, 32)
                    btn_del.setStyleSheet("border: none; background-color: transparent")
                    btn_del.clicked.connect(Invoice.deleteSales)

                    table.setCellWidget(row_index, 5, btn_del)

            Invoice.bloquearTablaSales()

        except Exception as error:
            print("Error en cargarVentas:", error)

    @staticmethod
    def bloquearTablaSales():
        try:
            table = globals.ui.tabsales
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item:
                        item.setFlags(
                            item.flags() &
                            ~QtCore.Qt.ItemFlag.ItemIsEditable
                        )

        except Exception as error:
            print("Error en bloquearTablaSales:", error)

    @staticmethod
    def deleteInvoice():
        try:
            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Can't delete Invoice")
                mbox.setText("This invoice have sales it can't be deleted.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
            else:
                Conexion.deleteInvoice(fact)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Deleted invoice")
                mbox.setText("Invoice Nº" + str(fact) + " has been successfully deleted.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Ok:
                    mbox.hide()
                Invoice.loadTableInvoice()
        except Exception as error:
            print("Error en deleteInvoice:", error)

    @staticmethod
    def deleteSales():
        try:
            btn = globals.ui.tabsales.sender()

            if not btn:
                return

            table = globals.ui.tabsales

            for row in range(table.rowCount()):
                if table.cellWidget(row, 5) == btn:
                    break
            else:
                return

            fact = globals.ui.lblnumfac.text()

            if Conexion.existeFacturaSales(fact):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("No permitido")
                mbox.setText("Esta factura ya está guardada y no se pueden borrar líneas.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            table.removeRow(row)

            if row < len(globals.linesales):
                globals.linesales.pop(row)

            subtotal = 0.0
            for r in range(table.rowCount()):
                item_total = table.item(r, 4)
                if item_total and item_total.text():
                    subtotal += float(item_total.text())

            globals.subtotal = subtotal
            iva = round(subtotal * 0.21, 2)
            total = round(subtotal + iva, 2)

            globals.ui.lblSubtotal.setText(f"{subtotal:.2f} €")
            globals.ui.lblIVA.setText(f"{iva:.2f} €")
            globals.ui.lblTotal.setText(f"{total:.2f} €")

        except Exception as error:
            print("Error en deleteSales:", error)
