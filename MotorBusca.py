import re
from CacheBusca import CacheBusca
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from lxml import etree as et
import time

class MotorBusca:
    def __init__(self, arquivo_xml):
        arquivo = et.parse(arquivo_xml)
        raiz = arquivo.getroot()
        self.paginas_armazenadas = raiz.xpath('//page')
        self.cache = CacheBusca()
        self.sw = stopwords.words('english')
        self.palavras_buscadas = set()
        self.pre_processar(self)

    def eh_stop_word(self, palavra):
        if palavra in self.sw:
            return True

    @staticmethod
    def filtrar_palavras(termo_buscado, texto):
        padrao = rf'\b{re.escape(termo_buscado)}\b'
        return bool(re.search(padrao, texto, re.IGNORECASE))

    def buscar_termo(self, termo_buscado):
        paginas = self.paginas_armazenadas
        artigos_encontrados = {}

        for pagina in paginas:
            pagina_titulo = pagina.find('title').text
            pagina_texto = pagina.find('text').text

            if self.filtrar_palavras(termo_buscado, pagina_texto):  # tem palavra que eu quero
                if pagina_titulo not in artigos_encontrados:
                    artigos_encontrados[pagina_titulo] = (pagina.find('id').text, pagina.find('text').text)

        artigos_encontrados = self.relevancia(artigos_encontrados, termo_buscado)
        return artigos_encontrados

    @staticmethod
    def relevancia(artigos, termo_buscado):
        artigos_classificados = {}
        termo_buscado_regex = re.compile(r'\b' + re.escape(termo_buscado) + r'\b', re.IGNORECASE)

        for artigo_titulo, (artigo_id, artigo_texto) in artigos.items():
            relevancia = 0
            num_palavras = len(artigo_texto.split())
            num_correspondencias = len(termo_buscado_regex.findall(artigo_texto))

            if num_palavras > 0:
                relevancia = num_correspondencias / num_palavras

            if termo_buscado_regex.search(artigo_titulo):  # relevancia aumentada
                relevancia += 0.1
            artigos_classificados[artigo_id] = (artigo_titulo, relevancia)

        return sorted(artigos_classificados.items(), key=lambda x: x[1][1], reverse=True)

    # def ordenarArtigos(self, artigos):
    #     return sorted(artigos.items(), key=lambda x: x[1][1], reverse=True)

    def buscar(self, termo_buscado):
        termo_buscado = termo_buscado.lower()

        if self.eh_stop_word(termo_buscado):
            return None
        if self.cache.in_cache(termo_buscado):
            return dict(self.cache.get(termo_buscado))

        artigos_encontrados = self.buscar_termo(termo_buscado)
        # artigos_classificados = self.relevancia(artigos_encontrados, termo_buscado)
        # artigos_ordenados = self.ordenarArtigos(artigos_classificados)
        artigos_relevantes = dict(artigos_encontrados[:5])
        self.cache.set(termo_buscado, artigos_relevantes)

        return artigos_relevantes

    @staticmethod
    def pre_processar(self):
        start_time = time.time()
        paginas = self.paginas_armazenadas
        i = 0
        for pagina in paginas:
            pagina_texto = pagina.find('text').text
            for palavra in pagina_texto.split():
                if palavra not in self.palavras_buscadas:
                    self.buscar(palavra)
                    if not self.eh_stop_word(palavra):
                        self.palavras_buscadas.add(palavra)
            i += 1
            print(f"Busca {i} realizada\n")
        end_time = time.time()  # Fim da medição
        print(f"Tempo de execução do método 'buscar': {end_time - start_time:.4f} segundos")

# def buscaPartePalavra(termo, texto):
#     # busca palavras 80% similares
#     SIMILARIDADE = 80
#     if fuzz.ratio(termo, texto) > SIMILARIDADE:
#         return True
