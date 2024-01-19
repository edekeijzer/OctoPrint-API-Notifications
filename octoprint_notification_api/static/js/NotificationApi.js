$(function() {
    function NotificationApiViewModel(parameters) {
        var self = this;

        self.onUserLoggedIn = function(user) {
            $.ajax({
                url: API_BASEURL + "plugin/notifications",
                type: "POST",
                dataType: "json",
                data: "{\"command\": \"retrieve\"}",
                contentType: "application/json; charset=UTF-8",
            });
        };

        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin == "notifications" && data.type == "popup") {
                if (data.msg_delay == 0) {
                    msg_delay = Infinity;
                }
                else {
                    msg_delay = data.msg_delay;
                }
                    
                if (data.msg_id === "none") {
                    var buttons = [
                        {
                            text: "Mark read",
                            click: function(notice) {
                                notice.remove();
                            }
                        },
                        {
                            text: "Should not be seen",
                            addClass: "remove_button"
                        },
                    ]
                }
                else {
                    var buttons = [
                        {
                            text: "Later",
                            click: function(notice) {
                                notice.remove();
                            }
                        },
                        {
                            text: "Mark read",
                            click: function(notice) {
                                self.removeNotification(data.msg_id);
                                notice.remove();
                            }
                        },
                    ]
                }
                new PNotify({
                    title: data.msg_title,
                    text: data.msg_text,
                    type: data.msg_level,
                    delay: msg_delay,
                    confirm: {
                        confirm: true,
                        buttons: buttons,
                    },
                    before_open: function(notice) {
                        // Remove the button we don't want
                        notice.get().find(".remove_button").remove();
                    },
                });
            }
        };
        
        self.removeNotification = function(id) {
            $.ajax({
                url: API_BASEURL + "plugin/notifications",
                type: "POST",
                dataType: "json",
                data: "{\"command\":\"remove\",\"id\":\"" + id + "\"}",
                contentType: "application/json; charset=UTF-8",
            });            
        }

        self.testPopUp = function(data) {
            self.onDataUpdaterPluginMessage("notifications", {'msg':'Notifications API pop up message example.','type':'popup'});
        };
            
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        NotificationApiViewModel
    ]);
});