import database_files.database as db
import helper_functions.system_test_helper_file as ch
import requests

# Reset the database
def test_reset():
    ch.make_post_request("workspace/reset", {})
    data = requests.get(f"http://127.0.0.1:42069/get/database")
    assert data.json() == {'users': [], 'messages': [], 'channels': []}
