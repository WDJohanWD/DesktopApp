import os
from datetime import date

from PyQt6  import QtSql, QtWidgets

import globals


class Conexion:
    def db_conexion(self = None):
        """
                Establece la conexión con la base de datos SQLite.

                :return: True si la conexión es exitosa y la base de datos es válida, False en caso contrario.
                :rtype: bool
                """
        ruta_db = './data/bbdd.sqlite'

        if not os.path.isfile(ruta_db):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(ruta_db)

        if db.open():
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    def listProv(self):
        """
                Obtiene la lista completa de nombres de las provincias desde la base de datos.

                :return: Lista con los nombres de las provincias.
                :rtype: list
                """
        listprov= []
        query  = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listprov.append(query.value(1))
        return listprov

    @staticmethod
    def listMuniProv(province):
        """
                Obtiene los municipios correspondientes a una provincia específica.

                :param province: Nombre de la provincia a consultar.
                :type province: str
                :return: Lista de nombres de municipios.
                :rtype: list
                """
        try:
            listaMunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = :province)")
            query.bindValue(":province", province)
            if query.exec():
                while query.next():
                    listaMunicipios.append(query.value(1))

            return  listaMunicipios
        except Exception as e:
            print("Error lista municipios", e)


    def listCustomers(varcli):
        """
                Recupera la lista de clientes de la base de datos.

                :param varcli: Si es True, filtra solo clientes históricos. Si es False, devuelve todos.
                :type varcli: bool
                :return: Lista de listas, donde cada sublista contiene los datos de un cliente.
                :rtype: list
                """
        list = []
        if varcli:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE historical = :true order by surname")
            query.bindValue(":true", str(True))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        else:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers ORDER BY surname")
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        return list

    def dataOneCustomer(dato):
        """
                Busca y devuelve los datos de un cliente específico mediante su móvil o DNI/NIE.

                :param dato: El número de móvil o DNI del cliente a buscar.
                :type dato: str
                :return: Lista con los datos del cliente encontrado.
                :rtype: list
                """
        try:
            list = []
            data = str(dato).strip()
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE mobile = :data")
            query.bindValue(":data", str(data))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(str(query.value(i)))

            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM customers WHERE dni_nie = :data")
                query.bindValue(":data", str(dato))
                if query.exec():
                    while query.next():
                        for i in range(query.record().count()):
                            list.append(str(query.value(i)))

            return list
        except Exception as e:
            print("Error data", e)

    def deleteCli(dni):
        """
                Realiza un borrado lógico de un cliente marcando su estado como no histórico.

                :param dni: DNI/NIE del cliente a eliminar.
                :type dni: str
                :return: True si la actualización fue exitosa, False en caso contrario.
                :rtype: bool
                """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET historical = :value WHERE dni_nie  = :dni")
            query.bindValue(":dni", dni)
            query.bindValue(":value", str(False))
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error data", e)

    @staticmethod
    def addCli(newCli):
        """
                Inserta un nuevo cliente en la base de datos.

                :param newCli: Lista con los datos del cliente (DNI, nombre, dirección, etc.).
                :type newCli: list
                :return: True si se insertó correctamente, False si hubo un error.
                :rtype: bool
                """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers (dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical) VALUES "
                          " ( :dni_nie, :adddata, :surname, :name, :mail, :mobile, :address, :province, :city, :invoicetype, :historical)")
            query.bindValue(":dni_nie", str(newCli[0]))
            query.bindValue(":adddata", str(newCli[1]))
            query.bindValue(":surname", str(newCli[2]))
            query.bindValue(":name", str(newCli[3]))
            query.bindValue(":mail", str(newCli[4]))
            query.bindValue(":mobile", str(newCli[5]))
            query.bindValue(":address", str(newCli[6]))
            query.bindValue(":province", str(newCli[7]))
            query.bindValue(":city", str(newCli[8]))
            query.bindValue(":invoicetype", str(newCli[9]))
            query.bindValue(":historical", str(True))
            if query.exec():
                print("SE ha añadido a la base de datos")
                return True
            else:
                print("Hubo un error")
                return False
        except Exception as e:
            print("Error addCli", e)

    def modifCli(dni, modifCli):
        """
                Actualiza los datos de un cliente existente.

                :param dni: DNI/NIE original del cliente a modificar.
                :type dni: str
                :param modifCli: Lista con los nuevos datos actualizados.
                :type modifCli: list
                :return: True si la modificación tuvo éxito, False si falló.
                :rtype: bool
                """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET addData= :adddata, surname= :surname, name= :name, mail= :mail, mobile= :mobile, address= :address, province= :province, city= :city, invoicetype= :invoicetype WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            query.bindValue(":adddata", str(modifCli[0]))
            query.bindValue(":surname", str(modifCli[1]))
            query.bindValue(":name", str(modifCli[2]))
            query.bindValue(":mail", str(modifCli[3]))
            query.bindValue(":mobile", str(modifCli[4]))
            query.bindValue(":address", str(modifCli[5]))
            query.bindValue(":province", str(modifCli[6]))
            query.bindValue(":city", str(modifCli[7]))
            query.bindValue(":historical", str(globals.estado))
            query.bindValue(":invoicetype", str(modifCli[8]))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error en conexion - modifCli", error)


    #Methods for products
    def listProds(self):
        """
                Obtiene la lista de todos los productos ordenados por su ID.

                :return: Lista de listas con la información de cada producto.
                :rtype: list
                """
        list = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM productos ORDER BY idprod")
        if query.exec():
            while query.next():
                row = [query.value(i) for i in range(query.record().count())]
                list.append(row)
        return list

    @staticmethod
    def addProd(newProd):
        """
                Registra un nuevo producto en el inventario.

                :param newProd: Lista con [nombre, stock, familia, precio unidad].
                :type newProd: list
                :return: Resultado de la ejecución de la consulta.
                :rtype: bool
                """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO productos (name, stock, family, unityprice) VALUES "
                " ( :name, :stock, :family, :unityprice)")
            query.bindValue(":name", str(newProd[0]))
            query.bindValue(":stock", str(newProd[1]))
            query.bindValue(":family", str(newProd[2]))
            query.bindValue(":unityprice", str(newProd[3]))

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error addProd", e)

    def dataOneProduct(code):
        """
                Obtiene los detalles de un producto específico según su código ID.

                :param code: ID del producto.
                :type code: int/str
                :return: Lista con los atributos del producto.
                :rtype: list
                """
        try:
            list = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM productos WHERE idprod = :id")
            query.bindValue(":id", str(code))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(str(query.value(i)))

            return list
        except Exception as e:
            print("Error en seleccionar producto", e)

    def deleteProd(id):
        """
                        Elimina un producto específico según su código ID.

                        :param code: ID del producto.
                        :type code: int/str
                        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM productos WHERE idprod = :id")
            query.bindValue(":id", id)
            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error data", e)

    def modifProd(id, modifProd):
        """
                        Modifica un producto específico según su código ID.

                        :param code: ID del producto.
                        :type code: int/str
                        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE productos SET name= :name, stock= :stock, family= :family, unityprice= :unityprice WHERE idprod = :id")
            query.bindValue(":id", id)
            query.bindValue(":name", str(modifProd[0]))
            query.bindValue(":stock", str(modifProd[1]))
            query.bindValue(":family", str(modifProd[2]))
            query.bindValue(":unityprice", str(modifProd[3]))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error en conexion - modifProd", error)

    def buscaCli(dni):
        '''
                Verifica si un cliente existe en la base de datos mediante su DNI/NIE.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers WHERE dni_nie = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                if query.next():
                    return True
                else:
                    return False
        except Exception as e:
            print("Error data", e)


    def insertInvoice(dni):
        '''
                Inserta una nueva factura en la base de datos asociada a un cliente específico mediante su DNI/NIE.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices (dni_nie, date) VALUES ( :dni_nie, :date)")
            query.bindValue(":dni_nie", str(dni))
            query.bindValue(":date", str(date.today()))

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error insert invoice", e)


    def invoiceWithReturn(dni):
        '''
                Inserta una nueva factura en la base de datos asociada a un cliente específico mediante su DNI/NIE y devuelve el ID de la factura creada.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO invoices (dni_nie, date) VALUES ( :dni_nie, :date)")
            query.bindValue(":dni_nie", str(dni))
            query.bindValue(":date", str(date.today()))

            if query.exec():
                invoice_id = query.lastInsertId()
                return invoice_id
            else:
                print(query.lastError().text())
                return None
        except Exception as e:
            print("Error insert invoice", e)



    def allInvoices(self):
        '''
                Recupera todas las facturas almacenadas en la base de datos, ordenadas por ID de factura en orden descendente.
        :return:
        '''
        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices ORDER BY idFac DESC")
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)

            return records

        except Exception as error:
            print("Error en conexion - allInvoices", error)

    def selectProduct(item):
        '''
                Recupera el nombre y el precio unitario de un producto específico según su ID.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT name, unityprice FROM productos WHERE idprod = :id")
            query.bindValue(":id", str(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    return row
        except Exception as e:
            print("Error selectProduct", e)

    def selectFullProduct(item):
        '''
                Recupera toda la información de un producto específico según su ID.
        :return:
        '''
        try:
            records = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM productos WHERE idprod = :id")
            query.bindValue(":id", str(item))
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    return row
        except Exception as e:
            print("Error selectProduct", e)


    def saveSale(data):
        '''
                Guarda una venta en la base de datos, insertando un nuevo registro en la tabla de ventas y actualizando el stock del producto correspondiente.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO sales (idFac, idProd, product, uniprice, amount, total) "
                            " VALUES (:idFac, :idProd, :product, :uniprice, :amount, :total)")
            query.bindValue(":idFac", int(data[0]))
            query.bindValue(":idProd", int(data[1]))
            query.bindValue(":product", str(data[2]))
            query.bindValue(":uniprice", float(data[3]))
            query.bindValue(":amount", int(data[4]))
            query.bindValue(":total", float(data[5]))


            queryProd = QtSql.QSqlQuery()
            queryProd.prepare("UPDATE productos SET stock = stock - :qty WHERE idProd = :idProd")
            queryProd.bindValue(":qty", int(data[4]))
            queryProd.bindValue(":idProd", int(data[1]))
            if query.exec() and queryProd.exec():
                return True

        except Exception as e:
            print("Error en saveSales", e)


    def getSales(idFac):
        '''
                Recupera todas las ventas asociadas a una factura específica, ordenadas por ID de venta en orden ascendente.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM sales WHERE idFac = :idFac ORDER BY idv ASC")
            query.bindValue(":idFac", str(idFac))
            records = []
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    records.append(row)

            return records

        except Exception as e:
            print("Error en getSales", e)

    def getOneInvoice(invoiceId):
        '''
                Recupera los detalles de una factura específica según su ID, incluyendo información del cliente y la fecha de la factura.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM invoices WHERE idFac = :id")
            query.bindValue(":id", str(invoiceId))
            record = []
            if query.exec():
                while query.next():
                    row = [str(query.value(i)) for i in range(query.record().count())]
                    record.append(row)
            return record

        except Exception as e:
            print("Error en getOneInvoice", e)

    def deleteInvoice(invoiceId):
        '''
                Elimina una factura específica según su ID, eliminando también todas las ventas asociadas a esa factura.
        :return:
        '''
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM invoices WHERE idFac = :id")
            query.bindValue(":id", str(invoiceId))
            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error en getOneInvoice", e)