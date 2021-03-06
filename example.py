#!/usr/bin/python

from pyrapidpush import PyRapidPush
import sys

def main(api_key):
    p = PyRapidPush(api_key)

    # Retrieve group test.
    groups = p.get_groups()
    print (groups)
    if groups.has_key('code'):
        if groups['code'] == 200:
            for item in groups['data']:
                print('Got group: ' + item['group'])
    else:
        for apikey in groups:
            print('Groups for api key: ' + apikey)
            if groups[apikey]['code'] == 200:
                for item in groups[apikey]['data']:
                    print('Got group: ' + item['group'])
    # Direct notification test.
    print(p.notify('python test', 'Test message'))

    # Scheduled test, change the given GMT time to a time in future.
    print(p.notify('Python test', 'Test message scheduled', 2, 'default', '', '2013-01-26 14:33:00'))

    # Broadcast notification test.
    print(p.broadcast('python test', 'Test message', 'MY-CHANNEL'))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('You have to provide your API-Key with the first parameter. Example: python test.py YOUR-API-KEY')
    else:
        main(sys.argv[1])
