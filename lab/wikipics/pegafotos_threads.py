from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx


BASE_URL = 'https://upload.wikimedia.org/wikipedia/commons/'
LISTA_FOTOS = 'potd_10MB.txt'
# LISTA_FOTOS = 'potd_100KB.txt'
LOCAL = 'img/'

dragão = '7/79/Phyllopteryx_taeniolatus1.jpg'


def pega_foto(caminho):
    resp = httpx.get(BASE_URL + caminho)
    octetos = resp.content
    nome_arq = caminho.split('/')[-1]
    with open(LOCAL + nome_arq, 'wb') as fp:
        fp.write(octetos)
    return nome_arq


def pega_fotos():
    caminhos = []
    for linha in open(LISTA_FOTOS):
        tamanho, caminho = linha.split('\t')
        caminhos.append(caminho.strip())

    with ThreadPoolExecutor() as fazedor:
        promessas = []
        for caminho in caminhos:
            promessas.append(fazedor.submit(pega_foto, caminho))
        for p in as_completed(promessas):
            try:
                nome_arq = p.result()
            except OSError:
                print('*** ERRO!!!')
            else:
                print(nome_arq)

if __name__ == '__main__':
    pega_fotos()
