from datetime import *

from reportlab.pdfgen import canvas
import os

from conexion import Conexion


class Reports():

    @staticmethod
    def runCustomerReports():
        report = Reports()
        report.reportCustomers()


    def __init__(self):
        rootPath = '.\\reports'
        data = datetime.now().strftime("%m_%d_%Y_%I_%M_%S")
        self.namereportcli = data + '_reportCustomers.pdf'
        self.pdf_path = os.path.join(rootPath, self.namereportcli)
        self.c = canvas.Canvas(self.pdf_path)
        self.rootPath = rootPath

    def footer(self, titulo):
        try:
            day = datetime.now().today()
            day = day.strftime("%d/%m/%Y %H:%M:%S  -  ")
            self.c.setFont('Helvetica', 7)
            texto = day + titulo
            self.c.drawString(50, 53, texto)
            self.c.drawString(500, 53, str('Página: ' + str(self.c.getPageNumber())))
        except Exception as e:
            print('Error en footer',e)

    def toReport(self, titulo):
        try:
            path_logo = ".\\img\\logo.png"

            if (path_logo):
                self.c.line(40, 65, 550, 65)
                self.c.setFont('Helvetica-Bold', 0)
                self.c.drawString(55, 785, "EMPRESA TEIS")
                self.c.drawImage(path_logo, 440, 700, width=100, height=100)
                self.c.drawCentredString(300, 675, titulo)
                self.c.line(40, 665, 550, 665)
                # Company details
                self.c.setFont('Helvetica', 9)
                self.c.drawString(55, 760, "CIF: B12345678")
                self.c.drawString(55, 745, "Dirección: Calle Galicia, 123")
                self.c.drawString(55, 730, "Vigo 36215 - España")
                self.c.drawString(55, 715, "Teléfono: +34 986 123 456")
                self.c.drawString(55, 700, "Email: teis@mail.com")

                self.c.rect(30, 685, 200, 90)
            else:
                print('No se pudo cargar el logo')

        except Exception as e:
            print('Error en toreport',e)

    def reportCustomers(self):
        try:
            titulo = "Listado de Clientes"
            self.footer(titulo)
            self.toReport(titulo)

            records = Conexion.listCustomers(False)
            items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATUS"]
            self.c.setFont("Helvetica-Bold", 10)
            self.c.drawString(55, 651, str(items[0]))
            self.c.drawString(120, 651, str(items[1]))
            self.c.drawString(215, 651, str(items[2]))
            self.c.drawString(270, 651, str(items[3]))
            self.c.drawString(330, 651, str(items[4]))
            self.c.drawString(395, 651, str(items[5]))
            self.c.drawString(490, 651, str(items[6]))
            self.c.line(40, 645, 550, 645)
            x = 55
            y = 630

            for record in records:
                if y <= 90:
                    self.c.setFont("Helvetica-Oblique", 8)
                    self.c.drawString(450, 75, "Página siguiente...")
                    self.c.showPage()  # crea una nueva página
                    items = ["DNI_NIE", "SURNAME", "NAME", "MOBILE", "CITY", "INVOICE TYPE", "STATUS"]
                    self.c.setFont("Helvetica-Bold", 10)
                    self.c.drawString(55, 650, str(items[0]))
                    self.c.drawString(75, 650, str(items[1]))
                    self.c.drawString(115, 650, str(items[2]))
                    self.c.drawString(230, 650, str(items[3]))
                    self.c.drawString(360, 650, str(items[4]))
                    self.c.drawString(390, 650, str(items[5]))
                    self.c.drawString(480, 650, str(items[6]))
                    self.c.line(40, 645, 550, 645)
                    x = 55
                    y = 630

                self.c.setFont("Helvetica", 8)
                dni = "***" + str(record[0][4:7] + "***")
                self.c.drawCentredString(x + 19, y, dni)
                self.c.drawString(x + 65, y, record[2])
                self.c.drawString(x + 160, y, record[3])
                self.c.drawString(x + 215, y, str(record[5]))
                self.c.drawString(x + 275, y, record[8])
                self.c.drawString(x + 340, y, record[9])
                if str(record[10]) == "True":
                    self.c.drawString(x + 430, y, "Active")
                else:
                    self.c.drawString(x + 430, y, "Inactive")
                y = y - 25
            self.c.save()

            for file in os.listdir(self.rootPath):
                if file.endswith(self.namereportcli):
                    os.startfile(self.pdf_path)

        except Exception as error:
            print("There was an error with customersReports: ", error)