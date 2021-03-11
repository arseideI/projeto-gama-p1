import requests
from conexao_db import ConexaoBD
from datetime import datetime
import pyodbc
import pandas as pd
pd.set_option('display.max_columns', 6)

"""
localhost
login = SA
password = sqlGama123
"""

def option_from_user_page():
    print('\n(1) ANTERIOR \t (2) PRÓXIMA \t (3) PESQUISAR POR DATA \t (0) VOLTAR')

    option = -1
    while option < 0 or option > 3:
        try:
            option = int(input("\nOPÇÃO: "))

        except ValueError:
            print("ENTRADA INVÁLIDA".center(80))
            continue

        if option < 0 or option > 3:
            print("OPÇÃO INVÁLIDA".center(80))

    return option

def show_cases(csr, msg, cases, page, diff):
    print(msg)
    conf_cases = get_cases(csr, cases, page=page, diff=diff)
    print(conf_cases)

def submenu_page(csr, msg, cases, diff):
    option_1 = 4
    page = 0

    show_cases(csr, msg, cases, page, diff)

    csr.execute("SELECT MAX(DT_CASE), MIN(DT_CASE) FROM CASE_COUNTRY")
    last_day, first_day = csr.fetchall()[0]
    total_days = (last_day - first_day).days

    while option_1 >= 0 and option_1 <= 4:

        if option_1 == 0:
            break

        if option_1 == 1:  # ANTERIOR
            if page == 0:
                print("\n" + "PRIMEIRA PÁGINA ATINGIDA!".center(80) + "\n")
                show_cases(csr, msg, cases, page, diff)
                option_1 = 4
                continue
            page += -1

            show_cases(csr, msg, cases, page, diff)
            option_1 = 4

        if option_1 == 2:  # PRÓXIMO
            if page >= total_days:
                print("\n" + "ÚLTIMA PÁGINA ATINGIDA!".center(80) + "\n")
                show_cases(csr, msg, cases, page, diff)
                option_1 = 4
                continue
            page += 1

            show_cases(csr, msg, cases, page, diff)
            option_1 = 4

        if option_1 == 3:
            specific_date = datetime.strptime(input("DIGITE A DATA DESEJADA (A PARTIR DO DIA 2020-01-22): "), '%Y-%m-%d').date()
            _page = (last_day - specific_date).days
            if total_days < _page or _page < 0:
                print("\n" + "DATA INVÁLIDA!".center(80) + "\n")
                show_cases(csr, msg, cases, page, diff)
                option_1 = 4
                continue

            page = _page
            show_cases(csr, msg, cases, page, diff)
            option_1 = 4

        if option_1 == 4:
            option_1 = option_from_user_page()


def option_from_user():
    print('\n' + '-- Balanço de casos e mortes por COVID-19 dos 10 países com maiores números --'.center(80) + '\n'
          '1 - Relatório de novos casos confirmados dos 10 países com maiores números\n'
          '2 - Relatório de novas mortes dos 10 países com maiores números\n'
          "3 - Relatório do total de mortes dos 10 países com maiores números\n"
          "4 - Relatório do total de casos confirmados dos 10 países com maiores números\n"
          "5 - Fechar o programa")

    option = 0
    while option < 1 or option > 5:
        try:
            option = int(input("DIGITE A OPÇÃO DESEJADA: "))
        except ValueError:
            print("ENTRADA INVÁLIDA!".center(80))
            option = 0
            continue
        if option < 1 or option > 5:
            print("OPÇÃO INVÁLIDA. DIGITE UMA OPÇÃO VÁLIDA DE ACORDO COM O MENU ACIMA!".center(80))

    return option


