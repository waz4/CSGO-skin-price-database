import requests, json, os
from dotenv import load_dotenv

def save_json(filename: str, json_data: dict):
    with open(filename, "w+") as file:
        file.write(json.dumps(json_data))

load_dotenv()

PROXY_LIST_ENDPOINT = r"https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=25"
WEBSHARE_API_KEY = os.environ.get("WEBSHARE_API_KEY")
 
rq = requests.get(
    PROXY_LIST_ENDPOINT,
    headers={"Authorization": WEBSHARE_API_KEY}
)
status_code = rq.status_code
response = json.loads(rq.content.decode("utf-8"))

print(f"Request status: {status_code}")

if status_code == 200:
    save_json("proxy_list.json", response)