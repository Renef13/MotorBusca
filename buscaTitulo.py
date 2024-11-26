from xml.dom.minidom import parse
import re


class XMLSearchProcessor:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.dom = parse(xml_file)

    def search_titles_and_count(self, search_term):
        search_term = search_term.lower()
        pattern = re.compile(rf'\b{re.escape(search_term)}\b')

        pages = self.dom.getElementsByTagName('page')
        matching_titles = {}

        for page in pages:
            title = page.getElementsByTagName('title')[0].firstChild.data

            # Contando o número de palavras no texto
            

            

            text_elements = page.getElementsByTagName('text')
            if text_elements and text_elements[0].firstChild:
                text = text_elements[0].firstChild.data.lower()
                words = text.split()
                total_words = len(words)

                count = len(pattern.findall(text))
                density = count / total_words

                if count > 0:
                    matching_titles[title] = (count, total_words,density)

        return dict(sorted(matching_titles.items(), key=lambda item: item[1][2], reverse=True))

def main():
    xml_file = '../../../Downloads/MotorBusca-master/MotorBusca-master/verbetesWikipedia.xml'
    processor = XMLSearchProcessor(xml_file)  


    # Dicionário para armazenar os resultados das pesquisas anteriores
    cache = {} 

    while True:
        search_term = input("Digite a palavra que deseja buscar (ou 'sair' para encerrar): ").strip()

        if search_term.lower() == 'sair':
            print("Saindo do programa...")
            break  

        # Verifica se o resultado já está em cache
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

