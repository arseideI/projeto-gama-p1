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

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=arseideltest.database.windows.net;'
#                       'Database=AT1_SQL_ARS;'
#                       'UID=arseidel;'
#                       'PWD=Seidelsenha123;')

# cursor = conn.cursor()

class CovidUpdate(ConexaoBD):
    def __init__(self):
        super().__init__()
    
    def __getUpdate(self):
        pass
    def postUpdate(self):
        self.__getUpdate()


