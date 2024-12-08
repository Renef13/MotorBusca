import re
# from CacheBusca import CacheBusca
from nltk.corpus import stopwords
from lxml import etree as et
import time
from collections import defaultdict


class MotorBusca:
    def __init__(self, arquivo_xml):
        arquivo = et.parse(arquivo_xml)
        raiz = arquivo.getroot()
        self.paginas_armazenadas = raiz.xpath('//page')
        # self.cache = CacheBusca()
        self.sw = stopwords.words('english')
        self.dicionario_global = {}
        self.pre_processar()

    def eh_stop_word(self, palavra):
        return palavra in self.sw

    def filtrar_palavras(self, termo_buscado, texto):
        padrao = re.compile(rf'\b{re.escape(termo_buscado)}\b', re.IGNORECASE)
        return bool(padrao.search(texto))

    def calcular_relevancia(self, texto):

        palavras = re.findall(r'\b\w+\b', texto.lower())
        palavras_filtradas = []

        for palavra in palavras:
            if not self.eh_stop_word(palavra):
                palavras_filtradas.append(palavra)

        frequencia_total = len(palavras_filtradas)
        dicionario_relevancia = defaultdict(float)

        for palavra in palavras_filtradas:
            dicionario_relevancia[palavra] += 1

        for palavra in dicionario_relevancia:
            dicionario_relevancia[palavra] /= frequencia_total

        return dicionario_relevancia

    def pre_processar(self):
        start_time = time.time()

        for pagina in self.paginas_armazenadas:
            pagina_id = pagina.find('id').text
            pagina_texto = pagina.find('text').text or ""

            self.dicionario_global[pagina_id] = self.calcular_relevancia(pagina_texto)

        end_time = time.time()
        print(f"Pré-processamento concluído em {end_time - start_time:.4f} segundos.")

    def buscar(self, termo_buscado):
        termo_buscado = termo_buscado.lower()

        if self.eh_stop_word(termo_buscado):
            return None

        # if self.cache.in_cache(termo_buscado):
        #     return self.cache.get(termo_buscado)

        start_time = time.time()

        relevancia_paginas = {}

        for pagina in self.paginas_armazenadas:
            pagina_id = pagina.find('id').text
            pagina_titulo = pagina.find('title').text or ""
            dicionario_relevancia = self.dicionario_global.get(pagina_id, {})

            relevancia = dicionario_relevancia.get(termo_buscado, 0)

            if self.filtrar_palavras(termo_buscado, pagina_titulo):
                relevancia += 0.1

            if relevancia > 0:
                relevancia_paginas[pagina_id] = (pagina_titulo, relevancia)

        paginas_ordenadas = sorted(relevancia_paginas.items(), key=lambda x: x[1][1], reverse=True)
        paginas_mais_relevantes = paginas_ordenadas[:5]

        end_time = time.time()
        print(f"Tempo de busca para '{termo_buscado}': {end_time - start_time:.4f} segundos.")

        resultado = {}
        for pagina_id, (titulo, relevancia) in paginas_mais_relevantes:
            resultado[titulo] = relevancia

        # self.cache.set(termo_buscado, resultado)
        return resultado
