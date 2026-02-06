import customers
import events
import globals
import invoice
from conexion import Conexion
from customers import *
from invoice import Invoice
from products import *
from dlgAbout import *
from venAux import *
from window import *
from dlgCalendar import *
import sys
from reports import *
from events import *
import styles


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)

        # Instances
        globals.vencal = Calendar()
        globals.about = DlgAbout()
        globals.dlgopen = FileDialogOpen
        self.report = Reports()
        self.invoice = Invoice()

        # Load styles
        self.setStyleSheet(styles.load_stylesheet())

        # Database connection
        varcli = True
        Conexion.db_conexion(self)
        Customers.loadTablecli(varcli)
        Events.resizeTabCustomer(self)
        Products.loadTableProducts()
        Events.resizeTabProducts(self)
        Events.resizeTabSales(self)

        Invoice.loadTableInvoice(self=None)
        Invoice.loadInvoiceirst()

        # Load combo from array
        combo = ["Foods", "Furniture", "Clothes", "Electronic"]
        globals.ui.comboBox.addItems(combo)

        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.actionAbout.triggered.connect(Events.messageAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestore_Backup.triggered.connect(Events.restoreBackup)
        globals.ui.actionCustomers.triggered.connect(Events.exportXlsCustomers)
        globals.ui.actionCustomer_Report.triggered.connect(self.report.reportCustomers)
        globals.ui.actionProducts_Report.triggered.connect(self.report.reportProducts)

        # Functions in line-edit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNomecli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtNomecli.text(), globals.ui.txtNomecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda: Customers.checkMail(globals.ui.txtEmailcli.text()))
        globals.ui.txtMobilecli.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.txtMobilecli.text()))
        globals.ui.txtPrice.editingFinished.connect(lambda: Products.comaPunto(globals.ui.txtPrice.text()))
        globals.ui.txtDniFac.editingFinished.connect(Invoice.searchInvoice)

        # Functions of chkHistoricocli
        globals.ui.chkHistoricocli.stateChanged.connect(Customers.Historicocli)

        # Functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnSavecli.clicked.connect(Customers.saveCli)
        globals.ui.btnCleancli.clicked.connect(Customers.cleanCli)
        globals.ui.btnModifcli.clicked.connect(Customers.modifcli)
        globals.ui.btnSearchcli.clicked.connect(Customers.searchCli)
        globals.ui.btnCleanpro.clicked.connect(Products.cleanPro)
        globals.ui.btnSavepro.clicked.connect(Products.savePro)
        globals.ui.btnModpro.clicked.connect(Products.modifyPro)
        globals.ui.btndelpro.clicked.connect(Products.delPro)
        globals.ui.btnCleanfac.clicked.connect(Invoice.reloadInvoice)
        globals.ui.btnSavefac.clicked.connect(Invoice.saveInvoice)
        globals.ui.btnsalesave.clicked.connect(Invoice.saveSales)

        # Keyboard shortcuts
        self.cleanFac = QtGui.QShortcut(QtGui.QKeySequence("F11"), self)
        self.cleanFac.activated.connect(invoice.Invoice.reloadInvoice)

        # Functions Combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)

        # Functions of tables
        globals.ui.tableCustomerlist.clicked.connect(Customers.selectCustomer)
        globals.ui.tblProducts.clicked.connect(Products.selectPro)
        globals.ui.tablefacv.clicked.connect(Invoice.selectInvoice)
        globals.ui.tabsales.itemChanged.connect(self.invoice.cellChangedSales)

        # Functions statusbar
        Events.loadStatusbar(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
