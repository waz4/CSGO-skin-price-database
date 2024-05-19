import requests, json, os
from src.Skins_DB import Skins_DB
from sqlite3 import IntegrityError
from src.CSGO_market import get_market_filters

def read_json(path_to_file: str):
    with open(path_to_file, "r") as file:
        data = json.loads(file.read())
    return data

def save_json(filename: str, json_data: dict):
    with open(filename, "w+") as file:
        file.write(json.dumps(json_data))

### Load Makrt Filters
### ALL GETS RETURN A TUPLE (NAME ,QUERY_NAME)
def get_wears(filters: dict):
    filters = filters["730_Exterior"]["tags"]
    wears = []

    for wear in filters:
        query_name = f"tag_{wear}"
        name = filters[wear]["localized_name"]

        wears.append( (name, query_name) )

    return wears

def get_collections(filters: dict):
    filters = filters["730_ItemSet"]["tags"]
    collections = []

    for collection in filters:
        query_name = f"tag_{collection}"
        name = filters[collection]["localized_name"]

        collections.append( (name, query_name) )

    return collections

def get_rarities(filters: dict):
    filters = filters["730_Rarity"]["tags"]
    rarities = []

    for rarity in filters:
        query_name = f"tag_{rarity}"
        name = filters[rarity]["localized_name"]

        rarities.append( (name, query_name) )

    return rarities

def get_qualities(filters: dict):
    filters = filters["730_Quality"]["tags"]
    qualities = []

    for quality in filters:
        query_name = f"tag_{quality}"
        name = filters[quality]["localized_name"]

        qualities.append( (name, query_name) )

    return qualities

def get_weapons(filters: dict):
    filters = filters["730_Weapon"]["tags"]
    weapons = []

    for weapon in filters:
        query_name = f"tag_{weapon}"
        name = filters[weapon]["localized_name"]

        weapons.append( (name, query_name) )

    return weapons

def load_wears(db: Skins_DB, wears: tuple):
    for wear in wears:
        db.update_wear_query_name(wear[0], wear[1])

def load_collections(db: Skins_DB, collections: tuple):
    for collection in collections:
        db.update_collection_query_name(collection[0], collection[1])

def load_rarities(db: Skins_DB, rarities: tuple):
    for rarity in rarities:
        db.update_rarity_query_name(rarity[0], rarity[1])

def load_market_filters(db: Skins_DB, filters: dict):
    wears = get_wears(filters)
    collections = get_collections(filters)
    rarities = get_rarities(filters)

    load_wears(db, wears)
    load_collections(db, collections)
    load_rarities(db, rarities)

### Load Prices
# Returns (item_name, Wear)
def parse_item(item: dict):
    inverse_name = item["name"][::-1]

    index_of_opening_bracket = inverse_name.index('(')
    index_of_closing_bracket = inverse_name.index(')')

    wear = inverse_name[index_of_closing_bracket + 1: index_of_opening_bracket][::-1].strip()

    item_name = inverse_name[index_of_opening_bracket + 1:][::-1].strip()

    value = item["sell_price"]

    return item_name, wear, value

def update_base_skins_price(db: Skins_DB, skin_name: str, wear_name: str, value: int):
    cursor_result = db.update_skin_price(skin_name, wear_name, value)
    
    if (cursor_result.rowcount == 0):
        print(f"Failed to Index: {skin_name} ({wear_name})")

def load_prices(db: Skins_DB, dir_prices_name: str):
    failed_to_parse_count = 0
    success_count = 0
    repeated_count = 0
    parsed = []

    for filename in os.listdir(dir_prices_name):
        file_path = f"{dir_prices_name}/{filename}"

        # print(f"File Path: {file_path}")
        print(f"Parsing file: '{filename}'...")
        with open(file_path, "r") as file:
            results = json.loads(file.read())["results"]
        
        while (len(results)):
            result = results.pop()
            item_name, wear, value = parse_item(result)
            try:
                update_base_skins_price(db, item_name, wear, value)
            except Exception as Err:
                print(f"Failed to index: {item_name} ({wear}) with value {value}")
                # raise Err
                failed_to_parse_count += 1
            else:
                # for debug
                if (result in parsed):
                    print(f"Repeat: {item_name} ({wear})")
                    # print(f"Item: {used[used.index(result)]}")
                    repeated_count += 1
                
                parsed.append(result)
                success_count += 1
                continue
                # print(f"{item_name}({wear}) updated with value {value}")

        print(f"Finished parsing: '{filename}'")

    print(f"\n\n\nFailed to parsed {failed_to_parse_count} entries")
    print(f"Repeated: {repeated_count} entries")
    print(f"Successfully parsed {success_count} entries")

