# -*- coding: utf-8 -*-
import time
import xbmc
import xbmcaddon
import xbmcgui
import sys
import numpy

reload(sys)
sys.setdefaultencoding('utf8')

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json

api_key = "NSV37MGG8Y01L2KG"
channel_id = "160735"
num_results = 5
dead_zone = 0.2

url="https://api.thingspeak.com/channels/"+channel_id+"/feeds.json?results="+num_results+"&api_key=" + api_key

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

line1 = "Service started"

xbmcgui.Dialog().ok(addonname, line1)

if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(5):
            # Abort was requested while waiting. We should exit
            break
        try
            response = urlopen(url)
            data = json.loads(response.read().decode("utf-8"))
        except ValueError, e:
            xbmc.log("No valid JSON loaded",level=xbmc.LOGDEBUG)
            pass # invalid json
        else
            # if more than 1 data point recieved do find out if the trend is
            # increasing or decreasing.

            for it in range(0,num_results)
                temp_results[it]    = data["feeds"][it]["field1"]
                rh_results[it]      = data["feeds"][it]["field2"]

            x = np.arange(0,num_results)
            y = np.array(temp_results)
            z = np.polyfit(x,y,1)

            if  z[0] > dead_zone
                trend_temp = "↑"
            elif z[0] < dead_zone
                trend_temp = "↓"
            else
                trend_temp = "-"

            # Show results
            result = data["feeds"][0]["field1"]  + " °C ("+trend_temp+")/ " + data["feeds"][0]["field2"] + "% RH "
            xbmcgui.Window(10000).setProperty('thingspeak', result)
            xbmc.log("Thingspeak service %s %s" % (time.time(), result), level=xbmc.LOGDEBUG)
