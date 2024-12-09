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
        print(f"Pre-processamento concluido em {end_time - start_time:.4f} segundos\n")

    def buscar(self, termos_buscados):

        termos_buscados = [termo.lower() for termo in termos_buscados.split()]
        relevancia_combinada = defaultdict(float)

        start_time = time.time()

        for termo in termos_buscados:
            if self.eh_stop_word(termo):
                continue

            if self.cache.in_cache(termo):
                resultados_termo = self.cache.get(termo)
            else:
                resultados_termo = {}
                for pagina in self.paginas_armazenadas:
                    pagina_id = pagina.find('id').text
                    pagina_titulo = pagina.find('title').text or ""
                    dicionario_relevancia = self.dicionario_global.get(pagina_id, {})

                    relevancia = dicionario_relevancia.get(termo, 0)

                    if self.filtrar_palavras(termo, pagina_titulo):
                        relevancia += 0.1

                    if relevancia > 0:
                        resultados_termo[pagina_id] = (pagina_titulo, relevancia)

                resultados_termo = {
                    pagina_id: (titulo, relevancia)
                    for pagina_id, (titulo, relevancia) in sorted(
                        resultados_termo.items(), key=lambda x: x[1][1], reverse=True
                    )
                }
                self.cache.set(termo, resultados_termo)

            for pagina_id, (titulo, relevancia) in resultados_termo.items():
                relevancia_combinada[pagina_id] += relevancia

        paginas_ordenadas = sorted(relevancia_combinada.items(), key=lambda x: x[1], reverse=True)
        paginas_mais_relevantes = paginas_ordenadas[:5]

        end_time = time.time()
        print(f"Tempo de busca para '{' '.join(termos_buscados)}': {end_time - start_time:.4f} segundos.")

        resultado = {}
        for pagina_id, relevancia in paginas_mais_relevantes:
            pagina_titulo = next(
                (pagina.find('title').text for pagina in self.paginas_armazenadas if pagina.find('id').text == pagina_id),
                "Título desconhecido"
            )
            resultado[pagina_titulo] = relevancia

        return resultado
