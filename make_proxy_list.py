# This file makes a proxy list from the proxy list output of webshare.io proxies
from src.DB_loader import read_json

proxy_list = read_json("proxy_list.json")["results"]
proxy_list = [f"{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}" for proxy in proxy_list]

with open("proxies.txt", "w+") as file:
    for proxy in proxy_list:
        file.write(f"{proxy}\n")

