import sqlite3
import sys
from datetime import datetime

import numpy as np
import pandas as pd
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import (QAbstractTableModel, QSize, QSortFilterProxyModel,
                          Qt, QTime, QTimer, pyqtSlot)
from PyQt5.QtGui import QFont, QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QRadioButton,
                             QTableView, QTableWidget, QTableWidgetItem,
                             QVBoxLayout, QWidget)

import cadastroCliente
import cadastroDespesa
import cadastroServico
import editar
import editar2
import editar3
import login
import menu
from testarlogin import (agendados, atualizar_dados, buscar_email,
                         cadastro_cliente, concluir, deletardados,
                         faturamento_mensal, gerarExel, grafico, mostrar,
                         mostrar_id, pesquisa, test_login)


class menuu(QMainWindow, menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        # ############################################### Serviços
        self.Todos_Servicos()
        self.btnTodosServicos.clicked.connect(self.Todos_Servicos)
        self.btnDeleteServicos.clicked.connect(self.DeleteServicos)
        self.btnGerarExelServicos.clicked.connect(self.GerarExelServicos)
        self.btnPesquisarServicos.clicked.connect(self.PesquisarServicos)
        self.btnLimparServicos.clicked.connect(self.LimparServicos)
        self.btnEditarServicos.clicked.connect(self.EditarServicos)
        self.btnInserirServicos.clicked.connect(self.InserirServicos)
        # ############################################### Serviços
        self.todosClientes()
        self.btnInserirClientes.clicked.connect(self.tela_Cadastro)
        self.btnLimparClientes.clicked.connect(self.limparTabela_cliente)
        self.btnPesquisarClientes.clicked.connect(self.Pesquisar_cliente)
        self.btnTodosClientes.clicked.connect(self.todosClientes)
        win = QWidget()
        btnDeleteClientes = QPushButton(win)
        btnDeleteClientes.setText("Show dialog!")
        btnDeleteClientes.move(50, 50)
        btnDeleteClientes.clicked.connect(self.deletar_cliente)
        self.btnDeleteClientes.clicked.connect(self.deletar_cliente)
        self.btnEditarClientes.clicked.connect(self.editar_cliente)
        self.btnGerarExelClientes.clicked.connect(self.Exel_cliente)
        # ############################################### Despesas
        self.TodosDespesa()
        self.btnTodosDespesa.clicked.connect(self.TodosDespesa)
        self.btnDeleteDespesa.clicked.connect(self.DeleteDespesa)
        self.btnGerarExelDespesa.clicked.connect(self.GerarExelDespesa)
        self.btnPesquisarDespesa.clicked.connect(self.PesquisarDespesa)
        self.btnLimparDespesa.clicked.connect(self.LimparDespesa)
        self.btnEditarDespesa.clicked.connect(self.EditarDespesa)
        self.btnInserirDespesa.clicked.connect(self.InserirDespesa)
        self.faturamento()
        self.showTime()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.btnPesquisar_2.clicked.connect(self.concluir)
        self.btnAtualizar_3.clicked.connect(self.menu)
        self.menu()

    def concluir(self):
        a = self.tableWidget.currentRow()
        if a > -1:
            id = self.tableWidget.item(a, 0).text()
            concluir(id)
            self.menu()

    def menu(self):
        a = agendados()
        print(a)
        if a:
            self.tableWidget.setRowCount(len(a))
            self.tableWidget.setEditTriggers(
                QtWidgets.QAbstractItemView.NoEditTriggers)
            row = 0
            for n in a:
                b = n[0]
                self.tableWidget.setItem(
                    row, 0, QTableWidgetItem(str(b)))
                b = n[1]
                self.tableWidget.setItem(
                    row, 1, QTableWidgetItem(str(b)))
                b = n[7]
                self.tableWidget.setItem(
                    row, 2, QTableWidgetItem(str(b)))
                b = n[8]
                self.tableWidget.setItem(
                    row, 3, QTableWidgetItem(str(b)))
                row += 1

    def showTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        self.hora.setText(label_time)

    def faturamento(self):
        data = datetime.now()
        Mes = str(data.month)
        a = faturamento_mensal(Mes)
        if a:
            despesas_totais = a[1] + a[2]
            fat_liquido = a[0] - despesas_totais
            fat = a[0]
            des_fix = a[1]
            des_var = a[2]
            quant_servicos = a[3]
            if fat_liquido < 0:
                self.fat_total.setStyleSheet(
                    """background-color: rgb(255, 0, 0);border-width:2px;border-style:outset;border-color:black;""")
            self.fat_total.setText(f"Faturamento liquido: R$: {fat_liquido}")
            self.val_lucro.setText(f"R$: {fat}")
            self.entrada_bruta.setText(f"Faturamento bruto R$: {fat}")
            self.fixo.setText(f"R$: {des_fix}")
            self.variaveis.setText(f"R$: {des_var}")
            self.saida_bruta.setText(f"Somatoria bruta R$: {despesas_totais}")
            self.qt_servicos.setText(f"{quant_servicos}")

    def TodosDespesa(self):
        self.inputPesquisaDespesa.clear()
        a = mostrar("tb_despesa")
        self.mostarDespesa(a)

    def DeleteDespesa(self):
        chave = 'tb_despesa'
        a = self.tabelaDespesa.currentRow()
        x = self.tabelaDespesa.item(a, 0)
        y = self.tabelaDespesa.item(a, 1)
        self.delet(chave, a, x.text(), y.text())
        self.TodosDespesa()

    def GerarExelDespesa(self):
        nome = 'Tabela de Despesas.xlsx'
        chave = 'tb_despesa'
        gerarExel(chave, nome)

    def PesquisarDespesa(self):
        paramentro = self.inputPesquisaDespesa.text()
        tipopesquisa = 3
        a = pesquisa(paramentro, tipopesquisa)
        self.mostarDespesa(a)

    def mostarDespesa(self, a):
        self.tabelaDespesa.setColumnWidth(0, 50)
        self.tabelaDespesa.setRowCount(len(a))
        self.tabelaDespesa.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        row = 0
        for n in a:
            b = n[0]
            self.tabelaDespesa.setItem(
                row, 0, QTableWidgetItem(str(b)))
            b = n[1]
            self.tabelaDespesa.setItem(
                row, 1, QTableWidgetItem(str(b)))
            b = n[2]
            self.tabelaDespesa.setItem(
                row, 2, QTableWidgetItem(str(b)))
            b = n[3]
            self.tabelaDespesa.setItem(
                row, 3, QTableWidgetItem(str(b)))
            b = n[4]
            self.tabelaDespesa.setItem(
                row, 4, QTableWidgetItem(str(b)))
            b = n[5]
            self.tabelaDespesa.setItem(
                row, 5, QTableWidgetItem(str(b)))
            b = n[6]
            self.tabelaDespesa.setItem(
                row, 6, QTableWidgetItem(str(b)))
            row += 1

    def LimparDespesa(self):
        self.tabelaDespesa.setRowCount(0)
        self.tabelaDespesa.clear()

    def EditarDespesa(self):
        a = self.tabelaDespesa.currentRow()
        id = self.tabelaDespesa.item(a, 0).text()
        self.window = editarDespesa(id)
        self.window.show()
        self.TodosDespesa()
        self.faturamento()

    def InserirDespesa(self):
        self.window = teladeCadastroDespesa()
        self.window.show()
        self.TodosDespesa()
        self.faturamento()

    def Todos_Servicos(self):
        self.inputPesquisaServicos.clear()
        a = mostrar("tb_servicos")
        self.mostarServicos(a)

    def DeleteServicos(self):
        chave = 'tb_servicos'
        a = self.tabelaServicos.currentRow()
        x = self.tabelaServicos.item(a, 0)
        y = self.tabelaServicos.item(a, 1)
        self.delet(chave, a, x.text(), y.text())
        self.Todos_Servicos()

    def GerarExelServicos(self):
        nome = 'Tabela de Serviços.xlsx'
        chave = 'tb_servicos'
        gerarExel(chave, nome)

    def PesquisarServicos(self):
        paramentro = self.inputPesquisaServicos.text()
        xsql = 'tb_servicos'
        tipopesquisa = 1
        nome = 'nome'
        tipodopet = 'tipodopet'
        a = pesquisa(paramentro, tipopesquisa, xsql,  nome, tipodopet)
        self.mostarServicos(a)

    def mostarServicos(self, a):
        self.tabelaServicos.setColumnWidth(0, 50)
        self.tabelaServicos.setRowCount(len(a))
        self.tabelaServicos.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        row = 0
        for n in a:
            b = n[0]
            self.tabelaServicos.setItem(
                row, 0, QTableWidgetItem(str(b)))
            b = n[1]
            self.tabelaServicos.setItem(
                row, 1, QTableWidgetItem(str(b)))
            b = n[2]
            self.tabelaServicos.setItem(
                row, 2, QTableWidgetItem(str(b)))
            b = n[3]
            self.tabelaServicos.setItem(
                row, 3, QTableWidgetItem(str(b)))
            b = n[4]
            self.tabelaServicos.setItem(
                row, 4, QTableWidgetItem(str(b)))
            b = f"{n[7]}/{n[6]}/{n[5]}"
            self.tabelaServicos.setItem(
                row, 6, QTableWidgetItem(str(b)))
            b = f"{n[8]}:{n[9]}"
            self.tabelaServicos.setItem(
                row, 7, QTableWidgetItem(str(b)))
            b = n[10]
            self.tabelaServicos.setItem(
                row, 8, QTableWidgetItem(str(b)))
            b = n[11]
            self.tabelaServicos.setItem(
                row, 5, QTableWidgetItem(str(b)))
            row += 1

    def LimparServicos(self):
        self.tabelaServicos.clear()

    def EditarServicos(self):
        a = self.tabelaServicos.currentRow()
        id = self.tabelaServicos.item(a, 0).text()
        self.window = editarServicos(id)
        self.window.show()
        self.todosClientes()
        self.faturamento()

    def InserirServicos(self):
        a = mostrar("tb_clientes")
        self.window = teladeCadastroServico(a)
        self.window.show()
        self.Todos_Servicos()
        self.faturamento()

    def Pesquisar_cliente(self):
        paramentro = self.inputPesquisaClientes.text()
        xsql = 'tb_clientes'
        tipopesquisa = 2
        email = 'email'
        a = pesquisa(paramentro, tipopesquisa, xsql,  email)
        self.mostrarCliente(a)

    def editar_cliente(self):
        a = self.tabelaClientes.currentRow()
        id = self.tabelaClientes.item(a, 0).text()
        self.window = editarCliente(id)
        self.window.show()
        self.todosClientes()

    def deletar_cliente(self):
        chave = 'tb_clientes'
        a = self.tabelaClientes.currentRow()
        x = self.tabelaClientes.item(a, 0)
        y = self.tabelaClientes.item(a, 1)
        self.delet(chave, a, x.text(), y.text())
        self.todosClientes()

    def delet(self, chave, a, x, y,):
        if x:
            def msgButtonClick(i):
                print("Button clicked is:", i.text())
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            y = f"deseja deletar o {y} com o id {x}?"
            msgBox.setText(y)
            msgBox.setWindowTitle("QMessageBox Example")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            msgBox.buttonClicked.connect(msgButtonClick)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')
                x = int(x)
                chave = chave
                deletardados(x, chave)

        else:
            msg = QMessageBox
            msg.warning(QMessageBox(), "Error",
                        "Selecione um dado para excluir",)

    def msgButtonClick(self, i):
        print("Button clicked is:", i.text())

    def limparTabela_cliente(self):
        self.tabelaClientes.setRowCount(0)
        self.tabelaClientes.clear()

    def todosClientes(self):
        self.inputPesquisaClientes.clear()
        a = mostrar('tb_clientes')
        self.mostrarCliente(a)

    def mostrarCliente(self, a):
        self.tabelaClientes.setColumnWidth(0, 25)
        self.tabelaClientes.setColumnWidth(1, 250)
        self.tabelaClientes.setColumnWidth(2, 250)
        self.tabelaClientes.setRowCount(len(a))
        self.tabelaClientes.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        row = 0
        for n in a:
            b = n[0]
            self.tabelaClientes.setItem(
                row, 0, QTableWidgetItem(str(b)))
            b = n[1]
            self.tabelaClientes.setItem(
                row, 1, QTableWidgetItem(str(b)))
            b = n[2]
            self.tabelaClientes.setItem(
                row, 2, QTableWidgetItem(str(b)))
            b = n[3]
            self.tabelaClientes.setItem(
                row, 3, QTableWidgetItem(str(b)))
            b = n[4]
            self.tabelaClientes.setItem(
                row, 4, QTableWidgetItem(str(b)))
            b = n[5]
            self.tabelaClientes.setItem(
                row, 5, QTableWidgetItem(str(b)))
            b = n[6]
            self.tabelaClientes.setItem(
                row, 6, QTableWidgetItem(str(b)))
            b = n[7]
            self.tabelaClientes.setItem(
                row, 7, QTableWidgetItem(str(b)))
            b = n[8]
            self.tabelaClientes.setItem(
                row, 8, QTableWidgetItem(str(b)))
            b = n[9]
            self.tabelaClientes.setItem(
                row, 9, QTableWidgetItem(str(b)))

            row += 1

    def tela_Cadastro(self):
        self.window = teladeCadastroCliente()
        self.window.show()
        self.todosClientes()

    def Exel_cliente(self):
        nome = 'Tabela de Clietnes.xlsx'
        chave = 'tb_clientes'
        gerarExel(chave, nome)


class editarServicos(QMainWindow, editar2.Ui_MainWindow):
    def __init__(self, id):
        super(editarServicos, self).__init__()
        self.setupUi(self)

        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnConfirmar.clicked.connect(self.Confirmar)
        self.tableWidget.setRowCount(1)
        tabela = "tb_servicos"
        self.id = id
        x = mostrar_id(self.id, tabela)
        a = x[0]
        row = 0
        i = 0
        for n in a:
            b = n
            self.tableWidget.setItem(
                row, i, QTableWidgetItem(str(b)))
            i += 1

    def Confirmar(self):
        a = 0
        id = self.tableWidget.item(a, 0)
        id_cliente = self.tableWidget.item(a, 1).text()
        servico = self.tableWidget.item(a, 2).text()
        pagamento = self.tableWidget.item(a, 3).text()
        total = self.tableWidget.item(a, 4).text()
        ano = self.tableWidget.item(a, 5).text()
        mes = self.tableWidget.item(a, 6).text()
        dia = self.tableWidget.item(a, 7).text()
        hora = self.tableWidget.item(a, 8).text()
        min = self.tableWidget.item(a, 9).text()
        descricao = self.tableWidget.item(a, 10).text()
        id = int(id.text())
        tipo = 2
        atualizar_dados(id, tipo, id_cliente, servico, pagamento,
                        total, ano, mes, dia, hora, min, descricao)

        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.close()

    def cancelar(self):
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.close()


class editarCliente(QMainWindow, editar.Ui_MainWindow):
    def __init__(self, id):
        super(editarCliente, self).__init__()
        self.setupUi(self)

        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnConfirmar.clicked.connect(self.Confirmar)
        self.tableWidget.setRowCount(1)
        tabela = "tb_clientes"
        self.id = id
        x = mostrar_id(self.id, tabela)
        a = x[0]
        row = 0
        i = 0
        for n in a:
            b = n
            self.tableWidget.setItem(
                row, i, QTableWidgetItem(str(b)))
            i += 1

    def Confirmar(self):
        a = self.tableWidget.currentRow()
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        if self.tableWidget.clicked:
            id = self.tableWidget.item(a, 0)
            nome = self.tableWidget.item(a, 1).text()
            tipodopet = self.tableWidget.item(a, 2).text()
            wats = self.tableWidget.item(a, 3).text()
            email = self.tableWidget.item(a, 4).text()
            cpf = self.tableWidget.item(a, 5).text()
            uf = self.tableWidget.item(a, 6).text()
            endereco = self.tableWidget.item(a, 7).text()
            numero = self.tableWidget.item(a, 8).text()
            sobrenome = self.tableWidget.item(a, 9).text()
            id = int(id.text())
            tipo = 1
        atualizar_dados(id, tipo, nome, tipodopet, email,
                        cpf, uf, endereco, numero, sobrenome, wats)
        self.close()

    def cancelar(self):
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.close()


class editarDespesa(QMainWindow, editar3.Ui_MainWindow):
    def __init__(self, id):
        super(editarDespesa, self).__init__()
        self.setupUi(self)
        self.id = id
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnConfirmar.clicked.connect(self.Confirmar)
        self.tableWidget.setRowCount(1)
        tabela = "tb_despesa"
        x = mostrar_id(self.id, tabela)
        a = x[0]
        row = 0
        i = 0
        for n in a:
            b = n
            self.tableWidget.setItem(
                row, i, QTableWidgetItem(str(b)))
            i += 1

    def Confirmar(self):
        a = 0
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        id = self.tableWidget.item(a, 0)
        despesas = self.tableWidget.item(a, 1).text()
        tipo = self.tableWidget.item(a, 2).text()
        agendado = self.tableWidget.item(a, 3).text()
        valor = self.tableWidget.item(a, 4).text()
        status = self.tableWidget.item(a, 5).text()
        data = self.tableWidget.item(a, 6).text()
        id = int(id.text())
        tipo = 3
        atualizar_dados(id, tipo, despesas, tipo, agendado, valor, status, data)
        self.close()

    def cancelar(self):
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.close()


class teladeCadastroCliente(QMainWindow, cadastroCliente.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent,)

        super().setupUi(self)
        print("tela de cadastro")
        self.btnCadastrar.clicked.connect(self.cadastrarClientes)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnReset.clicked.connect(self.reset)

    def reset(self):
        self.inpuNome.clear()
        self.inpuSobrenome.clear()
        self.inputPet.clear()
        self.inpuCpf.clear()
        self.inputWats.clear()
        self.inputEmail.clear()
        self.inputNumero.clear()

    def cancelar(self):
        self.close()

    def cadastrarClientes(self):
        nome = self.inpuNome.text()
        tipodopet = self.inputPet.text()
        wats = self.inputWats.text()
        email = self.inputEmail.text()
        cpf = self.inpuCpf.text()
        sobrenome = self.inpuSobrenome.text()
        uf = self.cb_uf.currentText()
        endereco = self.inpuEndereco.text()
        numero = self.inputNumero.text()

        if nome.strip() == "" or email.strip() == "" or tipodopet.strip() == "" or wats.strip() == "" or endereco.strip() == "":
            QMessageBox.warning(QMessageBox(), "Prencha todos os campos",
                                "Prencha todos os campos",)
        else:
            tipo = 1
            cadastro_cliente(tipo, nome, tipodopet, wats,
                             email, cpf, sobrenome, uf, endereco, numero)
            msg = QMessageBox
            msg.warning(QMessageBox(), "foi",
                        "foi",)
            self.close()


class teladeCadastroServico(QMainWindow, cadastroServico.Ui_MainWindow):
    def __init__(self, menuu):
        super(teladeCadastroServico, self).__init__()
        self.setupUi(self)
        print("tela de cadastro")
        self.btnCadastrar.clicked.connect(self.cadastrarServico)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnReset.clicked.connect(self.reset)
        self.radioButton.clicked.connect(self.mostra)
        self.radioButton_2.clicked.connect(self.esconde)
        self.frame_3.hide()
        self.a = menuu
        self.status = 0
        a = self.a
        self.tabelaClientes.setRowCount(len(a))
        self.tabelaClientes.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        row = 0
        for n in a:
            b = n[0]
            self.tabelaClientes.setItem(
                row, 0, QTableWidgetItem(str(b)))
            b = n[1]
            self.tabelaClientes.setItem(
                row, 1, QTableWidgetItem(str(b)))

            row += 1
        self.horario()

    def mostra(self):
        self.frame_3.setEnabled(True)
        self.frame_3.show()
        self.status = 1

    def esconde(self):
        self.frame_3.setEnabled(False)
        self.frame_3.hide()
        self.status = 0

    def horario(self):
        data = datetime.now()
        self.Dia = str(data.day)
        self.Mes = str(data.month)
        self.Ano = str(data.year)
        self.inpuDia.setText(self.Dia)
        self.inpuMes.setText(self.Mes)
        self.inpuAno.setText(self.Ano)

    def reset(self):
        self.inputPesquisa.clear()
        self.inputTotal.clear()
        self.inputDescricao.clear()

    def cancelar(self):
        self.close()

    def cadastrarServico(self):
        a = self.tabelaClientes.currentRow()
        if a > -1:
            id = self.tabelaClientes.item(a, 0)
            id = int(id.text())
        else:
            id = 1
        tipo = 2
        servico = self.cb_servico.currentText()
        pagamento = self.cb_pagamento.currentText()
        total = self.inputTotal.text()
        descricao = self.inputDescricao.text()
        if self.status == 1:
            data = datetime.now()
            hora = self.cb_perfil_6.currentText()
            min = self.cb_perfil_5.currentText()
            dia = self.inpuDia.text()
            mes = self.inpuMes.text()
            ano = self.inpuAno.text()
        else:
            data = datetime.now()
            hora = str(data.hour)
            min = str(data.minute)
            dia = str(data.day)
            mes = str(data.month)
            ano = str(data.year)
        if servico.strip() == "" or pagamento.strip() == "" or total.strip() == "" or ano.strip() == "" or mes.strip() == "" or dia.strip() == "" or hora.strip() == "" or min.strip() == "":
            QMessageBox.warning(QMessageBox(), "Prencha todos os campos",
                                "Prencha todos os campos",)
            return
        else:
            status = self.status
            cadastro_cliente(tipo, id,  servico, pagamento,
                             total, ano, mes, dia, hora, min, descricao, status)
            msg = QMessageBox
            msg.warning(QMessageBox(), "foi",
                        "foi",)

            self.close()


class teladeCadastroDespesa(QMainWindow, cadastroDespesa.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        print("tela de cadastro")
        self.btnCadastrar.clicked.connect(self.cadastrarServico)
        self.btnCancelar.clicked.connect(self.cancelar)
        self.btnReset.clicked.connect(self.reset)
        self.horario()

    def horario(self):
        data = datetime.now()
        self.Dia = str(data.day)
        self.Mes = str(data.month)
        self.Ano = str(data.year)
        self.inpuDia.setText(self.Dia)
        self.inpuMes.setText(self.Mes)
        self.inpuAno.setText(self.Ano)

    def reset(self):
        self.inputDespesa.clear()
        self.inputTotal.clear()
        self.inputTotal.clear()

    def cancelar(self):
        self.close()

    def cadastrarServico(self):
        tipo = 3
        tipo_despesa = self.cb_tipo.currentText()
        despesa = self.inputDespesa.text()
        status = self.cb_status.currentText()
        valor = self.inputTotal.text()
        agendado = self.cb_agendado.currentText()

        mes = self.inpuMes.text()
        data_despesa = mes
        if tipo_despesa.strip() == "" or despesa.strip() == "" or status.strip() == "" or valor.strip() == "" or agendado.strip() == "":
            QMessageBox.warning(QMessageBox(), "Prencha todos os campos",
                                "Prencha todos os campos",)
            return
        else:
            cadastro_cliente(tipo, despesa,  tipo_despesa,
                             agendado, valor, status, data_despesa)
            msg = QMessageBox
            msg.warning(QMessageBox(), "foi",
                        "foi",)

            self.close()


class teladeLogin(QMainWindow, login.Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        super().setupUi(self)
        print("asdasdas")

        self.btnLogin.clicked.connect(self.logar)

    def logar(self):
        print("cliquei")
        email = self.inputEmail.text()
        senha = self.inputPsw.text()
        estado = test_login(email, senha)
        if estado:
            self.window = menuu()
            self.close()
            self.window.show()
        else:
            QMessageBox.warning(QMessageBox(), "Email ou senha incorretos tente novamente",
                                "E-mail ou senha incorretos. Tente novamente!",)


if __name__ == '__main__':
    qt = QApplication(sys.argv)
    teladeLoginn = teladeLogin()
    teladeLoginn.show()
    qt.exec_()
