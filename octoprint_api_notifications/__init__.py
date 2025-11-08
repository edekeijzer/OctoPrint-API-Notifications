# coding=utf-8
from __future__ import absolute_import
import json
from uuid import uuid1 as uuid

__author__ = "Erik de Keijzer <erik@fscker.nl>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2025 Erik de Keijzer - Released under terms of the AGPLv3 License"

import octoprint.plugin

class API_Notifications(
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
        msg_types = ['notice','error','info','success']

        msg_text = data['message']

        if 'title' in data.keys():
            msg_title = data['title']
        else:
            msg_title = 'Notification'

        msg_type = None
        # If we received a msg_type, put it in var
        if 'type' in data.keys():
            msg_type = data['type']
        # If our type is None, it won't be in our valid types either
        if not (msg_type in msg_types):
            # If we did receive a msg_type, it apparently wasn't valid
            if msg_type:
                self._logger.warning(f"Unknown type {msg_type}, reverting to 'info'.`nValid types: {','.join(msg_types)}")
            else:
                self._logger.info(f"No type specified, reverting to 'info'.`nValid types: {','.join(msg_types)}")
            msg_type = 'info'

        msg_id = data['id']
        self._logger.debug(f"Message ID: {msg_id}")

        if 'delay' in data.keys():
            msg_delay = data['delay']
            if msg_delay < 1000:
                msg_delay = msg_delay * 1000
        elif msg_id is not None:
            msg_delay = 0
        else:
            msg_delay = 10000
        self._logger.debug(f"Delay set to {str(msg_delay)}")

        self._plugin_manager.send_plugin_message(self._identifier, dict(msg_id=msg_id, msg_text=msg_text, msg_title=msg_title, msg_type=msg_type, msg_delay=msg_delay))
        self._logger.debug(f"Message sent to {self._identifier}")


    ##~~ SimpleApiPlugin
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
                self.cached_notifications[msg_id] = data
                self._logger.debug(f"Message added to persistence cache as {msg_id}")
            else:
                msg_id = None
                self._logger.debug("Persistence was not requested")
            data['id'] = msg_id

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
            _api_commands = self.get_api_commands()
            self._logger.info(f"Unknown command {command}. Valid commands: {_api_commands.keys()}")


    def on_api_get(self, request):
        return "/api/plugin/api_notifications only has POST endpoints, please check documentation."


    ##~~ AssetPlugin
    def get_assets(self):
        return dict(js=["js/ApiNotifications.js"])


    ##~~ TemplatePlugin
    def is_template_autoescaped(self):
        return True


    def get_update_information(self):
        return dict(
            notification_api=dict(
                displayName="API Notifications",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="edekeijzer",
                repo="OctoPrint-API-Notifications",
                current=self._plugin_version,

                # update method: pip w/ dependency links
                pip="https://github.com/edekeijzer/OctoPrint-API-Notifications/archive/{target_version}.zip"
            )
        )


__plugin_name__ = "API Notifications"
__plugin_pythoncompat__ = ">=3,<4"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = API_Notifications()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }