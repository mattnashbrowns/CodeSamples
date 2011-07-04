from f_data import *
from f_util import make_post, get_json_obj

from google.appengine.api import urlfetch
from gaesessions import get_current_session
import urllib
import datetime


urlbase = "http://us2.lacunaexpanse.com/"

def login_tle(req_obj):

  username = req_obj.request.get("username")
  password = req_obj.request.get("password")
  api_key  = req_obj.request.get("api_key")

  url = urlbase + "empire"
  
  #Anonymous API key for login
  params = [username,password,api_key]
  
  post_data = make_post("login",params)
  data = get_json_obj(url,post_data,False)
  
  return data