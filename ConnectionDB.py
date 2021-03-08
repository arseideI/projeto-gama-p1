'''
CLASSE COM MÉTODOS PARA ABERTURA ABERTURA DE CONEXÃO COM BANCO DADOS.
INTERESSANTE TER POSSIBILIDADE DE ESCOLHER ENTRE LOCAL E CLOUD AZURE
INTERESSANTE LER CONFIGURAÇÕES DE UM ARQUIVO
INTERESSANTE TER TRATAMENTO DE EXCEÇÃO

'''
# EXEMPLO
def conexaoDB (tipo = 'local'):
    if tipo == 'azure':
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=casadocodigo-sql-srv-isr.database.windows.net;'
                      'Database=BD_SQL_GAMMA_IBGE;'
                      'UID=Administrador;'
                      'PWD=Alura!123;')
    else:
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-DPP33GN;'
                      'Database=BD_SQL_GAMMA_IBGE;'
                      'UID=sa;'
                      'PWD=sa;')

    return conn.cursor()