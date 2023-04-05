import os
import json
import github
from dotenv import load_dotenv

load_dotenv()

gh = github.Github(os.getenv("GH_API_TOKEN"))


# return details about the data repository
def library_repo() -> github.Repository.Repository:
    return gh.get_repo("Writers-Cave/data")


# return a python dictionary of library.json
def get_library() -> dict:
    return json.loads(library_repo().get_contents("library/library.json").decoded_content)


# add a work with a string title, list of authors, list of genres and a url
def create_work(title: str, authors: list[str], genres: list[str], url: str):
    # get library.json as a dictionary and assign it to library
    library = get_library()

    # get the value of the ticker to get the new work's id, and increment the ticker in preparation for the next work
    tick = library["data"]["id_ticker"]
    library["data"]["id_ticker"] += 1

    # create a dictionary with the id taken from the ticker and assign the given details
    library["library"][str(tick)] = {
        "title": title,
        "authors": authors,
        "genres": genres,
        "url": url
    }

    # get details of the repository and assign it to repo, get the details of the library.json file and push the updated dictionary to github to update it with the new work
    repo = library_repo()
    library_file = repo.get_contents("library/library.json")
    repo.update_file(library_file.path,
                     f"Added {title}", json.dumps(library, indent=4), library_file.sha)
