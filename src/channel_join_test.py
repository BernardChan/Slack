# Tests for the channel_join() function in channel.py

import pytest
import channels as chs
import channel as ch
from channel import channel_leave as leave
import auth
from error import InputError, AccessError
import channel_helpers


