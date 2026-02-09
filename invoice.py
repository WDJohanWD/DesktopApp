from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

import globals
from conexion import Conexion
from events import Events
from reports import Reports
from products import Products


class Invoice():
    reports = Reports()
    products = Products()

    @staticmethod
    def buscaCli(dni):
        try:
            if Conexion.buscaCli(dni):
                record = Conexion.dataOneCustomer(dni)
                globals.ui.lblNamefac.setText(record[2] + ' ' + record[3])
                globals.ui.lblTypefac.setText(record[9])
                globals.ui.lblDirfac.setText(record[6] + ", " + record[8] + ', ' + record[7])
                globals.ui.lblMobilefac.setText(record[5])
                if record[10] == "True":
                    globals.ui.lblStatusfac.setText("Activo")
                else:
                    globals.ui.lblStatusfac.setText("Inactivo")
                return True
            else:
                print("No existe el Usuario")
            return False
        except Exception as error:
            print("No se pudo obtener la factura", error)

    def cleanFac(self):
        try:
            # --- LIMPIAR CAMPOS DE TEXTO Y LABELS ---
            boxes = [
                globals.ui.txtDnifac, globals.ui.lblNamefac, globals.ui.lblTypefac,
                globals.ui.lblDirfac, globals.ui.lblMobilefac, globals.ui.lblStatusfac,
                globals.ui.lblNumfac, globals.ui.lblFechafac, globals.ui.lblSubtotal,
                globals.ui.lblTotal, globals.ui.lblIva
            ]

            for box in boxes:
                box.setText("")

            table = globals.ui.tblSales
            table.setRowCount(0)
            table.setRowCount(1)

            table.setEditTriggers(
                QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers
            )

            for c in range(6):
                table.setItem(0, c, QtWidgets.QTableWidgetItem(""))

            for c in range(6):
                item = table.item(0, c)
                if not item:
                    continue

                if c in (1, 4):
                    item.setFlags(
                        QtCore.Qt.ItemFlag.ItemIsSelectable |
                        QtCore.Qt.ItemFlag.ItemIsEnabled |
                        QtCore.Qt.ItemFlag.ItemIsEditable
                    )
                else:
                    item.setFlags(
                        QtCore.Qt.ItemFlag.ItemIsSelectable |
                        QtCore.Qt.ItemFlag.ItemIsEnabled
                    )

            globals.linesales.clear()
            globals.subtotal = 0

            globals.ui.btnSaveSale.setEnabled(True)
            Invoice.showDeleteButton(0)

        except Exception as e:
            print("Error en cleanFac:", e)

    def saveInvoice(self):
        dni = globals.ui.txtDnifac.text().upper()
        if dni == "":
            dni = "00000000T"

        try:
            if Invoice.buscaCli(dni):
                if Conexion.insertInvoice(dni):
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Information")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    mbox.setText("The invoice has been saved")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide
                else:
                    mbox = QtWidgets.QMessageBox()
                    mbox.setWindowTitle("Warning")
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setText("Error saving the invoice.")
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    if mbox.exec():
                        mbox.hide
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("The user is not registered")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide

            Invoice.loadInvoices(self)
        #    Invoice.activeSales()

        except Exception as e:
            print("Error en guardar factura", e)


    def saveWithReturn(self):
        dni = globals.ui.txtDnifac.text().upper()
        if dni == "":
            dni = "00000000T"
        try:
            if Invoice.buscaCli(dni):
                id = Conexion.invoiceWithReturn(dni)
                return id

        except Exception as e:
            print("Error en guardar factura", e)

    def loadInvoices(self):
        try:
            records = Conexion.allInvoices(self)
            index = 0

            for record in records:
                globals.ui.tblFaclist.setRowCount(index + 1)
                globals.ui.tblFaclist.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
                globals.ui.tblFaclist.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
                globals.ui.tblFaclist.setItem(index, 2, QtWidgets.QTableWidgetItem(str(record[2])))

                for col, value in enumerate(record[:3]):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    globals.ui.tblFaclist.setItem(index, col, item)

                btn_del = QtWidgets.QPushButton()
                btn_del.setText("")
                btn_del.setIcon(QIcon("img/basura.png"))
                btn_del.setIconSize(QtCore.QSize(28, 28))
                btn_del.setFixedSize(QtCore.QSize(32, 32))
                btn_del.setStyleSheet("background-color: transparent; border: none")
                btn_del.setProperty("numFac", record[0])
                btn_del.clicked.connect(Invoice.deleteInvoice)


                globals.ui.tblFaclist.setCellWidget(index, 3, btn_del)

                index += 1

        except Exception as e:
            print("Error en guardar factura", e)

    def deleteInvoice(item):
        try:
            btn = QtWidgets.QApplication.instance().sender()
            numFac = btn.property("numFac")
            ventas = Conexion.getSales(numFac)
            if ventas and len(ventas) > 0:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("The invoice is not empty")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide

                return False


            if Conexion.deleteInvoice(numFac):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The invoice has been deleted")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide

                Invoice.loadInvoices(self=None)

            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Error deleting the invoice in the database")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide




        except Exception as e:
            print("Error en guardar factura", e)


    def getOneInvoice(invoiceId):
        try:
            record = Conexion.getOneInvoice(invoiceId)
        except Exception as e:
            print("Error en cargar factura", e)

    def selectInvoice(self):
        try:
            row = globals.ui.tblFaclist.selectedItems()
            if not row or len(row) < 3:
                return

            invoice_id = row[0].text()
            dni = row[1].text()

            globals.ui.lblNumfac.setText(invoice_id)
            globals.ui.txtDnifac.setText(dni)
            globals.ui.lblFechafac.setText(row[2].text())
            Invoice.buscaCli(dni)

            lines = []
            try:
                lines = Conexion.getSales(invoice_id)
            except Exception:
                lines = []

            # Bloqueamos señales para evitar recursión al llenar la tabla
            globals.ui.tblSales.blockSignals(True)

            if lines:
                globals.ui.btnSaveSale.setEnabled(False)
                globals.ui.tblSales.setRowCount(len(lines))
                globals.linesales = []
                for i, ln in enumerate(lines):
                    idSale, idFac, pid, name, price, qty, total = ln

                    # Usamos una lista de valores para facilitar el llenado
                    valores = [str(idSale), str(pid), str(name), f"{float(price):.2f}", f"{int(qty):.2f}",
                               f"{float(total):.2f}"]

                    for c, valor in enumerate(valores):
                        item = QtWidgets.QTableWidgetItem(valor)
                        # Aplicamos flags
                        if c in (1, 4):
                            item.setFlags(
                                QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)

                        globals.ui.tblSales.setItem(i, c, item)

                    globals.linesales.append([idSale, pid, name, float(price), int(qty), float(total)])

                globals.ui.tblSales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
                Invoice.calculateTotals()


            else:
                # Factura nueva/vacía
                globals.ui.tblSales.setRowCount(1)
                for c in range(6):
                    item = QtWidgets.QTableWidgetItem("")
                    if c in (1, 4):
                        item.setFlags(
                            QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                    else:
                        item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    globals.ui.tblSales.setItem(0, c, item)

                globals.ui.tblSales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
                globals.linesales = []
                Invoice.calculateTotals()

            Invoice.updateSalesStyle()
            # Desbloqueamos señales ANTES de aplicar estilos y botones
            globals.ui.tblSales.blockSignals(False)

            # Aplicar estilos y botones fila por fila de forma segura
            for r in range(globals.ui.tblSales.rowCount()):
                Invoice.showDeleteButton(r)


        except Exception as e:
            print("error en selectInvoice ", e)

    @staticmethod
    def selectInvoiceById(invoice_id):
        try:
            try:
                lines = Conexion.getSales(invoice_id)
            except Exception:
                lines = []

            if lines:
                globals.ui.btnSaveSale.setEnabled(False)
                globals.ui.tblSales.setRowCount(len(lines))
                globals.linesales = []
                for i, ln in enumerate(lines):
                    idSale, idFac, pid, name, price, qty, total = ln
                    globals.ui.tblSales.setItem(i, 0, QtWidgets.QTableWidgetItem(str(idSale)))
                    globals.ui.tblSales.setItem(i, 1, QtWidgets.QTableWidgetItem(str(pid)))
                    globals.ui.tblSales.setItem(i, 2, QtWidgets.QTableWidgetItem(str(name)))
                    globals.ui.tblSales.setItem(i, 3, QtWidgets.QTableWidgetItem(f"{float(price):.2f}"))
                    globals.ui.tblSales.setItem(i, 4, QtWidgets.QTableWidgetItem(f"{int(qty):.2f}"))
                    globals.ui.tblSales.setItem(i, 5, QtWidgets.QTableWidgetItem(f"{float(total):.2f}"))

                    # make each cell in the row non-editable except IDProd (2) and Amount (5)
                    for c in range(6):
                        it = globals.ui.tblSales.item(i, c)
                        if it:
                            if c in (1, 4):
                                it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                            else:
                                it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)

                    # store internal representation: [idSale, idFac, pid, name, price, qty, total]
                    globals.linesales.append([idSale, pid, name, float(price), int(qty), float(total)])

                globals.ui.tblSales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)

                # Recalculate subtotal for this invoice

                iva = 0.21
                globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
                globals.ui.lblIva.setText(f"{globals.subtotal * iva:.2f} €")
                total = round(globals.subtotal + (globals.subtotal * iva), 2)
                globals.ui.lblTotal.setText(f"{total:.2f} €")

            else:
                # New / empty invoice: allow editing, clear table and subtotal
                globals.ui.tblSales.setRowCount(1)
                # Ensure 7 columns exist and fill with empty items
                for c in range(6):
                    globals.ui.tblSales.setItem(0, c, QtWidgets.QTableWidgetItem(""))

                # Keep idSale and idFac empty for new invoice; product id editable (col 2)
                globals.ui.tblSales.item(0, 0).setText("")

                # Set item flags: only columns 2 (IDProd) and 5 (Amount) editable
                for c in range(6):
                    it = globals.ui.tblSales.item(0, c)
                    if it:
                        if c in (1, 4):
                            it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)

                globals.ui.tblSales.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.AllEditTriggers)
                globals.linesales = []
                globals.subtotal = 0.0
                globals.ui.lblSubtotal.setText(f"0.00 €")
                globals.ui.lblIva.setText(f"0.00 €")
                globals.ui.lblTotal.setText(f"0.00 €")
            for row in range(globals.ui.tblSales.rowCount()):
                Invoice.showDeleteButton(row-1)
        except Exception as e:
            print("error en selectInvoiceById ", e)

    @staticmethod
    def activeSales(self=None, row=None):
        try:
            # If no row provided, add first editable row
            if row is None:
                row = 0
                globals.ui.tblSales.setRowCount(1)
            else:
                if row >= globals.ui.tblSales.rowCount():
                    globals.ui.tblSales.setRowCount(row + 1)

            globals.ui.tblSales.setStyleSheet("""
                                                /* Fila seleccionada */
                                                QTableWidget::item:selected {
                                                    background-color: rgb(255, 255, 202);
                                                    color: black;
                                                }
                                                """)

            # Initialize empty cells for 7 columns
            for c in range(6):
                globals.ui.tblSales.setItem(row, c, QtWidgets.QTableWidgetItem(""))

            # Make editable only product id (2) and amount (5)
            for c in range(6):
                it = globals.ui.tblSales.item(row, c)
                if it:
                    if c in (1, 4):
                        it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                    else:
                        it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)

            # Align columns: product id (2) and amount (5) centered
            globals.ui.tblSales.item(row, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            globals.ui.tblSales.item(row, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        except Exception as e:
            print("Error en guardar factura", e)
            import traceback
            traceback.print_exc()

    @staticmethod
    def cellsChanged(item):
        try:
            iva = 0.21
            row = item.row()
            col = item.column()

            # Only react on product ID (2) or amount (5)
            if col not in (1, 4):
                return

            value = item.text().strip()
            if not value:
                return

            globals.ui.tblSales.blockSignals(True)

            # If product ID changed, try to auto-fill name (3) and price (4)
            if col == 1:
                data = Conexion.selectProduct(value)
                if not data:
                    QtWidgets.QMessageBox.critical(None, "Error", "Product not found")
                    globals.ui.tblSales.blockSignals(False)
                    globals.ui.tblSales.setItem(row, 1, QtWidgets.QTableWidgetItem(""))
                    return
                # expected data: (name, price)
                name = data[0]
                price = float(data[1])
                # Set name and price as non-editable items
                name_item = QtWidgets.QTableWidgetItem(str(name))
                name_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                globals.ui.tblSales.setItem(row, 2, name_item)

                price_item = QtWidgets.QTableWidgetItem(f"{price:.2f}")
                price_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                globals.ui.tblSales.setItem(row, 3, price_item)

            # Calculate line total if we have price (4) and amount (5)
            price_item = globals.ui.tblSales.item(row, 3)
            qty_item = globals.ui.tblSales.item(row, 4)

            if price_item and qty_item and price_item.text().strip() and qty_item.text().strip():
                realQty = Invoice.checkStock(globals.ui.tblSales.item(row, 1).text().strip(), qty_item.text().strip())
                item = QtWidgets.QTableWidgetItem(str(realQty))
                globals.ui.tblSales.setItem(row, 4, item)

                try:
                    price = float(price_item.text())
                    qty = int(realQty)
                except Exception:
                    price = 0.0
                    qty = 0.0


                tot = round(price * qty, 2)
                tot_item = QtWidgets.QTableWidgetItem(f"{tot:.2f}")
                tot_item.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                globals.ui.tblSales.setItem(row, 5, tot_item)

            iva = 0.21
            subtotal = 0.0
            for r in range(globals.ui.tblSales.rowCount()):
                it = globals.ui.tblSales.item(r, 5)
                if it and it.text().strip():
                    try:
                        subtotal += float(it.text())
                    except Exception:
                        pass

            globals.subtotal = subtotal
            globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
            globals.ui.lblIva.setText(f"{globals.subtotal * iva:.2f} €")
            total = round(globals.subtotal + (globals.subtotal * iva), 2)
            globals.ui.lblTotal.setText(f"{total:.2f} €")

            # If both product id and qty are filled and this is the last row, append a new editable row
            last_row = globals.ui.tblSales.rowCount() - 1
            current_has_product = globals.ui.tblSales.item(row, 1) and globals.ui.tblSales.item(row, 1).text().strip()
            current_has_qty = globals.ui.tblSales.item(row, 4) and globals.ui.tblSales.item(row, 4).text().strip()

            if row == last_row and current_has_product and current_has_qty:
                record = [globals.ui.lblNumfac.text().strip(), globals.ui.tblSales.item(row, 1).text().strip(),
                         globals.ui.tblSales.item(row, 2).text().strip(), globals.ui.tblSales.item(row, 3).text().strip(),
                         globals.ui.tblSales.item(row, 4).text().strip(), globals.ui.tblSales.item(row, 5).text().strip()]
                globals.linesales.append(record)
                globals.ui.tblSales.setRowCount(last_row + 2)
                Invoice.showDeleteButton(last_row + 1)
                # Initialize new row (editable on cols 2 and 5)
                for c in range(6):
                    it = globals.ui.tblSales.item(last_row + 1, c)
                    if it:
                        if c in (1, 4):
                            it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled | QtCore.Qt.ItemFlag.ItemIsEditable)
                        else:
                            it.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)



        except Exception as e:
            print("Error en guardar factura", e)
            import traceback
            traceback.print_exc()

        finally:
            globals.ui.tblSales.blockSignals(False)

    @staticmethod
    def checkStock(prodID, qty):
        try:
            if qty in (None, '', 'None'):
                return 0

            qty = int(float(qty))
            prod = Conexion.selectFullProduct(prodID)

            if not prod or prod[2] in (None, 'None'):
                return 0

            stock = int(prod[2])

            return min(stock, qty)

        except Exception as e:
            print("error en checkStock ", e)

    @staticmethod
    def calculateTotals():
        iva = 0.21
        subtotal = 0.0
        for r in range(globals.ui.tblSales.rowCount()):
            it = globals.ui.tblSales.item(r, 5)
            if it and it.text().strip():
                try:
                    subtotal += float(it.text())
                except Exception:
                    pass

        globals.subtotal = subtotal
        globals.ui.lblSubtotal.setText(f"{globals.subtotal:.2f} €")
        globals.ui.lblIva.setText(f"{globals.subtotal * iva:.2f} €")
        total = round(globals.subtotal + (globals.subtotal * iva), 2)
        globals.ui.lblTotal.setText(f"{total:.2f} €")

    def saveSale(self):
        try:
            id = Invoice.invoiceExist(self)
            if (id != None):
                for row in globals.linesales:
                    row[0] = id

            data  = globals.linesales
            success = False
            for row in data:
                Conexion.saveSale(row)
                success = True

            if success:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Information")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setText("The sale has been saved")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide

                globals.ui.tblSales.setRowCount(0)
                Invoice.selectInvoiceById(globals.linesales[0][0])
                print(globals.linesales[0][0])


            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Error saving the sale.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide


            Invoice.loadInvoices(self)
            Invoice.products.loadTableProd()

        except Exception as e:
            print("Error en guardar factura", e)


    def invoiceExist(self):
        try:
            if globals.linesales[0][0] == "":
                globals.ui.txtDnifac.setText("00000000T")
                id = Invoice.saveWithReturn(self)
                return id
        except Exception as e:
            print("Error en guardar factura", e)

    @staticmethod
    def showDeleteButton(row):
        try:
            item = globals.ui.tblSales.item(0, 0)

            if item and item.text() == "":
                btn_del = QtWidgets.QPushButton()
                btn_del.setText("")
                btn_del.setIcon(QIcon("img/basura.png"))
                btn_del.setIconSize(QtCore.QSize(28, 28))
                btn_del.setFixedSize(QtCore.QSize(32, 32))
                btn_del.setStyleSheet("background-color: transparent; border: none")
                btn_del.setProperty("row", row)
                btn_del.clicked.connect(Invoice.deleteLine)

                globals.ui.tblSales.setCellWidget(row, 6, btn_del)
            else:
                globals.ui.tblSales.setCellWidget(row, 6, QtWidgets.QPushButton())

        except Exception as e:
            print("Error en mostrar boton", e)


    def deleteLine(self):
        try:
            btn = QtWidgets.QApplication.instance().sender()
            table = globals.ui.tblSales

            pos = btn.mapTo(table.viewport(), btn.rect().center())
            row = table.indexAt(pos).row()

            if row > 0:
                table.removeRow(row)
                Invoice.calculateTotals()

            Invoice.calculateTotals()
        except Exception as e:
            print("Error en eliminar linea", e)

    def printInvoice(self):
        try:
            id = globals.ui.lblNumfac.text().strip()
            if id == "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Warning")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setText("Error printing the invoice.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                if mbox.exec():
                    mbox.hide
            else:
                r = Reports()
                r.reportInvoice(id)

        except Exception as e:
            print("Error en guardar factura", e)

    @staticmethod
    def updateSalesStyle():
        try:
            table = globals.ui.tblSales
            table.blockSignals(True)
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    item = table.item(row, col)
                    if item is not None:
                        if col in (0, 1, 3, 4):
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        elif col == 5:
                            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

            table.blockSignals(False)
        except Exception as e:
            print("Error en guardar factura", e)
