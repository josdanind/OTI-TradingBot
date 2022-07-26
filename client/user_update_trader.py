import requests
from client_utils import URL, read_json, print_dict

jwt = read_json("./token.json")
username = "michelle"
url = URL + f"/users/update/trader/{username}"
HEADERS = {"Authorization": f"{jwt['token_type']} {jwt['access_token']}"}

update = {
    # "username": "string",
    # "position": "Gerente",
    # "email": "judith@example.com",
    "password": "michelle1234",
    # "first_name": "MICHELLE",
    # "last_name": "Navarrete Díaz",
    # "birth_date": "string",
    # "access_level": 1,
}

response = requests.put(url, json=update, headers=HEADERS)
data = response.json()

print_dict(data)
