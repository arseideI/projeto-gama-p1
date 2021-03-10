'''
    Equipe Zumbi Tech 4.0
    Script de automação para atualização diária de dados
    Conceitos utilizados:
        - Azure Functions
        - PL-SQL Triggers
        - POO python v3.x 
'''

import pyodbc
import requests
from conexao_bd import ConexaoBD
import datetime
import asyncio

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=arseideltest.database.windows.net;'
#                       'Database=AT1_SQL_ARS;'
#                       'UID=arseidel;'
#                       'PWD=Seidelsenha123;')

# cursor = conn.cursor()

# db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')

class CovidUpdate(ConexaoBD):
    def __init__(self, Server, BD, Login, Senha, verbose, driver='Driver = {SQL Server}'):
        super().__init__(Server, BD, Login, Senha, verbose, driver=driver)
        self.Server = Server
        self.BD = BD
        self.uid = Login
        self.pwd = Senha
        self.verbose = verbose
        self.driver = driver
        self.data_collected = []
        self.getUpdate(self)
    
    # Método que realiza GET request sobre as últimas atualizações de todos os países e armazena o json
    async def getUpdate(self):
        # Armazena em data
        await self.data_collected.append({"data": datetime.now(), "update_collected": requests.get("").json()})
    
    # Método que contém a function organiza os dados coletados e submete ao BD
    def postUpdate(self):
        conn = pyodbc.connect(self.driver + self.Server + self.BD + self.uid + self.pwd)
        cursor = conn.cursor()
        self.getUpdate()


