# coding=utf-8
from __future__ import absolute_import
import json
from uuid import uuid1 as uuid

__author__ = "Erik de Keijzer <erik@fscker.nl>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2024 Erik de Keijzer - Released under terms of the AGPLv3 License"

import octoprint.plugin

class Notification_API(
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.RestartNeedingPlugin,
):

    def __init__(self):
        # Add empty storage for caching notifications
        self.cached_notifications = dict()

    def send_notification(self, data):
        msg_levels = ['notice','error','info','success']

        msg_text = data['message']

        if 'title' in data.keys():
            msg_title = data['title']
        else:
            msg_title = 'Notification'

        msg_level = None
        # If we received a msg_level, put it in var
        if 'type' in data.keys():
            msg_level = data['type']
        # If our type is None, it won't be in our valid types either
        if not (msg_level in msg_levels):
            # If we did receive a msg_level, it apparently wasn't valid
            if msg_level:
                self._logger.warning(f"Unknown type {msg_level}, reverting to 'info'.`nValid types: {','.join(msg_levels)}")
            else:
                self._logger.info(f"No type specified, reverting to 'info'.`nValid types: {','.join(msg_levels)}")
            msg_level = 'info'

        msg_id = data['id']
        self._logger.debug(f"Message ID: {msg_id}")

        if 'delay' in data.keys():
            msg_delay = data['delay']
            if msg_delay < 1000:
                msg_delay = msg_delay * 1000
        else:
            msg_delay = 10000
        self._logger.debug(f"Delay set to {str(msg_delay)}")

        self._plugin_manager.send_plugin_message(self._identifier, dict(type='popup', msg_id=msg_id, msg_text=msg_text, msg_title=msg_title, msg_level=msg_level, msg_delay=msg_delay))
        self._logger.debug(f"Message sent to {self._identifier}")

    def get_api_commands(self):
        return dict(
            notify=["message"],
            retrieve=[],
            remove=["id"],
        )

    def on_api_command(self, command, data):
        self._logger.debug(f"Command {command} was received")

        if command == "notify":
            if not 'message' in data.keys():
                self._logger.error("No message text received, unable to continue!")
                return

            self._logger.info(f"{command} was called with message {data['message']}")

            msg_persist = ('persist' in data.keys() and data['persist'] == True)
            if msg_persist:
                if 'id' in data.keys():
                    msg_id = data['id']
                else:
                    msg_id = str(uuid())
                    data['id'] = msg_id
                self.cached_notifications[msg_id] = data
                self._logger.debug(f"Message added to persistence cache as {msg_id}")
            else:
                msg_id = None
                data['id'] = "none"
                self._logger.debug("Persistence was not requested")

            self.send_notification(data)

            if msg_id:
                return msg_id

        elif command == "retrieve":
            for key, message in self.cached_notifications.items():
                self.send_notification(message)

        elif command == "remove":
            msg_id = data['id']
            self._logger.debug(f"Remove {msg_id} from persistent cache")
            try:
                del self.cached_notifications[msg_id]
            except:
                self._logger.debug(f"ID {msg_id} not found in cached messages")
        else:
            self._logger.info(f"Unknown command {command}")

    def on_api_get(self, request):
        return "/api/plugin/notifications only has POST endpoints, please check documentation."

    def get_assets(self):
        return dict(js=["js/NotificationApi.js"])
        
    def get_update_information(self):
        return dict(
            notification_api=dict(
                displayName="Notification API",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="edekeijzer",
                repo="OctoPrint-Notification-API",
                current=self._plugin_version,

                # update method: pip w/ dependency links
                pip="https://github.com/edekeijzer/OctoPrint-Notification-API/archive/{target_version}.zip"
            )
        )

__plugin_name__ = "Notification API"
__plugin_pythoncompat__ = ">=3,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Notification_API()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }