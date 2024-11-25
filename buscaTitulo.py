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

            text_elements = page.getElementsByTagName('text')
            if text_elements and text_elements[0].firstChild:
                text = text_elements[0].firstChild.data.lower()

                count = len(pattern.findall(text))

                if count > 0:
                    matching_titles[title] = count

        return dict(sorted(matching_titles.items(), key=lambda item: item[1], reverse=True))

def main():
    xml_file = 'verbetesWikipedia.xml'
    search_term = 'computer'

    processor = XMLSearchProcessor(xml_file)

    resultados = processor.search_titles_and_count(search_term)

    print(f"\nPáginas encontradas com a palavra '{search_term}' (apenas os 10 primeiros):\n")
    for i, (title, count) in enumerate(resultados.items()):
        if i < 10:
            print(f"{i + 1}. Título: {title}, Ocorrências no texto: {count}")
        else:
            break

    print(f"\n{len(resultados)} resultados encontrados para '{search_term}'.")


if __name__ == "__main__":
    main()