def get_cases_by_day(days, cases, csr):
    daily_list = []

    for day in days:
        csr.execute(f"""
                    SELECT COUNTRY.NM_COUNTRY, {cases}, CC.DT_CASE
                    FROM COUNTRY INNER JOIN CASE_COUNTRY CC
                    ON COUNTRY.ID_COUNTRY = CC.ID_COUNTRY
                    WHERE CC.DT_CASE = {day}
                    ORDER BY CONFIRMED DESC
                    """)

        country_list = []

        for row in csr.fetchall():
            dict_info = {}
            dict_info["country"] = row[0]
            dict_info[f"{cases}"] = row[1]
            dict_info["dt_case"] = row[2]
            country_list.append(dict_info)

        daily_list.append(country_list)

    return daily_list

def get_cases(csr, cases, k_top_countries=10, n_elements=3, page=0, diff=False):
    if diff:
        n_elements += 1

    page -= n_elements

    csr.execute(f"""
                    SELECT COUNTRY.NM_COUNTRY, {cases}, CC.DT_CASE
                    FROM COUNTRY INNER JOIN CASE_COUNTRY CC
                    ON COUNTRY.ID_COUNTRY = CC.ID_COUNTRY
                    WHERE CC.DT_CASE IN
                        (SELECT DISTINCT DT_CASE
                        FROM CASE_COUNTRY
                        ORDER BY DT_CASE DESC
                        OFFSET {page + n_elements} ROWS
                        FETCH NEXT {n_elements} ROWS ONLY)
                    ORDER BY CC.DT_CASE DESC, {cases} DESC
                    """)

    df = pd.DataFrame().from_records(csr.fetchall())
    covid_cases = df.pivot_table(values=1, index=[0], columns=[2])
    covid_cases = covid_cases[covid_cases.columns[::-1]]
    covid_cases = covid_cases.sort_values(by=[covid_cases.columns[0]], ascending=False)
    covid_cases.index.name = 'PAÍSES'
    covid_cases.columns.name = 'DATA'

    if diff:
        covid_cases = (covid_cases.T - covid_cases.T.shift(-1)).T.sort_values(by=[covid_cases.columns[0]],
                                                                              ascending=False)
        n_elements -= 1

    return covid_cases.iloc[:k_top_countries, :n_elements].applymap(lambda x: int(x) if pd.isna(x) == False else 'SEM REGISTRO')


#'Server=casadocodigo-sql-srv-isr.database.windows.net;'
#'Database=BD_COVID_GAMMA;'
#'UID=Administrador;'
#'PWD=Alura!123;'


if __name__ == '__main__':

    # driver = "{SQL Server}"
    # server = "localhost"
    server = 'casadocodigo-sql-srv-isr.database.windows.net'
    driver = "Driver={ODBC Driver 17 for SQL Server}"
    bd = "BD_COVID_GAMMA"

    print('---- Login no banco de dados ----'.center(80))
    login = input("LOGIN: ")
    psswd = input("SENHA: ")

    conn = ConexaoBD(server,
                     bd,
                     login,
                     psswd,
                     'sqlserver',
                     driver=driver).conexao_azure()

    csr = conn.cursor()

    option = 0
    while option >= 0 and option <= 5:

        if option == 0: # Voltar ao menu principal
            option = option_from_user()

        if option == 1:  # Relatório de casos confirmados dos 10 países com maiores números
            submenu_page(
                csr,
                '-- Relatório de novos casos confirmados dos 10 países com maiores números --',
                'CC.CONFIRMED',
                True
                )
            option = 0
            continue

        if option == 2:  # Relatório de mortes dos 10 países com maiores números
            submenu_page(
                csr,
                '-- Relatório de novas mortes dos 10 países com maiores números --',
                'CC.DEATHS',
                True
            )
            option = 0
            continue

        if option == 3: # Total de mortes por COVID-19 dos 10 países do mundo com maiores números
            submenu_page(
                csr,
                '-- Relatório do total de mortes dos 10 países com maiores números --',
                'CC.DEATHS',
                False
            )
            option = 0
            continue

        if option == 4: # Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números
            submenu_page(
                csr,
                '-- Relatório do total de casos confirmados dos 10 países com maiores números --',
                'CC.CONFIRMED',
                False
            )
            option = 0


        if option == 5:
            conn.close_azure()
            print("PROGRAMA FINALIZADO!".center(80))
            break
