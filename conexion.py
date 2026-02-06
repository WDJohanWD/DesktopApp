import os

from PyQt6 import QtSql, QtWidgets, QtCore, QtGui


class Conexion:
    def db_conexion(self=None):
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'The database file does not exist',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():
                QtWidgets.QMessageBox.critical(None, 'Error', 'Empty database or not valid',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Database connected successfully',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'Database could not be opened',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    def listProv(self=None):
        listProv = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias;")
        if query.exec():
            while query.next():
                listProv.append(query.value(1))
        return listProv

    def listMuniProv(province):
        try:
            listmunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :province)")
            query.bindValue(":province", province)
            if query.exec():
                while query.next():
                    listmunicipios.append(query.value(1))
            return listmunicipios
        except Exception as e:
            print("error en cargar MuniProv", e)

    @staticmethod
    def listTabCustomers(var):
        list = []
        if var:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers  where historical = :true order by surname")
            query.bindValue(":true", str(True))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        else:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers order by surname")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        return list

    @staticmethod
    def listTabProducts(self):
        list = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM products order by code")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                list.append(row)
        return list

    @staticmethod
    def dataOneCustomer(dato):
        try:
            list = []
            dato = str(dato).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where mobile = :dato")
            query.bindValue(":dato", str(dato))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM customers where dni_nie = :dato")
                query.bindValue(":dato", str(dato))
                if query.exec():
                    while query.next():
                        for i in range(query.record().count()):
                            list.append(query.value(i))
            return list
        except Exception as error:
            print("error dataOneCustomer", error)

    @staticmethod
    def dataOneProduct(dato):
        try:
            listpro = []
            dato = str(dato).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM products where code = :dato")
            query.bindValue(":dato", str(dato))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        listpro.append(query.value(i))
            return listpro
        except Exception as e:
            print("error in load dataOneProduct", e)

    @staticmethod
    def deleteCli(dni):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers set historical = :value WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":value", str(False))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error in delete", e)

    @staticmethod
    def addCli(newcli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers(dni_nie, adddata,surname,name,mail,mobile,address,province,city, invoicetype, historical) VALUES(:dnicli, :adddata,:surname,:name,:mail,:mobile,:address,:province,:city,:invoicetype,:historical)")
            query.bindValue(":dnicli", str(newcli[0]))
            query.bindValue(":adddata", str(newcli[1]))
            query.bindValue(":surname", str(newcli[2]))
            query.bindValue(":name", str(newcli[3]))
            query.bindValue(":mail", str(newcli[4]))
            query.bindValue(":mobile", str(newcli[5]))
            query.bindValue(":address", str(newcli[6]))
            query.bindValue(":province", str(newcli[7]))
            query.bindValue(":city", str(newcli[8]))
            query.bindValue(":invoicetype", str(newcli[9]))
            query.bindValue(":historical", str(True))
            if query.exec():
                return True
            else:
                return False
        except:
            print("error in addCli")

    @staticmethod
    def addPro(newpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO products(name,stock,family,unitprice) VALUES(:name,:stock,:family,:unitprice)")
            query.bindValue(":name", str(newpro[0]))
            query.bindValue(":stock", str(newpro[1]))
            query.bindValue(":family", str(newpro[2]))
            query.bindValue(":unitprice", str(newpro[3]))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("error in addPro", e)

    @staticmethod
    def modifyCli(dni, modifcli):
        try:
            if str(dni) == "":
                return False
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET adddata = :data, surname = :surname, name = :name ,mail = :mail ,mobile = :mobile, address = :address,province = :province, city = :city, invoicetype = :invoicetype, historical = :historical  WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(modifcli[0]))
            query.bindValue(":surname", str(modifcli[1]))
            query.bindValue(":name", str(modifcli[2]))
            query.bindValue(":mail", str(modifcli[3]))
            query.bindValue(":mobile", str(modifcli[4]))
            query.bindValue(":address", str(modifcli[5]))
            query.bindValue(":province", str(modifcli[6]))
            query.bindValue(":city", str(modifcli[7]))
            query.bindValue(":historical", str(modifcli[8]))
            query.bindValue(":invoicetype", str(modifcli[9]))
            if query.exec():
                return True
            else:
                return False
        except:
            print("error in modifyCli")

    def modifyPro(id, modpro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE products SET name= :name, stock = :stock,family =:family, "
                          " unitprice =:unitprice where code = :id")
            query.bindValue(":id", str(id))
            query.bindValue(":name", str(modpro[0]))
            query.bindValue(":stock", int(modpro[2]))
            query.bindValue(":family", str(modpro[1]))
            price = modpro[3].replace("€", "")
            query.bindValue(":unitprice", str(price))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error modifyPro", error)

    def deletePro(id):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM products WHERE name = :id")
            query.bindValue(":id", str(id))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error deletePro in conexion", error)

    @staticmethod
    def searchClient(dni):
        try:
            dni = str(dni).upper()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as error:
            print("error searchClient", error)

    @staticmethod
    def insertInvoice(dni, data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices(dninie,data) VALUES(:dni, :data)")
            query.bindValue(":dni", str(dni))
            query.bindValue(":data", str(data))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error insertInvoice in conexion", error)

    @staticmethod
    def deleteInvoice(numfac):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM invoices WHERE idfac= :numfac")
            query.bindValue(":numfac", int(numfac))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("error deleteInvoice in conexion", error)

    def allInvoices(self):
        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices ORDER BY idfac DESC")
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)
            return records
        except Exception as error:
            print("error allInvoices in conexion", error)

    def selectProduct(item):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT name, unitprice FROM products WHERE code = :code")
            query.bindValue(":code", str(item))
            if query.exec():
                if query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                else:
                    row = []
            return row
        except Exception as error:
            print("error selectProduct in conexion", error)

    @staticmethod
    def saveSales(data):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales (idfac, idpro, product, unitprice, amount, total) "
                          " VALUES (:idfac, :idpro, :product, :unitprice, :amount, :total)")
            query.bindValue(":idfac", data[0])
            query.bindValue(":idpro", data[1])
            query.bindValue(":product", data[2])
            query.bindValue(":unitprice", data[3])
            query.bindValue(":amount", data[4])
            query.bindValue(":total", data[5])
            if query.exec():
                return True
            else:
                print("Error: Insert into sales failed.")
                return False
        except Exception as error:
            print("Error en saveSales conexion:", error)

    def existFac(item):
        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales WHERE idfac = :item")
            query.bindValue(":item", int(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)
            return records
        except Exception as error:
            print("error existFac in conexion", error)

    @staticmethod
    def existeFacturaSales(fact):
        try:
            if not fact or not str(fact).isdigit():
                return False
            query = QtSql.QSqlQuery()
            query.prepare("SELECT 1 FROM sales WHERE idfac = :idfac LIMIT 1")
            query.bindValue(":idfac", int(fact))
            if query.exec() and query.next():
                return True
            return False
        except Exception as error:
            print("Error en existeFacturaSales:", error)
            return False

    @staticmethod
    def datosFac(id_factura):
        try:
            all_data_sales = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales where idfac = :idfac;")
            query.bindValue(":idfac", int(id_factura))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    all_data_sales.append(row)
            else:
                print("Error: Query for invoice data failed.")
            return all_data_sales
        except Exception as error:
            print("Error en datosFac:", error)

    @staticmethod
    def dataOneSale(idfac):
        try:
            rows = []
            idfac = str(idfac).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idpro, product, unitprice, amount, total FROM sales WHERE idfac = :idfac")
            query.bindValue(":idfac", idfac)
            if query.exec():
                while query.next():
                    codigo = query.value(0)
                    concepto = query.value(1)
                    precio = query.value(2)
                    cantidad = query.value(3)
                    total = query.value(4)
                    rows.append([codigo, concepto, precio, cantidad, total])
        except Exception as error:
            print(f"Error en dataOneSale: {error}")
            return []
        return rows

    @staticmethod
    def dataOneInvoice(idfact):
        try:
            list = []
            idfact = str(idfact).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices WHERE idfac = :idfac")
            query.bindValue(":idfac", idfact)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            return list
        except Exception as error:
            print("error dataOneInvoice", error)

    @staticmethod
    def dataOnlyOneInvoice(dni):
        try:
            list = []
            idfact = str(dni).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices WHERE dninie = :dninie")
            query.bindValue(":dninie", idfact)
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(query.value(i))
            return list
        except Exception as error:
            print("error dataOnlyOneInvoice", error)

    @staticmethod
    def descontarStock(code, cantidad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT stock FROM products WHERE code = :code")
            query.bindValue(":code", code)
            if not query.exec() or not query.next():
                print(f"Error: Could not get stock for product {code}.")
                return False
            stock_actual = query.value(0)
            if stock_actual < cantidad:
                print(f"Error: Insufficient stock for product {code}. Available: {stock_actual}, requested: {cantidad}.")
                return False
            nuevo_stock = stock_actual - cantidad
            query.prepare("UPDATE products SET stock = :nuevo_stock WHERE code = :code")
            query.bindValue(":nuevo_stock", nuevo_stock)
            query.bindValue(":code", code)
            if query.exec():
                return True
            else:
                print(f"Error: Could not update stock for product {code}.")
                return False
        except Exception as error:
            print("Error en descontarStock:", error)
            return False

    @staticmethod
    def listProducts():
        list = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM products")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                list.append(row)
        return list
