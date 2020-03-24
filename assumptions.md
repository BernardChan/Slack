# Assumptions for the slackr Project

## General Assumptions
- The string `"INVALIDTOKEN"` is not a valid token
- Assume that any data is not persistent between function calls for tests
- Assume that the first person to register is the owner of the slakr
- Assume that -100000 is an invalid user_id and channel_id
- The string `"INVALIDUID"` is not a valid user_id

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

## `channels_create()`
- Assume that user joins channel immediately becomes channel owner and a member

## `search()`
- Assume that search() is case sensitive
- Assume that an empty string will return everything
- Assume that having a search string that contains the same words does not return a match, or searching with a superset of the string
    - e.g. searching "hello world" will not match "the world is hello" or "hello"
- Assume that 👌🏻 and 👌 are different (different emoji skin modifiers)

## `user_profile()`
- Assume that user1 can request profile information of user2

## `user_profile_setname()`
- ".", "+", "=" and other symbols can be in a name as long as they are in a string
- Names with numbers in them are valid
- Names with special characters ("\n", "\t", etc.) are valid names as long as they are in a string
- "Between 1 and 50 characters" in project spec is inclusive (includes names with 1 and 50 characters)
- Assume that two users can have the same names

## `user_profile_sethandle()`
- Assume that special characters ("\n", "\t") can be used in a handle
- Assume that "between 3 and 20 characters" is inclusive of 3 and 20.

## `user_profile_setemail()`
- Assume that emails with the period `.` delimiter will be treated as different emails
- Assume that a user CANNOT set their email again to their current email - considers it in use by another user
