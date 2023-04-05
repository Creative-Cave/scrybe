import os
import json
import github
from dotenv import load_dotenv

load_dotenv()

gh = github.Github(os.getenv("GH_API_TOKEN"))

def library_repo() -> github.Repository.Repository:
    return gh.get_repo("Writers-Cave/data")

def get_library() -> dict:
    return json.loads(library_repo().get_contents("library/library.json").decoded_content)
