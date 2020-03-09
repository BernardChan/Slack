import message
import helper_functions.channel_helpers as ch
import channel
from error import InputError, AccessError


def test_message_edit():
    if message == "":
        channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
        channel_messages_list = channel_messages["messages"]
        
        m_id = channel_messages_list[0]["message_id"]    
        mess = channel_messages_list[0]["message"]
        
        message.message_remove(ch.chan_owner_token, m_id)
        
        new_channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
        new_list = new_channel_messages["messages"]
        assert mess not in new_list
    else:
        channel_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
        channel_messages_list = channel_messages["messages"]
        m_id = channel_messages_list[0]["message_id"]
        
        message.message_edit(ch.chan_owner_token, m_id, message)
        
        new_messages = channel.channel_messages(ch.chan_owner_token, ch.channel_id, 0)
        new_list = channel_messages["messages"]
        assert new_list[0]["message"] == message
    
    
