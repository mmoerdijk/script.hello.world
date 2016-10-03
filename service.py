import time
import xbmc
import xbmcaddon
import xbmcgui

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json

api_key = ""
channel_id = ""
url="https://api.thingspeak.com/channels/" + channel_id +"/feeds.json?results=1&api_key=" + api_key

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

line1 = "Service started"

xbmcgui.Dialog().ok(addonname, line1)

if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
            break
        response = urlopen(url)
        data = json.loads(response.read().decode("utf-8"))
	xbmc.log(data["channel"]["field1"],level=xbmc.LOGDEBUG)
        result = data["feeds"][0]["field1"]  + " C " + data["feeds"][0]["field2"] + " RH "
        xbmcgui.Window(10000).setProperty('thingspeak', result)
        xbmc.log("Thingspeak service %s %s" % (time.time(), result), level=xbmc.LOGDEBUG)
