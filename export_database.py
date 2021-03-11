import pyodbc
import requests
import json
import datetime

class ExportDatabase():

    def __init__(self, cursor):
        self.cursor = cursor

    def request_confirmed(self):
        # conn = pyodbc.connect('Driver={SQL Server};'
        #                     'Server=LOCALHOST\\SQLEXPRESS;'
        #                     'Database=BD_COVID_GAMMA;'
        #                     'UID=sa;'
        #                     'PWD=sa;')

        date = self.cursor.execute("""
            SELECT TOP 1 DT_CASE FROM CASE_COUNTRY
            ORDER BY DT_CASE DESC
        """)

        initial_date = datetime.date(2020, 1, 1) # datetime.datetime(2020, 1, 1)

        max_date = date.fetchall()

        formated_date = max_date[0][0] # datetime.datetime.strptime(max_date[0][0], "%Y-%m-%d")

        date_diff = formated_date - initial_date

        result_list = {}

        start_date = datetime.datetime(2020, 1, 1)

        for date in (start_date + datetime.timedelta(n) for n in range(date_diff.days + 1)):
            country_list = []
            test = self.cursor.execute("""
                SELECT TOP 10 C.NM_COUNTRY, CC.CONFIRMED
                FROM CASE_COUNTRY CC
                INNER JOIN COUNTRY C ON C.ID_COUNTRY = CC.ID_COUNTRY
                WHERE DT_CASE = ?
                ORDER BY CONFIRMED DESC
            """, date).fetchall()

            # print(f"Registros de casos confirmados do dia {date} carregados!")
            for row in test:
                new_list = {}
                new_list["Countries"] = row[0]
                new_list["Confirmed"] = row[1]
                country_list.append(new_list)

            result_list[str(date)] = country_list

        today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        file_path = (f"./export/confirmed/confirmed_results_{today}.json")

        with open(file_path, 'w') as outfile:
            json.dump(result_list, outfile)

        print(f"ARQUIVO confirmed_results_{today}.json EXPORTADO!")


    def request_deaths(self):
        # conn = pyodbc.connect('Driver={SQL Server};'
        #                     'Server=LOCALHOST\\SQLEXPRESS;'
        #                     'Database=BD_COVID_GAMMA;'
        #                     'UID=sa;'
        #                     'PWD=sa;')

        # cursor = conn.cursor()

        date = self.cursor.execute("""
            SELECT TOP 1 DT_CASE FROM CASE_COUNTRY
            ORDER BY DT_CASE DESC
        """)

        initial_date = datetime.date(2020, 1, 1) # datetime.datetime(2020, 1, 1)

        max_date = date.fetchall()

        formated_date = max_date[0][0] # datetime.datetime.strptime(max_date[0][0], "%Y-%m-%d")

        date_diff = formated_date - initial_date

        result_list = {}

        start_date = datetime.datetime(2020, 1, 1)

        for date in (start_date + datetime.timedelta(n) for n in range(date_diff.days + 1)):
            country_list = []
            test = self.cursor.execute("""
                SELECT TOP 10 C.NM_COUNTRY, CC.DEATHS
                FROM CASE_COUNTRY CC
                INNER JOIN COUNTRY C ON C.ID_COUNTRY = CC.ID_COUNTRY
                WHERE DT_CASE = ?
                ORDER BY DEATHS DESC
            """, date).fetchall()
            # print(f"Registros de mortes no dia {date} carregados!")
            for row in test:
                new_list = {}
                new_list["Countries"] = row[0]
                new_list["Deaths"] = row[1]
                country_list.append(new_list)

            result_list[str(date)] = country_list

        today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

        file = (f"./export/deaths/death_results_{today}.json")


        with open(file, 'w') as outfile:
            json.dump(result_list, outfile)

        print(f"ARQUIVO death_results_{today}.json EXPORTADO!")

    # request_confirmed()
    #
    # request_deaths()