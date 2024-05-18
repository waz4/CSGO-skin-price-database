import os
from src.Skins_DB import Skins_DB
from src.price_by_wear import price_by_wears
from src.DB_loader import load_item_data, load_market_filters, load_prices, read_json, save_json
from src.base_items import get_base_skins, verify_dir_exists
from src.CSGO_market import get_market_filters

path_to_database = "db.sqlite3"

data_directory = "data_to_load/"
requests_directory = data_directory + "requests/"

base_skins_filename = "base_skins.json"
market_filters_filename = "app_filters.json"

proxy_list_filename = "proxies.txt"

db = Skins_DB(path_to_database)

if (not os.path.exists(data_directory + base_skins_filename)):
    get_base_skins(data_directory, base_skins_filename)
base_skins = read_json(data_directory + base_skins_filename)

print("Loading item data")
load_item_data(db, base_skins)

if (not os.path.exists(data_directory + market_filters_filename)):
    status_code, market_filters = get_market_filters()
    save_json(data_directory + market_filters_filename, market_filters)
market_filters = read_json(data_directory + market_filters_filename)["facets"]
    
print("Loading market filters")
load_market_filters(db, market_filters)

if (os.path.exists(proxy_list_filename)):
    print("Loading proxy list")
    with open(proxy_list_filename) as file:
        proxy_list = file.read().splitlines()
else:
    proxy_list = [""]

by_wear_dir = "by_wear/"
verify_dir_exists (requests_directory + by_wear_dir)

wears = db.get_wears()
# price_by_wears(wears=wears,
            #    proxy_list=proxy_list,
            #    output_dir=requests_directory + by_wear_dir)

print("Loading Prices")
load_prices(db, requests_directory + by_wear_dir)