import json
import re
import os
import traceback
import time
from urllib import urlopen

MINUTE = 60

BART_URL = "http://api.bart.gov/api/etd.aspx?cmd=etd&orig=ALL&key=MW9S-E7SL-26DU-VV8V"

BITDELI_URL = "https://in.bitdeli.com/events/i-04ba8c056f4d54-5b80e881"
BITDELI_AUTH = os.environ['BITDELI_AUTH']

TIME_RE = "<time>(.*?)</time>"

def read_tstamp():
    try:
        return open('last-update').read()
    except:
        return ''

def write_tstamp(tstamp):
    f = open('last-update', 'w')
    f.write(tstamp)
    f.close()

def pump(previous_tstamp):
    while True:
        try:
            data = urlopen(BART_URL).read()
            tstamp = re.search(TIME_RE, data).group(0)
            if tstamp != previous_tstamp:
                event = json.dumps({'auth': BITDELI_AUTH,
                                    'group_key': int(time.time()),
                                    'object': {'bart-xml': data}})
                print urlopen(BITDELI_URL, event).read()
                write_tstamp(tstamp)
                previous_tstamp = tstamp
        except:
            traceback.print_exc()
        time.sleep(MINUTE)

if __name__ == '__main__':
    pump(read_tstamp())
