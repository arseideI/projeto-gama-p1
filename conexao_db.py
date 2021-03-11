#Classe para realizar a conexão com o BD e inserção dos valores
import pyodbc
import mysql.connector

"""
Esta classe é responsável por fazer a conexão com o servidor e o banco de dados. Foi feita de maneira a ser a mais genérica 
possível, permitindo a conexão com servidores em nuvem ou locais, ou utilizando SQL Server ou MySQL. Além disso, também
há a possibilidade de escolher entre os drivers do Linux ou Windows.

Os tratamentos de erros foram feitos de forma específica, para que o usuário entenda qual foi a problemática e possa resolvê-la de forma simples.
"""

class ConexaoBD(object): #classe de conexão com o BD
    
    flag = 0 #variável responsável por informar se a conexão foi executada com êxito ou não. Será utilizada posteriormente quando fecharmos a conexão.

    def __init__(self,Server,BD,Login,Senha,verbose, driver = "Driver={SQL Server}"):
        self.Server = Server
        self.BD = BD
        self.Login = Login
        self.Senha = Senha
        self.verbose = verbose
        self.driver = driver

    def conexao_azure(self): #aqui é feita a conexão com o bd, podendo ser mysql ou sqlserver, linux ou windows, local ou azure

        if self.verbose == "sqlserver": #opção que indica conexão com o sql server
            try:
                print(f"Conexão com o banco de dados {self.verbose} Azure iniciada...")
                self.conn = pyodbc.connect(f"{self.driver};"
                                           f"Server={self.Server};"
                                           f"Database={self.BD};"
                                           f"UID={self.Login};"
                                           f"PWD={self.Senha};")
                print("A conexão ocorreu com êxito!")
                self.flag = 1 #set da variável que indica êxito na conexão
                return self

            except pyodbc.Error as err: #etapa de tratamento dos possíveis erros relativos à conexão.
                if err.args[0] == "IM002":
                    print("Não foi possível realizar a conexão com o banco de dados (nome do Driver incorreto). Por favor, reveja o nome do Driver desejado.") #erro de driver
                elif err.args[0] == "08001":
                    print("Não foi possível realizar a conexão com o banco de dados (Servidor inexistente ou acesso negado). Por favor, reveja o nome do Servidor desejado.") #erro de servidor
                elif err.args[0] == "42000":
                    print("Não foi possível Realizar a conexão com o banco de dados (BD inexistente). Por favor, reveja o nome do BD desejado.") # erro de banco de dados
                elif err.args[0] == "28000":
                    print("Não foi possível Realizar a conexão com o banco de dados (Login ou senha invalidos). Por favor, reveja os respectivos campos.") #erro de login ou senha
                else:
                    print(f"Não foi possível Realizar a conexão com o banco de dados: {err.args[1]}. Por favor, tente novamente. ") #erro genérico não listado acima
                    
        
        elif self.verbose == "mysql": #opção que indica conexão com o mysql
            try:
                print(f"Conexão com o banco de dados {self.verbose} Azure iniciada...")
                self.conn = mysql.connector.connect(host=self.Server,
                                                    user=self.Login,
                                                    password=self.Senha,
                                                    database=self.BD)
                print("A conexão ocorreu com êxito!")
                self.flag = 1 #set da variável que indica êxito na conexão
                return self

            except mysql.connector.Error as err: #etapa de tratamento dos possíveis erros relativos à conexão.
                if err.sqlstate == "42000":
                    print("Não foi possível Realizar a conexão com o banco de dados (BD inexistente). Por favor, reveja o nome do BD desejado.") #erro de banco de dados
                elif err.errno == 2003:
                    print("Não foi possível realizar a conexão com o banco de dados (Servidor inexistente ou acesso negado). Por favor, reveja o nome do Servidor desejado.") #erro de servidor
                elif err.errno == 1045:
                    print("Não foi possível realizar a conexão com o banco de dados (Login ou senha invalidos). Por favor, reveja os respectivos campos.") #erro de login ou senha
                else:
                    print(f"Não foi possível Realizar a conexão com o banco de dados: {err.msg}. Por favor, tente novamente. ") #erro genérico não listado acima
                
        else:
            print("SGBD não suportado. Por favor, selecione sqlserver ou mysql.")

    def close_azure(self): #classe de fechamento da conexão com o servidor
        if self.flag == 1:
            self.conn.close()
            print("Conexão com o servidor encerrada...")
        else:
            return -1