from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import *

a = ('Gol', 'Celta', 'Corsa', 'Uno', 'Fox', 'Cruze',
     'Brasilia', 'Saveiro', 'Fusca', 'Hilux', 'Onix')
modelo = QStandardItemModel(len(a), 1)
modelo.setHorizontalHeaderLabels(['a'])

for linha, carro in enumerate(a):    # [(1, 'Gol'), (2,'Celta') ]
    elemento = QStandardItem(carro)
    modelo.setItem(linha, 0, elemento)

filtro = QSortFilterProxyModel()
filtro.setSourceModel(modelo)
filtro.setFilterKeyColumn(0)
# filtro.setFilterCaseSensitivity(Qt.CaseInsensitive)

app = QtWidgets.QApplication([])
tela = uic.loadUi("layout.ui")
tela.tableView.setModel(filtro)
tela.tableView.horizontalHeader().setStyleSheet(
    "font-size: 35px;color: rgb(50, 50, 255);")
tela.lineEdit.textChanged.connect(filtro.setFilterRegExp)

tela.show()
app.exec()
