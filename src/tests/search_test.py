# Testing search function

# Dependencies:
#   message_send()
#   auth_register

# Tested:
#   searching for exact match and substrings (numbers, letters, both)
#       for start/end/middle of the message
#   search for different capitalisations
#   search with empty string
#   search with no matches
#   search for symbols
#   search for emoji
#   search for reserved characters/escaped characters (\n, \b, \, ', ")

# Note: chose to keep asserts outside of the is_correct_message() function to make its purpose clearer and to stand out

from interface_functions.other import search
from interface_functions.message import message_send as send
import helper_functions.test_helper_file as ch
from helper_functions.test_helper_file import chan_owner_token as token
from helper_functions.test_helper_file import chan_owner_id as id
from helper_functions.test_helper_file import private_channel_id as private_id
from helper_functions.test_helper_file import channel_id as public_id
from interface_functions.workspace_reset import workspace_reset_messages, workspace_reset

# Returns boolean on whether the messages returned match exactly the given msg_IDs list
def is_correct_message(messages, msg_IDs):
    # check that the message and amount of messages matches the msg_IDs list
    
    input_message_IDs = [message["message_id"] for message in messages["messages"]]
    return set(input_message_IDs) == set(msg_IDs)


# Search for messages with exactly the string given
def test_search_exactly_substring():
    
    ch.init_helper()
    msg_IDs = []
    
    # Send to both private and public and check that both are returned by search()
    msg_IDs.append(send(token, public_id, "hello")["message_id"])
    msg_IDs.append(send(token, private_id, "hello")["message_id"])
    assert(is_correct_message(search(token, "hello"), msg_IDs))
    msg_IDs = []
    # Test with a message with numbers
    msg_IDs.append(send(token, public_id, "123hi")["message_id"])
    msg_IDs.append(send(token, private_id, "123hi")["message_id"])
    assert (is_correct_message(search(token, "123hi"), msg_IDs))
    msg_IDs = []
    # Test with a message containing exactly only numbers
    msg_IDs.append(send(token, public_id, "123454321")["message_id"])
    msg_IDs.append(send(token, private_id, "123454321")["message_id"])
    assert (is_correct_message(search(token, "123454321"), msg_IDs))


# Messages containing part of the string
def test_search_substring():
    workspace_reset_messages()
    msg_IDs = []


    # Test searching for a substring of the message
    msg_IDs.append(send(token, public_id, "helloworld")["message_id"])
    msg_IDs.append(send(token, private_id, "helloworld")["message_id"])
    
    assert (is_correct_message(search(token, "hello"), msg_IDs))

    # Search for other parts of the string
    assert (is_correct_message(search(token, "llowo"), msg_IDs))
    assert (is_correct_message(search(token, "orld"), msg_IDs))
    msg_IDs = []
    workspace_reset_messages()
    # Search for a substring of numbers only
    msg_IDs.append(send(token, public_id, "123454321")["message_id"])
    msg_IDs.append(send(token, private_id, "123454321")["message_id"])
    assert (is_correct_message(search(token, "1234"), msg_IDs))

    # Search for another part of the substring
    assert (is_correct_message(search(token, "4321"), msg_IDs))
    assert (is_correct_message(search(token, "34543"), msg_IDs))
    msg_IDs = []
    workspace_reset_messages()
    # Search for a substring of both numbers and letters
    msg_IDs.append(send(token, public_id, "12hi34")["message_id"])
    msg_IDs.append(send(token, private_id, "12hi34")["message_id"])
    assert (is_correct_message(search(token, "12hi"), msg_IDs))

    # Search for another part of the substring
    assert (is_correct_message(search(token, "hi34"), msg_IDs))
    assert (is_correct_message(search(token, "2hi3"), msg_IDs))


# Messages containing uppercase and lowercase - assumption is that it is case sensitive
# TODO: verify casing assumption after implementation or clarification
def test_search_cases():
    workspace_reset_messages()
    msg_IDs = []

    # Test searching for an exact match
    msg_IDs.append(send(token, public_id, "mY pHoNE dIEd")["message_id"])
    msg_IDs.append(send(token, private_id, "mY pHoNE dIEd")["message_id"])
    assert (is_correct_message(search(token, "mY pHoNE dIEd"), msg_IDs))

    # Search for a substring
    assert (is_correct_message(search(token, "mY pHo"), msg_IDs))

    # Search for end of substring
    assert (is_correct_message(search(token, "dIEd"), msg_IDs))


