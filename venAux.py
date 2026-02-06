import events
import globals
from dlgAbout import Ui_dlgAbout
from dlgCalendar import *
from datetime import datetime

from events import *


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        globals.vencal = Ui_dlgCalendar()
        globals.vencal.setupUi(self)
        day = datetime.now().day
        month = datetime.now().month
        year = datetime.now().year

        globals.vencal.Calendar.setSelectedDate(QtCore.QDate(year, month, day))
        globals.vencal.Calendar.clicked.connect(events.Events.loadData)


class DlgAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DlgAbout, self).__init__()
        globals.about = Ui_dlgAbout()
        globals.about.setupUi(self)
        globals.about.btnCloseabout.clicked.connect(events.Events.closeabout)


class FileDialogOpen(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogOpen, self).__init__()
