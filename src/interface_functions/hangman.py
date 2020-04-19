import wikiquote
import random
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
    "active": False,
    "is_winner": False
}

"""


# 1. Get a random quote
# 2. Split each word to create a list of words
# 3. Remove non-letter characters
# 4. Remove words < 5 letters long - probably can't fail since most quotes contain > 5 letter words
# 5. Pick a random word
def generate_word():
    """
    Returns a random word from a random quote by Linus Torvalds
    :return: returns a string containing a random quote
    """

    word_not_found = True
    quote = "foobar"  # default word in case we couldn't find a word
    while word_not_found:
        try:
            quote = random.choice(wikiquote.quotes("Linus Torvalds"))
            print(quote)
            quote = quote.split()
            quote = ["".join(filter(str.isalpha, string)) for string in quote]
            quote = list(filter(lambda x: len(x) > 4, quote))
            quote = random.choice(quote)
            print(quote)
            quote = quote.lower()
            word_not_found = False
        except IndexError:
            print("Couldn't find a word that was at least 5 letters long, trying again")

    return quote


# Gets the details of a hangman game for a given channel
# This includes: mistake, guessed, hangmanWord
# It should retrieve from the database and return the details in a dictionary
def hangman_details(token, channel_id):
    """
    Gets details about the hangman game, including mistakes made, words guessed, and the HangmanWord
    :param token: String for authorised user's identifier
    :param channel_id: Integer for a specific channel
    :return: dictionary containing hangman details
    """
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    return channel["hangman"]


# Starts a game of hangman
# Should mark a channel as having an active hangman game
# Input error if a game is already active
def hangman_start(token, channel_id):
    channel = db.get_channels_by_key("channel_id", channel_id)[0]

    if channel["hangman"]["active"]:
        raise InputError("Hangman Game already active")

    channel["hangman"] = {
        "mistake": 0,
        "guessed": [" "],
        "hangmanWord": generate_word(),
        "guess": "",
        "active": True,
        "is_winner": False
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

    if not guess_letter or not str.isalpha(guess_letter):
        raise InputError("Incorrect letter passed in")

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

    if hasWonHangman(hangman["hangmanWord"], hangman["guessed"]):
        hangman["is_winner"] = True

    return hangman
