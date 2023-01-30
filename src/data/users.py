import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
gh_auth = os.getenv("GH_API_TOKEN")

gist_id = "d4d1d84466b5298d877aed2823afe5c9"

def get_user_balance(id: int):
    ...

def get_user_pronouns(id: int) -> list | None:
    request = requests.get(f"https://api.github.com/gists/{gist_id}")
    rcontent = json.loads(request.content)
    users = json.loads(rcontent["files"]["wc_users.json"]["content"])
    try:
        return users[str(id)]["pronouns"]
    except KeyError:
        return None
