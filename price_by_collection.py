import requests, json, time
from src.CSGO_market import get_all_results
from src.Skins_DB import Skins_DB
 
def save_json(filename: str, json_data: dict):
    with open(filename, "w+") as file:
        file.write(json.dumps(json_data))

def read_file(filename: str):
    with open(filename, "r") as file:
        data = file.read()
    return data

# collections comes from the database
def price_by_collection(collections: dict, proxy_list: list, output_dir: str):
    #                    0            1           2       3
    # collection: (Collection_id, base_name, query_name, name)
    for collection in collections:
        print(f"Pricing collection: {collection[3]}")
        get_all_results(output_dir, output_filename=collection[2], collections=[collection[2]], proxy_list=proxy_list)

if __name__ == "__main__":
    
    output_dir = "data_to_load/requests/by_collection/"
    path_to_db = "db.sqlite3"

    db = Skins_DB(path_to_db)

    collections = db.get_collections()
    
    proxy_list = read_file("proxies.txt").splitlines()

    price_by_collections(collections=collections,
                         proxy_list=proxy_list,
                         output_dir=output_dir);
