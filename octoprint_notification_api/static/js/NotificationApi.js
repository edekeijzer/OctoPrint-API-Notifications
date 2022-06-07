$(function() {
    function NotificationApiViewModel(parameters) {
        var self = this;
        
        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin == "NotificationApi") {
				console.log(data.messsage);
				new PNotify({
					title: data.msg_title,
					text: data.msg_text,
					type: data.msg_level,
					delay: data.msg_timeout
				});
            }
        }
        
        self.testPopUp = function(data) {
            self.onDataUpdaterPluginMessage("NotificationApiPopUp", {'message':'Notification API Pop up message example.','title':'Notification','type':'popup','timeout':10});
        }
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        NotificationApiViewModel
    ]);
});
