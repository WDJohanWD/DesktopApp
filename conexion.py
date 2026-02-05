import os
from PyQt6  import QtSql, QtWidgets

import globals


class Conexion:
    def db_conexion(self = None):
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
        listprov= []
        query  = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listprov.append(query.value(1))
        return listprov

    @staticmethod
    def listMuniProv(province):

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
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET historical = :value WHERE dni = :dni")
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
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers (dni_nie, adddata, surname, name, mail, mobile, address, province, city, invoicetype, historical) VALUES "
                          " ( :dni_cli, :adddata, :surname, :surname, :name, :mail, :mobile, :address, :province, :city, :invoicetype, :historical)")
            query.bindValue(":dni_cli", str(newCli[0]))
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
            query.exec()

            if query.exec():
                return True
            else:
                return False
        except Exception as e:
            print("Error addCli", e)

    def modifCli(dni, modifCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE customers SET addData= :adddata, surname= :surname, name= :name, mail= :mail, mobile= :mobile, address= :address, province= :province, city= :city, invoicetype= :invoicetype WHERE dni = :dni")
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