# Assumptions for the slackr Project
- Emails with the period `.` delimiter will be treated as different emails
- The string `"INVALIDTOKEN"` is not a valid token
- Assuming that a non "valid channel" implies a non existent channel ID except when `InputError` is the only exception.
- Assuming for `channel_leave()` that `InputError` is raised before `AccessError` in the case that the `channel_id` doesn't exist.
- Assume that slackr owners are not part of every channel by default (e.g. if another member creates a channel, private OR public, then owner is NOT automatically added)
- Assume that any data is not persistent between function calls for tests
- Assume that AccessError is thrown when user is not authorised (token invalidated)