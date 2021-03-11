from conexao_db import ConexaoBD
import requests
import datetime

def request_api(url_api):
    resposta = requests.get(url_api)
    if resposta.status_code == 200:
        return resposta.json()
    else:
        return resposta.status_code

def load_cases_covid_from_date():
    # db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa', 'sqlserver')

    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    conn = db.conexao_azure()
    cursor = conn.cursor()
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY")

    conn2 = db.conexao_azure()
    cursor2 = conn2.cursor()

    conn3 = db.conexao_azure()
    cursor3 = conn3.cursor()

    data_atual = datetime.date.today()

    for next_country in list_country:
        max_data = cursor2.execute(f"SELECT MAX(DT_CASE), COUNT(*) FROM CASE_COUNTRY WHERE ID_COUNTRY = {next_country[1]}")

        for list_date in max_data:

            if list_date[1] != 0:
                last_date = list_date[0]
                n_last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d').date()

                add_last_date = n_last_date + datetime.timedelta(days=1)
                if add_last_date < data_atual:
                    url_api = (f'https://api.covid19api.com/total/country/{next_country[0]}?from={add_last_date}T00:00:00Z&to={add_last_date}T23:59:59Z')
                    #print(url_api)
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

if __name__ == '__main__':
    load_cases_covid_from_date()