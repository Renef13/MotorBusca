from lxml import etree as et
import re
from fuzzywuzzy import fuzz


def abrirXML():
    arquivo = et.parse('verbetesWikipedia.xml')
    raiz = arquivo.getroot()
    paginas = raiz.xpath('//page')
    return paginas


def buscaPalavraInteira(termo, texto):
    # busca a palavra inteira ignorando especias
    palavra = r'\b' + re.escape(termo) + r'\b'
    return bool(re.search(palavra, texto, re.IGNORECASE))


def buscaPartePalavra(termo, texto):
    # busca palavras 80% similares
    SIMILARIDADE = 80
    if fuzz.ratio(termo, texto) > SIMILARIDADE:
        return True


def buscarTermo(termo_buscado):
    termo_buscado = termo_buscado.lower()
    paginas = abrirXML()
    artigos_encontrados = {}

    for pagina in paginas:
        pagina_titulo = pagina.find('title').text
        pagina_texto = pagina.find('text').text
        for palavra in pagina_texto.split():
            if buscaPalavraInteira(termo_buscado, palavra):  # or buscaPartePalavra(termo_buscado, palavra):
                if pagina_titulo not in artigos_encontrados:
                    artigos_encontrados[pagina_titulo] = (pagina.find('id').text, pagina.find('text').text)
                    break
    return artigos_encontrados


def relevancia(artigos, termo_buscado):
    artigos_classificados = {}
    for artigo_titulo, (artigo_id, artigo_texto) in artigos.items():
        relevancia = 0
        num_palavras = 0
        num_correspondecias = 0

        for palavra in artigo_texto.split():
            num_palavras += 1
            if buscaPalavraInteira(termo_buscado, palavra):
                num_correspondecias += 1

        if num_palavras > 0:
            relevancia = num_correspondecias / num_palavras

        for palavra_titulo in artigo_titulo:
            if buscaPalavraInteira(termo_buscado, palavra_titulo):
                relevancia += 0.1
                break
        artigos_classificados[artigo_id] = (artigo_titulo, relevancia)

    return artigos_classificados


def buscar(termo_buscado):
    termo_buscado = termo_buscado.lower()
    artigos_encontrados = buscarTermo(termo_buscado)
    artigos_classificados = relevancia(artigos_encontrados, termo_buscado)

    artigos_ordenados = sorted(artigos_classificados.items(), key=lambda x: x[1][1], reverse=True)

    return artigos_ordenados


resultados = buscar('computers')

cont = 0

for artigo_id, (artigo_titulo, relevancia) in resultados[:5]:
    print(f'Id: {artigo_id},Titulo: {artigo_titulo}, Relevancia: {(relevancia * 10):.2f}\n')
    print('-' * 40)
    cont += 1
print('Resultados encontrados: ', cont)
