class CacheBusca:
    def __init__(self):
        self.cache = {}

    def get(self, termo_buscado):
        return self.cache.get(termo_buscado)

    def set(self, termo_buscado, resultados):
        if termo_buscado not in self.cache:
            self.cache[termo_buscado] = resultados

    def in_cache(self, termo_buscado):
        if termo_buscado in self.cache:
            return True
        return False