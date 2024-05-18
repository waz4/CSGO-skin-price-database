import requests, os, json

# For my use I dont want items matching these paterns
UNWANTED_ITEMS = ["karambit", "knife", "bayonet", "shadow daggers", "gloves"]

def verify_dir_exists(dir_to_check: str):
    if not os.path.exists(dir_to_check):
        os.makedirs(dir_to_check)

def make_request():
    rq = requests.get(r"https://bymykel.github.io/CSGO-API/api/en/skins.json")
    return rq.status_code, rq.content.decode("utf-8")

def save_skins(output_dir: str, output_filename: str, content: dict):
    verify_dir_exists(output_dir)
    with open(f"{output_dir}{output_filename}", "w+") as file:
        file.write(json.dumps(content) )

def remove_unwanted_items(response):
    data = json.loads(response)
    new_data = []
    for i, result in enumerate(data):
        if not any([knife_name in result["name"].lower() for knife_name in UNWANTED_ITEMS]):
            new_data.append(result)
        else:
            print(f"Removed '{result['name']} at index {i}")
        
    # print(data)
    return new_data
    
def get_base_skins(output_dir: str, output_filename: str):
    status_code, response = make_request()
    if (status_code != 200):
        return False
    data = remove_unwanted_items(response)
    save_skins(output_dir, output_filename, data)
    return True

if __name__ == "__main__":
    output_dir = r"data_to_load/"
    output_filename = r"base_skins.json"
    
    get_base_skins(output_dir, output_filename)
    print("Finished")