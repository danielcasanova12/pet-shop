import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox,
                             QTableWidget, QTableWidgetItem)


class DB:
    def __init__(self, arquivo):
        self.conn = sqlite3.connect(arquivo)
        self.cursor = self.conn.cursor()

    def concluir(self, id):
        try:
            xsql = f"""UPDATE tb_servicos Set agendamento = 'Não' WHERE id= {id}"""
            self.cursor.execute(xsql)
            self.conn.commit()
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def agendados(self):
        try:
            xsql = """SELECT * FROM tb_servicos WHERE agendamento = 'Sim'"""
            self.cursor.execute(xsql)
            a = self.cursor.fetchall()
            return a
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def mostrar_id(self, id, tabela):
        try:
            id = int(id)
            xsql = f"""SELECT * FROM {tabela} WHERE id = {id}"""
            self.cursor.execute(xsql)
            a = self.cursor.fetchall()
            return a
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def grafico(self, mes):
        try:
            lista = []
            for i in range(5):
                xsql = f"""SELECT * FROM tb_servicos WHERE mes = {mes} """
                self.cursor.execute(xsql)
                a = self.cursor.fetchall()
                lista.append(a)
                mes = int(mes)
                if mes == 1:
                    mes = 12
                else:
                    mes -= 1
                mes = str(mes)

            return lista
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def faturamento(self, mes):
        try:
            lucro = 0
            despesa_variavel = 0
            despesa_fixa = 0
            self.cursor.execute(
                'SELECT * FROM tb_servicos WHERE mes = ? ', (mes))
            a = self.cursor.fetchall()
            for row in range(len(a)):
                lucro += int(a[row][4])
            qt_servico = len(a)

            self.cursor.execute(
                'SELECT * FROM tb_despesa WHERE data = ? ', (mes))
            a = self.cursor.fetchall()

            for row in range(len(a)):
                if a[row][5] == '1':
                    despesa_fixa += int(a[row][4])
                if a[row][5] == '2':
                    despesa_variavel += int(a[row][4])
            total = [(lucro), (despesa_fixa), (despesa_variavel),
                     (qt_servico)]
            return total
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')

    def select_db(self, username, password):
        try:
            self.cursor.execute('SELECT * FROM tb_clientes WHERE email = ? AND password = ?',
                                (username, password))
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')

    def cadastrarCliente(self, *args):
        try:
            tipo = args[0]

            if tipo == 1:
                nome = args[1]
                tipodopet = args[2]
                wats = args[3]
                email = args[4]
                cpf = args[5]
                sobrenome = args[6]
                uf = args[7]
                endereco = args[8]
                numero = args[9]
                query = '''INSERT INTO tb_clientes (nome, tipodopet, wats, email, cpf,
                        sobrenome, uf, endereco, numero)VALUES (?, ?,?, ?,?, ?,?, ?,?);'''

                data = (nome, tipodopet, wats, email, cpf,
                        sobrenome, uf, endereco, numero)
                self.cursor.execute(query, data)
                self.conn.commit()
                print('\n[!] Registro inserido com sucesso [!]')
            elif tipo == 2:
                id = args[1]
                servico = args[2]
                pagamento = args[3]
                total = args[4]
                ano = args[5]
                mes = args[6]
                dia = args[7]
                hora = args[8]
                min = args[9]
                descricao = args[10]
                agendamento = args[11]
                query = '''INSERT INTO tb_servicos ( id_cliente,  servico, pagamento,
                            total, ano, mes, dia, hora, min,descricao,agendamento)VALUES (?,?, ?,?, ?,?, ?,?, ?,?,?);'''

                data = (id,  servico, pagamento,
                        total, ano, mes, dia, hora, min, descricao, agendamento)
                self.cursor.execute(query, data)
                self.conn.commit()
                print('\n[!] Registro inserido com sucesso [!]')
            else:
                despesas = args[1]
                tipo_despesa = args[2]
                agendado = args[3]
                valor = args[4]
                status = args[5]
                data_despesa = args[6]
                query = '''INSERT INTO tb_despesa (despesas, tipo, agendado,
                valor, tipodespesa,data)VALUES (?, ?,?, ?,?, ?);'''

                data = (despesas, tipo_despesa, agendado,
                        valor, status, data_despesa)
                self.cursor.execute(query, data)
                self.conn.commit()
                print('\n[!] Registro inserido com sucesso [!]')
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')

    def buscar_login(self, email, password):
        """Busca um cliente pelo cpf"""
        try:
            cursor = self.conn.cursor()

            # obtém todos os dados
            cursor.execute("""SELECT * FROM tb_login;""")

            # o fetchall retorna o resultado do select
            # o retorno é uma lista, um iterável
            for linha in cursor.fetchall():
                if linha[1] == email and linha[2] == password:
                    return True

        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def buscar_emaill(self, email):
        """Busca um cliente pelo cpf"""
        try:
            cursor = self.conn.cursor()

            # obtém todos os dados
            cursor.execute("""SELECT * FROM tb_clientes ;""")

            # o fetchall retorna o resultado do select
            # o retorno é uma lista, um iterável
            for linha in cursor.fetchall():
                if linha[1] == email:
                    return True
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def Mostrar(self, chave):
        chave = f'{chave}'
        cursor = self.conn.cursor()
        # obtém todos os dados
        try:
            sqlx = (f"""SELECT * FROM {chave};""")
            cursor.execute(sqlx)
            lista = cursor.fetchall()
            return lista
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
            return False

    def deletardado(self, id, chave):
        try:
            id_cliente = id
            chave = f'{chave}'

        # excluindo um registro da tabela
            xsql = f"DELETE FROM {chave} WHERE id = ?"
            self.cursor.execute(xsql, (id_cliente,))

            self.conn.commit()
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')

    def atualiza(self, *args):
        try:
            id_cliente = args[0]
            id_cliente = str(id_cliente)
            tipo = args[1]
            if tipo == 1:
                nome = args[2]
                tipodopet = args[3]
                email = args[4]
                cpf = args[5]
                uf = args[6]
                endereco = args[7]
                numero = args[8]
                sobrenome = args[9]
                wats = args[10]
                xsql = f"""UPDATE tb_clientes SET nome= '{nome}', tipodopet = '{tipodopet}', wats= '{wats}', email= '{email}', cpf= '{cpf}' , uf= '{uf}', endereco= '{endereco}', numero= '{numero}', sobrenome= '{sobrenome}'  WHERE id= {id_cliente}"""

                self.cursor.execute(xsql)
                self.conn.commit()
            elif tipo == 2:
                id_cliente_2 = args[2]
                servico = args[3]
                pagamento = args[4]
                total = args[5]
                ano = args[6]
                mes = args[7]
                dia = args[8]
                hora = args[9]
                min = args[10]
                descricao = args[11]
                xsql = f"""UPDATE tb_servicos SET id_cliente= '{id_cliente_2}', servico= '{servico}', pagamento= '{pagamento}', total= '{total}', ano= '{ano}', mes= '{mes}', dia= '{dia}', hora= '{hora}', min= '{min}', descricao= '{descricao}' WHERE id= {id_cliente}"""

                self.cursor.execute(xsql)

                self.conn.commit()
                # """UPDATE tb_servicos SET email = 'sdasd', nome = '123123' WHERE id = 2"""
            else:
                despesas = args[2]
                tipo2 = args[3]
                agendamento = args[4]
                valor = args[5]
                status = args[6]
                data = args[7]
                xsql = f"""UPDATE tb_despesa SET despesas = '{despesas}', tipo= '{tipo2}', agendado= '{agendamento}', valor= '{valor}', tipodespesa= '{status}', data= '{data}' WHERE id= {id_cliente}"""

                self.cursor.execute(xsql)

                self.conn.commit()
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')

    def gerar(self, chave, nome):
        try:
            print("gerar")
            chave = f'{chave}'
            comando_sql2 = f"SELECT * FROM {chave}"
            empresas = pd.read_sql_query(comando_sql2, self.conn)

            empresas.to_excel(f"{nome}", sheet_name='empresas', index=False)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Excel")
            msg.setText("Relatório Excel gerado com sucesso!")
            msg.exec()
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')

    def pesquisar(self, *args):
        # excluindo um registro da tabela
        try:
            a = args[0]
            a = str(a)

            tipo = args[1]
            if tipo == 1:
                chave = args[2]
                chave = f'{chave}'
                vsql = f"""SELECT * FROM tb_servicos WHERE id LIKE '%{a}%' or servico like '%{a}%' or id like '%{a}%' or descricao like '%{a}%' or id_cliente like '%{a}%'"""

                self.cursor.execute(vsql)
                lista = self.cursor.fetchall()
                return lista

            elif tipo == 2:
                chave = args[2]
                chave = f'{chave}'
                vsql = f"""SELECT * FROM tb_clientes WHERE id LIKE '%{a}%' or nome like '%{a}%'"""

                self.cursor.execute(vsql)
                lista = self.cursor.fetchall()
                return lista
            else:
                vsql = f"""SELECT * FROM tb_despesa WHERE id LIKE '%{a}%' or data like '%{a}%' or tipo like '%{a}%' or tipodespesa like '%{a}%' or agendado like '%{a}%' or valor like '%{a}%'"""

                self.cursor.execute(vsql)
                lista = self.cursor.fetchall()
                return lista
        except AttributeError:
            print('Faça a conexão do banco antes de buscar clientes.')
    ###########################################################################

        # vsql = "SELECT * FROM tbl_login WHERE id LIKE '%"+a+"%' or email LIKE '%"+a+"%'"
        # print(vsql)
        # self.cursor.execute(vsql)

        # lista = self.cursor.fetchall()
        # return lista

    ###########################################################################


