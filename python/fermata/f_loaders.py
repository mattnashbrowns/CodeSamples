## ********************************************************
# f_loaders contains functions for parsing JSON objects 
# into the DB objects defined in f_data
# -These functions will check to see if the entity described already exists
#   and will perform an update if they are stale (more than 24 hours old)
## *********************************************************
from f_util import make_post, get_json_obj, tle_to_datetime
from f_data import *
import f_tle

import datetime

day = datetime.timedelta(days=1)

# Loads up an Alliance object, given a JSON object containing alliance data
# Makes an empire query on the leader to get leader name
# Then writes it to the DB
# And returns it
def load_alliance(alliance_data):
  all_id   = alliance_data['id']
  all_name = alliance_data['name']
  leader_id = alliance_data['leader_id']
  member_list = []
  
  #Get leader's empire data
  leader_data = f_tle.pub_empire_query(leader_id)
  
  #Build list of member IDs
  for member in alliance_data['members']:
    member_list.append(int(member['id']))
  
  #Convert TLE time to a datetime object
  cdate = alliance_data['date_created']
  cdate = tle_to_datetime(cdate)
  
  #Create new f_data.Alliance DB object and set its properties
  alliance              =   Alliance(name=all_name)
  alliance.id           =   int(all_id)
  alliance.leader_id    =   int(leader_id)
  alliance.leader_name  =   leader_data['name']
  alliance.create_date  =   cdate
  alliance.description  =   alliance_data['description']
  alliance.member_ids   =   member_list
  
  #Write data to DB
  alliance.put()
  
  return alliance

#Loads an Ally DB object, given a JSON object resulting from a public empire query
#Use only when you are adding a player to the DB for the first time
#For a player who is becoming an ally, use promote_player(f_data.Player)
#Also, if you could write that fxn that would be great!
def load_ally(ally_obj):
  alliance_id = int(ally_obj['alliance']['id'])
  ally = Ally()
  
  q = Alliance.all()
  q.filter('id =',alliance_id)
  alliance = q.get()
  
  fdate = ally_obj['date_founded']
  dt = tle_to_datetime(fdate)
  
  ally.name                 = ally_obj['name']
  ally.id                   = int(ally_obj['id'])
  ally.colony_count         = int(ally_obj['colony_count'])
  ally.date_founded         = dt
  ally.alliance_id          = int(alliance_id)
  ally.alliance             = alliance.key()
  ally.active               = True
  ally.current              = True
  ally.admin                = False
  ally.full_data            = False
  
  ally.put()
  
  return ally

  
#Promotes an existing Player to an Ally
#def promote_player(player_obj):
  