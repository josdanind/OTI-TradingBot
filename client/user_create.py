import requests
from client_utils import URL, read_json, print_dict

jwt = read_json("./token.json")
users = read_json("./users.json")
url = URL + f"/users/signup"
HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

username = "michelle"
role = "trader"

user = users[role][username]
response = requests.post(url, json=user, headers=HEADERS)
data = response.json()

if response.status_code == 201:
    print_dict(data)
else:
    print_dict(data)
