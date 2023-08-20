import os
import json
import github
from dotenv import load_dotenv

load_dotenv()

DEFAULT_USER_BALANCE = 0

gh = github.Github(os.getenv("GH_API_TOKEN"))


# return data repository
def data_repo() -> github.Repository.Repository:
    return gh.get_repo("Creative-Cave/data")


# return economy.json as a dictionary
def get_economy() -> dict:
    return json.loads(
        data_repo().get_contents("users/economy.json").decoded_content)


# create an "account" for a user and default their balance to DEFAULT_USER_BALANCE
def create_account(user_id: int) -> None:
    economy = get_economy()
    economy[str(user_id)] = DEFAULT_USER_BALANCE
    update_economy(economy, f"Added user - {user_id}")


# adjust a given user's balance (can be negative to deduct money)
def adjust_balance(user_id: int, adjustment: int):
    economy.get_economy()
    economy[str(user_id)] += adjustment
    update_economy(economy, f"Adjusted balance - {user_id}")


# update the repo with a modified version of the current economy dict
def update_economy(new_economy: dict, commit_msg: str) -> None:
    repo = data_repo()
    economy_file = repo.get_contents("users/economy.json")
    repo.update_file(economy_file.path, commit_msg, json.dumps(new_economy, indent=4), economy_file.sha)

