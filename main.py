from customers import *
import events
from products import Products
from styles import load_stylesheet
from window import *
from venAux import Calendar, About, FileDialogOpen
from reports import Reports
from invoice import *
from PyQt6.QtCore import Qt

import styles
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)


        globals.vencal = Calendar()
        globals.about = About()
        globals.dlgopen = FileDialogOpen()

        # Cargar estilos
        Events.resizeTabCustomer(self)
        Events.resizeTabProds(self)
        Events.resizeTabFac(self)
        Events.resizeTabSales(self)
        Events.loadStatusBar(self)
        Invoice.activeSales()
        self.setStyleSheet(load_stylesheet())
        globals.ui.lblPrint.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)


        # Conexion
        varcli = True
        Conexion.db_conexion(self)
        Customers.loadTablecli(varcli)
        Products.loadTableProd(self)
        Invoice.loadInvoices(self)



        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.action_about.triggered.connect(Events.messageAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestoreBackup.triggered.connect(Events.restoreBackup)
        globals.ui.actionCustomers.triggered.connect(Events.exportXlsCustomers)
        globals.ui.actionCustomers_Reports.triggered.connect(Reports.runCustomerReports)

        # Functions of Historical Checkbox
        globals.ui.chkHistoricocli.stateChanged.connect(Customers.HistoricoCli)

        # Load combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)


        # Functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNomecli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtNomecli.text(), globals.ui.txtNomecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda: Customers.checkEmail(globals.ui.txtEmailcli.text()))
        globals.ui.txtMobilcli.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.txtMobilcli.text()))

        globals.ui.txtPrice.editingFinished.connect(lambda: Products.comaPunto(globals.ui.txtPrice.text()))
        globals.ui.txtNameProd.editingFinished.connect(lambda: Products.capitalizar(globals.ui.txtNameProd))

        # Functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnSavecli.clicked.connect(Customers.saveCli)
        globals.ui.btnCleanCli.clicked.connect(Customers.resetCustomer)
        globals.ui.btnModifcli.clicked.connect(Customers.modifCli)
        globals.ui.btnSearchCli.clicked.connect(Customers.buscaCli)

        globals.ui.btnSavefac.clicked.connect(Invoice.saveInvoice)
        globals.ui.btnResetfac.clicked.connect(Invoice.cleanFac)
        globals.ui.btnSaveSale.clicked.connect(Invoice.saveSale)
        globals.ui.btnPrint.clicked.connect(Invoice.printInvoice)

        globals.ui.btnSaveprod.clicked.connect(Products.saveProd)
        globals.ui.btnModifprod.clicked.connect(Products.modifProd)
        globals.ui.btnDelprod.clicked.connect(Products.delProd)




        # Functions of tables
        globals.ui.tblCustomerlist.clicked.connect(Customers.selectCustomer)

        globals.ui.tblProdlist.clicked.connect(Products.selectProd)

        globals.ui.tblFaclist.clicked.connect(Invoice.selectInvoice)

        globals.ui.tblSales.itemChanged.connect(Invoice.cellsChanged)
        Invoice.showDeleteButton(0)

        globals.ui.tblSales.itemChanged.connect(Invoice.updateSalesStyle)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()

    sys.exit(app.exec())