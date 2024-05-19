import requests, json, time

QUERY_URL_MARKET_FILTERS = r"https://steamcommunity.com/market/appfilters/730"
QUERY_BASE_URL_MARKET_SEARCH = r"http://steamcommunity.com/market/search/render"

REQUEST_TIMEOUT = 10

# 1 - Stattrack
# 0 - Normal 
REQUEST_QUALITIES = ["tag_normal", "tag_strange"]

def save_json(filename: str, json_data: dict):
    with open(filename, "w+") as file:
        file.write(json.dumps(json_data))

def get_market_filters(appid: int = 730):
    APP_DETAILS_ENDPOINT = f"https://steamcommunity.com/market/appfilters/{appid}"

    rq = requests.get(APP_DETAILS_ENDPOINT)
    response = json.loads(rq.content.decode("utf-8"))

    return rq.status_code, response

def is_response_valid(response: str):
    return response != None and "results" in response and len(response["results"]) # Check if response if empty

def make_request(offset: int, user_agent: str = "", stattrack: bool = False, weapons: list = [], wears: list = [], collections: list = [], rarities: list = [], qualities: list = [], proxy: str = "", timeout = REQUEST_TIMEOUT):

    if len(proxy):
        proxy_dict = {
            "http": "socks5://" + proxy,
            "https": "socks5://" + proxy,
        }
    else:
        proxy_dict = {
            "http": proxy,
            "https": proxy,
        }

    params = {
        "norender": 1,
        "start": offset,
        "count": 100,
        "q": "",
        "sort_column": "price",
        "sort_dir": "asc",
        "category_730_ItemSet[]": ["any"],
        "category_730_ProPlayer[]": ["any"],
        "category_730_StickerCapsule[]": ["any"],
        "category_730_Tournament[]": ["any"],
        "category_730_TournamentTeam[]": ["any"],
        "category_730_Type[]": ["any"],
        "category_730_Weapon[]": ["any"],
        "category_730_Rarity[]": ["any"],
        "category_730_Quality[]": ["any"],
        "category_730_Exterior[]": ["any"],
        "appid": 730
        }
    
    if isinstance(rarities, list) and len(rarities):
        params["category_730_Rarity[]"] = rarities
    if isinstance(collections, list) and len(collections):
        params["category_730_ItemSet[]"] = collections
    if isinstance(wears, list) and len(wears):
        params["category_730_Exterior[]"] = wears
    if isinstance(weapons, list) and len(weapons):
        params["category_730_Weapon[]"] = weapons
    if stattrack:
        params["category_730_Quality[]"] = ["tag_strange"]
    else:
        params["category_730_Quality[]"] = ["tag_normal"]

    headers = {
        "User-agent": user_agent
    }

    try:
        rq = requests.get(QUERY_BASE_URL_MARKET_SEARCH, proxies=proxy_dict, timeout=timeout, params=params, headers = headers)
        status_code = rq.status_code
        response = json.loads(rq.content.decode("utf-8"))

    except TimeoutError as Err:
        return 408, "Timeout Error"

    except Exception as Err:
        return 404, Err
    else:

        if (status_code == 200 and is_response_valid(response)):
            # print("Request Succeed")
            return 200, response
        if (status_code == 429):
            return 429, "Too Many Requests"
        return 400, "Empty Response" 

    raise "Ah Oh why am I here"

def get_all_results(output_path: str, output_filename: str, proxy_list: list = [], weapons: list = [], user_agent: str = "I love sushi", stattrack: bool = False, collections: list = [],  wears: list = [],rarities: list = [], qualities: list = [], proxy: str = "", timeout = REQUEST_TIMEOUT):
    offset = 0
    total_count = 1
    proxy_index = 0

    while offset < total_count:
        proxy = proxy_list[proxy_index]

        print(f"Proxy: {proxy}")
        
        status_code, response = make_request(offset=offset, proxy=proxy, wears=wears, weapons=weapons, collections=collections, rarities=rarities, qualities=qualities, timeout=timeout)

        print(f"Status Code: {status_code}")

        if status_code == 200:
            total_count = response["total_count"] if response["total_count"] > total_count else total_count

            print(f"Offset: {offset}\tTotal Count: {total_count}")

            filename = f"{output_filename}_{round(offset/100)}.json"
            save_json(output_path + filename, response)

            offset += 100
        elif status_code == 404:
            print(f"Response: {response}")
            print(f"Used proxy: {proxy}")
        elif status_code != 400:
            proxy_index = (proxy_index + 1) % len(proxy_list)
        time.sleep(2)

if __name__ == "__main__":

    rarities = []

    offset = 100

    status_code, data = make_request(offset, rarities=rarities)
    print(status_code)

    if (status_code == 200):
        with open(f"output3.json", "w+") as file:
                file.write(json.dumps(data))