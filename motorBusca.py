import re

from lxml import etree as et

paginas_cache = None


def abrirXML():
    global paginas_cache
    if paginas_cache is None:
        arquivo = et.parse('verbetesWikipedia.xml')
        raiz = arquivo.getroot()
        paginas_cache = raiz.xpath('//page')
    return paginas_cache


def filtrarPalavras(termo_buscado, texto):
    padrao = rf'\b{re.escape(termo_buscado)}\b'
    return bool(re.search(padrao, texto,re.IGNORECASE))

def buscarTermo(termo_buscado):
    termo_buscado = termo_buscado.lower()
    paginas = abrirXML()
    artigos_encontrados = {}

    for pagina in paginas:
        pagina_titulo = pagina.find('title').text
        pagina_texto = pagina.find('text').text

        if  filtrarPalavras(termo_buscado, pagina_texto):  # tem palavra que eu quero
            if pagina_titulo not in artigos_encontrados:
                artigos_encontrados[pagina_titulo] = (pagina.find('id').text, pagina.find('text').text)

    return artigos_encontrados


def relevancia(artigos, termo_buscado):
    artigos_classificados = {}
    termo_buscado_regex = re.compile(r'\b' + re.escape(termo_buscado) + r'\b', re.IGNORECASE)

    for artigo_titulo, (artigo_id, artigo_texto) in artigos.items():
        relevancia = 0
        num_palavras = len(artigo_texto.split())
        num_correspondecias = len(termo_buscado_regex.findall(artigo_texto))

        if num_palavras > 0:
            relevancia = num_correspondecias / num_palavras

        # print(f'artigo_titulo: {artigo_titulo} | termo_buscado: {termo_buscado}')
        if termo_buscado_regex.search(artigo_titulo): # ordem errada ?
            relevancia += 0.1
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
