import requests
from client_utils import URL, read_json, print_dict

jwt = read_json("./token.json")
username = "pauline"
url = URL + f"/users/update/user/{username}"
HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

update = {
    # "username": "string",
    # "email": "louella@example.com",
    "password": "pauline",
    # "first_name": "PAULINE",
    # "last_name": "ROGERS",
    # "birth_date": "string",
}

response = requests.put(url, json=update, headers=HEADERS)

print_dict(response.json())
