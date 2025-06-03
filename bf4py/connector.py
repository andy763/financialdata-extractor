#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class BF4PyConnector():
    def __init__(self, salt: str=None):
        import requests, re
        
        self.session = requests.Session()
        
        self.session.headers.update({'authority': 'api.boerse-frankfurt.de', 
                                     'origin': 'https://www.boerse-frankfurt.de',
                                     'referer': 'https://www.boerse-frankfurt.de/',})
        
        if salt is None:
            # Step 1: Get Homepage
            response = self.session.get('https://www.boerse-frankfurt.de/')
            if response.status_code != 200:
                raise Exception('Could not connect to boerse-frankfurt.de homepage (status code: {})'.format(response.status_code))
            
            homepage_html = response.text

            # Step 2: Find all local JS file URLs mentioned in script tags
            # Regex looks for <script ... src="/path/to/file.js" ...> or src='/path/to/file.js'
            # It also handles potential query strings like /main.123.js?v=4
            js_file_paths = re.findall(r'<script[^>]+src\\s*=\\s*["\'](/[^"\']+\\.js(?:\\?[^"\']*)?)["\']', homepage_html)

            if not js_file_paths:
                # Fallback: Sometimes script tags might be relative without leading slash but still local.
                # This is less common for main bundles but good to have a slightly broader search if the first fails.
                # However, the original bf4py and our attempts focused on paths starting with '/', let's stick to that for now
                # to avoid fetching external scripts unintentionally if the regex is too broad.
                # If the above strictly local path fails, this is a critical point.
                raise Exception('Could not find any local JS file references (starting with /) in homepage HTML')

            found_salt = None
            # print(f"BF4PY_DEBUG: Found {len(js_file_paths)} potential JS files: {js_file_paths}")

            for js_path in js_file_paths:
                # Construct full URL for the JS file
                if js_path.startswith('//'): # schemaless URL
                    js_url = 'https:' + js_path
                elif js_path.startswith('/'): # Expected case
                    js_url = 'https://www.boerse-frankfurt.de' + js_path
                else:
                    # This case should ideally not be hit with the current regex focusing on paths starting with '/'
                    # print(f"BF4PY_DEBUG: Skipping JS path with unexpected format: {js_path}")
                    continue 

                try:
                    # print(f"BF4PY_DEBUG: Trying JS file: {js_url}")
                    js_response = self.session.get(js_url, timeout=10) # Timeout for fetching each JS file
                    if js_response.status_code == 200:
                        js_content = js_response.text
                        # Look for salt:"..." or salt:'...' or salt : "..." etc.
                        salt_match = re.search(r'salt\\s*:\\s*["\'](\\w+)["\']', js_content) 
                        if salt_match:
                            found_salt = salt_match.group(1)
                            # print(f"BF4PY_DEBUG: Found salt '{found_salt}' in {js_url}")
                            break # Salt found, exit loop
                        # else:
                            # print(f"BF4PY_DEBUG: Salt pattern not found in {js_url}")
                    # else:
                        # print(f"BF4PY_DEBUG: Failed to fetch {js_url}, status: {js_response.status_code}")
                except requests.exceptions.RequestException as e:
                    # print(f"BF4PY_DEBUG: RequestException for {js_url}: {e}")
                    continue # Try next JS file if one fails to download

            if found_salt:
                self.salt = found_salt
            else:
                # More detailed error if salt is not found after checking all candidates
                error_message = 'Could not find tracing-salt in any of the {} linked JS files checked. '.format(len(js_file_paths))
                if not js_file_paths: # Should be caught earlier, but as a safeguard
                    error_message = 'No JS files were identified to search for salt. '
                # Consider logging the paths checked if this error persists, for manual inspection.
                # For now, keeping the exception message concise.
                raise Exception(error_message + 'The website structure for salt extraction might have changed.')
        else:
            self.salt = salt
   
    def __del__(self):
        self.session.close()
   
    def _create_ids(self, url):
        import hashlib
        from datetime import datetime
        timeutc = datetime.utcnow()
        timelocal = datetime.now()
        timestr = timeutc.isoformat(timespec='milliseconds') + 'Z'

        traceidbase = timestr + url + self.salt
        encoded = traceidbase.encode()
        traceid = hashlib.md5(encoded).hexdigest()

        xsecuritybase = timelocal.strftime("%Y%m%d%H%M") 
        encoded = xsecuritybase.encode()
        xsecurity = hashlib.md5(encoded).hexdigest()
        
        return {'client-date':timestr, 'x-client-traceid':traceid, 'x-security':xsecurity}
    
    
    
    def _get_data_url(self, function: str, params:dict):
        import urllib
        baseurl = "https://api.boerse-frankfurt.de/v1/data/"
        p_string = urllib.parse.urlencode(params)
        return baseurl + function + '?' + p_string

    
    def data_request(self, function: str, params: dict):
        import json
        
        url = self._get_data_url(function, params)
        header = self._create_ids(url)
        header['accept'] = 'application/json, text/plain, */*'
        req = self.session.get(url, headers=header, timeout=(3.5, 15))
        
        if req.text is None:
            raise Exception('Boerse Frankfurt returned no data, check parameters, especially period!')
        
        data = json.loads(req.text)
        
        if 'messages' in data:
            raise Exception('Boerse Frankfurt did not process request:', *data['messages'])
        
        return data
    
    def _get_search_url(self, function: str, params:dict):
        import urllib
        baseurl = "https://api.boerse-frankfurt.de/v1/search/"
        p_string = urllib.parse.urlencode(params)
        return baseurl + function + ('?' + p_string if p_string != '' else '')

    def search_request(self, function: str, params: dict):
        import json
        
        url = self._get_search_url(function, {})
        header = self._create_ids(url)
        header['accept'] = 'application/json, text/plain, */*'
        header['content-type'] = 'application/json; charset=UTF-8'
        req = self.session.post(url, headers=header, timeout=(3.5, 15), json=params)
        data = json.loads(req.text)
        
        return data

    # Functions for STREAM requests

    def stream_request(self, function: str, params: dict):
        import sseclient, requests
        
        url = self._get_data_url(function, params)
        header = self._create_ids(url)
        header['accept'] = 'text/event-stream'
        header['cache-control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        
        socket = requests.get(url, stream=True, headers=header, timeout=(3.5, 5))
        client = sseclient.SSEClient(socket)
        
        return client
    
