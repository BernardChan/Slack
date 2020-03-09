# Channel_invite(token, channel_id, u_id): test

# Dependancies:
    # user_profile()
    # auth_register()
    # channel_details()

import pytest
from channel import channel_invite
from channel import channel_details
from channels import channels_create
from auth import auth_register
from user import user_profile
from error import InputError, AccessError

import sys
sys.path.append('../')

Tests to check
    # register, channel create, channel invite success
    # register, channel create, channel invite success with additional person
    # channel invite without tokens
    # channel invite to a non member access error
    # channel invite no channel existing

def test_channel_invite_success():
    register1 = auth_register("bill.gates@microsoft.com", "123456", "Bill", "Gates")
    login1 = auth_login("bill.gates@microsoft.com", "123456")
    channel1 = channels_create(login1["token"], "Channel_name", True)
    channel_invite(login1["token"], channel1["channel_id"], login["u_id"]
