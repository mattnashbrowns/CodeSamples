##
# f_tle performs queries against TLE and returns the data object,
# which has been deserialized from the JSON response text
# By the utility functions in f_util.py

from f_data import *
from f_util import make_post, get_json_obj

from google.appengine.api import urlfetch
from gaesessions import get_current_session
import urllib
import datetime

urlbase = "http://us2.lacunaexpanse.com/"

# ***TODO:
  #           Exceptions!
  #           Every remote interaction should be trapped!
  #           Should we do this in f_util?

#Log in to TLE using the provided username, password, and api-key
#Returns the JSON response object, which contains the session key
def tle_login(username,password,api_key):
  
  url = urlbase + "empire"
  
  params = [username,password,api_key]
  
  post_data = make_post("login",params)
  data = get_json_obj(url,post_data)
  
  return data

#Performs an online TLE query of publicly available information about an empire, 
#   given that empire ID
# Returns the JSON response
def pub_empire_query(emp_id):
  session = get_current_session()
  
  #Check to see if we have gotten a session key yet
  if 'tle_session' not in session:
    return 0
  
  #Get the TLE session key out of the GAE session
  session_key = session['tle_session']
  
  #Build the correct URL for interacting with the Empire module
  url = urlbase + "empire"
  
  #Make a list of parameters for the view_public_profile function
  params = [session_key,emp_id]
  #Build a POST payload
  post_data = make_post("view_public_profile",params)
  #Send payload and retrieve response in object form
  e_profile = get_json_obj(url,post_data)
  
  return e_profile['profile']


def alliance_search(all_name):
  session = get_current_session()
  
  #Check to see if we have gotten a session key yet
  if 'tle_session' not in session:
    return 0
  
  session_key = session['tle_session']
  
  url = urlbase + 'alliance'
  
  params = [session_key, all_name]
  
  post_data = make_post('find',params)
                        
  data = get_json_obj(url,post_data)
  
  alliance_result = data['result']
  
  return alliance_result
  
#Gets an alliance profile, given an alliance ID number
#Returns the JSON response object
def alliance_profile(all_id):

  session = get_current_session()
  
  session_key = session['tle_session']
  url = urlbase + 'alliance'
  
  params = [session_key,all_id]
  
  post_data = make_post('view_profile',params)
  
  alliance_data = get_json_obj(url,post_data)
  
  return alliance_data['profile']
  

