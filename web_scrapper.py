# O SelectorLib é uma ferramenta poderosa para extrair dados de websites em Python. Ele combina dois pacotes:
# Extensão Chrome SelectorLib: Permite que você marque dados em websites e exporte um arquivo YAML com eles.
# Biblioteca Python SelectorLib: Lê o arquivo YAML e extrai os dados do website usando XPath.

# Casos de uso do SelectorLib:
# Web scraping: Extrair dados de websites para análise, automação ou pesquisa.
# Monitoramento de websites: Rastrear mudanças em websites e notificar os usuários.
# Agregação de dados: Coletar dados de vários websites e consolidá-los num só lugar.
# Automação de tarefas: Automatizar tarefas repetitivas que envolvem websites.
import selectorlib
import requests
from send_email import send_emails
import time
from twilio.rest import Client
from os import getenv


def scrape(url: str) -> str:
    """Scrape the page source from the `url`"""
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    text: str = response.text
    return text


def extract(source: str) -> str:
    """Vai extrair uma específica data/value from a `source`"""
    # Tenho que criar o extract.yaml no meu directory, se não, não vai dar!!
    # E tenho que acrescentar código:
    # tours(pode ser qualquer nome):\n(mudo de linha) css: '#displaytimer'(posso ir ao site, inspecionar elemento, copy,
    # copy selector)
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value: str = extractor.extract(source)['tours']
    return value


def store(extracted: str) -> None:
    """Vai guardar os `extracted` num documento de texto"""
    with open('data.txt', 'a', encoding='utf-8') as file:
        file.write(extracted + '\n')


def read() -> list:
    with open('data.txt', encoding='utf-8') as file:
        data: list = file.readlines()
    return data


def main():
    print(scrape(URL))
    while True:
        extracted: str = extract(scrape(URL))
        if extracted != 'No upcoming tours':
            data: list = read()
            if extracted not in data:
                store(extracted)
                message: str = '''\
Subject: A new content

Hey, new event was found: {}
'''.format(extracted)
                send_emails(message)
                print('Email was sent!')
                client = Client(getenv('account_sid_twilio'), getenv('auth_token_twilio'))
                client.messages.create(from_=getenv('phone_number_twilio'), body=message, to=getenv('my_number'))
                print('SMS was sent!')
        time.sleep(2)


if __name__ == '__main__':
    URL: str = 'http://programmer100.pythonanywhere.com/tours/'
    # Neste caso, não era preciso acrescentar headers, pois dava na mesma, mas fica mais completo e versátil
    HEADERS: dict = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                      '39.0.2171.95 Safari/537.36'
    }
    main()
