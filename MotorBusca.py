import re
from CacheBusca import CacheBusca
from nltk.corpus import stopwords
from lxml import etree as et
import time
from collections import defaultdict

class MotorBusca:
    def __init__(self, arquivo_xml):
        arquivo = et.parse(arquivo_xml)
        raiz = arquivo.getroot()
        self.paginas_armazenadas = raiz.xpath('//page')
        self.cache = CacheBusca()
        self.sw = stopwords.words('english')
        self.dicionario_global = {}  # Armazena os dicionários de relevância por página
        self.pre_processar()

    def eh_stop_word(self, palavra):
        return palavra in self.sw

    def filtrar_palavras(self, termo_buscado, texto):
        """
        Filtra as palavras do texto, retornando True se o termo exato for encontrado.
        """
        padrao = re.compile(rf'\b{re.escape(termo_buscado)}\b', re.IGNORECASE)  # Expressão regular para buscar a palavra
        return bool(padrao.search(texto))  # Retorna True se encontrar o termo no texto

    def calcular_relevancia(self, texto):
        """
        Calcula a relevância de cada palavra no texto, retornando um dicionário.
        """
        palavras = re.findall(r'\b\w+\b', texto.lower())  # Encontra todas as palavras
        palavras_filtradas = []  # Lista de palavras filtradas (sem stopwords)

        # Filtra palavras, removendo as stopwords
        for palavra in palavras:
            if not self.eh_stop_word(palavra):
                palavras_filtradas.append(palavra)

        frequencia_total = len(palavras_filtradas)
        dicionario_relevancia = defaultdict(float)

        # Calcula a frequência relativa de cada palavra no texto
        for palavra in palavras_filtradas:
            dicionario_relevancia[palavra] += 1

        # Normaliza as frequências pela frequência total de palavras no texto
        for palavra in dicionario_relevancia:
            dicionario_relevancia[palavra] /= frequencia_total

        return dicionario_relevancia

    def pre_processar(self):
        """
        Preprocessa todas as páginas e calcula o dicionário de relevância para cada uma.
        """
        start_time = time.time()

        for pagina in self.paginas_armazenadas:
            pagina_id = pagina.find('id').text
            pagina_texto = pagina.find('text').text or ""
            # Calcula o dicionário de relevância para o texto da página
            self.dicionario_global[pagina_id] = self.calcular_relevancia(pagina_texto)

        end_time = time.time()
        print(f"Pré-processamento concluído em {end_time - start_time:.4f} segundos.")

    def buscar(self, termo_buscado):
        """
        Realiza a busca pelo termo e retorna as 5 páginas com maior relevância.
        """
        termo_buscado = termo_buscado.lower()

        if self.eh_stop_word(termo_buscado):
            return None

        if self.cache.in_cache(termo_buscado):
            return self.cache.get(termo_buscado)

        # Medindo o tempo de busca
        start_time = time.time()

        # Verifica a relevância do termo em todas as páginas
        relevancia_paginas = {}

        for pagina in self.paginas_armazenadas:
            pagina_id = pagina.find('id').text
            pagina_titulo = pagina.find('title').text or ""
            dicionario_relevancia = self.dicionario_global.get(pagina_id, {})

            # Inicializa a relevância com o valor calculado do texto
            relevancia = dicionario_relevancia.get(termo_buscado, 0)

            # Aplica a bonificação se a palavra estiver no título
            if self.filtrar_palavras(termo_buscado, pagina_titulo):
                relevancia += 0.1

            # Adiciona a página ao dicionário de relevância se o termo foi encontrado
            if relevancia > 0:
                relevancia_paginas[pagina_id] = (pagina_titulo, relevancia)

        # Ordena as páginas pela relevância do termo
        paginas_ordenadas = sorted(relevancia_paginas.items(), key=lambda x: x[1][1], reverse=True)
        paginas_mais_relevantes = paginas_ordenadas[:5]

        end_time = time.time()  # Fim da medição do tempo de busca
        print(f"Tempo de busca para '{termo_buscado}': {end_time - start_time:.4f} segundos.")

        # Monta o resultado
        resultado = {}
        for pagina_id, (titulo, relevancia) in paginas_mais_relevantes:
            resultado[titulo] = relevancia

        self.cache.set(termo_buscado, resultado)
        return resultado
