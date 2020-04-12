from error import InputError
import database_files.database_retrieval as db

# TODO: add a route for hangman stuffs
# TODO: error checking
"""
channels[channel:{"hangman":
{
    "mistake": 0,
    "guessed": [" "],  # letters that have been guessed
    "hangmanWord": "word",
    "guess": guessLetter,  # currently guessed letter
    "active": False
}

"""


def generate_word():
    return "footbarf"


# Gets the details of a hangman game for a given channel
# This includes: mistake, guessed, hangmanWord
# It should retrieve from the database and return the details in a dictionary
def hangman_details(token, channel_id):
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    return channel["hangman"]


# Starts a game of hangman
# Should mark a channel as having an active hangman game
# Input error if a game is already active
# TODO: determine if this is necessary
def hangman_start(token, channel_id):
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    if channel["hangman"]["active"]:
        raise InputError("Hangman Game already active")

    channel["hangman"] = {
        "mistake": 0,
        "guessed": [" "],
        "hangmanWord": generate_word(),
        "guess": "",
        "active": True
    }

    return channel["hangman"]


def hasWonHangman(hangman_word, guesses):
    for letter in hangman_word:
        if letter not in guesses:
            return False

    return True


# Adds the guessLetter (character) to the hangman dictionary
# Calculates the mistake value and number of guesses
def hangman_guess(token, channel_id, guess_letter):
    channel = db.get_channels_by_key("channel_id", channel_id)

    # Raise errors
    hangman = channel[0]["hangman"]
    if not hangman["active"]:
        raise InputError("Please start a hangman game first")

    if guess_letter in hangman["guessed"]:
        raise InputError("You have already guessed this letter")

    # Add guess_letter to the guessed string
    hangman["guessed"] += guess_letter

    # If the guess_letter was not in the hangmanWord, increase mistake
    if guess_letter not in hangman["hangmanWord"]:
        hangman["mistake"] += 1

    # Set the current guess to guess_letter
    hangman["guess"] = guess_letter

    # if we have 10 mistakes, end the game
    if hangman["mistake"] >= 10 or hasWonHangman(hangman["hangmanWord"], hangman["guessed"]):
        hangman["active"] = False

    # TODO: check if we have guessed the word already

    return hangman
