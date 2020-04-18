# pylint disable=W0105
"""
Resets the workspace state by resetting the database to blank
"""

import database_files.database as db
import os
import shutil

def workspace_reset():
    db.DATABASE = {
        "users": [],
        "messages": [],
        "channels": [],
    }

    # if the user_images directory exists, delete it
    dirname = os.path.dirname(__file__)
    if os.path.exists(f"{dirname}/../database_files/user_images"):
        shutil.rmtree(f"{dirname}/../database_files/user_images")

    return {}


def workspace_reset_messages():
    db.DATABASE["messages"] = []
    return {}