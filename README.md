# projeto-gama-p1
Projeto Gama Accenture


Armazenamento de dados d COVID-19 de todos os países do mundo através da API: https://documenter.getpostman.com/view/10808728/SzS8rjbc.
1) Crie um Script SQL para criação de um DataBase com um Schema para armazenar os registros de países e os dados de COVID-19 por todo o mundo. Na tabela que será armazenada os dados de países, 2 campos são obrigatórios de serem consistidos:
Nome do país
Código ISO2
Em outros repositórios devem ser armazenados a quantidade de casos confirmados e mortes de cada um dos países do mundo, desde o dia 01/01/2020.
2) Crie um banco de dados relacional no provedor de nuvem Azure para armazenamento dos dados em questão, estabelecidos pelo script com o dito schema, criado na etapa anterior. O banco de dados pode ser SQL Server, MySQL, MariaDB, Postgres ou algum outro SQL.
3) Desenvolva um script Python que faça leitura da API determinada no enunciado inicial desta atividade para realizar o armazenamento de países e dos casos confirmados e de mortes da COVID-19. O armazenamento destas informações deverá ser em BD SQL, consistido no Azure através do schema definido na etapa 1 desta atividade.
Após armazenamento dos valores no BD, este dito script Python deverá retornar as seguintes informações em tela, caso o usuário escolha:
1) Panorama diário de quantidade de casos confirmados de COVID-19 dos 10 países do mundo com maiores números.
2) Panorama diário de quantidade de mortes de COVID-19 dos 10 países do mundo com números.
3) Total de mortes por COVID-19 dos 10 países do mundo com maiores números.
4) Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números.
A impressão das 4 informações citadas acima deverá acontecer em tela, através do prompt de comando de execução do programa.