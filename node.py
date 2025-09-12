class Node:
    def __init__(self, hash_id, title, authors, year, filename):
        self.hash_id = hash_id  
        
        self.title = title
        self.authors = authors
        self.year = year
        self.filename = filename  

        self.next = None

    def __repr__(self):
        return f"Node({self.hash_id}, {self.title}, {self.authors}, {self.year})"
