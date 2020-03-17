def message_send(token, channel_id, message):
    print(f"message from token {token} to channel_id {channel_id} was: {message}")
    return {
        'message_id': 1,
    }

def message_remove(token, message_id):
    return {
    }

def message_edit(token, message_id, message):
    return {
    }
