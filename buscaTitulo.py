from xml.dom.minidom import parse


def search_titles(xml_file, search_term):
    dom = parse(xml_file)

    search_term = search_term.lower()

    pages = dom.getElementsByTagName('page')
    matching_titles = []

    for page in pages:
        title = page.getElementsByTagName('title')[0].firstChild.data.lower()

        if search_term in title.split():
            matching_titles.append(title)

    return matching_titles


xml_file = 'verbetesWikipedia.xml'
search_term = 'Zoo'
result = search_titles(xml_file, search_term)
print(f"\nTítulos encontrados com '{search_term}':")
for title in result:
    print(title)
