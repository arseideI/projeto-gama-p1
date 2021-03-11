from conexao_db import ConexaoBD
from RequestApi import api_covid
import datetime

"""
    Método para atualização da base de dados COVID, com dados publicados diariamente 
    na API https://api.covid19api.com/total/country/brazil?from=2020-01-22T00:00:00Z&to=2020-01-22T23:59:59Z
    
    O método consulta o DB e retorna uma lista com todos os paises cadastrados na tabela COUNTRY e percorre
    todos os países, verificando a maior data e a quantidade de linhas cadastradas. Utilizando o slug e a maior data
    inserida, consulta a API com os dados publicados e cadastra no DB na cloud Azure.
    
    A proposta é que essa aplicação fique publicada e no schedule para rodar a cada 15 minutos para garantir a atualização
    
"""
def load_cases_covid_from_date():
    db = ConexaoBD('casadocodigo-sql-srv-isr.database.windows.net', 'BD_COVID_GAMMA', 'Administrador', 'Alura!123', 'sqlserver')
    # db = ConexaoBD('DESKTOP-DPP33GN', 'BD_COVID_GAMMA', 'sa', 'sa', 'sqlserver')

    conn = db.conexao_azure()
    cursor = conn.cursor()

    # BUSCAR UMA LISTA DE PAISES PARA CONSULTA
    list_country = cursor.execute(f"SELECT NM_COUNTRY_SLUG, ID_COUNTRY FROM COUNTRY")

    conn2 = db.conexao_azure()
    cursor2 = conn2.cursor()

    conn3 = db.conexao_azure()
    cursor3 = conn3.cursor()

    data_atual = datetime.date.today()

    for next_country in list_country:
        print(next_country[1])

        # BUSCA A ÚLTIMA DATA DOS CASOS INSERIDOS PARA UM PAIS ESPECÍFICO
        max_data = cursor2.execute(f"SELECT MAX(DT_CASE), COUNT(*) FROM CASE_COUNTRY WHERE ID_COUNTRY = {next_country[1]}")

        for list_date in max_data:

            if list_date[1] != 0:
                last_date = list_date[0]
                if not isinstance(last_date, datetime.date):
                    n_last_date = datetime.datetime.strptime(last_date, '%Y-%m-%d').date()
                else:
                    n_last_date = last_date
                add_last_date = n_last_date + datetime.timedelta(days=1)
                if add_last_date < data_atual:
                    object = api_covid(f'https://api.covid19api.com/total/country/{next_country[0]}?from={add_last_date}T00:00:00Z&to={add_last_date}T23:59:59Z')
                    response = object.get_connection(False)

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