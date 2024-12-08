from xml.dom.minidom import parse
import re
# COMO ESTÁ A ESTRUTURA DE DADOS DESSA BOMBA
# {
#     "Título da Página 1": {
#         "palavra1": 10,
#         "palavra2": 5,
#         ...
#     },
#     "Título da Página 2": {
#         "palavra1": 3,
#         "palavra3": 7,
#         ...
#     },
#     ...
# }

class XMLSearchProcessor:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.dom = parse(xml_file)
        self.pages_data = self._process_pages()


    def _process_pages(self):
        """
        Percorre o arquivo XML inteiro e cria um dicionário onde as chaves são os títulos
        das páginas e os valores são dicionários contendo as palavras e suas ocorrências.
        """
        pages_data = {}
        pages = self.dom.getElementsByTagName('page')

        for page in pages:
            title = page.getElementsByTagName('title')[0].firstChild.data
            text_elements = page.getElementsByTagName('text')

            if text_elements and text_elements[0].firstChild:
                text = text_elements[0].firstChild.data.lower()
                words = re.findall(r'\b\w+\b', text)  
                word_counts = {}

                for word in words:
                    word_counts[word] = word_counts.get(word, 0) + 1

                pages_data[title] = word_counts  

        return pages_data

    def search_titles_and_count(self, search_term):
        """
        Realiza a busca por uma palavra nos títulos e seus textos,
        retornando um dicionário com os resultados ordenados por densidade.
        Se a palavra buscada estiver no título, 0.3 pontos são adicionados à densidade.
        """
        search_term = search_term.lower()
        matching_titles = {}

        for title, word_dict in self.pages_data.items():
            count = word_dict.get(search_term, 0)
            total_words = sum(word_dict.values())
            density = count / total_words if total_words > 0 else 0

            
            if search_term in title.lower():
                density += 0.3

            if count > 0 or search_term in title.lower():
                matching_titles[title] = (count, total_words, density)

        return dict(sorted(matching_titles.items(), key=lambda item: item[1][2], reverse=True))

def main():
    xml_file = 'verbetesWikipedia.xml'  
    processor = XMLSearchProcessor(xml_file)  


    
    cache = {} 

    while True:
        search_term = input("Digite a palavra que deseja buscar (ou 'sair' para encerrar): ").strip()

        if search_term.lower() == 'sair':
            print("Saindo do programa...")
            break  
        
        if len(search_term) < 4:
            print("Palavra muito curta. Digite novamente.")
            continue  
        
        if search_term in cache:
            print(f"\nResultado encontrado no cache para '{search_term}':")
            resultados = cache[search_term]  
        else:
            resultados = processor.search_titles_and_count(search_term)
            cache[search_term] = resultados  

        
        if resultados:
            print(f"\nPáginas encontradas com a palavra '{search_term}' (apenas os 10 primeiros):\n")
            for i, (title, count) in enumerate(resultados.items()):
                if i < 10:
                    print(f"{i + 1}. Título: {title}|   |Ocorrências no texto/Total de palavras/Densidade: {count}")
                else:
                    break
            print(f"\n{len(resultados)} resultados encontrados para '{search_term}'.")
        else:
            print(f"\nNenhum resultado encontrado para '{search_term}'.")


if __name__ == "__main__":
    main()
