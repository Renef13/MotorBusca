import re
from lxml import etree as et


class XMLData:
    def __init__(self, arquivo_xml):
        self.paginas_armazenadas = None
        self.arquivo_xml = arquivo_xml

    def abrirXML(self):
        if self.paginas_armazenadas is None:
            arquivo = et.parse(self.arquivo_xml)
            raiz = arquivo.getroot()
            self.paginas_armazenadas= raiz.xpath('//page')
        return self.paginas_armazenadas


class MotorBusca:
    def __init__(self, paginas_armazenadas):
        self.paginas_armazenadas = paginas_armazenadas

    def filtrarPalavras(self, termo_buscado, texto):
        padrao = rf'\b{re.escape(termo_buscado)}\b'
        return bool(re.search(padrao, texto, re.IGNORECASE))

    def buscarTermo(self, termo_buscado):
        termo_buscado = termo_buscado.lower()
        paginas = self.paginas_armazenadas.abrirXML()
        artigos_encontrados = {}

        for pagina in paginas:
            pagina_titulo = pagina.find('title').text
            pagina_texto = pagina.find('text').text

            if self.filtrarPalavras(termo_buscado, pagina_texto):  # tem palavra que eu quero
                if pagina_titulo not in artigos_encontrados:
                    artigos_encontrados[pagina_titulo] = (pagina.find('id').text, pagina.find('text').text)

        return artigos_encontrados

    def relevancia(self, artigos, termo_buscado):
        artigos_classificados = {}
        termo_buscado_regex = re.compile(r'\b' + re.escape(termo_buscado) + r'\b', re.IGNORECASE)

        for artigo_titulo, (artigo_id, artigo_texto) in artigos.items():
            relevancia = 0
            num_palavras = len(artigo_texto.split())
            num_correspondecias = len(termo_buscado_regex.findall(artigo_texto))

            if num_palavras > 0:
                relevancia = num_correspondecias / num_palavras

            if termo_buscado_regex.search(artigo_titulo): # relevancia aumentada
                relevancia += 0.1
            artigos_classificados[artigo_id] = (artigo_titulo, relevancia)

        return artigos_classificados

    def buscar(self, termo_buscado):
        termo_buscado = termo_buscado.lower()

        artigos_encontrados = self.buscarTermo(termo_buscado)
        artigos_classificados = self.relevancia(artigos_encontrados, termo_buscado)

        artigos_ordenados = sorted(artigos_classificados.items(), key=lambda x: x[1][1], reverse=True)

        return artigos_ordenados

arquivo_xml = XMLData('verbetesWikipedia.xml')

buscador = MotorBusca(arquivo_xml)
resultados = buscador.buscar('computers')

cont = 0

for artigo_id, (artigo_titulo, relevancia) in resultados[:5]:
    print(f'Id: {artigo_id},Titulo: {artigo_titulo}, Relevancia: {(relevancia * 10):.2f}\n')
    print('-' * 40)
    cont += 1
print('Resultados encontrados: ', cont)
