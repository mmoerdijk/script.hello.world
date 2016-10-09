# -*- coding: utf-8 -*-
import time
import xbmc
import xbmcaddon
import xbmcgui
import sys
import numpy as np
import json

reload(sys)
sys.setdefaultencoding('utf8')
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen


# thingspeak api key
api_key = ""
# thingspeak api id
channel_id = ""
# number of results to download for trend detection
# (an up or down arrow is shown if the trend is upwards or downwards)
num_results = 5
dead_zone = 0.01



url="https://api.thingspeak.com/channels/"+ channel_id+"/feeds.json?results="+str(num_results)+"&api_key=" + api_key
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
line1 = "Service started"
xbmcgui.Dialog().ok(addonname, line1)

# Enter main loop
if __name__ == '__main__':
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():


    	try: # to request url
             response = urlopen(url)
    	except URLError as e:
    	     response='';
    	     xbmcgui.Window(10000).setProperty('thingspeak', 'url error')
    	     pass


        try: # to parse json
            data = json.loads(response.read().decode("utf-8"))

        except ValueError, e:
    	    xbmcgui.Window(10000).setProperty('thingspeak', 'json error')
            xbmc.log("No valid JSON loaded",level=xbmc.LOGDEBUG)
                pass # invalid json
        else:
            # if more than 1 data point recieved do find out if the trend is
            # increasing or decreasing.
            trend_temp = ""
            trend_hr=""

            if num_results > 1 :
        	    temp_results=[]
        	    rh_results=[]

                for it in range(0,num_results):
                    temp_results.append(float(data["feeds"][it]["field1"]))
                    rh_results.append(float(data["feeds"][it]["field2"]))

                x = np.arange(0,num_results)
                y = np.array(temp_results)
                z = np.polyfit(x,y,1)

                if  z[0] > dead_zone :
                    trend_temp = "↑"
                elif z[0] < -1.0*dead_zone :
                    trend_temp = "↓"
                else:
                    trend_temp = ""

                y = np.array(rh_results)
                z = np.polyfit(x,y,1)

                if  z[0] > dead_zone :
                    trend_hr = "↑"
                elif z[0] < -1.0*dead_zone :
                    trend_hr = "↓"
                else:
                    trend_hr = ""

            # Show results
            result = data["feeds"][num_results-1]["field1"]  + " °C "+trend_temp+" / " + data["feeds"][num_results-1]["field2"] + "% RH " + trend_hr
            xbmcgui.Window(10000).setProperty('thingspeak', result)
            xbmc.log("Thingspeak service %s %s" % (time.time(), result), level=xbmc.LOGDEBUG)

            # Sleep/wait for abort for 10 seconds
            if monitor.waitForAbort(10):
            # Abort was requested while waiting. We should exit
                 break
