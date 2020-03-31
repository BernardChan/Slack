import helper_functions.test_helper_file as ch
from interface_functions import channel, message


# # NOTE: This is commented out due to having bugged logic
# # Creator of this function is trying to 
# # 1. Delete non existent messages
# # 2. Retrieving messages when there are no messages in the database
# def test_message_remove():
    
#     channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
#     channel_messages_list = channel_messages["messages"]
    
#     m_id = channel_messages_list[0]["message_id"]    
#     mess = channel_messages_list[0]["message"]
    
#     message.message_remove(ch.chan_owner_token, m_id)
    
#     new_channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
#     new_list = new_channel_messages["messages"]
#     assert mess not in new_list

 

"""    Not sure what this is about. Leaving here until we find out
def test_message_send_access_error():
    assert(not ch.is_member(ch.member_id, True))

    # User is not part of the channel, raise AccessError exception
    with pytest.raises(AccessError):
        leave(ch.member_id, ch.channel_id)

    # User does not exist, raise AccessError
    with pytest.raises(AccessError):
        leave("INVALIDTOKEN", ch.channel_id)


# Test if InputError's are raised
# Should raise when:
#   channel_id does not exist
def test_message_send_input_error():

    # Channel does not exist, raise InputError
    with pytest.raises(InputError):
        leave(ch.chan_owner_id, -100000)
"""
    

    
