# coding=utf-8
from __future__ import absolute_import

__author__ = "Erik de Keijzer <erik@fscker.nl>"
__license__ = "GNU Affero General Public License http://www.gnu.org/licenses/agpl.html"
__copyright__ = "Copyright (C) 2022 Erik de Keijzer - Released under terms of the AGPLv3 License"

import octoprint.plugin

class Notification_API(
    octoprint.plugin.SimpleApiPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.RestartNeedingPlugin,
):

    def get_api_commands(self):
        return dict(
            notify=["message"],
        )

    def on_api_command(self, command, data):
        import flask
        if command == "notify":
            if "message" in data:
                message = data['message']
                self._logger.info("{} was called with message {}".format(command,message))
            else:
                self._logger.warning("{} was called without a message!".format(command))
        else:
            self._logger.warning("Unknown command {}".format(command))

    def on_api_get(self, request):
        return flask.jsonify(foo="bar")

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