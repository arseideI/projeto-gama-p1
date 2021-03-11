import requests
from requests import ReadTimeout, HTTPError, Timeout, ConnectionError

class api_covid:

    def __init__(self, url):
        self.url = url

    #@staticmethod
    def get_connection(self, verbose=True):
        try:
            url_request = requests.get(self.url)
            if url_request.raise_for_status() is None:
                if verbose:
                    print('Conexão Estabelecida')
                return url_request.json()

        except requests.ConnectionError:
            print("OOPS!! Erro de Conexão. Tenha a certeza que está conectado a internet.\n")

        except requests.Timeout:
            print("OOPS!! Erro no Tempo de Conexão\n")

        except requests.RequestException:
            print("OOPS!! Erro Geral\n")

        except KeyboardInterrupt:
            print("O programa foi fechado\n")