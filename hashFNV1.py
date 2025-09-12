import json 
from node import Node

def custom_hash(data, size = 10):
    serialized = json.dumps(data, sort_keys=True)
    hash_value = 2166136261
    fnv_prime = 16777619

    for char in serialized.encode('utf-8'):
        hash_value = (hash_value * fnv_prime) ^ char

    hash_value = hash_value & 0xFFFFFFFF
    return  hash_value % size

class TablaHash:
    def __init__(self, size=10):
        self.size = size
        self.tabla = [None] * size

    def insert(self, hash_id, title, authors, year, filename):
        # Usamos el hash del artículo como clave
        key = {"hash_id": hash_id}
        pos = custom_hash(key, self.size)

        new_node = Node(hash_id, title, authors, year, filename)

        if self.tabla[pos] is None:
            self.tabla[pos] = new_node
        else:
            current = self.tabla[pos]
            while current.next:
                current = current.next
            current.next = new_node

    def mostrar(self):
        for i in range(self.size):
            print(f"Position {i}:", end=" ")
            current = self.tabla[i]
            if current is None:
                print("Empty")
            else:
                while current:
                    print(f"[{current.hash_id} | {current.title}]", end=" -> ")
                    current = current.next
                print("None")

    def buscar(self, hash_id):
        clave = {"hash_id": hash_id}
        pos = custom_hash(clave, self.size)

        current = self.tabla[pos]
        while current:
            if current.hash_id == hash_id:
                return current
            current = current.next
        return None

    def eliminar(self, hash_id):
        clave = {"hash_id": hash_id}
        pos = custom_hash(clave, self.size)

        current = self.tabla[pos]
        prev = None
        while current:
            if current.hash_id == hash_id:
                if prev:
                    prev.next = current.next
                else:
                    self.tabla[pos] = current.next
                return True  # Eliminado
            prev = current
            current = current.next
        return False  # No encontrado

    def modificar(self, hash_id, new_title=None, news_authors=None, new_year=None):
        article = self.buscar(hash_id)
        if article:
            if new_title:
                article.title = new_title
            if news_authors:
                article.authors = news_authors
            if new_year:
                article.year = new_year
            return True
        return False