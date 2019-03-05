import json, requests
from core.env import SIGINT_handler
import signal
from core.logger import Output

NAME        = 'virustotal'
ARG_HELP    = 'virus total subdomain scanner'

handler = SIGINT_handler()
signal.signal(signal.SIGINT, handler.signal_handler)

class VTError(Exception):
   """Base class for Virus Total exceptions"""
   pass

def execute(domain, credentials):
    if handler.SIGINT:
        Output().warn("Aborted plugin: %s" % NAME, False)
        return None
    try:
        query = "https://www.virustotal.com/vtapi/v2/domain/report?apikey=%s&domain=%s" % (credentials['api-key'], domain.rstrip())
        r = requests.get(query)
        if r.status_code == 200:
            data = json.loads(r.text)
            if 'subdomains' in data:
                # data should always be returned as a array
                return data['subdomains']
            else:
                return None
        elif r.status_code == 403:
            raise VTError('Virustotal Plugin: API Unauthorized')
        else:
            raise VTError('Virustotal Plugin: Unexpected Error')
    except:
        raise