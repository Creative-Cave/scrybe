import os
import requests
import json
import github
from dotenv import load_dotenv

load_dotenv()

gh = github.Github(os.getenv("GH_API_TOKEN"))

# return data repository
def data_repo() -> github.Repository.Repository:
    return gh.get_repo("Creative-Cave/data")


# return pronouns_page.json as a dictionary
def get_pronouns_page() -> dict:
    return json.loads(
        data_repo().get_contents("users/pronouns_page.json").decoded_content)


# add a pronouns.page username
def add_pp_username(user_id: int, pp_username: str) -> None:
    repo = data_repo()
    pronouns_page = get_pronouns_page()

    pronouns_page[str(user_id)] = pp_username
    pronouns_page_file = repo.get_contents("users/pronouns_page.json")
    repo.update_file(pronouns_page_file.path, f"Added @{pp_username}", json.dumps(pronouns_page, indent=4), pronouns_page_file.sha)


# get a pronouns.page username
def get_pp_username(user_id: int) -> str | None:
    pronouns_page = get_pronouns_page()

    if str(user_id) in pronouns_page.keys():
        return pronouns_page[str(user_id)]
    else:
        return None


# remove a pronouns.page username
def remove_pp_username(user_id: int) -> None:
    repo = data_repo()
    pronouns_page = get_pronouns_page()

    del pronouns_page[str(user_id)]
    pronouns_page_file = repo.get_contents("users/pronouns_page.json")
    repo.update_file(pronouns_page_file.path, f"Removed {user_id}", json.dumps(pronouns_page, indent=4), pronouns_page_file.sha)


def get_user_if_exists(username: str) -> dict | None:
    r = requests.get(f"https://en.pronouns.page/api/profile/get/{username}?version=2")
    json = r.json()

    if "id" not in json.keys():
        return None
    else:
        return json


def get_pronouns(username: str) -> dict | None:
    json = get_user_if_exists(username)

    if not json:
        return None
    else:
        return json["profiles"]["en"]["pronouns"]
