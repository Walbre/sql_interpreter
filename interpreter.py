import sqlite3
from sqlite3 import Error



class sqldb:
    """Classe sql qui permet d'interagir avec le fichieer sql"""

    def __init__(self, path):
        self.path = path
        self.connection = self.create_connection()
    
    def create_connection(self):
        """Créé la connection avec le fichier sql et créé le fichier si il n'existe pas"""
        conn = None
        try:
            conn = sqlite3.connect(self.path)
        except Error as e:
            print(f"Error : {e}")
        
        return conn
    
    def exec(self,code):
        """Permet d'executer du code sql pour interagir avec la db"""
        cursor = self.connection.cursor()
        
        try:
            cursor.executescript(code)
            self.connection.commit()
        except Error as e:
            print(f"Error : {e}")
        
    def read(self, code):
        """Permet de récuperer les infos venant de la db avec du code sql"""
        cursor = self.connection.cursor()
        
        try:
            cursor.execute(code)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error : {e}")