import webapp2
import urllib
import json

from google.appengine.api import urlfetch
from firebase_token_generator import create_token


FIREBASE_SECRET = '__THE_FIREBASE_SECRET__'
FIREBASE_URL = 'https://__THE_FIREBASE_ID__.firebaseio.com/%s/records%s.json?auth=%s'
JSON_STR = '{"%s":"%s"}'
JSON_STR_WITH_LAST = '{"%s":%s,"last":{"value":0}}'

def get_entries_json(entry_key, value):
    return JSON_STR % (entry_key, value)

def get_day_json(entry_key, value, day):
    return JSON_STR_WITH_LAST % (day, get_entries_json(entry_key, value))

def get_month_json(entry_key, value, day, month):
    return JSON_STR_WITH_LAST % (month, get_day_json(entry_key, value, day))

def get_year_json(entry_key, value, day, month, year):
    return JSON_STR_WITH_LAST % (year, get_month_json(entry_key, value, day, month))
 
def get_patch(records, year, month, day, entry_index, value):
    all_entry_keys = ['entry1', 'exit1', 'entry2', 'exit2']
    entry_key = all_entry_keys[int(entry_index)]

    patch = {}
    if year in records:
        if month in records[year]:
            if day in records[year][month]:
                patch['data'] = get_entries_json(entry_key, value)
                patch['resource'] = '/%s/%s/%s' % (year, month, day)
            else:
                patch['data'] = get_day_json(entry_key, value, day)
                patch['resource'] = '/%s/%s' % (year, month)
        else:
            patch['data'] = get_month_json(entry_key, value, day, month)
            patch['resource'] = '/%s' % (year)
    else:
        patch['data'] = get_year_json(entry_key, value, day, month, year)
        patch['resource'] = ''
    return patch

def get_firebase_credential(token):
    auth_payload = {'uid': '', 'token': token}
    return create_token(FIREBASE_SECRET, auth_payload)

def get_firebase_url(user, credential, resource):
    return FIREBASE_URL % (user, resource, credential)

def get_records_from_firebase(user, credential):
    url = get_firebase_url(user, credential, '')
    result = urlfetch.fetch(url=url, method=urlfetch.GET)
    records = json.loads(result.content)
    return records

def save_on_firebase(user, credential, resource, data):
    url = get_firebase_url(user, credential, resource)
    result = urlfetch.fetch(url=url,
        payload=data,
        method=urlfetch.PATCH,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return result


class MainPage(webapp2.RequestHandler):

    def print_result(self, result):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(result.status_code)
        self.response.write(result.content)

    def post(self):
        token = self.request.get('token')
        user = self.request.get('user')
        year = self.request.get('year')
        month = self.request.get('month')
        day = self.request.get('day')
        entry_index = self.request.get('entry')
        value = self.request.get('value')

        credential = get_firebase_credential(token)
        records = get_records_from_firebase(user, credential)
        patch = get_patch(records, year, month, day, entry_index, value)
        result = save_on_firebase(user, credential, patch['resource'], patch['data'])
        self.print_result(result)


app = webapp2.WSGIApplication([
    ('/register', MainPage),
], debug=True)
