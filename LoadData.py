from conexao_db import ConexaoBD
from RequestApi import api_covid


def load_country():
    object = api_covid('https://api.covid19api.com/countries')
    response = object.get_connection()

    # db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa','sqlserver')
    db2 = db.conexao_azure()
    cursor = db2.cursor()

    for js in response:
        country = (js['Country'])
        slug    = (js['Slug'])
        iso2    = (js['ISO2'])
        cons = cursor.execute(f"SELECT NM_COUNTRY_SLUG FROM COUNTRY WHERE NM_COUNTRY_SLUG = ?", slug)
        s = [True for x in cons if x[0] == slug]
        if len(s) != 1:
            cursor.execute(f"INSERT INTO COUNTRY(NM_COUNTRY, NM_COUNTRY_SLUG, NM_COUNTRY_ISO2) VALUES (?,?,?)", country, slug, iso2)
            cursor.commit()

    cursor.close()


def load_cases_covid():
    # db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa', 'sqlserver')
    conn = db.conexao_azure()
    cursor = conn.cursor()

    conn2 = db.conexao_azure()
    cursor2 = conn2.cursor()

    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY WHERE ID_COUNTRY > 127")

    for next_country in list_country:
        print(next_country[0])

        object = api_covid(f'https://api.covid19api.com/total/country/{next_country[0]}')
        response = object.get_connection(False)

        for n_load in response:
            id_country = (next_country[1])
            confirmed = (n_load['Confirmed'])
            deaths = (n_load['Deaths'])
            recovered = (n_load['Recovered'])
            active = (n_load['Active'])
            dt_case = (n_load['Date'])
            cursor2.execute(f"INSERT INTO CASE_COUNTRY(ID_COUNTRY, CONFIRMED, DEATHS, RECOVERED, ACTIVE, DT_CASE) VALUES (?,?,?,?,?,?)", id_country, confirmed, deaths, recovered, active, dt_case)
            cursor2.commit()

#load_country()
load_cases_covid()
#load_cases_covid_from_date()
