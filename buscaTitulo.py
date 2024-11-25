from xml.dom.minidom import parse
import re


class XMLSearchProcessor:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.dom = parse(xml_file)

    def conta_ocorrencias_e_texto(self, search_term):
        print("Renef é gay")
        search_term = search_term.lower()
        pattern = re.compile(rf'\b{re.escape(search_term)}\b')

        pages = self.dom.getElementsByTagName('page')
        relevancias = {}

        for page in pages:
            title_elements = page.getElementsByTagName('title')
            if not title_elements or not title_elements[0].firstChild:
                continue
            title = title_elements[0].firstChild.data.strip()

            text_elements = page.getElementsByTagName('text')
            if not text_elements or not text_elements[0].firstChild:
                continue
            text = text_elements[0].firstChild.data.lower()

            count = len(pattern.findall(text))
            word_count = len(text.split())
            if word_count == 0:
                continue

            relevancia = count / word_count
            if title.lower() == search_term:
                relevancia += 0.1

            relevancias[title] = relevancia * 100

        return dict(sorted(relevancias.items(), key=lambda item: item[1], reverse=True))


def main():
    xml_file = 'verbetesWikipedia.xml'
    search_term = 'computer'

    processor = XMLSearchProcessor(xml_file)

    resultados = processor.conta_ocorrencias_e_texto(search_term)

    print(f"\nPáginas encontradas com a palavra '{search_term}' (apenas os 5 primeiros):\n")
    for i, (title, relevancia) in enumerate(resultados.items()):
        if i < 5:
            print(f"{i + 1}. Título: {title}, Relevância: {relevancia:.2f}%")
        else:
            break

    print(f"\n{len(resultados)} resultados encontrados para '{search_term}'.")


if __name__ == "__main__":
    main()
