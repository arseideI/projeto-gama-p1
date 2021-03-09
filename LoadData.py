'''
Carga massiva das tabelas da API postman COVID19
'''

import pyodbc
import requests

''' Conexão com o DB. 
    Defini se o banco de dados é local ou na núvem.
    Retorna um cursor de conexão aberta
    Por defaul a conexão será local
'''
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
                      'Database=BD_COVID_GAMMA;'
                      'UID=sa;'
                      'PWD=sa;')

    return conn.cursor()

''' 
    Realiza uma chamada da API countryes COVID19    
'''
def request_api(url_api):
    resposta = requests.get(url_api)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        return resposta.status_code

'''
    Consulta se um determinado registro já está cadastrado na tabela.
    Retorna um True para existente e false para não
'''
def query_table (table, column, filter):
    cursor = conexaoDB()
    cons = cursor.execute(f"SELECT {column} FROM {table} WHERE {column} = ?", filter)
    s = [True for x in cons if x[0] == filter]
    resp = False
    if len(s) == 1:
        resp = True
    return resp

'''
   
'''
def load_country():
    response = request_api('https://api.covid19api.com/countries')

    cursor = conexaoDB()

    for js in response:
        country = (js['Country'])
        slug    = (js['Slug'])
        iso2    = (js['ISO2'])
        cons = cursor.execute(f"SELECT NM_COUNTRY_SLUG FROM COUNTRY WHERE NM_COUNTRY_SLUG = ?", slug)
        s = [True for x in cons if x[0] == filter]
        if len(s) != 1:
            cursor.execute(f"INSERT INTO COUNTRY(NM_COUNTRY, NM_COUNTRY_SLUG, NM_COUNTRY_ISO2) VALUES (?,?,?)", country, slug, iso2)
            cursor.commit()

'''
CARGA MASSIVA DOS CASOS DESDE O DIA PRIMEIRO DIA POR PAISES
'''
def load_cases_covid():
    cursor = conexaoDB()
    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY WHERE ID_COUNTRY = 219")

    #https://api.covid19api.com/total/country/united-states

    for next_country in list_country:
        print(next_country[0])
        url_api = (f'https://api.covid19api.com/dayone/country/{next_country[0]}?from=2020-01-01T00:00:00Z&to=2020-01-31T00:00:00Z')
        response = request_api(url_api)
        for n_load in response:
            cursor2 = conexaoDB()
            id_case_system = (n_load['ID'])
            id_country = (next_country[1])
            province = (n_load['Confirmed'])
            city = (n_load['Confirmed'])
            city_code = (n_load['Confirmed'])
            confirmed = (n_load['Confirmed'])
            deaths = (n_load['Deaths'])
            recovered = (n_load['Recovered'])
            active = (n_load['Active'])
            dt_case = (n_load['Date'])

            cursor2.execute(f"INSERT INTO CASE_COUNTRY(ID_CASE_SISTEM, ID_COUNTRY, PROVINCE, CITY, CITY_CODE, CONFIRMED, DEATHS, RECOVERED, ACTIVE, DT_CASE) VALUES (?,?,?,?,?,?,?,?,?,?)", id_case_system, id_country, province, city, city_code, confirmed, deaths, recovered, active, dt_case)
            cursor2.commit()

def update_country_lat_lon():
    cursor = conexaoDB()
    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY WHERE LATITUDE IS NULL")

    for next_country in list_country:

        print(next_country[0])
        cursor2 = conexaoDB()

        #url_api = (f'https://api.covid19api.com/dayone/country/wallis-and-futuna-islands')
        url_api = (f'https://api.covid19api.com/total/dayone/country/{next_country[0]}')

        response = request_api(url_api)

        for n_load in response:
            cons = cursor2.execute(f"SELECT LATITUDE FROM COUNTRY WHERE ID_COUNTRY = {next_country[1]} AND LATITUDE IS NOT NULL")
            s = [True for x in cons if x[0] != '']
            if len(s) != 1:
                latitude = (n_load['Lat'])
                longitude = (n_load['Lon'])

                cursor2.execute(f"UPDATE COUNTRY SET LATITUDE = {latitude} WHERE ID_COUNTRY = {next_country[1]}")
                cursor2.execute(f"UPDATE COUNTRY SET LONGITUDE = {longitude} WHERE ID_COUNTRY = {next_country[1]}")
                cursor2.commit()
                print('OK')

print("Inicio da carga")
#load_country()
#update_country_lat_lon()
load_cases_covid()

print("Término carga")