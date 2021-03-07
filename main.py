import pyodbc
import requests

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=arseideltest.database.windows.net;'
#                       'Database=AT1_SQL_ARS;'
#                       'UID=arseidel;'
#                       'PWD=Seidelsenha123;')

# cursor = conn.cursor()

countries = requests.get("https://api.covid19api.com/countries").json()

for country in countries:
    nome = country["Country"]
    slug = country["Slug"]
    iso = country["ISO2"]
    print("Country: " + nome + " Slug: " + slug + " ISO2: " + iso)