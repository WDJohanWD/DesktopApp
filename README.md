# DesktopApp - Aplicacion de Gestion Empresarial

Aplicacion de escritorio desarrollada con **Python** y **PyQt6** para la gestion de clientes, productos, facturas y ventas de una empresa. Usa **SQLite** como base de datos y **ReportLab** para generar informes en PDF.

---

## Indice

1. [Estructura del Proyecto](#estructura-del-proyecto)
2. [Arquitectura General](#arquitectura-general)
3. [Base de Datos (SQLite)](#base-de-datos-sqlite)
4. [Archivos del Proyecto - Explicacion Detallada](#archivos-del-proyecto---explicacion-detallada)
   - [main.py - Punto de Entrada](#mainpy---punto-de-entrada)
   - [window.py - Interfaz Grafica (UI)](#windowpy---interfaz-grafica-ui)
   - [globals.py - Variables Globales](#globalspy---variables-globales)
   - [conexion.py - Capa de Datos (Base de Datos)](#conexionpy---capa-de-datos-base-de-datos)
   - [customers.py - Logica de Clientes](#customerspy---logica-de-clientes)
   - [products.py - Logica de Productos](#productspy---logica-de-productos)
   - [invoice.py - Logica de Facturas y Ventas](#invoicepy---logica-de-facturas-y-ventas)
   - [events.py - Eventos Generales](#eventspy---eventos-generales)
   - [reports.py - Generacion de Informes PDF](#reportspy---generacion-de-informes-pdf)
   - [venAux.py - Ventanas Auxiliares (Dialogos)](#venauxpy---ventanas-auxiliares-dialogos)
   - [styles.py y styles.qss - Estilos Visuales](#stylespy-y-stylesqss---estilos-visuales)
   - [dlgAbout.py y dlgCalendar.py - UI de Dialogos](#dlgaboutpy-y-dlgcalendarpy---ui-de-dialogos)
5. [Flujo de la Aplicacion](#flujo-de-la-aplicacion)
6. [Nombres de Widgets Importantes](#nombres-de-widgets-importantes)
7. [Patrones y Convenciones del Codigo](#patrones-y-convenciones-del-codigo)
8. [Guia Practica: Como Anadir Funcionalidades](#guia-practica-como-anadir-funcionalidades)
9. [Dependencias](#dependencias)

---

## Estructura del Proyecto

```
DesktopApp/
├── main.py              # Punto de entrada, crea la ventana principal y conecta senales
├── window.py            # UI generada con Qt Designer (pyuic6) - NO EDITAR MANUALMENTE
├── globals.py           # Variables globales compartidas entre modulos
├── conexion.py          # Todas las consultas SQL (CRUD) a la base de datos
├── customers.py         # Logica de negocio para clientes
├── products.py          # Logica de negocio para productos
├── invoice.py           # Logica de negocio para facturas y lineas de venta
├── events.py            # Eventos generales (exit, calendar, backup, resize tablas, etc.)
├── reports.py           # Generacion de PDFs con ReportLab
├── venAux.py            # Clases para ventanas auxiliares (Calendar, About, FileDialog)
├── styles.py            # Funcion que carga el archivo QSS
├── styles.qss           # Hoja de estilos QSS (como CSS pero para Qt)
├── dlgAbout.py          # UI del dialogo "Acerca de" (generado con pyuic6)
├── dlgCalendar.py       # UI del dialogo del calendario (generado con pyuic6)
├── conexionserver.py    # (Extra) Conexion alternativa a servidor
├── data/
│   └── bbdd.sqlite      # Base de datos SQLite
├── img/                 # Iconos e imagenes de la aplicacion
├── templates/
│   ├── window.ui        # Archivo Qt Designer de la ventana principal
│   ├── dlgAbout.ui      # Archivo Qt Designer del dialogo About
│   └── dlgCalendar.ui   # Archivo Qt Designer del dialogo Calendar
├── reports/             # Carpeta donde se guardan los PDFs de informes de clientes
└── invoices/            # Carpeta donde se guardan los PDFs de facturas
```

---

## Arquitectura General

La aplicacion sigue una arquitectura de **3 capas** separadas:

```
┌──────────────────────────────────────────────────────┐
│                    PRESENTACION (UI)                  │
│  window.py, dlgAbout.py, dlgCalendar.py, styles.qss  │
│  (Generados con Qt Designer - NO tocar manualmente)  │
└──────────────────┬───────────────────────────────────┘
                   │ globals.ui.widgetName
┌──────────────────▼───────────────────────────────────┐
│               LOGICA DE NEGOCIO                       │
│  customers.py, products.py, invoice.py, events.py     │
│  (Aqui se valida, se procesan datos, se reacciona)    │
└──────────────────┬───────────────────────────────────┘
                   │ Conexion.metodo()
┌──────────────────▼───────────────────────────────────┐
│               CAPA DE DATOS                           │
│  conexion.py (SQL con QtSql) + data/bbdd.sqlite       │
│  (Todas las consultas SELECT, INSERT, UPDATE, DELETE) │
└──────────────────────────────────────────────────────┘
```

**Flujo general:**
1. `main.py` crea la ventana y conecta **senales** (clicks, edits) a **metodos** de las clases de logica
2. Cuando el usuario interactua, se ejecuta el metodo correspondiente (ej: `Customers.saveCli`)
3. Ese metodo accede a la UI mediante `globals.ui.widgetName` para leer/escribir datos
4. Para operaciones de BD, llama a `Conexion.metodo()` que ejecuta la consulta SQL
5. Tras la operacion, se recarga la tabla correspondiente para reflejar los cambios

---

## Base de Datos (SQLite)

La base de datos `data/bbdd.sqlite` contiene estas tablas:

### Tabla `customers` (Clientes)
| Columna      | Tipo   | Descripcion                          | Indice |
|--------------|--------|--------------------------------------|--------|
| dni_nie      | TEXT   | DNI o NIE del cliente (clave unica)  | 0      |
| adddata      | TEXT   | Fecha de alta                        | 1      |
| surname      | TEXT   | Apellidos                            | 2      |
| name         | TEXT   | Nombre                               | 3      |
| mail         | TEXT   | Email                                | 4      |
| mobile       | TEXT   | Telefono movil                       | 5      |
| address      | TEXT   | Direccion                            | 6      |
| province     | TEXT   | Provincia                            | 7      |
| city         | TEXT   | Municipio                            | 8      |
| invoicetype  | TEXT   | Tipo factura: "paper" o "electronic" | 9      |
| historical   | TEXT   | "True" = activo, "False" = baja      | 10     |

### Tabla `productos` (Productos)
| Columna    | Tipo    | Descripcion            | Indice |
|------------|---------|------------------------|--------|
| idprod     | INTEGER | ID auto-incremental    | 0      |
| name       | TEXT    | Nombre del producto    | 1      |
| stock      | INTEGER | Cantidad en stock      | 2      |
| family     | TEXT    | Familia/Categoria      | 3      |
| unityprice | REAL    | Precio por unidad      | 4      |

### Tabla `invoices` (Facturas)
| Columna | Tipo    | Descripcion                    | Indice |
|---------|---------|--------------------------------|--------|
| idFac   | INTEGER | ID factura auto-incremental    | 0      |
| dni_nie | TEXT    | DNI del cliente                | 1      |
| date    | TEXT    | Fecha de la factura            | 2      |

### Tabla `sales` (Lineas de venta)
| Columna   | Tipo    | Descripcion                    | Indice |
|-----------|---------|--------------------------------|--------|
| idv       | INTEGER | ID venta auto-incremental      | 0      |
| idFac     | INTEGER | ID factura (FK a invoices)     | 1      |
| idProd    | INTEGER | ID producto (FK a productos)   | 2      |
| product   | TEXT    | Nombre del producto            | 3      |
| uniprice  | REAL    | Precio unitario                | 4      |
| amount    | INTEGER | Cantidad vendida               | 5      |
| total     | REAL    | Total de la linea (price*qty)  | 6      |

### Tabla `provincias`
| Columna   | Tipo    | Descripcion          |
|-----------|---------|----------------------|
| idprov    | INTEGER | ID provincia         |
| provincia | TEXT    | Nombre de provincia  |

### Tabla `municipios`
| Columna   | Tipo    | Descripcion                    |
|-----------|---------|--------------------------------|
| id        | INTEGER | ID municipio                   |
| municipio | TEXT    | Nombre del municipio           |
| idprov    | INTEGER | ID provincia (FK a provincias) |

---

## Archivos del Proyecto - Explicacion Detallada

### main.py - Punto de Entrada

Este es el archivo que arranca la aplicacion. Su funcion es:

1. **Crear la ventana principal** usando `Ui_MainWindow` de `window.py`
2. **Instanciar ventanas auxiliares** (Calendar, About, FileDialog) y guardarlas en `globals`
3. **Inicializar la UI** (resize de tablas, cargar statusbar, estilos)
4. **Conectar a la BD** con `Conexion.db_conexion()`
5. **Cargar datos iniciales** en las tablas (clientes, productos, facturas)
6. **Conectar TODAS las senales** (clicks de botones, cambios en campos, etc.)

```python
# Asi se conecta una senal a una funcion:
globals.ui.btnSavecli.clicked.connect(Customers.saveCli)
#         ^widget       ^senal          ^metodo que se ejecuta

# Para senales con parametros se usa lambda:
globals.ui.txtEmailcli.editingFinished.connect(
    lambda: Customers.checkEmail(globals.ui.txtEmailcli.text())
)
```

**IMPORTANTE - Aqui es donde se conectan TODOS los botones y acciones.** Si en el examen te piden anadir un boton nuevo, tienes que:
1. Crear el widget en Qt Designer (o en window.py)
2. Crear el metodo en la clase correspondiente
3. Conectar la senal aqui en main.py

**Senales conectadas actualmente:**

| Widget | Senal | Metodo | Que hace |
|--------|-------|--------|----------|
| `actionExit` | triggered | `Events.messageExit` | Pregunta si quieres salir |
| `action_about` | triggered | `Events.messageAbout` | Muestra dialogo About |
| `actionBackup` | triggered | `Events.saveBackup` | Guarda backup en ZIP |
| `actionRestoreBackup` | triggered | `Events.restoreBackup` | Restaura backup |
| `actionCustomers` | triggered | `Events.exportXlsCustomers` | Exporta clientes a CSV |
| `actionCustomers_Reports` | triggered | `Reports.runCustomerReports` | Genera PDF de clientes |
| `chkHistoricocli` | stateChanged | `Customers.HistoricoCli` | Filtra clientes activos/todos |
| `cmbProvcli` | currentIndexChanged | `Events.loadMunicli` | Carga municipios al cambiar provincia |
| `txtDnicli` | editingFinished | `Customers.checkDni` | Valida formato DNI/NIE |
| `txtNomecli` | editingFinished | `Customers.capitalizar` | Capitaliza nombre |
| `txtApelcli` | editingFinished | `Customers.capitalizar` | Capitaliza apellidos |
| `txtEmailcli` | editingFinished | `Customers.checkEmail` | Valida formato email |
| `txtMobilcli` | editingFinished | `Customers.checkMobil` | Valida formato movil |
| `txtPrice` | editingFinished | `Products.comaPunto` | Reemplaza coma por punto |
| `txtNameProd` | editingFinished | `Products.capitalizar` | Capitaliza nombre producto |
| `btnFechaltacli` | clicked | `Events.openCalendar` | Abre calendario |
| `btnDelcli` | clicked | `Customers.delCliente` | Baja logica del cliente |
| `btnSavecli` | clicked | `Customers.saveCli` | Guarda nuevo cliente |
| `btnCleanCli` | clicked | `Customers.resetCustomer` | Limpia formulario cliente |
| `btnModifcli` | clicked | `Customers.modifCli` | Modifica cliente existente |
| `btnSearchCli` | clicked | `Customers.buscaCli` | Busca cliente por DNI |
| `btnSavefac` | clicked | `Invoice.saveInvoice` | Guarda nueva factura |
| `btnResetfac` | clicked | `Invoice.cleanFac` | Limpia formulario factura |
| `btnSaveSale` | clicked | `Invoice.saveSale` | Guarda las lineas de venta |
| `btnPrint` | clicked | `Invoice.printInvoice` | Imprime factura en PDF |
| `btnSaveprod` | clicked | `Products.saveProd` | Guarda nuevo producto |
| `btnModifprod` | clicked | `Products.modifProd` | Modifica producto |
| `btnDelprod` | clicked | `Products.delProd` | Elimina producto |
| `tblCustomerlist` | clicked | `Customers.selectCustomer` | Carga datos del cliente seleccionado |
| `tblProdlist` | clicked | `Products.selectProd` | Carga datos del producto seleccionado |
| `tblFaclist` | clicked | `Invoice.selectInvoice` | Carga factura seleccionada y sus ventas |
| `tblSales` | itemChanged | `Invoice.cellsChanged` | Reacciona cuando se edita una celda de venta |
| `tblSales` | itemChanged | `Invoice.updateSalesStyle` | Actualiza alineacion de la tabla |

---

### window.py - Interfaz Grafica (UI)

**NO EDITAR ESTE ARCHIVO MANUALMENTE.** Es generado automaticamente desde `templates/window.ui` con el comando:

```bash
pyuic6 -x templates/window.ui -o window.py
```

Si necesitas modificar la interfaz:
1. Abre `templates/window.ui` con **Qt Designer**
2. Haz los cambios visuales
3. Regenera `window.py` con el comando anterior

Este archivo define la clase `Ui_MainWindow` que contiene TODOS los widgets de la ventana principal. La ventana tiene un `QTabWidget` llamado `TabProducts` con pestanas para Clientes, Productos, Facturas y Ventas.

---

### globals.py - Variables Globales

```python
ui = None          # Referencia a la UI principal (Ui_MainWindow)
vencal = None      # Referencia al dialogo del calendario
about = None       # Referencia al dialogo About
estado = None      # Estado del cliente seleccionado ("True"/"False")
dlgopen = None     # Referencia al dialogo de abrir archivo
subtotal = 0       # Subtotal actual de la factura
linesales = []     # Lista de lineas de venta pendientes de guardar
```

**Como se usa `globals`:**
- Desde cualquier archivo puedes acceder a la UI: `globals.ui.txtDnicli.text()`
- Para leer un campo: `globals.ui.txtNomecli.text()`
- Para escribir en un campo: `globals.ui.txtNomecli.setText("valor")`
- Para acceder a una tabla: `globals.ui.tblCustomerlist`
- `globals.linesales` almacena las lineas de venta que aun no se han guardado en BD
- `globals.subtotal` acumula el subtotal de la factura actual

---

### conexion.py - Capa de Datos (Base de Datos)

Contiene la clase `Conexion` con TODOS los metodos que interactuan con SQLite. Usa **QtSql** (no sqlite3 directamente).

**Patron de todas las consultas:**
```python
def metodoEjemplo(parametro):
    query = QtSql.QSqlQuery()
    query.prepare("SELECT * FROM tabla WHERE campo = :param")
    query.bindValue(":param", str(parametro))
    if query.exec():
        while query.next():
            # query.value(0) = primera columna, query.value(1) = segunda, etc.
            resultado.append(query.value(0))
    return resultado
```

**Metodos disponibles:**

| Metodo | Parametros | Retorna | Descripcion |
|--------|------------|---------|-------------|
| `db_conexion()` | - | bool | Conecta con `data/bbdd.sqlite` |
| `listProv()` | - | list[str] | Lista de provincias |
| `listMuniProv(province)` | nombre provincia | list[str] | Municipios de una provincia |
| `listCustomers(varcli)` | bool (True=activos, False=todos) | list[list] | Lista de clientes |
| `dataOneCustomer(dato)` | DNI o movil | list | Datos de un cliente |
| `addCli(newCli)` | list con 10 campos | bool | Inserta cliente nuevo |
| `modifCli(dni, modifCli)` | DNI + list con campos | bool | Actualiza cliente |
| `deleteCli(dni)` | DNI | bool | Baja logica (historical=False) |
| `buscaCli(dni)` | DNI | bool | Comprueba si existe cliente |
| `listProds()` | - | list[list] | Lista de productos |
| `dataOneProduct(code)` | ID producto | list | Datos de un producto |
| `addProd(newProd)` | list[nombre,stock,familia,precio] | bool | Inserta producto |
| `modifProd(id, modifProd)` | ID + list de campos | bool | Actualiza producto |
| `deleteProd(id)` | ID producto | bool | Elimina producto (DELETE real) |
| `insertInvoice(dni)` | DNI | bool | Crea factura (fecha automatica) |
| `invoiceWithReturn(dni)` | DNI | int/None | Crea factura y devuelve su ID |
| `allInvoices()` | - | list[list] | Todas las facturas (orden DESC) |
| `getOneInvoice(invoiceId)` | ID factura | list | Datos de una factura |
| `deleteInvoice(invoiceId)` | ID factura | bool | Elimina factura |
| `selectProduct(item)` | ID producto | [nombre,precio] | Nombre y precio de un producto |
| `selectFullProduct(item)` | ID producto | list completa | Todos los datos de un producto |
| `saveSale(data)` | list[idFac,idProd,product,price,qty,total] | bool | Guarda venta + actualiza stock |
| `getSales(idFac)` | ID factura | list[list] | Lineas de venta de una factura |

**IMPORTANTE para el examen - Como anadir una nueva consulta:**
```python
# Ejemplo: anadir metodo para buscar productos por nombre
def buscarProductoPorNombre(nombre):
    try:
        resultados = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM productos WHERE name LIKE :nombre")
        query.bindValue(":nombre", "%" + str(nombre) + "%")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                resultados.append(row)
        return resultados
    except Exception as e:
        print("Error buscando producto", e)
```

---

### customers.py - Logica de Clientes

Clase `Customers` con toda la logica de la pestana de clientes.

**Metodos:**

| Metodo | Que hace |
|--------|----------|
| `checkDni()` | Valida que el DNI/NIE tenga formato correcto (8 digitos + letra). Si falla pone fondo rosa |
| `capitalizar(texto, widget)` | Convierte texto a formato Title (primera letra mayuscula) |
| `checkEmail(email)` | Valida formato email con regex `^[\w\.-]+@[\w\.-]+\.\w+$`. Si falla pone fondo rosa |
| `checkMobil(numero)` | Valida movil espanol (empieza por 6 o 7, 9 digitos). Si falla pone fondo rosa |
| `loadTablecli(varcli)` | Carga la tabla de clientes desde BD. `varcli=True` solo activos, `False` todos |
| `selectCustomer()` | Al hacer click en una fila, carga los datos en el formulario |
| `saveCli()` | Lee el formulario y guarda nuevo cliente en BD |
| `modifCli()` | Lee el formulario y actualiza el cliente existente |
| `delCliente()` | Baja logica: pone `historical=False` (no borra de BD) |
| `resetCustomer()` | Limpia todos los campos del formulario |
| `buscaCli()` | Busca cliente por DNI y muestra sus datos |
| `HistoricoCli()` | Al cambiar el checkbox, filtra clientes activos o muestra todos |

**Validaciones con colores:**
- **Fondo verde claro** `rgb(255, 255, 220)`: dato valido
- **Fondo rosa** `#FFC0CB`: dato invalido

---

### products.py - Logica de Productos

Clase `Products` con la logica de la pestana de productos.

**Metodos:**

| Metodo | Que hace |
|--------|----------|
| `loadTableProd()` | Carga tabla productos. Si stock < 10, muestra la fila en rojo y negrita |
| `saveProd()` | Guarda nuevo producto (nombre, stock, familia, precio) |
| `modifProd()` | Modifica producto existente |
| `delProd()` | Elimina producto (DELETE real, no logico) |
| `selectProd()` | Al hacer click, carga datos del producto en el formulario |
| `resetProduct()` | Limpia formulario de productos |
| `capitalizar(widget)` | Capitaliza el texto de un widget |
| `comaPunto(valor)` | Convierte comas a puntos en el precio (formato europeo a decimal) |

---

### invoice.py - Logica de Facturas y Ventas

Clase `Invoice` - La mas compleja. Gestiona facturas y lineas de venta.

**Conceptos clave:**
- Una **factura** (`invoices`) es una cabecera con DNI + fecha
- Una factura tiene **lineas de venta** (`sales`) con productos, cantidades y precios
- Las lineas se editan en `tblSales` antes de guardarse
- `globals.linesales` almacena las lineas pendientes (en memoria, no en BD)
- Si el DNI es "00000000T" se crea como **factura simplificada**

**Metodos:**

| Metodo | Que hace |
|--------|----------|
| `buscaCli(dni)` | Busca cliente y rellena labels de la factura (nombre, tipo, direccion, estado) |
| `cleanFac()` | Limpia todo el formulario de facturas y la tabla de ventas |
| `saveInvoice()` | Crea nueva factura en BD (solo cabecera, sin lineas) |
| `saveWithReturn()` | Crea factura y devuelve su ID (para despues anadir lineas) |
| `loadInvoices()` | Carga tabla de facturas con boton de eliminar en cada fila |
| `deleteInvoice()` | Elimina factura (solo si no tiene ventas asociadas) |
| `selectInvoice()` | Al hacer click en factura, carga sus datos y lineas de venta |
| `selectInvoiceById(id)` | Carga una factura por ID (usado internamente) |
| `activeSales()` | Prepara la tabla de ventas con celdas editables |
| `cellsChanged(item)` | **CLAVE** - Se ejecuta cuando el usuario edita una celda de venta |
| `checkStock(prodID, qty)` | Verifica que haya stock suficiente |
| `calculateTotals()` | Recalcula subtotal, IVA (21%) y total |
| `saveSale()` | Guarda TODAS las lineas de `globals.linesales` en BD |
| `invoiceExist()` | Si no hay factura creada, la crea automaticamente |
| `showDeleteButton(row)` | Muestra boton de eliminar linea en cada fila |
| `deleteLine()` | Elimina una linea de venta de la tabla |
| `printInvoice()` | Genera PDF de la factura |
| `updateSalesStyle()` | Aplica alineacion a las celdas de la tabla de ventas |

**Como funciona `cellsChanged` (la logica mas compleja):**
```
Usuario escribe ID producto (columna 1)
  → Se busca el producto en BD con Conexion.selectProduct()
  → Se auto-rellena nombre (col 2) y precio (col 3)

Usuario escribe cantidad (columna 4)
  → Se verifica stock con checkStock()
  → Se calcula total = precio * cantidad (col 5)
  → Se recalculan subtotal, IVA y total general

Si es la ultima fila y esta completa
  → Se anade la linea a globals.linesales
  → Se crea una nueva fila vacia para seguir anadiendo
```

**Columnas de tblSales:**
| Col | Campo | Editable |
|-----|-------|----------|
| 0 | ID Venta | No |
| 1 | ID Producto | Si |
| 2 | Nombre producto | No (auto) |
| 3 | Precio unitario | No (auto) |
| 4 | Cantidad | Si |
| 5 | Total linea | No (auto) |
| 6 | Boton eliminar | - |

---

### events.py - Eventos Generales

Clase `Events` con funciones transversales que no pertenecen a una entidad especifica.

**Metodos:**

| Metodo | Que hace |
|--------|----------|
| `messageExit()` | Muestra dialogo de confirmacion para salir |
| `openCalendar()` | Muestra el dialogo del calendario |
| `loadData(qDate)` | Recibe la fecha seleccionada del calendario y la pone en `txtAltacli` |
| `loadProv()` | Carga el combobox de provincias desde BD |
| `loadMunicli()` | Carga municipios segun la provincia seleccionada |
| `messageAbout()` | Muestra dialogo About |
| `closeAbout()` | Cierra dialogo About |
| `resizeTabCustomer()` | Ajusta columnas de tabla clientes (Stretch + ResizeToContents) |
| `resizeTabProds()` | Ajusta columnas de tabla productos |
| `resizeTabFac()` | Ajusta columnas de tabla facturas (anchos fijos) |
| `resizeTabSales()` | Ajusta columnas de tabla ventas |
| `saveBackup()` | Abre dialogo para guardar backup (ZIP de la BD) |
| `restoreBackup()` | Abre dialogo para restaurar backup (descomprime ZIP) |
| `exportXlsCustomers()` | Exporta clientes a CSV |
| `loadStatusBar()` | Carga fecha y version en la barra de estado |

---

### reports.py - Generacion de Informes PDF

Usa la libreria **ReportLab** para generar PDFs.

**Clase `Reports`:**

| Metodo | Que hace |
|--------|----------|
| `runCustomerReports()` | Metodo estatico que crea instancia y llama a `reportCustomers()` |
| `footer(titulo)` | Dibuja el pie de pagina (fecha + titulo + numero de pagina) |
| `toReport(titulo)` | Dibuja la cabecera del informe (logo, datos empresa, titulo) |
| `reportCustomers()` | Genera PDF con listado de todos los clientes |
| `reportInvoice(idFac)` | Genera PDF de una factura especifica con sus lineas de venta |

**Como funciona la generacion de PDF:**
```python
# 1. Crear el canvas (lienzo PDF)
self.c = canvas.Canvas("ruta/archivo.pdf")

# 2. Dibujar elementos
self.c.setFont("Helvetica-Bold", 10)        # Establecer fuente
self.c.drawString(x, y, "texto")             # Texto en posicion (x,y)
self.c.drawCentredString(x, y, "texto")      # Texto centrado en x
self.c.drawRightString(x, y, "texto")        # Texto alineado derecha
self.c.line(x1, y1, x2, y2)                  # Linea
self.c.drawImage("ruta.png", x, y, w, h)     # Imagen
self.c.rect(x, y, ancho, alto)               # Rectangulo

# 3. Nueva pagina
self.c.showPage()

# 4. Guardar
self.c.save()

# NOTA: Las coordenadas Y empiezan ABAJO (0) y suben (842 para A4)
# Es decir, y=785 esta arriba, y=50 esta abajo
```

---

### venAux.py - Ventanas Auxiliares (Dialogos)

Define 3 clases que heredan de widgets Qt:

```python
class Calendar(QtWidgets.QDialog):    # Ventana del calendario
class About(QtWidgets.QDialog):       # Ventana "Acerca de"
class FileDialogOpen(QtWidgets.QFileDialog):  # Dialogo abrir/guardar archivo
```

**Calendar:** Usa `QCalendarWidget`, al hacer click en una fecha llama a `Events.loadData()`
**About:** Dialogo modal con version y autor
**FileDialogOpen:** Se usa para backup/restore y exportar CSV

---

### styles.py y styles.qss - Estilos Visuales

`styles.py` simplemente lee el archivo QSS:
```python
def load_stylesheet():
    with open('styles.qss', 'r') as file:
        return file.read()
```

`styles.qss` es como CSS pero para Qt. **Selectores importantes:**

```css
/* Por tipo de widget */
QPushButton { ... }
QLineEdit { ... }
QTableWidget { ... }

/* Por ID de widget (objectName) */
QPushButton#btnDelcli { background-color: red; }

/* Por estado */
QPushButton:hover { ... }
QPushButton:pressed { ... }
QPushButton:disabled { ... }
QLineEdit:focus { ... }

/* Sub-elementos */
QComboBox::drop-down { ... }
QHeaderView::section { ... }
QScrollBar::handle:vertical { ... }
```

---

### dlgAbout.py y dlgCalendar.py - UI de Dialogos

Generados con `pyuic6` desde los archivos `.ui`. Para regenerarlos:
```bash
pyuic6 -x templates/dlgAbout.ui -o dlgAbout.py
pyuic6 -x templates/dlgCalendar.ui -o dlgCalendar.py
```

---

## Flujo de la Aplicacion

### Flujo: Dar de Alta un Cliente
```
1. Usuario rellena formulario (DNI, nombre, apellidos, email, movil, direccion, provincia, municipio, tipo factura)
2. Cada campo se valida al perder el foco (editingFinished):
   - checkDni() valida formato DNI
   - capitalizar() pone mayusculas
   - checkEmail() valida email
   - checkMobil() valida movil
3. Click en "Guardar" → Customers.saveCli()
4. saveCli() lee todos los campos del formulario
5. Llama a Conexion.addCli(newCli)
6. addCli() ejecuta INSERT INTO customers
7. Si OK: muestra mensaje exito + recarga tabla + limpia formulario
8. Si error: muestra mensaje de error
```

### Flujo: Crear Factura con Ventas
```
1. Usuario escribe DNI en txtDnifac (o deja vacio para "00000000T")
2. Click "Guardar Factura" → Invoice.saveInvoice()
3. Se busca el cliente (Invoice.buscaCli) y se muestran sus datos
4. Se inserta factura en BD (Conexion.insertInvoice)
5. Se recarga tabla de facturas
6. Usuario hace click en la factura recien creada → selectInvoice()
7. Se carga la tabla de ventas vacia con celdas editables
8. Usuario escribe ID de producto en columna 1 → cellsChanged()
9. Se auto-rellena nombre y precio del producto
10. Usuario escribe cantidad en columna 4 → cellsChanged()
11. Se verifica stock, se calcula total, se actualiza subtotal/IVA/total
12. Si la fila esta completa, se crea nueva fila automaticamente
13. Click "Guardar Venta" → Invoice.saveSale()
14. Se guardan TODAS las lineas en BD + se descuenta stock
```

### Flujo: Generar Informe PDF
```
1. Menu → Reports → Customers Reports
2. Reports.runCustomerReports() → crea instancia de Reports
3. reportCustomers():
   a. Crea canvas PDF en ./reports/
   b. Dibuja cabecera (logo, datos empresa)
   c. Dibuja pie de pagina (fecha, titulo, num pagina)
   d. Dibuja cabecera de tabla (columnas)
   e. Recorre registros, dibuja fila por fila
   f. Si se acaba la pagina (y <= 90): nueva pagina + repetir cabecera
   g. Guarda PDF y lo abre con os.startfile()
```

---

## Nombres de Widgets Importantes

### Pestana Clientes
| Widget | Tipo | Descripcion |
|--------|------|-------------|
| `txtDnicli` | QLineEdit | Campo DNI/NIE |
| `txtAltacli` | QLineEdit | Fecha de alta |
| `txtNomecli` | QLineEdit | Nombre |
| `txtApelcli` | QLineEdit | Apellidos |
| `txtEmailcli` | QLineEdit | Email |
| `txtMobilcli` | QLineEdit | Movil |
| `txtDircli` | QLineEdit | Direccion |
| `cmbProvcli` | QComboBox | Provincia |
| `cmbMunicli` | QComboBox | Municipio |
| `rbtFacpaper` | QRadioButton | Factura papel |
| `rbtFacmail` | QRadioButton | Factura electronica |
| `chkHistoricocli` | QCheckBox | Filtrar historicos |
| `lblWarning` | QLabel | Mensajes de aviso |
| `tblCustomerlist` | QTableWidget | Tabla de clientes |
| `btnSavecli` | QPushButton | Guardar cliente |
| `btnModifcli` | QPushButton | Modificar cliente |
| `btnDelcli` | QPushButton | Eliminar cliente |
| `btnCleanCli` | QPushButton | Limpiar formulario |
| `btnSearchCli` | QPushButton | Buscar cliente |
| `btnFechaltacli` | QPushButton | Abrir calendario |

### Pestana Productos
| Widget | Tipo | Descripcion |
|--------|------|-------------|
| `lblCodeId` | QLabel | ID del producto seleccionado |
| `txtNameProd` | QLineEdit | Nombre producto |
| `txtStock` | QLineEdit | Stock |
| `txtPrice` | QLineEdit | Precio |
| `cmbFamily` | QComboBox | Familia/Categoria |
| `tblProdlist` | QTableWidget | Tabla de productos |
| `btnSaveprod` | QPushButton | Guardar producto |
| `btnModifprod` | QPushButton | Modificar producto |
| `btnDelprod` | QPushButton | Eliminar producto |

### Pestana Facturas
| Widget | Tipo | Descripcion |
|--------|------|-------------|
| `txtDnifac` | QLineEdit | DNI para factura |
| `lblNumfac` | QLabel | Numero de factura |
| `lblFechafac` | QLabel | Fecha factura |
| `lblNamefac` | QLabel | Nombre cliente |
| `lblTypefac` | QLabel | Tipo factura |
| `lblDirfac` | QLabel | Direccion cliente |
| `lblMobilefac` | QLabel | Movil cliente |
| `lblStatusfac` | QLabel | Estado cliente |
| `lblSubtotal` | QLabel | Subtotal |
| `lblIva` | QLabel | IVA (21%) |
| `lblTotal` | QLabel | Total |
| `lblPrint` | QLabel | Icono impresion |
| `tblFaclist` | QTableWidget | Tabla de facturas |
| `tblSales` | QTableWidget | Tabla de lineas de venta |
| `btnSavefac` | QPushButton | Guardar factura |
| `btnResetfac` | QPushButton | Limpiar formulario |
| `btnSaveSale` | QPushButton | Guardar ventas |
| `btnPrint` | QPushButton | Imprimir factura PDF |

---

## Patrones y Convenciones del Codigo

### 1. Acceso a widgets siempre por globals.ui
```python
# LEER un campo de texto
valor = globals.ui.txtDnicli.text()

# ESCRIBIR en un campo de texto
globals.ui.txtNomecli.setText("Juan")

# LEER combobox seleccionado
provincia = globals.ui.cmbProvcli.currentText()

# ESCRIBIR en combobox
globals.ui.cmbProvcli.setCurrentText("Pontevedra")

# LEER checkbox
if globals.ui.chkHistoricocli.isChecked():

# LEER radiobutton
if globals.ui.rbtFacpaper.isChecked():
```

### 2. Mensajes al usuario (QMessageBox)
```python
mbox = QtWidgets.QMessageBox()
mbox.setWindowTitle("Titulo")
mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)  # o Warning, Question
mbox.setText("Mensaje")
mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
mbox.exec()

# Con botones Yes/No:
mbox.setStandardButtons(
    QtWidgets.QMessageBox.StandardButton.Yes |
    QtWidgets.QMessageBox.StandardButton.No
)
if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
    # usuario dijo si
```

### 3. Cargar datos en una tabla
```python
def cargarTabla():
    registros = Conexion.listarDatos()  # obtener datos de BD
    index = 0
    for record in registros:
        globals.ui.miTabla.setRowCount(index + 1)  # anadir fila
        globals.ui.miTabla.setItem(index, 0, QtWidgets.QTableWidgetItem(str(record[0])))
        globals.ui.miTabla.setItem(index, 1, QtWidgets.QTableWidgetItem(str(record[1])))
        # ... mas columnas
        index += 1
```

### 4. Leer fila seleccionada de una tabla
```python
def seleccionarFila(self):
    row = globals.ui.miTabla.selectedItems()
    dato = row[0].text()  # primera columna de la fila seleccionada
```

### 5. Cambiar estilo de un widget dinamicamente
```python
# Fondo rosa (error)
globals.ui.txtDnicli.setStyleSheet('background-color: #FFC0CB;')

# Fondo normal
globals.ui.txtDnicli.setStyleSheet('background-color: rgb(255, 255, 220);')

# Sin fondo
globals.ui.txtDnicli.setStyleSheet('background-color: none;')
```

### 6. Bloquear/desbloquear senales de tabla (evitar recursion)
```python
globals.ui.tblSales.blockSignals(True)   # desactiva itemChanged
# ... hacer cambios en la tabla sin disparar eventos ...
globals.ui.tblSales.blockSignals(False)  # reactiva itemChanged
```

### 7. Hacer una celda editable o no editable
```python
item = QtWidgets.QTableWidgetItem("texto")

# Editable
item.setFlags(
    QtCore.Qt.ItemFlag.ItemIsSelectable |
    QtCore.Qt.ItemFlag.ItemIsEnabled |
    QtCore.Qt.ItemFlag.ItemIsEditable
)

# Solo lectura
item.setFlags(
    QtCore.Qt.ItemFlag.ItemIsSelectable |
    QtCore.Qt.ItemFlag.ItemIsEnabled
)
```

---

## Guia Practica: Como Anadir Funcionalidades

### Ejemplo 1: Anadir un nuevo campo a Clientes (ej: "Observaciones")

**Paso 1 - Base de datos:** Anadir columna a la tabla
```sql
ALTER TABLE customers ADD COLUMN observations TEXT;
```

**Paso 2 - UI (Qt Designer):** Abrir `templates/window.ui`, anadir un `QLineEdit` llamado `txtObscli` y regenerar:
```bash
pyuic6 -x templates/window.ui -o window.py
```

**Paso 3 - conexion.py:** Modificar `addCli()` y `modifCli()` para incluir el nuevo campo:
```python
query.prepare("INSERT INTO customers (..., observations) VALUES (..., :observations)")
query.bindValue(":observations", str(newCli[10]))
```

**Paso 4 - customers.py:** Modificar `saveCli()`, `modifCli()`, `selectCustomer()` para leer/escribir el nuevo campo:
```python
# En saveCli:
newCli.append(globals.ui.txtObscli.text())

# En selectCustomer:
globals.ui.txtObscli.setText(str(record[11]))

# En resetCustomer:
globals.ui.txtObscli.setText("")
```

### Ejemplo 2: Anadir un boton nuevo (ej: "Exportar Productos a CSV")

**Paso 1 - UI:** Anadir QPushButton `btnExportProd` en Qt Designer y regenerar window.py

**Paso 2 - main.py:** Conectar la senal:
```python
globals.ui.btnExportProd.clicked.connect(Events.exportCsvProducts)
```

**Paso 3 - events.py (o products.py):** Crear el metodo:
```python
def exportCsvProducts(self):
    try:
        import csv
        records = Conexion.listProds(self)
        # ... logica de exportacion similar a exportXlsCustomers
    except Exception as e:
        print("Error exportando", e)
```

### Ejemplo 3: Anadir un nuevo informe PDF

**Paso 1 - conexion.py:** Crear consulta para obtener los datos necesarios

**Paso 2 - reports.py:** Crear metodo nuevo siguiendo el patron de `reportCustomers()`:
```python
def reportProductos(self):
    rootPath = '.\\reports'
    data = datetime.now().strftime("%m_%d_%Y_%I_%M_%S")
    self.c = canvas.Canvas(os.path.join(rootPath, data + '_reportProd.pdf'))

    titulo = "Listado de Productos"
    self.footer(titulo)      # pie de pagina
    self.toReport(titulo)    # cabecera empresa

    records = Conexion.listProds(self)
    # ... dibujar tabla con los datos ...

    self.c.save()
```

**Paso 3 - main.py:** Conectar desde un menu o boton:
```python
globals.ui.actionProductReports.triggered.connect(Reports.runProductReports)
```

### Ejemplo 4: Anadir una pestana nueva (ej: "Proveedores")

**Paso 1 - Qt Designer:** Anadir nueva pestana al `TabProducts`, con tabla y formulario

**Paso 2 - Regenerar:** `pyuic6 -x templates/window.ui -o window.py`

**Paso 3 - BD:** Crear tabla `proveedores` en SQLite

**Paso 4 - conexion.py:** Anadir metodos CRUD para proveedores

**Paso 5 - Crear `proveedores.py`:** Nueva clase con la logica (siguiendo el patron de customers.py)

**Paso 6 - main.py:** Importar la clase y conectar senales

**Paso 7 - events.py:** Anadir `resizeTabProveedores()` si tiene tabla

---

## Dependencias

```
PyQt6          # Framework de interfaz grafica
reportlab      # Generacion de PDFs
```

Instalar con:
```bash
pip install PyQt6 reportlab
```

Para regenerar los archivos .py desde los .ui:
```bash
pip install pyqt6-tools
pyuic6 -x templates/window.ui -o window.py
pyuic6 -x templates/dlgAbout.ui -o dlgAbout.py
pyuic6 -x templates/dlgCalendar.ui -o dlgCalendar.py
```
