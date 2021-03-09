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
"""
login = SA
password = sqlGama123
"""

def option_from_user():
    print('\n-- Informações sobre o total de mortes por COVID-19 dos 10 países com maiores números --\n'
          '1 - Relatório de hoje da quantidade de casos confirmados dos 10 países do mundo com maiores números\n'
          '2 - Panorama diário de quantidade de mortes de COVID-19 dos 10 países do mundo com maiores números\n'
          "3 - Total de mortes por COVID-19 dos 10 países do mundo com maiores números\n"
          "4 - Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números\n"
          "5 - Fechar o programa"
          )
    option = 0
    while option < 1 or option > 4:
        try:
            option = int(input("Digite a opção desejada!"))
        except ValueError:
            print("Entrada inválida!")
            option = 0
            continue
        if option < 1 or option > 4:
            print("Opção inválida. Digite uma opção válida de acordo com o menu acima!")

    return option


def ConexaoBD(driver, server, bd, login, psswd):
    conn = pyodbc.connect(f"{driver}"
                          f"{server}"
                          f"{bd}"
                          f"UID={login};"
                          f"PWD={psswd};")
    print('-- Conexao estabelecida com banco de dados --')
    csr = conn.cursor()
    return csr, conn


def commit_close(conn):
    conn.commit()
    conn.close()


if __name__ == '__main__':

    option = option_from_user()
    # driver = "{SQL Server}"
    driver = "Driver={ODBC Driver 17 for SQL Server};"
    server = "Server=localhost;"
    bd = "Database=BD_COVID_GAMMA;"

    while option >= 0 and option <= 5:

        if option == 0:
            option = option_from_user()

        if option == 1:  # Relatório de casos confirmados dos 10 países  com maiores números
            login = input("Insira o login para o banco de dados: \n")
            psswd = input("Insira a senha para o banco de dados: \n")
            csr, conn = ConexaoBD(driver, server, bd, login, psswd)
            today = str(datetime.date.today())
            csr.execute("""
                        SELECT TOP 10 COUNTRY.NM_COUNTRY, CC.CONFIRMED, CC.DEATHS, CC.RECOVERED, CC.ACTIVE, CC.DT_CASE
                        FROM COUNTRY INNER JOIN CASE_COUNTRY CC
                        ON COUNTRY.ID_COUNTRY = CC.ID_COUNTRY
                        WHERE DT_CASE = '2021-03-08'
                        ORDER BY CONFIRMED DESC
                        """)
            country_list = []

            for row in csr.fetchall():
                dict_info = {}
                dict_info["country"] = row[0]
                # print(row[0])
                dict_info["confirmed"] = row[1]
                dict_info["deaths"] = row[2]
                dict_info["recovered"] = row[3]
                dict_info["active"] = row[4]
                dict_info["dt_case"] = row[5]
                country_list.append(dict_info)

            print(country_list)

            if option == 2:
                pass
            if option == 3:
                pass
            if option == 4:
                pass
            if option == 5:
                print("Programa finalizado!")
                break