### Load Base skins
def get_collection_id(collections: {}, collection_id_name: str):
    for collection in collections:
        if (collection[1] == collection_id_name):
            return collection[0]
    return False

def get_rarity_id(rarities: {}, rarity_id_name_to_seach: str):
    for rarity in rarities:
        if (rarity[1] == rarity_id_name_to_seach):
            return rarity[0]
    return False

def get_wear_id(wears: (), wear_to_search: {}):
    for wear in wears:
        if (wear[1] == wear_to_search["id"]):
            return wear[0]
    return False

def load_identifiers(db: Skins_DB, base_skins: {}):
    collections = db.get_collections()
    rarities = db.get_rarities()
    wears = db.get_wears()
    for skin in base_skins:
        if ("collections" not in skin or len(skin["collections"]) == 0):
            continue

        skin_rarity_id_name = skin["rarity"]["id"]
        skin_rarity_name = skin["rarity"]["name"]

        skin_wears = skin["wears"]

        collection_id_name = skin["collections"][0]["id"]
        collection_name = skin["collections"][0]["name"]

        if not get_collection_id(collections, collection_id_name):
            print(f"New Colletion: {collection_name}")
            db.add_collection(collection_id_name, collection_name)
            collections = db.get_collections()
        
        # Make sure rarity exists in db
        # To be removed
        if not get_rarity_id(rarities, skin_rarity_id_name):
            print(f"New Rarity: {skin_rarity_name}")
            db.add_rarity(skin_rarity_id_name, skin_rarity_name)
            rarities = db.get_rarities()


        # Make sure all wears are in db
        # to be removed thats why its in a separate equal for loop
        for skin_wear in skin_wears:
            if not get_wear_id(wears, skin_wear):
                print(f"New wear: {skin_wear['name']}")
                db.add_wear(skin_wear["id"], skin_wear["name"])        
                wears = db.get_wears()

def load_skins(db: Skins_DB, base_skins: {}):

    collections = db.get_collections()
    rarities = db.get_rarities()
    wears = db.get_wears()

    for skin in base_skins:
        if ("collections" not in skin or len(skin["collections"]) == 0):
            continue
        
        skin_name = skin["name"]

        skin_rarity_id_name = skin["rarity"]["id"]
        skin_rarity_name = skin["rarity"]["name"]

        skin_wears = skin["wears"]

        collection_id_name = skin["collections"][0]["id"]
        collection_name = skin["collections"][0]["name"]

        min_float = skin["min_float"]
        max_float = skin["max_float"]

        collection_id = get_collection_id(collections, collection_id_name)

        rarity_id = get_rarity_id(rarities, skin_rarity_id_name)
        for skin_wear in skin_wears:

            wear_id = get_wear_id(wears, skin_wear)

            try:
                db.add_skin(collection_id, rarity_id, wear_id, skin_name, min_float, max_float)
            except IntegrityError:
                print("Repeated entry, skipping")
                print(f"Repeated skin: {skin_name} ({skin_wear['name']})")
            else:
                # print("")
                continue

    # print(db.get_wears())

def load_item_data(db: Skins_DB, base_skins: dict):
    load_identifiers(db, base_skins)

    load_skins(db, base_skins)
    
def load_all(db: Skins_DB, path_to_base_skins: str, path_to_price_requests: str, path_to_filters: str):
    load_item_data(db, path_to_base_skins)
    load_market_filters(db, path_to_filters)
    load_prices(db, path_to_price_requests)
    
if __name__ == "__main__":
    PATH_TO_DB = "db.sqlite3"
    db = Skins_DB("db.sqlite3")

    # Load Base Skins
    PATH_TO_BASE_SKINS = "data_to_load/base_skins.json"

    load_item_data(db, PATH_TO_BASE_SKINS)

    print("Finished loading base skins")    
    # Load Prices
    # PATH_TO_REQUESTS = "../../pricer/requests/by_wear/"
    PATH_TO_REQUESTS = "data_to_load/requests/by_wear/"

    load_prices(db, PATH_TO_REQUESTS)
    
    print("Finished Loading Prices")
    
    # Load Market Filters
    PATH_TO_FILTERS = "data_to_load/app_filters.json"

    if os.path.exists(PATH_TO_FILTERS):
        filters = read_json(PATH_TO_FILTERS)["facets"]
    else:
        status_code, filters = get_market_filters()
        save_json(PATH_TO_FILTERS, filters)

        filters = filters["facets"]

    load_market_filters(db, filters)
    print("Finished Loading Filters")
    
    