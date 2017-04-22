import json
import requests
from Authentication import *
import requests
from pyquery import PyQuery as pq

class UMLS:
    def __init__(self, apikey='021fb6e5-0e1c-443d-8ec0-0b697140042c'):
        self.apikey = apikey
        self.service = 'http://umlsks.nlm.nih.gov'
        self.auth_endpoint = '/cas/v1/api-key'
        self.authURI = "https://utslogin.nlm.nih.gov"
        self.tgt = self.gettgt()
        print(self.tgt)

    def gettgt(self):
        params = {'apikey': self.apikey}
        h = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent': 'python'}
        r = requests.post(self.authURI + self.auth_endpoint, data=params, headers=h)
        d = pq(r.text)
        tgt = d.find('form').attr('action')
        return tgt

    def getst(self, tgt):
        params = {'service': self.service}
        h = {'Content-type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain', 'User-Agent': 'python'}
        r = requests.post(tgt, data=params, headers=h)
        st = r.text
        print(st)
        return st

    def search(self, words, format='l'):
        ticket = self.getst(self.tgt)
        print(ticket)
        query = {'string': words, 'ticket': ticket}
        uri = 'https://uts-ws.nlm.nih.gov'
        content_endpoint = '/rest/search/current'
        r = requests.get(uri + content_endpoint, params=query)
        r.raise_for_status() # throws error if bad response from API endpoint
        r.encoding = 'utf-8'
        items = json.loads(r.text)
        jsonData = items['result']
        if format == 'l':
            termList = []
            for result in jsonData['results']:
                termList.append(result['name'])
            print('Terms returned: ')
            print(termList)
            return termList
        if format == 'j':
            print(json.dumps(items, indent = 4))
            return jsonData
        if format == 'c':
            i = 1
            for result in jsonData['results']:
                i += 1
                print('\n\nRESULT NUMBER ' + str(i) + ' : \n')
                try:
                    print('name: ' + result['name'])
                except:
                    NameError
                try:
                    print('uri: ' + result['uri'])
                except:
                    NameError
                try:
                    print('ui: ' + result['ui'])
                except:
                    NameError
                try:
                    print('Source Vocabulary: ' + result['rootSource'])
                except:
                    NameError

# creates a UMLS object and gets a ticket granting ticket from the API authentication server
u = UMLS()

# performs a search of UMLS, optional parameter determines format of result.
resultsJSON = u.search('heart attack', 'j') #returns JSON object of full results and metadata
resultsList = u.search('heart attack', 'l')  #returns list of only the terms to add to queries, default if no param passed
u.search('heart attack', 'c') #outputs data into the console