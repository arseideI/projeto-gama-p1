#Classe para realizar a conexão com o BD e inserção dos valores
import pyodbc
import mysql.connector


class ConexaoBD(object):

    def __init__(self,Server,BD,Login,Senha,verbose):
        self.Server = Server
        self.BD = BD
        self.Login = Login
        self.Senha = Senha
        self.verbose = verbose

    def conexao_azure(self):

        if self.verbose == "sqlserver":
            try:
                print(f"Conexão com o banco de dados {self.verbose} Azure iniciada...")
                self.conn = pyodbc.connect("Driver={SQL Server};"
                                      f"Server={self.Server};"
                                      f"Database={self.BD};"
                                      f"UID={self.Login};"
                                      f"PWD={self.Senha}")
                print("A conexão ocorreu com êxito!")

            except pyodbc.Error as err:
                if err.args[0] == "IM002":
                    print("Não foi possível realizar a conexão com o banco de dados (nome do Driver incorreto). Por favor, reveja o nome do Driver desejado.")
                elif err.args[0] == "08001":
                    print("Não foi possível realizar a conexão com o banco de dados (Servidor inexistente ou acesso negado). Por favor, reveja o nome do Servidor desejado.")
                elif err.args[0] == "42000":
                    print("Não foi possível Realizar a conexão com o banco de dados (BD inexistente). Por favor, reveja o nome do BD desejado.")
                elif err.args[0] == "28000":
                    print("Não foi possível Realizar a conexão com o banco de dados (Login ou senha invalidos). Por favor, reveja os respectivos campos.")
                else:
                    print(f"Não foi possível Realizar a conexão com o banco de dados: {err.args[1]}. Por favor, tente novamente. ")
                    
        
        elif self.verbose == "mysql":
            try:
                print(f"Conexão com o banco de dados {self.verbose} Azure iniciada...")
                self.conn = mysql.connector.connect(host={self.Server},
                                                    user={self.Login},
                                                    password={self.Senha},
                                                    database={self.BD})
                print("A conexão ocorreu com êxito!")

            except mysql.connector.Error as err:
                print(f"Não foi possível Realizar a conexão com o banco de dados: {err}")
                
        else:
            print("SGBD não suportado. Por favor, selecione sqlserver ou mysql.")

    def close_azure(self):
        self.conn.close()
        print("Conexão com o servidor encerrada...")