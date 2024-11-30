from lxml import etree as et
import re
from fuzzywuzzy import fuzz
#print(f'Num de páginas: {len(paginas)}')
# for pagina in paginas:
#     paginaId = pagina.find('id').text
#     paginaTitulo = pagina.find('title').text
#     print(f'Id: {paginaId}: Titulo: {paginaTitulo}\n')


def abrirXML():
    arquivo = et.parse('verbetesWikipedia.xml')
    raiz = arquivo.getroot()
    paginas = raiz.xpath('//page')
    return  paginas

def buscaPalavrainteira(termo, texto):
    #busca a palavra inteira ignorando especias
    palavra = r'\b' + re.escape(termo) + r'\b'
    return bool(re.search(palavra, texto, re.IGNORECASE))

def buscaPartePalavra(termo, texto):
    # busca palavras 80% similares
    SIMILARIDADE = 80
    if fuzz.ratio(termo, texto) > SIMILARIDADE:
        return True


def buscarTitulo(termo_buscado):
    termo_buscado = termo_buscado.lower()
    paginas = abrirXML()
    titulos_encontrados = {}

    for pagina in paginas:
        paginaTitulo = pagina.find('title').text
        for palavra in paginaTitulo.split():
            if buscaPalavrainteira(termo_buscado, palavra) or buscaPartePalavra(termo_buscado, palavra):
                if paginaTitulo not in titulos_encontrados:
                    titulos_encontrados[paginaTitulo] = pagina.find('id').text
                break

    return titulos_encontrados

resultados = buscarTitulo('computers')

cont = 0
for titulo, id in resultados.items():
    print(f'Id {id}, Titulo {titulo} \n')
    cont += 1

print('Resultados encontrados',cont)