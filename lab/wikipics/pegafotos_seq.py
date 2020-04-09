import httpx

BASE_URL = 'https://upload.wikimedia.org/wikipedia/commons/'
LISTA_FOTOS = 'potd_100KB.txt'

dragão = '7/79/Phyllopteryx_taeniolatus1.jpg'


def pega_foto(caminho):
    resp = httpx.get(BASE_URL + caminho)
    octetos = resp.content
    print(len(octetos), 'baixados')
    nome_arq = caminho.split('/')[-1]
    print('salvando', nome_arq)
    with open(nome_arq, 'wb') as fp:
        fp.write(octetos)


def pega_fotos():
    for linha in open(LISTA_FOTOS):
        tamanho, caminho = linha.split('\t')
        caminho = caminho.strip()
        pega_foto(caminho)


if __name__ == '__main__':
    pega_fotos()
