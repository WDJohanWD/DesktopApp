import os
from PyQt6 import QtSql, QtWidgets

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

            if not query.next():
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

    def listProv(self=None):

        listprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listprov.append(query.value(1))
        return listprov

    @staticmethod
    def listMuniProv(province):
        try:
            listmunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias "
                          " where provincia = :province)")
            query.bindValue(":province", province)
            if query.exec():
                while query.next():
                    listmunicipios.append(query.value(1))
            return listmunicipios
        except Exception as error:
            print("error lista muni", error)

    @staticmethod
    def listCustomers(var):
        list = []
        if var:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where historical = :true order by surname")
            query.bindValue(":true", str(True))
            if query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        else:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers order by surname")
            if  query.exec():
                while query.next():
                    row = [query.value(i) for i in range(query.record().count())]
                    list.append(row)
        return list

    @staticmethod
    def dataOneCustomer(dato):
        try:
            list = []
            data = str(dato).strip() #quita espacios en blanco
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM customers where mobile = :data")
            query.bindValue(":data", str(data))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        list.append(str(query.value(i)))

            if len(list) == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM customers where dni_nie = :data")
                query.bindValue(":dato", str(data))
                if query.exec():
                    while query.next():
                        for i in range(query.record().count()):
                            list.append(str(query.value(i)))
            print(list)
            return list
        except Exception as error:
            print("error dataOneCustomer", error)

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
        except Exception as error:
            print("error deleteCli", error)

    @staticmethod
    def addCli(newcli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO customers ( dni_nie, adddata, surname, name, mail, mobile, address, province, "
                          " city, invoicetype, historical ) VALUES (:dnicli, :adddata, :surname, :name, :mail, :mobile, :address, "
                          " :province, :city, :invoicetype, :historical)")
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
        except Exception as error:
            print("error addCli", error)

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
            print(query)
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error en conexion - modifCli", error)