def test_login(email, password):
    db = DB('login.db')
    email = str(email)
    password = str(password)
    # data = (email, password)
    # db.insert_row(data)
    if db.buscar_login(email, password):
        return True
    return False


def mostrar(chave):
    db = DB('login.db')
    return db.Mostrar(chave)


def deletardados(id, chave):
    db = DB('login.db')
    id = str(id)
    print("entrou na funçao id :", id)
    db.deletardado(id, chave)


def cadastro_cliente(*args):
    db = DB('login.db')
    db.cadastrarCliente(*args)


def buscar_email(email):
    db = DB('login.db')
    if db.buscar_emaill(email):
        return False
    return True


def atualizar_dados(*args):
    db = DB('login.db')
    db.atualiza(*args)


def gerarExel(chave, nome):
    print("gerarExel")
    db = DB('login.db')
    db.gerar(chave, nome)


def pesquisa(*args):
    db = DB('login.db')
    return db.pesquisar(*args)


def faturamento_mensal(mes):
    db = DB('login.db')
    return db.faturamento(mes)


def mostrar_id(id, tabela):
    db = DB('login.db')
    return db.mostrar_id(id, tabela)


def grafico(mes):
    db = DB('login.db')
    return db.grafico(mes)


def agendados():
    db = DB('login.db')
    return db.agendados()


def concluir(id):
    db = DB('login.db')
    return db.concluir(id)
