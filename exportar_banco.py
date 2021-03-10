import pyodbc
import requests
import json
import datetime

def request_confirmed():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=LOCALHOST\\SQLEXPRESS;'
                        'Database=BD_COVID_GAMMA;'
                        'UID=sa;'
                        'PWD=sa;')

    cursor = conn.cursor()

    data = cursor.execute("""
        SELECT TOP 1 DT_CASE FROM CASE_COUNTRY
        ORDER BY DT_CASE DESC
    """)

    data_inicial = datetime.datetime(2020, 1, 1)

    data_maxima = data.fetchall()

    data_formatada = datetime.datetime.strptime(data_maxima[0][0], "%Y-%m-%d")

    data_diferenca = data_formatada - data_inicial

    lista_resultados = {}

    start_date = datetime.datetime(2020, 1, 1)

    for data in (start_date + datetime.timedelta(n) for n in range(data_diferenca.days + 1)):
        lista_pais = []
        teste = cursor.execute("""
            SELECT TOP 10 C.NM_COUNTRY, CC.CONFIRMED
            FROM CASE_COUNTRY CC
            INNER JOIN COUNTRY C ON C.ID_COUNTRY = CC.ID_COUNTRY
            WHERE DT_CASE = ?
            ORDER BY CONFIRMED DESC
        """, data).fetchall()
        for row in teste:
            nova_lista = {}
            nova_lista["Pais"] = row[0]
            nova_lista["Confirmados"] = row[1]
            lista_pais.append(nova_lista)
        
        lista_resultados[str(data)] = lista_pais

        hoje = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        arquivo = (f"./export/confirmed/confirmed_results_{hoje}.json")

    with open(arquivo, 'w') as outfile:
        json.dump(lista_resultados, outfile)


def request_deaths():
    conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=LOCALHOST\\SQLEXPRESS;'
                        'Database=BD_COVID_GAMMA;'
                        'UID=sa;'
                        'PWD=sa;')

    cursor = conn.cursor()

    data = cursor.execute("""
        SELECT TOP 1 DT_CASE FROM CASE_COUNTRY
        ORDER BY DT_CASE DESC
    """)

    data_inicial = datetime.datetime(2020, 1, 1)

    data_maxima = data.fetchall()

    data_formatada = datetime.datetime.strptime(data_maxima[0][0], "%Y-%m-%d")

    data_diferenca = data_formatada - data_inicial

    lista_resultados = {}

    start_date = datetime.datetime(2020, 1, 1)

    for data in (start_date + datetime.timedelta(n) for n in range(data_diferenca.days + 1)):
        lista_pais = []
        teste = cursor.execute("""
            SELECT TOP 10 C.NM_COUNTRY, CC.DEATHS
            FROM CASE_COUNTRY CC
            INNER JOIN COUNTRY C ON C.ID_COUNTRY = CC.ID_COUNTRY
            WHERE DT_CASE = ?
            ORDER BY DEATHS DESC
        """, data).fetchall()
        for row in teste:
            nova_lista = {}
            nova_lista["Pais"] = row[0]
            nova_lista["Mortes"] = row[1]
            lista_pais.append(nova_lista)
        
        lista_resultados[str(data)] = lista_pais

        hoje = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        arquivo = (f"./export/deaths/death_results_{hoje}.json")

    with open(arquivo, 'w') as outfile:
        json.dump(lista_resultados, outfile)


request_confirmed()

request_deaths()