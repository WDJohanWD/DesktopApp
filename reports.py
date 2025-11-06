import datetime

from reportlab.pdfgen import canvas
import os

class Reports():

    def reportCustomers(self):
        try:
            rootPath = ".\\reports"
            data = datetime.now.strftime("%d/%m/%Y %H:%M:%S")
            namereportcli = data + "_reportcustomers"
            pdf_path = os.path.join(rootPath, namereportcli)
            c = canvas.Canvas('reports/customers.pdf')
            c.drawString(100,100, 'Customers')
            c.save()

            for file in os.listdir(rootPath):
                if file.endswith(namereportcli):
                    os.startfile(pdf_path)
        except Exception as error:
            print("Error en reportCustomers", error)