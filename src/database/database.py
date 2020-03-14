# Example DATABASE shown at the bottom of the file
# Gives 2 functions to save and restore the DATABASE from database.py

import pickle

DATABASE = {
    "users": [],
    "messages": [],
    "channels": [],
}


# Saves the current database
def pickle_database():
    with open("database.p", "wb") as FILE:
        pickle.dump(DATABASE, FILE)


# Restores the database from last save
def unpickle_database():
    global DATABASE
    DATABASE = pickle.load(open("database.p", "rb"))


# Example formatting of "users" - added an additional key, "token", to the "users" data type
# DATABASE = {
#     "users": [
#         {
#             "token": "fake token",
#             "u_id": 0,
#             "name_first": "Toshi",
#             "name_last": "Tabata",
#         },
#         {
#             "token": "INVALID",
#             "u_id": 1,
#             "name_first": "Hayden",
#             "name_last": "Smith",
#         }
#     ]
# }
