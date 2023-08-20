import os
import json
import github
from dotenv import load_dotenv

load_dotenv()

gh = github.Github(os.getenv("GH_API_TOKEN"))


# return data repository
def data_repo() -> github.Repository.Repository:
    return gh.get_repo("Creative-Cave/data")


# return library.json as a dictionary
def get_library() -> dict:
    return json.loads(
        data_repo().get_contents("library/library.json").decoded_content)


# add a work with a title, author, genre and url
def create_work(title: str, author: str, genre: str, url: str, submitter: int) -> int:
    library = get_library()

    tick = library["data"]["id_ticker"]
    library["data"]["id_ticker"] += 1

    library["library"][f"id{tick}"] = {
        "title": title,
        "author": author,
        "genre": genre,
        "url": url,
        "submitted_by": submitter
    }

    return tick
    update_library(library, f"Added #{tick}")


# create a submission for server review
def create_submission(title: str, author: str, genre: str, url: str, submitter: int) -> int:
    library = get_library()

    tick = library["data"]["submission_ticker"]
    library["data"]["submission_ticker"] += 1

    library["submissions"][f"id{tick}"] = {
        "title": title,
        "author": author,
        "genre": genre,
        "url": url,
        "submitted_by": submitter
    }

    update_library(library, f"Added submission #{tick}")
    return tick


# delete a specified submission and optionally update the repo
def delete_submission(sub_id: int, commit_after: bool) -> dict:
    library = get_library()

    del library["submissions"][f"id{sub_id}"]

    if commit_after:
        update_library(library, f"Removed submission #{sub_id}")

    return library


# delete a specified work and optionally update the repo
def delete_work(work_id: int, commit_after: bool) -> dict:
    library = get_library()

    del library["library"][f"id{work_id}"]

    if commit_after:
        update_library(library, f"Removed #{work_id}")


# delete a specified submission and move it to the library
def approve_submission(sub_id: int, new_title: str = None) -> dict:
    library = get_library()

    tick = library["data"]["id_ticker"]
    library["data"]["id_ticker"] += 1

    sub = library["submissions"][f"id{sub_id}"]

    if new_title:
        sub["title"] = new_title

    work = {
        "title": sub["title"],
        "author": sub["author"],
        "genre": sub["genre"],
        "url": sub["url"],
        "submitted_by": sub["submitted_by"]
    }

    library["library"][f"id{tick}"] = work
    del library["submissions"][f"id{sub_id}"]

    update_library(library, f"Approved submission #{sub_id}")

    return sub


# update the repo with a modified version of the current library dict
def update_library(new_library: dict, commit_msg: str) -> None:
    repo = data_repo()
    library_file = repo.get_contents("library/library.json")
    repo.update_file(library_file.path, commit_msg, json.dumps(new_library, indent=4), library_file.sha)
