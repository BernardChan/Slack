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

from other import search
from message import message_send as send
from helper_functions.channel_helpers import chan_owner_token as token
from helper_functions.channel_helpers import chan_owner_token as id
from helper_functions.channel_helpers import chan_owner_token as private_id


# Returns boolean on whether the messages returned match exactly the given msg_IDs list
def is_correct_message(messages, msg_IDs):

    # check that the message and amount of messages matches the msg_IDs list
    for message in messages["messages"]:
        try:
            msg_IDs.remove(message["message_id"])
        except ValueError:
            return False

    if len(msg_IDs) == 0:
        return True
    else:
        return False


# Search for messages with exactly the string given
def test_search_exactly():
    msg_IDs = []

    # Send to both private and public and check that both are returned by search()
    msg_IDs += send(token, id, "hello")
    msg_IDs += send(token, private_id, "hello")
    assert(is_correct_message(search(token, "hello"), msg_IDs))

    # Test with a message with numbers
    msg_IDs = send(token, id, "123hi")
    msg_IDs += send(token, private_id, "123hi")
    assert (is_correct_message(search(token, "123hi"), msg_IDs))

    # Test with a message containing exactly only numbers
    msg_IDs = send(token, id, "123454321")
    msg_IDs += send(token, private_id, "123454321")
    assert (is_correct_message(search(token, "123454321"), msg_IDs))


# Messages containing part of the string
def test_search_substring():
    msg_IDs = []

    # Test searching for a substring of the message
    msg_IDs += send(token, id, "helloworld")
    msg_IDs += send(token, private_id, "helloworld")
    assert (is_correct_message(search(token, "hello"), msg_IDs))

    # Search for other parts of the string
    assert (is_correct_message(search(token, "llowo"), msg_IDs))
    assert (is_correct_message(search(token, "orld"), msg_IDs))

    # Search for a substring of numbers only
    msg_IDs = send(token, id, "123454321")
    msg_IDs += send(token, private_id, "123454321")
    assert (is_correct_message(search(token, "1234"), msg_IDs))

    # Search for another part of the substring
    assert (is_correct_message(search(token, "4321"), msg_IDs))
    assert (is_correct_message(search(token, "34543"), msg_IDs))

    # Search for a substring of both numbers and letters
    msg_IDs = send(token, id, "12hi34")
    msg_IDs += send(token, private_id, "12hi34")
    assert (is_correct_message(search(token, "12hi"), msg_IDs))

    # Search for another part of the substring
    assert (is_correct_message(search(token, "hi34"), msg_IDs))
    assert (is_correct_message(search(token, "2hi3"), msg_IDs))


# Messages containing uppercase and lowercase - assumption is that it is case sensitive
# TODO: verify casing assumption after implementation or clarification
def test_search_cases():
    msg_IDs = []

    # Test searching for an exact match
    msg_IDs += send(token, id, "mY pHoNE dIEd")
    msg_IDs += send(token, private_id, "mY pHoNE dIEd")
    assert (is_correct_message(search(token, "mY pHoNE dIEd"), msg_IDs))

    # Search for a substring
    assert (is_correct_message(search(token, "mY pHo"), msg_IDs))

    # Search for end of substring
    assert (is_correct_message(search(token, "dIEd"), msg_IDs))


# Test empty string as search parameter
# Assumption that it returns everything
def test_search_empty():
    msg_IDs = []

    # Test searching for an exact match
    msg_IDs += send(token, id, "mY pHoNE123 dIEd")
    msg_IDs += send(token, private_id, "mY pHoNE123 dIEd")
    assert (is_correct_message(search(token, ""), msg_IDs))


# Search using a query string that doesn't return any results
# Assuming that if a string is a superset or contains similar words, a match is NOT returned
def test_search_no_matches():
    msg_IDs = []

    # Test searching for no matches
    msg_IDs += send(token, id, "mY pHoNE dIEd")
    msg_IDs += send(token, private_id, "mY pHoNE dIEd")
    assert (not is_correct_message(search(token, "shoulda died with it"), msg_IDs))

    # Search using a superset of the message
    assert (not is_correct_message(search(token, "mY pHoNE dIEd LOL"), msg_IDs))


# Test unicode symbols and emojis?
# Search with symbols !@#$%^&*()_+=-\|{}][
def test_search_symbols():
    msg_IDs = []

    # Test searching exactly for symbols
    msg_IDs += send(token, id, "!@#$%^&*()_+=-':")
    msg_IDs += send(token, private_id, "!@#$%^&*()_+=-':")
    assert (is_correct_message(search(token, "!@#$%^&*()_+=-':"), msg_IDs))

    # Search using a subset of the message
    assert (is_correct_message(search(token, "!@#"), msg_IDs))
    assert (is_correct_message(search(token, "-':"), msg_IDs))
    assert (is_correct_message(search(token, "^&*("), msg_IDs))


# Search with escape characters, reserved characters and emojis
# Note: These tests may be better suited for blackbox testing or UI testing since I need to escape the characters myself
def test_search_special_characters():
    msg_IDs = []

    # Search for a message with single quotes: '
    msg_IDs += send(token, id, "'hello''")
    msg_IDs += send(token, private_id, "'hello''")
    assert (is_correct_message(search(token, "'hello"), msg_IDs))

    # Search for a message with double quotes: "
    msg_IDs = send(token, id, "\"\"hello\"")
    msg_IDs += send(token, private_id, "\"\"hello\"")
    assert (is_correct_message(search(token, "\"\"hello\""), msg_IDs))
    assert (is_correct_message(search(token, "\"\"hello\""), msg_IDs))

    # Search for a message with escaped characters: \n, \b, \
    msg_IDs = send(token, id, "hello\\nWo\\brld\\")
    msg_IDs += send(token, private_id, "hello\\nWo\\brld\\")
    assert (is_correct_message(search(token, "hello\\nWo\\brld\\"), msg_IDs))
    assert (is_correct_message(search(token, "hello\\nWo\\brld\\"), msg_IDs))

    # Search for a message with emojis: 👉🏻👌🏻
    # Assume that 👌🏻 and 👌 are different
    msg_IDs = send(token, id, "👉👌🏻")
    msg_IDs += send(token, private_id, "👉👌🏻")
    assert (is_correct_message(search(token, "👉👌🏻"), msg_IDs))
    assert (is_correct_message(search(token, "👉👌🏻"), msg_IDs))
