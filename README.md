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
`command` | `string` | `true` | This has to be `notify`, this currently is the only command our API endpoint understands
`message` | `string` | `true` | The message body that will be shown in the pop-up
`title` | `string` | `false` | The title on the pop-up. Default: Notification
`type` | `string` | `false` | The type of pop-up message shown. Possible values: `error`, `notice`, `success`, `info`. Default: info
`timeout` | `int` | `false` | The amount of (milli)seconds after which the message will automatically disappear. A value of 1000 or greater will be interpreted as milliseconds, use 0 to keep the pop-up indefinitely. Default: 10 seconds

POST body example:
```json
{
    "command": "notify",
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
/usr/bin/curl -s -H 'Content-Type: application/json' -H "X-API-Key: ${API_KEY}" -X POST -d "{\"command\":\"notify\",\"message\":\"This is an example of a pop-up message through the notifications API endpoint.\",\"title\":\"Example\",\"type\":\"info\",\"timeout\":30}" ${OCTO_HOST}/api/plugin/notifications
```

## Known issue
An API call will trigger an action in the OctoPrint frontend. If, however, no frontend is currently active, there is no mechanism that will show the pop-up at a later time. This might be addressed by adding notifications to the status panel sidebar.

## Support
Please check your logs first. If they do not explain your issue, open an issue in GitHub. Please set ```octoprint.plugins.notification_api``` to ```DEBUG``` and include the relevant logs. Feature requests are welcome as well.

## Todo
- [ ] Add buttons to execute system actions
- [ ] Support callback commands
- [ ] Show persistent messages in the status panel