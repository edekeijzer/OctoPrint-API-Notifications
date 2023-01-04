# OctoPrint Notification API
Adds an API endpoint to OctoPrint to show notifications from external sources

## Setup
Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/edekeijzer/OctoPrint-Notification-API/archive/main.zip

## Usage
Generate an API key under ***Application Keys*** in settings and use some method to post a message against the API endpoint ```/api/plugin/notifications```

Key | Type | Required | Description
-- | -- | -- | --
`command` | `string` | `true` | This has to be `notify` or `remove`.
`message` | `string` | `true` | The message body that will be shown in the pop-up
`title` | `string` | `false` | The title on the pop-up. Default: Notification
`type` | `string` | `false` | The type of pop-up message shown. Possible values: `error`, `notice`, `success`, `info`. Default: info
`timeout` | `int` | `false` | The amount of (milli)seconds after which the message will automatically disappear. A value of 1000 or greater will be interpreted as milliseconds. Default: 10 seconds
`persist` | `bool` | `false` | Should the message be persisted until explicitly marked as read? Default: false
`id` | `string` | | Required for remove, optional for notify.

## Persistent notification
When a message is posted with persist=true, it will be saved in memory until it is removed again. This will make the pop-up reappear each time the UI is reloaded, until the _Mark read_ button is clicked, or otherwise removed through the API.
Each message in the cache has a unique ID. This can be auto generated or you can specify an ID when posting your message so an existing message in the cache will be overwritten. You do not want to have an automated check for updates on your system to report the number of available updates each hour and have to click away 100 pop-ups after four days..

## Examples
POST body examples:
```json
{
    "command": "notify",
    "message": "This is an example of a pop-up message through the notifications API endpoint.",
    "title": "Example",
    "type": "success",
    "timeout": 30,
    "persist": true,
    "id": "my_unique_message_id"
}
```

```json
{
    "command": "remove",
    "message": "This is an example of a pop-up message through the notifications API endpoint.",
    "title": "Example",
    "type": "success",
    "timeout": 30
}
```

A simple example script using curl could look like this:
```sh
#!/bin/sh
OCTO_HOST='http://localhost:5000'
API_KEY='myapikey'
/usr/bin/curl -s -H 'Content-Type: application/json' -H "X-API-Key: ${API_KEY}" -X POST -d "{\"command\":\"notify\",\"message\":\"This is an example of a pop-up message through the notifications API endpoint, which will be overwritten.\",\"title\":\"Example\",\"type\":\"info\",\"timeout\":30,\"persist\":true,\"id\":\"example_message\"}" ${OCTO_HOST}/api/plugin/notifications
```

## Support
Please check your logs first. If they do not explain your issue, open an issue in GitHub. Please set ```octoprint.plugins.notification_api``` to ```DEBUG``` and include the relevant logs. Feature requests are welcome as well.

## Todo
- [ ] Add buttons to execute actions
- [ ] Add a status panel to send messages to