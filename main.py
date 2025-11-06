



from customers import *
import events
from styles import load_stylesheet
from window import *
from venAux import Calendar, About, FileDialogOpen

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
        self.setStyleSheet(load_stylesheet())

        # Conexion
        varcli = True
        Conexion.db_conexion(self)
        Customers.loadTablecli(varcli)



        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)
        globals.ui.action_about.triggered.connect(Events.messageAbout)
        globals.ui.actionBackup.triggered.connect(Events.saveBackup)
        globals.ui.actionRestoreBackup.triggered.connect(Events.restoreBackup)
        globals.ui.actionCustomers.triggered.connect(Events.exportXlsCustomers)

        # Functions of Historical Checkbox
        globals.ui.chkHistoricocli.stateChanged.connect(Customers.Historicocli)

        # Load combobox
        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)


        # Functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNomecli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtNomecli.text(), globals.ui.txtNomecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda: Customers.checkEmail(globals.ui.txtEmailcli.text()))
        globals.ui.txtMobilcli.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.txtMobilcli.text()))

        # Functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        globals.ui.btnSavecli.clicked.connect(Customers.saveCli)
        globals.ui.btnCleanCli.clicked.connect(Customers.resetCustomer)
        globals.ui.btnModifcli.clicked.connect(Customers.modifCli)
        globals.ui.btnSearchCli.clicked.connect(Customers.buscaCli)


        # Functions of tables
        globals.ui.tblCustomerlist.clicked.connect(Customers.selectCustomer)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()

    sys.exit(app.exec())