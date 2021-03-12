# Projeto Gama (Parte 1)
Projeto Gama Accenture

<details>
<summary>Desafio</summary>
Armazenamento de dados de COVID-19 de todos os países do mundo através da API: https://documenter.getpostman.com/view/10808728/SzS8rjbc.
<br>
1) Crie um Script SQL para criação de um DataBase com um Schema para armazenar os registros de países e os dados de COVID-19 por todo o mundo. Na tabela que será armazenada os dados de países, 2 campos são obrigatórios de serem consistidos:
Nome do país
Código ISO2
<br>
Em outros repositórios devem ser armazenados a quantidade de casos confirmados e mortes de cada um dos países do mundo, desde o dia 01/01/2020.
<br>
2) Crie um banco de dados relacional no provedor de nuvem Azure para armazenamento dos dados em questão, estabelecidos pelo script com o dito schema, criado na etapa anterior. O banco de dados pode ser SQL Server, MySQL, MariaDB, Postgres ou algum outro SQL.
<br>
3) Desenvolva um script Python que faça leitura da API determinada no enunciado inicial desta atividade para realizar o armazenamento de países e dos casos confirmados e de mortes da COVID-19. O armazenamento destas informações deverá ser em BD SQL, consistido no Azure através do schema definido na etapa 1 desta atividade.
<br>
Após armazenamento dos valores no BD, este dito script Python deverá retornar as seguintes informações em tela, caso o usuário escolha:
<br>
1) Panorama diário de quantidade de casos confirmados de COVID-19 dos 10 países do mundo com maiores números.
<br>
2) Panorama diário de quantidade de mortes de COVID-19 dos 10 países do mundo com números.
<br>
3) Total de mortes por COVID-19 dos 10 países do mundo com maiores números.
<br>
4) Total de casos confirmados por COVID-19 dos 10 países do mundo com maiores números.
<br>
A impressão das 4 informações citadas acima deverá acontecer em tela, através do prompt de comando de execução do programa.
</details>

<details>
  <summary> Configurando a aplicação </summary>
  Primeiramente, é necessário rodar o comando abaixo para a aplicação baixar todas as suas dependências.
  <br>
  <code>pip install -r requirements.txt</code>
  <br>
  Após esse comando, a aplicação poderá ser iniciada normalmente.
  <br>
  Ao iniciar a aplicação, a opção de LOGIN e SENHA será apresentada ao usuário:
</details>

<details>
  <summary> Utilizando a aplicação </summary>
  Ao logar no sistema, são apresentadas algumas opções para verificar os dados. O usuário consegue escolher uma dessas opções (de 1 a 6) ou então a opção 7 para sair do programa.


</details>

<details>
  <summary> Equipe </summary>
  Product Owner/Liderança:
  <br>
  -- Responsáveis pela coordenação da equipe como um todo; apoio para integração de todo o projeto e familiarização com as ferramentas.
  <br>
  ==> Alexandre Seidel
  <br>
  <br>
  Desenvolvimento SQL Server/Azure:
  <br>
  -- Responsáveis pela criação do Banco de Dados, assim como queries e rotinas diárias para requisições de novos dados automaticamente.
  <br>
  ==> Israel de Souza
  <br>
  ==> Beatriz Machado
  <br>
  ==> Tulio Caviquioli
  <br>
  <br>
  Desenvolvimento Python:
  <br>
  -- Responsáveis pelo desenvolvimento da aplicação, assim como menus, requisições e apresentação de dados ao usuário final.
  <br>
  ==> Luís Souza
  <br>
  ==> Sidicley Ribeiro
  <br>
  ==> João Araújo
  <br>
  ==> Raphael Ote
  <br>
  ==> Igor Otacilio
</details>
