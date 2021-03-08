'''
CLASSE PARA TRATAMENTO DE CHAMADAS DAS API POSTMAN COM AS INFORMAÇÕES DO COVID
INTERESSANTE TRATAMENTO DE EXCESSÃO PARA CASO ESTEJA INDISPONÍVEL

'''
# EXEMPLO
def requisicao_api():
    resposta = requests.get('https://servicodados.ibge.gov.br/api/v1/localidades/distritos')
    if resposta.status_code == 200:
        return resposta.json()
    else:
        return resposta.status_code
