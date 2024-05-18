import requests, json, time
from CSGO_market import get_all_results
from Skins_DB import Skins_DB

 
def save_json(filename: str, json_data: dict):
    with open(filename, "w+") as file:
        file.write(json.dumps(json_data))

def read_json(filename: str):
    with open(filename, "r") as file:
        data = json.loads(file.read())
    return data

# wears comes from the database
def price_by_wears(wears: dict, proxy_list: list, output_dir: str):
    #           0         1           2       3
    # wear: (Wear_id, base_name, query_name, name)
    for wear in wears:
        print(f"Pricing wear: {wear[3]}")
        get_all_results(output_dir, output_filename=wear[2], wears=[wear[2]], proxy_list=proxy_list)

if __name__ == "__main__":
    
    output_dir = "data_to_load/requests/by_wear/"
    path_to_db = "db.sqlite3"

    db = Skins_DB(path_to_db)

    wears = db.get_wears()
    
    proxy_list = read_json("../proxy_list.json")["results"]
    proxy_list = [f"{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}" for proxy in proxy_list]
