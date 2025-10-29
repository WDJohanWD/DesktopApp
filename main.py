from asyncio import Event

from PyQt6.QtWidgets import QTabWidget

import customers
import events
import globals

from conexion import Conexion
from events import *
from customers import *
from styles import load_stylesheet
from window import *
from venAux import Calendar

import sys
import  styles
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.setStyleSheet(load_stylesheet())
        globals.ui = Ui_MainWindow()
        globals.ui.setupUi(self)
        globals.vencal = Calendar()

        #Conexion
        varcli = True
        Conexion.db_conexion(self)
        customers.Customers.loadTablecli(varcli)

        # Functions in menu bar
        globals.ui.actionExit.triggered.connect(Events.messageExit)

        Events.loadProv(self)
        globals.ui.cmbProvcli.currentIndexChanged.connect(events.Events.loadMunicli)


        # Functions in lineEdit
        globals.ui.txtDnicli.editingFinished.connect(Customers.checkDni)
        globals.ui.txtNomecli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtNomecli.text(), globals.ui.txtNomecli))
        globals.ui.txtApelcli.editingFinished.connect(lambda: Customers.capitalizar(globals.ui.txtApelcli.text(), globals.ui.txtApelcli))
        globals.ui.txtEmailcli.editingFinished.connect(lambda: Customers.checkEmail(globals.ui.txtEmailcli.text()))
        globals.ui.txtMobilcli.editingFinished.connect(lambda: Customers.checkMobil(globals.ui.txtMobilcli.text()))


        globals.ui.chkHistoricocli.stateChanged.connect(Customers.Historicocli)
        # Functions of buttons
        globals.ui.btnFechaltacli.clicked.connect(Events.openCalendar)
        globals.ui.btnDelcli.clicked.connect(Customers.delCliente)
        # function of table
        globals.ui.tableCustomerlist.clicked.connect(Customers.selectCustomer)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())