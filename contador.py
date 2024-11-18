from xml.dom.minidom import parse

xml_file = 'verbetesWikipedia.xml'
dom = parse(xml_file)

pages = dom.getElementsByTagName('page')
num_pages = len(pages)
print(f"\nNúmero total de páginas: {num_pages}")

for page in pages:
    page_id = page.getElementsByTagName('id')[0].firstChild.data
    page_title = page.getElementsByTagName('title')[0].firstChild.data
    print(f"ID: {page_id}, Título: {page_title}")

