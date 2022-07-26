import requests
from client_utils import URL, read_json, print_dict

jwt = read_json("./token.json")
username = "pauline"

db_traders = bool(input("You are a trader?:"))

url = URL + f"/users/{username}?trader={db_traders}"
HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

response = requests.get(url, headers=HEADERS)
data = response.json()

if response.status_code == 200:
    print_dict(data)
else:
    print_dict(data)
