import requests
from client_utils import URL, read_json, print_dict

jwt = read_json("./token.json")

username = "krin"
db_traders = False
url = URL + f"/users/delete/{username}?db_traders={db_traders}"

HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

response = requests.delete(url, headers=HEADERS)
data = response.json()

if response.status_code == 200:
    print_dict(data)
else:
    print_dict(data)
