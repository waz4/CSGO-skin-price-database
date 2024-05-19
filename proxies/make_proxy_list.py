# This file makes a proxy list from the proxy list output of webshare.io proxies
import json

def read_json(path_to_file: str):
    with open(path_to_file, "r") as file:
        data = json.loads(file.read())
    return data

output_dir = "../"

proxy_list = read_json("proxy_list.json")["results"]
proxy_list = [f"{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}" for proxy in proxy_list]

with open(output_dir + "proxies.txt", "w+") as file:
    for proxy in proxy_list:
        file.write(f"{proxy}\n")

