import helper_functions.test_helper_file as ch
from interface_functions import channel, message


def test_message_edit():
    if not ch.isFunctionImplemented(message.message_edit, -1, -1, -1):
        return

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
    
    
