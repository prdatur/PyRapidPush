#!/usr/bin/python

import json

try:
        from http.client import HTTPSConnection
except ImportError:
        from httplib import HTTPSConnection

try:
        from urllib.parse import urlencode
except ImportError:
        from urllib import urlencode

__version__ = "1.1"
API_SERVER  = 'rapidpush.net'
ADD_PATH    = '/api'
USER_AGENT  = "PyRapidPush/v%s"%__version__

class PyRapidPush(object):
    """PyRapidPush(apikey=None)
takes 1 optional arguments:
 - (opt) apikey:      the api key string, multiple keys seperated by comma
"""

    def __init__(self, apikey=None):
        self.apikey = apikey

    def notify(self, title, message, priority=2, category="default", group="", schedule_at=""):
        """Sends a notification to the api key.
takes 2 required arguments:
 - (req) title:       the title        [255]
 - (req) message:     description      [10000]
takes 4 optional arguments:
 - (opt) priority:    from 0 (lowest) to 6 (highest) (def:2)
 - (opt) category:    category name    [255] (def:default)
 - (opt) group:       The device group (def:"")
 - (opt) schedule_at: if provided, the notification will be scheduled, the string is a Datetime in GMT format: Y-m-d H:i:00 (def:"")

 cf: https://rapidpush.net/content/view/3
"""
        # Verify that the provided priority is in range.
        if priority < 0 or priority > 6:
            return {
                'code': 405,
                'data': None,
                'desc': 'Priority must be between 0 and 6'
            }

        # Build the "data"-Params.
        datas = {
            'title':       title[:255].encode('utf8'),
            'message':     message[:10000].encode('utf8'),
            'priority':    priority
        }

        # Provide default values.
        if category:
            datas['category'] = category[:255].encode('utf8')

        if group:
            datas['group'] = group[:255].encode('utf8')

        if schedule_at:
            datas['schedule_at'] = schedule_at[:19].encode('utf8')

        # Setup API-Params.
        post_param = {
            'apikey' : self.apikey,
            'command' : 'notify',
            'data' : json.dumps(datas)
        }

        # Do the api call and get the response back.
        return self.callapi('POST', ADD_PATH, post_param)

    def broadcast(self, title, message, channel):
        """Sends a broadcast notification to the channel.
takes 3 required arguments:
 - (req) title:       the title        [255]
 - (req) message:     description      [10000]
 - (req) channel:     channel          [255]

 cf: https://rapidpush.net/content/view/3
"""
        # Build the "data"-Params.
        datas = {
            'title':       title[:255].encode('utf8'),
            'message':     message[:10000].encode('utf8'),
            'channel':     channel[:255].encode('utf8'),
        }

        # Setup API-Params.
        post_param = {
            'apikey' : self.apikey,
            'command' : 'broadcast',
            'data' : json.dumps(datas)
        }

        # Do the api call and get the response back.
        return self.callapi('POST', ADD_PATH, post_param)

    def get_groups(self):
        """Get the configurated groups back.
takes no arguments:

 cf: https://rapidpush.net/content/view/3
"""

        # Setup API-Params.
        post_param = {
            'apikey' : self.apikey,
            'command' : 'get_groups',
            'data' : '{}'
        }

        # Do the api call and get the response back.
        return self.callapi('POST', ADD_PATH, post_param)

    def callapi(self, method, path, args):
        # Set headers.
        headers = {
            'User-Agent': USER_AGENT
        }

        # Set content type if we want to post the data.
        if method == "POST":
            headers['Content-type'] = "application/x-www-form-urlencoded"

        # Create the HTTPSConnection and do the api call.
        http_handler = HTTPSConnection(API_SERVER)
        http_handler.request(method, path, urlencode(args), headers)

        # Get the response.
        resp = http_handler.getresponse()

        try:
            # Return the API-Response.
            return self._parse_reponse_json(resp.read())

        except Exception as e:
            # Return response could not be parsed.
            return {
                'type':    "RapidPush parse error",
                'code':    600,
                'message': str(e)
            }

    def _parse_reponse_json(self, response):

        # Get the json data.
        return json.loads(response)
