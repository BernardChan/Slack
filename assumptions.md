# Assumptions for the slackr Project

## General Assumptions
- The string `"INVALIDTOKEN"` is not a valid token
- Assume that any data is not persistent between function calls for tests
- Assume that the first person to register is the owner of the slakr
- Assume that -100000 is an invalid user_id and channel_id

## `auth_register()`
- Emails with the period `.` delimiter will be treated as different emails

## `channel_join()`
- Assuming that a non "valid channel" implies a non existent channel ID except when `InputError` is the only exception.
- Assume nothing happens if the channel owner or channel member tries to channel_join() a channel they are part of

## `channel_leave()`
- Assuming that `InputError` is raised before `AccessError` in the case that the `channel_id` doesn't exist.

## `channel_addowner()`
- Assume that slackr owners are not part of every channel by default (e.g. if another member creates a channel, private OR public, then owner is NOT automatically added)
- Assume that AccessError is thrown when user is not authorised (token invalidated)
- Assume that channel_addowner will also add the user to the channel if they were not already a part of it

## `channel_removeowner()`
- Assume that not having a channel owner is fine

## `search()`
- Assume that search() is case sensitive
- Assume that an empty string will return everything
- Assume that having a search string that contains the same words does not return a match, or searching with a superset of the string
    - e.g. searching "hello world" will not match "the world is hello" or "hello"
- Assume that 👌🏻 and 👌 are different (different emoji skin modifiers)

## `user_profile_sethandle()`
- Assume that special characters ("\n", "\t") can be used in a handle
