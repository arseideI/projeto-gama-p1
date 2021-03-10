import pyodbc
import requests

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=arseideltest.database.windows.net;'
#                       'Database=AT1_SQL_ARS;'
#                       'UID=arseidel;'
#                       'PWD=Seidelsenha123;')

# cursor = conn.cursor()

# countries = requests.get("https://api.covid19api.com/countries").json()
#
# for country in countries:
#     nome = country["Country"]
#     slug = country["Slug"]
#     iso = country["ISO2"]
#     print("Country: " + nome + " Slug: " + slug + " ISO2: " + iso)
#
# print("Todos os países buscados com sucesso!")

# from conexao_bd import ConexaoBD
import datetime
import pyodbc
import pandas as pd
pd.set_option('display.max_columns', 6)

"""
login = SA
password = sqlGama123
"""

def option_from_user_page():
    print('\n(1) ANTERIOR \t (2) PRÓXIMA \t\t\t (0) VOLTAR')

    option = -1
    while option < 0 or option > 2:
        try:
            option = int(input("\nOPÇÃO: "))

        except ValueError:
            print("Entrada inválida!")
            continue

        if option < 0 or option > 2:
            print("Opção inválida. Digite uma opção válida de acordo com o menu acima!")

    return option


def option_from_user():
    print('\n-- Balanço de casos e mortes por COVID-19 dos 10 países com maiores números --\n'
          '1 - Relatório de novos casos confirmados dos 10 países com maiores números\n'
          '2 - Relatório de novas mortes dos 10 países com maiores números\n'
          "3 - Relatório do total de mortes dos 10 países com maiores números\n"
          "4 - Relatório do total de casos confirmados dos 10 países com maiores números\n"
          "5 - Fechar o programa")

    option = 0
    while option < 1 or option > 5:
        try:
            option = int(input("Digite a opção desejada: "))
        except ValueError:
            print("Entrada inválida!")
            option = 0
            continue
        if option < 1 or option > 5:
            print("Opção inválida. Digite uma opção válida de acordo com o menu acima!")

    return option

def ConexaoBD(driver, server, bd, login, psswd):
    conn = pyodbc.connect(f"{driver}"
                          f"{server}"
                          f"{bd}"
                          f"UID={login};"
                          f"PWD={psswd};")
    print('-- Conexao estabelecida com banco de dados --')
    return conn


def commit_close(conn):
    conn.commit()
    conn.close()


def get_cases_by_day(days, cases, csr):
    daily_list = []

    for day in days:
        # print('TESTE: ', day)
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

def get_cases(cases, k_top_countries=10, n_elements=3, page=0, diff=False ):
    # n_elements = 5
    # page = 0
    # k_top_countries = 10
    # diff = True
    # cases = 'CC.CONFIRMED'
    corr = 0
    if page != 0:
        corr = page

    if diff:
        n_elements += 1

    csr.execute(f"""
                    SELECT COUNTRY.NM_COUNTRY, {cases}, CC.DT_CASE
                    FROM COUNTRY INNER JOIN CASE_COUNTRY CC
                    ON COUNTRY.ID_COUNTRY = CC.ID_COUNTRY
                    WHERE CC.DT_CASE IN
                        (SELECT DISTINCT DT_CASE
                        FROM CASE_COUNTRY
                        ORDER BY DT_CASE DESC
                        OFFSET {page * n_elements - corr} ROWS
                        FETCH NEXT {n_elements} ROWS ONLY)
                    ORDER BY CC.DT_CASE DESC, {cases} DESC
                    """)

    df = pd.DataFrame().from_records(csr.fetchall())
    covid_cases = df.pivot_table(values=1, index=[0], columns=[2])
    covid_cases = covid_cases[covid_cases.columns[::-1]]
    covid_cases = covid_cases.sort_values(by=[covid_cases.columns[0]], ascending=False)
    covid_cases.index.name = 'COUNTRIES'
    covid_cases.columns.name = 'DATE'

    if diff:
        covid_cases = (covid_cases.T - covid_cases.T.shift(-1)).T.sort_values(by=[covid_cases.columns[0]],
                                                                              ascending=False)
        n_elements -= 1

    return covid_cases.iloc[:k_top_countries, :n_elements].applymap(lambda x: int(x))


