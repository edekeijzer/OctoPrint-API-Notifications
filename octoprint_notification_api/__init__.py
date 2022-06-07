# coding=utf-8
from __future__ import absolute_import
import json

__author__ = "Erik de Keijzer <erik@fscker.nl>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2022 Erik de Keijzer - Released under terms of the AGPLv3 License"

import octoprint.plugin

class Notification_API(
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.RestartNeedingPlugin,
):

    def get_api_commands(self):
        return dict(
            notify=["message"],
        )

    def on_api_command(self, command, data):
        self._logger.debug("Command {} was received".format(command))
        _msg_levels = ['notice','error','info','success']
        if command == "notify":
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
            if not (msg_level in _msg_levels):
                # If we did receive a msg_level, it apparently wasn't valid
                if msg_level:
                    _msg_levels = ','.join(_msg_levels)
                    self._logger.warning("Unknown type {}, reverting to 'info'.`nValid types: {}".format(msg_level, _msg_levels))
                msg_level = 'info'

            if 'timeout' in data.keys():
                msg_timeout = data['timeout'] * 1000
            else:
                msg_timeout = 0
            self._logger.info("{} was called with message {}".format(command,message))
            self._plugin_manager.send_plugin_message(self._identifier, dict(type='popup', msg_text=msg_text, msg_title=msg_title, level=msg_level, timeout=msg_timeout))


    def on_api_get(self, request):
        return "Usage: POST /api/plugin/notifications {\"command\":\"notify\",\"message\":\"My message\"}"

    ##-- AssetPlugin hooks
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