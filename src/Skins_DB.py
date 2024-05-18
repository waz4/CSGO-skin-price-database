import sqlite3

class Skins_DB:
    def __init__(self, path_to_db: str):
        self.db_conn = self._connect_to_db(path_to_db)
        self._setup_database()
            
    def _connect_to_db(self, path_to_db: str):
        return sqlite3.connect(path_to_db)
    
    def _get_cursor(self):

        return self.db_conn.cursor()

    def _setup_database(self):
        cursor = self._get_cursor()
        skins_db_create = '''
            CREATE TABLE IF NOT EXISTS skins (
            skin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            collection_id INTEGER,
            rarity_id INTEGER,
            wear_id INTEGER,
            skin_name TEXT,
            min_float REAL,
            max_float REAL,
            value INTEGER,
            UNIQUE(skin_name, wear_id),
            FOREIGN KEY (collection_id) REFERENCES collections(collection_id),
            FOREIGN KEY (rarity_id) REFERENCES rarities(rarity_id),
            FOREIGN KEY (wear_id) REFERENCES wear(wear_id)
        );'''    

        rarity_db_create = '''
            CREATE TABLE IF NOT EXISTS rarities (
            rarity_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_name TEXT,
            query_name INTEGER,
            name TEXT
        );'''

        collection_db_create = '''
            CREATE TABLE IF NOT EXISTS collections (
            collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_name TEXT,
            query_name TEXT,
            name TEXT
        );'''

        wears_db_create = '''
            CREATE TABLE IF NOT EXISTS wears (
            wear_id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_name TEXT,
            query_name TEXT,
            name TEXT
        );'''

        cursor.execute(skins_db_create)
        cursor.execute(rarity_db_create)
        cursor.execute(collection_db_create)
        cursor.execute(wears_db_create)

        self.db_conn.commit()

    def add_rarity(self, id_name: str, name: str, query_name: str = ""):
        cursor = self._get_cursor()
        add_rarity_query = f'''
            INSERT INTO rarities (id_name, query_name, name) VALUES
                ('{id_name}', '{query_name}', '{name}')
        ;'''

        cursor.execute(add_rarity_query)
        self.db_conn.commit()

    def add_collection(self, id_name: str, name: str, query: str = ""):
        cursor = self._get_cursor()
        add_collection_query = f'''
            INSERT INTO collections (id_name, query_name, name) VALUES
                ('{id_name}', '{query}' , '{name}')
        ;'''

        cursor.execute(add_collection_query)
        self.db_conn.commit()

    def add_wear(self, id_name: str, name: str, query_name: str = ""):
        cursor = self._get_cursor()
        add_wear_query = f'''
            INSERT INTO wears (id_name, query_name, name) VALUES 
                ('{id_name}', '{query_name}', '{name}')
        ;'''

        cursor.execute(add_wear_query)
        self.db_conn.commit()

    def add_skin(self, collection_id: int, rarity_id: int, wear_id: int, skin_name: str, min_float: float, max_float: float, value: int = -1):
        cursor = self._get_cursor()
        add_skin_query = f'''
            INSERT INTO skins (collection_id, rarity_id, wear_id, skin_name, min_float, max_float, value) VALUES 
                (?, ?, ?, ?, ?, ?, ?)
        ;'''

        values = (collection_id, rarity_id, wear_id, skin_name, min_float, max_float, value)
        # print(add_skin_query)
        cursor.execute(add_skin_query, values)
        self.db_conn.commit()

    def get_collections(self):
        cursor = self._get_cursor()
        select_collections_query = '''
            SELECT * from collections
        ;'''
        
        result = cursor.execute(select_collections_query)
        
        return result.fetchall()

    def get_rarities(self):
        cursor = self._get_cursor()
        select_rarities_query = '''
            SELECT * from rarities
        ;'''
        
        result = cursor.execute(select_rarities_query)
        
        return result.fetchall()

    def get_wears(self):
        cursor = self._get_cursor()
        select_wears_query = '''
            SELECT * from wears
        ;'''
        
        result = cursor.execute(select_wears_query)
        
        return result.fetchall()

    def get_skins(self):
        cursor = self._get_cursor()
        select_skins_query = '''
            SELECT * from skins
        ;'''
        
        result = cursor.execute(select_skins_query)
        
        return result.fetchall()

    def update_skin_price(self, skin_name: str, wear_name: str, value: int):
        cursor = self._get_cursor()
        update_query = '''
            UPDATE skins
            SET value = ?
            WHERE skin_name = ? AND wear_id = (SELECT wear_id FROM wears WHERE name = ?);
        '''

        values = (value, skin_name, wear_name)

        result = cursor.execute(update_query, values)
        self.db_conn.commit()

        return result

    def update_rarity_query_name(self, rarity_name: str, rarity_query_name: str):
        cursor = self._get_cursor()
        update_query = '''
            UPDATE rarities 
            SET query_name = ?
            WHERE name = ?
        ;'''

        values = (rarity_query_name, rarity_name)

        cursor.execute(update_query, values)
        self.db_conn.commit()

    def update_collection_query_name(self, collection_name: str, collection_query_name: str):
        cursor = self._get_cursor()
        update_query = '''
            UPDATE collections 
            SET query_name = ?
            WHERE name = ?
        ;'''

        values = (collection_query_name, collection_name)

        cursor.execute(update_query, values)
        self.db_conn.commit()

    def update_wear_query_name(self, wear_name: str, wear_query_name: str):
        cursor = self._get_cursor()
        update_query = '''
            UPDATE wears 
            SET query_name = ?
            WHERE name = ?
        ;'''

        values = (wear_query_name, wear_name)

        cursor.execute(update_query, values)
        self.db_conn.commit()

    def make_query(self, query: str, values: list):
        cursor = self._get_cursor()
        
        result = cursor.execute(query, values)
        return result.fetchall()

if __name__ == "__main__":
    path_to_db = "test_db.sqlite3"

    db = Skins_DB(path_to_db)
    
    db.setup_database()

    db.add_collection("collection_id_A", "collection_query_name_A", "collection_name_A")
    db.add_collection("collection_id_B", "collection_query_name_B", "collection_name_B")
    
    collection_list = db.get_collections()

    print(f"Collection list: {collection_list}")

    db.add_rarity("rarity_id_name_A", "rarity_request_name_A", "rarity_name_A")
    db.add_rarity("rarity_id_name_B", "rarity_request_name_B", "rarity_name_B")

    rarity_list = db.get_rarities()

    print(f"Rarities list: {rarity_list}")

    db.add_wear("wear_id_A", "wear_request_name_A", "wear_name_A")
    db.add_wear("wear_id_B", "wear_request_name_B", "wear_name_B")

    wear_list = db.get_wears()

    print(f"Wears list: {wear_list}")

    db.add_skin(0, 0, 0, "skin_name_A", 0, 1, 100)
    db.add_skin(0, 0, 0, "skin_name_B", 0, 1, 100)

    skins_list = db.get_skins()
    
    print(f"Skins list: {skins_list}")