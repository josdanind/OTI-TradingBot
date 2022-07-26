import requests
from client_utils import URL, read_json, print_dict

jwt = read_json("./token.json")
HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

db_traders = bool(input("Search in the trader table?: "))

url = URL + f"/users?db_traders={db_traders}"

response = requests.get(url, headers=HEADERS)
content = response.json()

if response.status_code == 200:
    print(content)
else:
    print_dict(content)
