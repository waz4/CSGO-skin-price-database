# CSGO-skin-price-database
This project collects data from the Steam Market, allowing users to store the prices of all CSGO skins at a given moment, like a market snapshot. The collected data is saved into a database for easy access and analysis.

## Features
- Skins relational informaton: Collection, Wear, Rarity
- Pricing by diferent references: Wear, Weapon, Collection, Quality (StatTrack)
- Database Storage: Stores the scraped data in a structured database for efficient retrieval and analysis.
- Extensible: Easily integrate with other tools or expand the functionality as needed.

## Preview

TODO: add video of tool in action

## Requirements
 - Python3.x
 - SQLite3
 - Requests

## Installation process

1. Clone this repository
```bash
git clone https://github.com/waz4/CSGO-skin-price-database.git
```
2. Navigate to project directory
```bash
cd CSGO-skin-price-database
```
3. Instal required dependencies
```bash
pip install -r requirements.txt
```

## Usage
Simply run the build_database.py to go throught the whole process of creating and fetching the data to populate the database
```bash
python3 build_database.py data_base_filename
```

## Pricers
Pricers are used to get the market prices for all the skins, these can filter and subdivide the data which can be usefull for precision.

If the proxy list is very small choose a pricer that divides the data more. Because if the skins price changes substancially during the pricing the skin might be moved to a diferent page of the steam requests and be lost. 

This behaviour can be check for when running  ```DB_loader.load_prices()``` in which it will count how many repeated skins. Each repeated skin means one skin changed price during the queries and swaped place with a skin that was previously received.

## Proxy Recommendations
To avoid being blocked by the Steam Market due to excessive requests, it is highly recommended to use a list of proxies. This will help distribute the requests and reduce the amount of times your IP address put on cooldown.

1. Create a file named `proxies.txt` in the project directory.
2. Add a list of proxy addresses (one per line) to `proxies.txt`.

Example of `proxies.txt`:
```text
proxy1:port
proxy2:port
proxy3:port
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for any bugs, feature requests, or improvements.