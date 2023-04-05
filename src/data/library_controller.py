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


def create_work(title: str, authors: list[str], genres: list[str], url: str):
    library = get_library()
    tick = library["data"]["id_ticker"]
    library["data"]["id_ticker"] += 1

    library["library"][str(tick)] = {
        "title": title,
        "authors": authors,
        "genres": genres,
        "url": url
    }

    library_file = library_repo().get_contents("library/library.json")
    library_repo().update_file(library_file.path,
                               f"Added {title}", library, library_file.sha)


