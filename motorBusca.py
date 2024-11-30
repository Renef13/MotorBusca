from lxml import etree as et

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

def buscarTitulo(termo_buscado):
    termo_buscado.lower()
    paginas = abrirXML()
    titulos_encontrados = {}

    for pagina in paginas:
        paginaTitulo = pagina.find('title').text
        if termo_buscado in paginaTitulo.lower():
            titulos_encontrados[paginaTitulo] = pagina.find('id').text


    return titulos_encontrados

resultados = buscarTitulo('a')

cont = 0
for titulo, id in resultados.items():
    print(f'Id {id}, Titulo {titulo} \n')
    cont += 1

print('Resultados encontrados',cont)