# Test empty string as search parameter
# Assumption that it returns everything
def test_search_empty():
    workspace_reset_messages()
    msg_IDs = []

    # Test searching for an exact match
    msg_IDs.append(send(token, public_id, "mY pHoNE123 dIEd")["message_id"])
    msg_IDs.append(send(token, private_id, "mY pHoNE123 dIEd")["message_id"])
    assert (is_correct_message(search(token, ""), msg_IDs))


# Search using a query string that doesn't return any results
# Assuming that if a string is a superset or contains similar words, a match is NOT returned
def test_search_no_matches():
    workspace_reset_messages()
    msg_IDs = []

    # Test searching for no matches
    msg_IDs.append(send(token, public_id, "mY pHoNE dIEd")["message_id"])
    msg_IDs.append(send(token, private_id, "mY pHoNE dIEd")["message_id"])
    assert (not is_correct_message(search(token, "shoulda died with it"), msg_IDs))

    # Search using a superset of the message
    assert (not is_correct_message(search(token, "mY pHoNE dIEd LOL"), msg_IDs))


# Test unicode symbols and emojis?
# Search with symbols !@#$%^&*()_+=-\|{}][
def test_search_symbols():
    workspace_reset_messages()
    msg_IDs = []

    # Test searching exactly for symbols
    msg_IDs.append(send(token, public_id, "!@#$%^&*()_+=-':")["message_id"])
    msg_IDs.append(send(token, private_id, "!@#$%^&*()_+=-':")["message_id"])
    assert (is_correct_message(search(token, "!@#$%^&*()_+=-':"), msg_IDs))

    # Search using a subset of the message
    assert (is_correct_message(search(token, "!@#"), msg_IDs))
    assert (is_correct_message(search(token, "-':"), msg_IDs))
    assert (is_correct_message(search(token, "^&*("), msg_IDs))


# Search with escape characters, reserved characters and emojis
# Note: These tests may be better suited for blackbox testing or UI testing since I need to escape the characters myself
def test_search_special_characters():
    workspace_reset_messages()
    msg_IDs = []

    # Search for a message with single quotes: '
    msg_IDs.append(send(token, public_id, "'hello''")["message_id"])
    msg_IDs.append(send(token, private_id, "'hello''")["message_id"])
    assert (is_correct_message(search(token, "'hello"), msg_IDs))
    msg_IDs = []
    workspace_reset_messages()
    # Search for a message with double quotes: "
    msg_IDs.append(send(token, public_id, "\"\"hello\"")["message_id"])
    msg_IDs.append(send(token, private_id, "\"\"hello\"")["message_id"])
    assert (is_correct_message(search(token, "\"\"hello\""), msg_IDs))
    assert (is_correct_message(search(token, "\"\"hello\""), msg_IDs))
    msg_IDs = []
    workspace_reset_messages()
    # Search for a message with escaped characters: \n, \b, \
    msg_IDs.append(send(token, public_id, "hello\\nWo\\brld\\")["message_id"])
    msg_IDs.append(send(token, private_id, "hello\\nWo\\brld\\")["message_id"])
    assert (is_correct_message(search(token, "hello\\nWo\\brld\\"), msg_IDs))
    assert (is_correct_message(search(token, "hello\\nWo\\brld\\"), msg_IDs))
    msg_IDs = []
    workspace_reset_messages()
    # Search for a message with emojis: 👉🏻👌🏻
    # Assume that 👌🏻 and 👌 are different
    msg_IDs.append(send(token, public_id, "👉👌🏻")["message_id"])
    msg_IDs.append(send(token, private_id, "👉👌🏻")["message_id"])
    assert (is_correct_message(search(token, "👉👌🏻"), msg_IDs))
    assert (is_correct_message(search(token, "👉👌🏻"), msg_IDs))
