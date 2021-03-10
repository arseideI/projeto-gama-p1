from conexao_db import ConexaoBD
import requests
from datetime import date

'''
Carga massiva das tabelas da API postman COVID19
'''

''' 
    Realiza uma chamada da API countryes COVID19    
'''
def request_api(url_api):
    resposta = requests.get(url_api)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        return resposta.status_code


def load_country():
    response = request_api('https://api.covid19api.com/countries')

    #db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa','sqlserver')
    db2 = db.conexao_azure()
    cursor = db2.cursor()

    for js in response:
        country = (js['Country'])
        slug    = (js['Slug'])
        iso2    = (js['ISO2'])
        cons = cursor.execute(f"SELECT NM_COUNTRY_SLUG FROM COUNTRY WHERE NM_COUNTRY_SLUG = ?", slug)
        s = [True for x in cons if x[0] == filter]
        if len(s) != 1:
            cursor.execute(f"INSERT INTO COUNTRY(NM_COUNTRY, NM_COUNTRY_SLUG, NM_COUNTRY_ISO2) VALUES (?,?,?)", country, slug, iso2)
            cursor.commit()

    cursor.close()


def load_cases_covid():
    # db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa', 'sqlserver')
    conn = db.conexao_azure()
    conn2 = db.conexao_azure()

    cursor = conn.cursor()

    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY")

    for next_country in list_country:
        print(next_country[0])
        url_api = (f'https://api.covid19api.com/total/country/{next_country[0]}')

        response = request_api(url_api)
        for n_load in response:

            cursor2 = conn2.cursor()
            id_country = (next_country[1])
            confirmed = (n_load['Confirmed'])
            deaths = (n_load['Deaths'])
            recovered = (n_load['Recovered'])
            active = (n_load['Active'])
            dt_case = (n_load['Date'])

            cursor2.execute(f"INSERT INTO CASE_COUNTRY(ID_COUNTRY, CONFIRMED, DEATHS, RECOVERED, ACTIVE, DT_CASE) VALUES (?,?,?,?,?,?)", id_country, confirmed, deaths, recovered, active, dt_case)
            cursor2.commit()

'''
CARGA MASSIVA DOS CASOS DESDE O DIA PRIMEIRO DIA POR PAISES
'''
def load_cases_covid_from_date():
    # db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa', 'sqlserver')

    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    conn = db.conexao_azure()
    cursor = conn.cursor()
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY where id_country > 98")
    print(list_country)

    conn2 = db.conexao_azure()
    cursor2 = conn2.cursor()

    conn3 = db.conexao_azure()
    cursor3 = conn3.cursor()

    data_atual = date.today()

    #max_data = cursor2.execute(f"SELECT MAX(DT_CASE) FROM CASE_COUNTRY WHERE ID_COUNTRY > 88")

    for next_country in list_country:

        max_data = cursor2.execute(f"SELECT MAX(DT_CASE), COUNT(*) FROM CASE_COUNTRY WHERE ID_COUNTRY = {next_country[1]}")
        print(next_country[0])
        for list_date in max_data:
            print(list_date)
            if list_date[1] != 0:
                last_date = list_date[0]
                print(len(last_date))

                if last_date < data_atual:
                    print(type(last_date))
                    url_api = (f'https://api.covid19api.com/total/country/{next_country[0]}?from={last_date}T00:00:00Z&to={data_atual}T00:00:00Z')
                    print(type())

                    response = request_api(url_api)
                    for n_load in response:
                        id_country = (next_country[1])
                        confirmed = (n_load['Confirmed'])
                        deaths = (n_load['Deaths'])
                        recovered = (n_load['Recovered'])
                        active = (n_load['Active'])
                        dt_case = (n_load['Date'])

                        cursor3.execute(f"INSERT INTO CASE_COUNTRY(ID_COUNTRY, CONFIRMED, DEATHS, RECOVERED, ACTIVE, DT_CASE) VALUES (?,?,?,?,?,?)", id_country, confirmed, deaths, recovered, active, dt_case)
                        cursor3.commit()


print("Inicio da carga")
#load_country()
#update_country_lat_lon()
#load_cases_covid()
#update_country_lat_lon()
load_cases_covid_from_date()
print("Término carga")