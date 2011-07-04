import os
import cgi
import datetime
import urllib
import wsgiref.handlers

#Custom modules
from f_data import *        #Data object definitions. important reading!
import f_tle                #TLE API query functions
import f_loaders            #Functions for populating data objects


from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from gaesessions import get_current_session

# Dashboard provides a user and alliance status report and links to other reports
class Dashboard(webapp.RequestHandler):
  def get(self):
    
    session = get_current_session()
    
    #Get the user id 
    userid = users.get_current_user()
  
    #Check for logged-in user
    if userid:
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
      path = os.path.join(os.path.dirname(__file__), 'dash.html')
    #If not logged in, redirect to Google login page
    else:
      self.redirect(users.create_login_url(self.request.uri))
    
    
    template_values = {
      'ally'      : '',
      'url'       : url,
      'linktext'  : url_linktext,
    }
    
    self.response.out.write(template.render(path, template_values))

# AdminPage lets us bootstrap new users of the application, so that they can log in.
#   Also so that WE can log in and give ourselves rights.
class AdminPage(webapp.RequestHandler):
  #Normal invocation of Admin page, with or without "action" parameter, is with GET
  def get(self):
    #Possible actions:
    #Add ally
    #Initialize alliance
    action = self.request.get("action",default_value = "None")
    
    #Get a list of current allies
    allies = Ally.all()
    allies.filter("current =","True")
    allies = allies.run()
    
    #Set up data to pass to the template
    template_values = {
      'allies'  : allies, 
    }
    
    path = os.path.join(os.path.dirname(__file__), 'admin.html')  
    
    self.response.out.write(template.render(path, template_values))
    
  #New-ally form POSTs its results, which trigger this function
  def post(self):
    #Retrieve parameters from form
    ally_email = self.request.get("googID",default_value = "None")
    ally_name = self.request.get("TLEname",default_value = "None")
    
    if (ally_email == "None") or (ally_name == "None"):
      self.redirect(self.request.uri)
    
    empire = f_decoder.pub_empire_query(ally_name)
    
    template_values = {
      'empire'  : empire,
      'email'   : ally_email,
      'name'    : ally_name,
    }
    
    path = os.path.join(os.path.dirname(__file__), 'ally_add_conf.html')
    self.response.out.write(template.render(path, template_values))
    
class InitPage(webapp.RequestHandler):
  def get(self):
    userid = users.get_current_user()
    
    if not userid:
      self.redirect(users.create_login_url(self.request.uri))
  
    template_values = {
        'user'    : userid,
    }
    path = os.path.join(os.path.dirname(__file__), 'f_initialize.html')
    self.response.out.write(template.render(path, template_values))
  def post(self):
    allies = []
    ally_keys = []
    
    tle_user = self.request.get("username")
    tle_pass = self.request.get("password")
    api_key = self.request.get("api_key")
    
    session = get_current_session()
    
    #Try to log in
    result = f_tle.tle_login(tle_user,tle_pass,api_key)
  
    if result == 0:   #Failed login
      self.error(503) #Need better way to express this
    
    #Stick the TLE session ID into the GAE session.
    #All of the query functions will expect it.
    session['tle_session'] = result['session_id']
    
    #Get my empire ID from JSON result
    e_id = result['status']['empire']['id']
    
    #Status message is a little spare so we are going to do an empire query on ourselves
    #For more data
    empire_data = f_tle.pub_empire_query(e_id)
    
    #Extract my alliance ID from the empire query
    alliance_id = empire_data['alliance']['id']
    
    #And use that ID to gather information about our alliance
    alliance_data = f_tle.alliance_profile(alliance_id)
    
    #Create a new Alliance DB object for our alliance
    alliance = f_loaders.load_alliance(alliance_data)
    #Grab a key
    alliance_key = alliance.key()
    #And mark it as ours
    alliance.is_us = True
    
    #Gather info about the alliance members
    e_ids = alliance.member_ids
    #Loop through member IDs
    for e_id in e_ids:
      member_data = f_tle.pub_empire_query(e_id)        #Get member data from TLE
      new_ally = f_loaders.load_ally(member_data)       #Create an Ally DB object
      ally_keys.append(new_ally.key())                  #And add that key to the list
      allies.append(new_ally)                           #Keep a list of allies for the status page
      
    #Add list of ally references to alliance object
    alliance.members = ally_keys
    
    alliance.put()  
    
    template_values = { 
                        'alliance'  : alliance,
                        'allies'    : allies
                      }
    
    path = os.path.join(os.path.dirname(__file__), 'app_init_report.html')
    self.response.out.write(template.render(path, template_values))
    

# RequestHandler Services --
# Respond to requests for data from main app
# Uses a dispatch table defined in __init__ to fire the appropriate function
class Services(webapp.RequestHandler):
  def __init__(self):  
    self.dtable = {
      'login_tle'   : f_server.login_tle,
      }
      
  # Only accept POST requests
  # functions are all defined in f_server
  # and each returns a JSON representation of an object
  # which contains either the requested data or an error message.
  # We will let the web page figure out what to do with the result
  def post(self):
    fxn_call = self.request.get('fxn')
    json_data = self.dtable[fxn_call](self)
    self.response.out.write(json_data)
    

application = webapp.WSGIApplication(
                                       [('/', Dashboard),
                                       ('/admin', AdminPage),
                                       ('/init', InitPage),
                                       ('/svr', Services),],
                                       debug=True)

def main():
    run_wsgi_app(application)
    
if __name__ == "__main__":
    main()