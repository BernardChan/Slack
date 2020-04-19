"""
File for the database for the Slackr server and functions to pickle and unpickle it
"""
import pickle
import time
from pathlib import Path

# pylint: disable=W0105 #pointless-string-statement
# pylint: disable=W0603 #global-statement

# Dictionary for all data to be contained within the server
DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}

# File path for the pickled file
PICKLED_FILE = Path(__file__).parent/'database.p'


# Saves the current database_files
def pickle_database():
    """
    Saves the database in a pickled file
    :return: returns nothing
    """
    global DATABASE
    with open(PICKLED_FILE, "wb+") as files:
        pickle.dump(DATABASE, files)


# Restores the database_files from last save
def unpickle_database():
    """
    Retrieves the database from the pickled file
    :return: returns nothing
    """
    global DATABASE
    try:
        with open(PICKLED_FILE, "rb") as files:
            DATABASE = pickle.load(files)
    except FileNotFoundError:
        pickle_database()


def pickle_database_routinely(length):
    """
    Pickles the database every length seconds
    :param length: integer for number of seconds between file pickling
    :return: returns nothing
    """
    while True:
        pickle_database()
        print("pickling database")
        time.sleep(length)
