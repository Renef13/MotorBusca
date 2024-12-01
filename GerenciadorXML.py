from lxml import etree as et
class XMLData:
    def __init__(self, arquivo_xml):
        self.paginas_armazenadas = None
        self.arquivo_xml = arquivo_xml

    def abrirXML(self):
        if self.paginas_armazenadas is None:
            arquivo = et.parse(self.arquivo_xml)
            raiz = arquivo.getroot()
            self.paginas_armazenadas= raiz.xpath('//page')
        return self.paginas_armazenadas