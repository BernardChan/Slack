# File for functions to interface with the database
# Avoid directly accessing database since implementation/structure may change (A G I L E LUL)
# Basically lets us work on our functions without
#   having to wait for everyone to agree on a database structure

import database_files.database as db


# returns all messages from a given channel_id
def get_channel_messages(channel_id):
    return []


def get_channels():
    return []
