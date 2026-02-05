"""
reports.py

Adapted from DI_Proyecto/reports.py. Uses os.path.join for paths
and ensures the reports directory exists before writing the PDF.
"""
from datetime import datetime
import os

from reportlab.pdfgen import canvas

# Try to import Conexion (which depends on PyQt6). If unavailable, fall back to
# reading the sqlite database directly with the standard library so reports can
# be generated without the PyQt6 dependency.
Conexion = None
def _get_records_sqlite(var):
    """Fallback: read the customers table directly from the sqlite DB.
    Returns a list of rows (lists) matching the shape used in the PDF generator.
    """
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'bbdd.sqlite')
    if not os.path.exists(db_path):
        print('Base de datos no encontrada en', db_path)
        return []
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        if var:
            cur.execute("SELECT * FROM customers WHERE historical = 'True' ORDER BY surname")
        else:
            cur.execute("SELECT * FROM customers ORDER BY surname")
        rows = cur.fetchall()
        # convert tuples to lists for compatibility
        rows_list = [list(r) for r in rows]
        conn.close()
        return rows_list
    except Exception as e:
        print('Error leyendo sqlite:', e)
        return []

try:
    from conexion import Conexion as _Conexion
    Conexion = _Conexion
except Exception:
    # Conexion (PyQt6) not available; we'll use the sqlite fallback above
    Conexion = None

def get_records(var):
    """Unified accessor for records: prefer Conexion.listCustomers when available,
    otherwise fall back to direct sqlite access.
    """
    if Conexion:
        try:
            return Conexion.listCustomers(var)
        except Exception:
            return _get_records_sqlite(var)
    else:
        return _get_records_sqlite(var)


class Reports:

    @staticmethod
    def runCustomerReports():
        report = Reports()
        report.reportCustomers()


    def __init__(self):
        # create reports directory inside project root if missing
        rootPath = os.path.join(os.path.dirname(__file__), 'reports')
        os.makedirs(rootPath, exist_ok=True)
        data = datetime.now().strftime("%m_%d_%Y_%I_%M_%S")
        self.namereportcli = data + '_reportCustomers.pdf'
        self.pdf_path = os.path.join(rootPath, self.namereportcli)
        self.c = canvas.Canvas(self.pdf_path)
        self.rootPath = rootPath

    def footer(self, titulo):
        try:
            day = datetime.now().strftime("%d/%m/%Y %H:%M:%S  -  ")
            self.c.setFont('Helvetica', 7)
            texto = day + titulo
            self.c.drawString(50, 53, texto)
            self.c.drawString(500, 53, str('Página: ' + str(self.c.getPageNumber())))
        except Exception as e:
            print('Error en footer', e)

    def toReport(self, titulo):
        try:
            # use a safe relative path to the project's img folder
            path_logo = os.path.join(os.path.dirname(__file__), 'img', 'logo.png')

            if os.path.exists(path_logo):
                self.c.line(40, 65, 550, 65)
                self.c.setFont('Helvetica-Bold', 0)
                self.c.drawString(55, 785, "EMPRESA TEIS")
                # drawImage expects a path; coordinates are tuned for the PDF
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
                print('No se pudo cargar el logo:', path_logo)

        except Exception as e:
            print('Error en toReport', e)

    def reportCustomers(self):
        try:
            titulo = "Listado de Clientes"
            self.footer(titulo)
            self.toReport(titulo)

            # obtain records via the unified accessor (may use Conexion or sqlite fallback)
            records = get_records(False)
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
                    self.c.showPage()
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
                try:
                    dni_raw = str(record[0]) if record and len(record) > 0 else ''
                    # mask part of the DNI safely
                    if len(dni_raw) >= 7:
                        dni = "***" + dni_raw[4:7] + "***"
                    else:
                        dni = dni_raw
                except Exception:
                    dni = ''

                self.c.drawCentredString(x + 19, y, dni)
                # Guard against index errors if record has different shape
                try:
                    self.c.drawString(x + 65, y, record[2])
                except Exception:
                    pass
                try:
                    self.c.drawString(x + 160, y, record[3])
                except Exception:
                    pass
                try:
                    self.c.drawString(x + 215, y, str(record[5]))
                except Exception:
                    pass
                try:
                    self.c.drawString(x + 275, y, record[8])
                except Exception:
                    pass
                try:
                    self.c.drawString(x + 340, y, record[9])
                except Exception:
                    pass
                try:
                    if str(record[10]) == "True":
                        self.c.drawString(x + 430, y, "Active")
                    else:
                        self.c.drawString(x + 430, y, "Inactive")
                except Exception:
                    pass

                y = y - 25
            self.c.save()

            # open the created PDF if it exists
            if os.path.exists(self.pdf_path):
                try:
                    os.startfile(self.pdf_path)
                except Exception:
                    print('PDF creado en', self.pdf_path)

        except Exception as error:
            print("There was an error with customersReports:", error)
