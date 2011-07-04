import simplejson as json
import datetime

from google.appengine.api import urlfetch
from google.appengine.ext import db

#Create a JSONified POST string for TLE
#Pass the method name and a list of the parameters (or a dict, if that is what the fxn wants)
#Get back an escaped string suitable for sticking into a POST payload
def make_post(method, params): 
  post_data = json.dumps({  'jsonrpc' : '2.0',
                            'id'      : '1',
                            'method'  : method,
                            'params'  : params,
                        })
  return post_data

#Send a JSONified request, retrieve and parse the JSON response
#Return the deserialized object that the response represents
#url: the URL to fetch
#post_data: the serialized POST payload
#ret_obj: (optional, default True) if false, return the text of the JSON response instead of the object
def get_json_obj(url, post_data, ret_obj=True):
  s = urlfetch.fetch(url, method=urlfetch.POST, payload=post_data)
  json_obj = json.loads(s.content)
  res = json_obj
  if ret_obj:
    return res
  else:
    return json.dumps(res)

# Gets the age of a provided DB object
# Expects the DB object to have an "updated" field which contains a datetime object.
# returns a datetime.timedelta object
def obj_age(db_obj):
  now = datetime.utcnow()
  update_time = db_obj.updated
  diff = now - update_time
  
  return diff

def tle_to_datetime(tle_date):
  #TLE string looks like
  # '14 05 2011 00:15:57 +0000'
  dt = datetime.datetime.strptime(tle_date, '%d %m %Y %H:%M:%S +0000')
  
  return dt

#Delete everything in the datastore
#I mean it!
def wipe_datastore():
    query = Entry.all()
    entries = query.fetch(500)
    while entries:
      db.delete(entries)
      entries = query.fetch(500)    