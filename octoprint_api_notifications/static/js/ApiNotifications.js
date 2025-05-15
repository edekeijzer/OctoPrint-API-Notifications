$(function() {
    function ApiNotificationsViewModel(parameters) {
        var self = this;

        self.onUserLoggedIn = function(user) {
            $.ajax({
                url: API_BASEURL + "plugin/api_notifications",
                type: "POST",
                dataType: "json",
                data: "{\"command\": \"retrieve\"}",
                contentType: "application/json; charset=UTF-8",
            });
        };

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin == "api_notifications") {
                if (data.msg_delay == 0) {
                    msg_delay = Infinity;
                }
                else {
                    msg_delay = data.msg_delay;
                }

                var pnotify_options = {
                    title: data.msg_title,
                    title_escape: true,
                    text: data.msg_text,
                    text_escape: true,
                    type: data.msg_type,
                    delay: msg_delay,
                    before_open: function(notice) {
                        // Remove the button we don't want
                        notice.get().find(".remove_button").remove();
                    },
                }

                if (data.msg_delay == 0) {
                    pnotify_options["hide"] = false;
                }
                else {
                    pnotify_options["delay"] = data.msg_delay;
                }

                if (data.msg_id !== "none") {
                    var buttons = [
                        {
                            text: "Mark read",
                            click: function(notice) {
                                self.removeNotification(data.msg_id);
                                notice.remove();
                            }
                        },
                        {
                            text: "Should not be seen",
                            addClass: "remove_button"
                        },
                    ];
                    var confirm = {
                        confirm: true,
                        buttons: buttons,
                    };
                    pnotify_options["confirm"] = confirm;

                }

                new PNotify(pnotify_options);
            }
        };
        
        self.removeNotification = function(id) {
            $.ajax({
                url: API_BASEURL + "plugin/api_notifications",
                type: "POST",
                dataType: "json",
                data: "{\"command\":\"remove\",\"id\":\"" + id + "\"}",
                contentType: "application/json; charset=UTF-8",
            });            
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        ApiNotificationsViewModel
    ]);
});