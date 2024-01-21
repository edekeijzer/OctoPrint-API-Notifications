# OctoPrint API Notifications
Adds an API endpoint to OctoPrint to show notifications from external sources

## Setup
Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/edekeijzer/OctoPrint-API-Notifications/archive/main.zip

## Usage
Generate an API key under ***Application Keys*** in settings and use some method to post a message against the API endpoint ```/api/plugin/api_notifications```

To post a message:
Key | Type | Required | Description
-- | -- | -- | --
`command` | `string` | `true` | `notify`
`message` | `string` | `true` | The message body that will be shown in the pop-up
`title` | `string` | `false` | The title on the pop-up. Default: Notification
`type` | `string` | `false` | The type of pop-up message shown. Possible values: `error`, `notice`, `success`, `info`. Default: info
`delay` | `int` | `false` | The amount of (milli)seconds after which the message will automatically disappear. A value of 1000 or greater will be interpreted as milliseconds. Default: 10 seconds
`persist` | `bool` | `false` | Should the message be persisted until explicitly marked as read? Default: false
`id` | `string` | `false` | Only used when persist is true. If omitted, an ID will be generated. The ID will be returned with the POST request.

To remove a persistent message:
Key | Type | Required | Description
-- | -- | -- | --
`command` | `string` | `true` | `remove`
`id` | `string` | `true` | The message ID to remove from the cache.

## Persistent notification
When a message is posted with persist=true, it will be saved in memory until it is removed again. This will make the pop-up reappear each time the UI is reloaded, until the _Mark read_ button is clicked, or otherwise removed through the API.
Each message in the cache has a unique ID. This can be auto generated or you can specify an ID when posting your message so an existing message in the cache will be overwritten. You do not want to have an automated check for updates on your system to report the number of available updates each hour and have to click away 100 pop-ups after four days..

## Examples
POST body examples:
```json
{
    "command": "notify",
    "message": "This is an example of a pop-up message through the api_notifications API endpoint.",
    "title": "Example",
    "type": "success",
    "delay": 10,
    "persist": true,
    "id": "my_unique_message_id"
}
```

```json
{
    "command": "remove",
    "message": "This is an example of a pop-up message through the api_notifications API endpoint.",
    "title": "Example",
    "type": "success",
    "delay": 5
}
```

A simple example script using curl could look like this:
```sh
#!/bin/sh
OCTO_HOST='http://localhost:5000'
API_KEY='myapikey'
/usr/bin/curl -s -H 'Content-Type: application/json' -H "X-API-Key: ${API_KEY}" -X POST -d "{\"command\":\"notify\",\"message\":\"This is an example of a pop-up message through the notifications API endpoint, which will be overwritten.\",\"title\":\"Example\",\"type\":\"info\",\"delay\":10,\"persist\":true,\"id\":\"example_message\"}" ${OCTO_HOST}/api/plugin/api_notifications
```

## Support
Please check your logs first. If they do not explain your issue, open an issue in GitHub. Please set ```octoprint.plugins.api_notifications``` to ```DEBUG``` and include the relevant logs. Feature requests are welcome as well.

## Todo
- [ ] Add buttons to execute actions
- [ ] Add a status panel to send messages to

## Known issues
- Any delay larger than 10 seconds doesn't seem to be possible.