if __name__ == '__main__':

    # driver = "{SQL Server}"
    driver = "Driver={ODBC Driver 17 for SQL Server};"
    server = "Server=localhost;"
    bd = "Database=BD_COVID_GAMMA;"

    print('---- Login no banco de dados ----')
    login = input("Insira o login para o banco de dados: \n")
    psswd = input("Insira a senha para o banco de dados: \n")

    connection = -1
    # while connection == -1:
    #     try:
    #         conn = ConexaoBD(driver, server, bd, login, psswd)
    #         connection = 1
    #     except pyodbc.InterfaceError:
    #         print("Login ou senha incorretos, tente novamente.")
    #         break

    conn = ConexaoBD(driver, server, bd, login, psswd)
    csr = conn.cursor()

    # print('Login precisa ser feito antes de acessar o banco de dados!\n')
    option = 0
    while option >= 0 and option <= 5:

        if option == 0: # Voltar ao menu principal
            option = option_from_user()

        if option == 1:  # Relatório de casos confirmados dos 10 países com maiores números
            print('-- Relatório de novos casos confirmados dos 10 países com maiores números --')
            conf_cases = get_cases("CC.CONFIRMED", diff=True)
            print(conf_cases)
            option_1 = 3
            page = 0
            while option_1 >= 0 and option_1 <= 3:

                if option_1 == 0:
                    break

                if option_1 == 1: # ANTERIOR
                    page += -1
                    if page < 0:
                        print("Última página atingida! ")
                        option_1 = 3

                    print('-- Relatório de novos casos confirmados dos 10 países com maiores números --')
                    conf_cases = get_cases("CC.CONFIRMED", page=page, diff=True)
                    print(conf_cases)
                    option_1 = 3

                if option_1 == 2: # PRÓXIMO
                    page += 1

                    print('-- Relatório de novos casos confirmados dos 10 países com maiores números --')
                    conf_cases = get_cases("CC.CONFIRMED", page=page, diff=True)
                    print(conf_cases)
                    option_1 = 3

                if option_1 == 3:
                    option_1 = option_from_user_page()

            option = 0
            continue

        if option == 2:  # Relatório de mortes dos 10 países com maiores números
            print('-- Relatório de novas mortes dos 10 países com maiores números --')
            conf_deaths = get_cases("CC.DEATHS", diff=True)
            print(conf_deaths)
            option_2 = 3
            page = 0
            while option_2 >= 0 and option_2 <= 3:

                if option_2 == 0:
                    break

                if option_2 == 1:  # ANTERIOR
                    page += -1
                    if page < 0:
                        print("Última página atingida! ")
                        option_2 = 3

                    print('-- Relatório de novas mortes dos 10 países com maiores números --')
                    conf_deaths = get_cases("CC.DEATHS", page=page, diff=True)
                    print(conf_deaths)
                    option_2 = 3

                if option_2 == 2:  # PRÓXIMO
                    page += 1

                    print('-- Relatório de novas mortes dos 10 países com maiores números --')
                    conf_deaths = get_cases("CC.DEATHS", page=page, diff=True)
                    print(conf_deaths)
                    option_2 = 3

                if option_2 == 3:
                    option_2 = option_from_user_page()

            option = 0
            continue

        if option == 3: # Total de mortes por COVID-19 dos 10 países do mundo com maiores números
            print('-- Relatório do total de mortes dos 10 países com maiores números --')
            total_deaths = get_cases("CC.DEATHS")
            print(total_deaths)

            option_3 = 3
            page = 0
            while option_3 >= 0 and option_3 <= 3:

                if option_3 == 0:
                    break

                if option_3 == 1:  # ANTERIOR
                    page += -1
                    if page < 0:
                        print("Última página atingida! ")
                        option_3 = 3

                    print('-- Relatório do total de mortes dos 10 países com maiores números --')
                    total_deaths = get_cases("CC.DEATHS", page=page)
                    print(total_deaths)
                    option_3 = 3

                if option_3 == 2:  # PRÓXIMO
                    page += 1

                    print('-- Relatório do total de mortes dos 10 países com maiores números --')
                    total_deaths = get_cases("CC.DEATHS", page=page)
                    print(total_deaths)
                    option_3 = 3

                if option_3 == 3:
                    option_3 = option_from_user_page()

            option = 0
            continue

        if option == 4: # Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números
            print('-- Relatório do total de casos confirmados dos 10 países com maiores números --')
            total_cases = get_cases("CC.CONFIRMED")
            print(total_cases)

            option_4 = 3
            page = 0
            while option_4 >= 0 and option_4 <= 3:

                if option_4 == 0:
                    break

                if option_4 == 1:  # ANTERIOR
                    page += -1
                    if page < 0:
                        print("Última página atingida! ")
                        option_4 = 3

                    print('-- Relatório do total de casos confirmados dos 10 países com maiores números --')
                    total_cases = get_cases("CC.CONFIRMED", page=page)
                    print(total_cases)
                    option_4 = 3

                if option_4 == 2:  # PRÓXIMO
                    page += 1

                    print('-- Relatório do total de casos confirmados dos 10 países com maiores números --')
                    total_cases = get_cases("CC.CONFIRMED", page=page)
                    print(total_cases)
                    option_4 = 3

                if option_4 == 3:
                    option_4 = option_from_user_page()


            option = 0
            continue

        if option == 5:
            csr.close_Azure()
            print("Programa finalizado!")
            break




# Extra

        # if option == 1:  # Relatório de casos confirmados dos 10 países com maiores números
        #     today = datetime.date.today()
        #     current_day = '\'' + str(today) + '\''
        #     daily_list_cd = get_cases_by_day([current_day], "CC.CONFIRMED", csr)
        #     count = 1
        #     while len(daily_list_cd[0]) == 0:
        #         current_day = '\'' + str(today - datetime.timedelta(count)) + '\''
        #         daily_list_cd = get_cases_by_day([current_day], "CC.CONFIRMED", csr)
        #         if len(daily_list_cd[0]) != 0:
        #             print(f"Mostrando resultados do dia {current_day}. Resultados indisponíveis para o dia {str(today)}. ")
        #             break
        #         count += 1
        #
        #     day_before = '\'' + str(today - datetime.timedelta(count+1)) + '\''
        #     daily_list_db = get_cases_by_day([day_before], "CC.CONFIRMED", csr)
        #
        #     # print(daily_list_cd[0][0])
        #     # print(daily_list_db[0][0])
        #     print("TOTAL PAISES", len(daily_list_db[0]))
        #     for count_cd, count_db in zip(daily_list_cd[0], daily_list_db[0]):
        #         print(daily_list_cd[0][0]['CC.CONFIRMED'])
        #         daily_list_cd[0][0]['CC.CONFIRMED'] = count_cd['CC.CONFIRMED'] - count_db['CC.CONFIRMED']