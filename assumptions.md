# Assumptions for the slackr Project
- Emails with the plus `+` delimiter and the period `.` delimiter will be treated as different emails
- The string `"THISISNOTATOKEN"` is not a valid token
- Assuming that a non "valid channel" implies a non existent channel ID except when `InputError` is the only exception.
- Assuming for `channel_leave()` that `InputError` is raised before `AccessError` in the case that the `channel_id` doesn't exist.
