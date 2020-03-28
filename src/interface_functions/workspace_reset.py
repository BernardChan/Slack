"""
Resets the workspace state by resetting the database to blank
"""

import database_files.database as db

def workspace_reset():
    db.DATABASE = {
        "users": [],
        "messages": [],
        "channels": [],
    }
