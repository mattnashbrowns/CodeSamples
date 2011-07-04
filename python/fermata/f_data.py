from google.appengine.ext import db
from google.appengine.ext.db import polymodel

# An official Alliance in TLE
class Alliance(polymodel.PolyModel):
  name          = db.StringProperty(required=True)        #Official TLE Alliance name
  id            = db.IntegerProperty()                    #TLE alliance ID
  description   = db.StringProperty()                     #Alliance description
  create_date   = db.DateTimeProperty()                   #Alliance Creation date
  leader_id     = db.IntegerProperty()                    #TLE ID of alliance leader
  leader_name   = db.StringProperty()                     #Name of alliance leader
  leader        = db.ReferenceProperty()                  #Reference to alliance leader
  member_ids    = db.ListProperty(long)                   #List of TLE IDs of members
  members       = db.ListProperty(db.Key)                 #List of References to member empire DB objects
  station_ids   = db.ListProperty(long)                   #List of TLE IDs of space stations
  stations      = db.ListProperty(db.Key)                 #List of references to space station DB objects
  is_us         = db.BooleanProperty()                    #Is this our alliance?
  created       = db.DateTimeProperty(auto_now_add=True)  #Record creation
  updated       = db.DateTimeProperty(auto_now_add=True)  #Record update
  
# A player on our server
class Player(polymodel.PolyModel):
  name = db.StringProperty()                                  #Official TLE Empire name
  id = db.IntegerProperty()                                   #TLE empire ID
  real_name   = db.StringProperty()                           #Real name, if known
  uni_level = db.IntegerProperty()                            #University level
  is_iso = db.BooleanProperty()                               #Is isolationist?
  colony_count = db.IntegerProperty()                         #Number of colonies
  date_founded = db.DateTimeProperty()                        #Date empire was founded
  alliance_id = db.IntegerProperty()                           #TLE ID of Alliance belonged to, if any
  alliance = db.ReferenceProperty(Alliance,
                                collection_name="player_alliance")               #Reference to DB object storing alliance
  created = db.DateTimeProperty(auto_now_add=True)        #Date/time of record creation
  updated = db.DateTimeProperty(auto_now_add=True)        #Date/time of last record update
  planet_ids = db.ListProperty(long)                             #List of TLE planet IDs
  planets = db.ListProperty(db.Key)                           #List of references to planet DB objects

  
# A member of our alliance
class Ally(Player):
  user_id     = db.UserProperty()                         #Google ID of ally
  user_email  = db.StringProperty()                       #email associated with Google ID
  sitter_pass = db.StringProperty()                       #Sitter password
  api_key     = db.StringProperty()                       #TLE API key
  auto_update = db.BooleanProperty()                      #Automatically log in to TLE and collect info?
  active      = db.BooleanProperty()                      #Actively playing?
  current     = db.BooleanProperty()                      #Still an alliance member?
  admin       = db.BooleanProperty()                      #Administrator of this app?
  full_data   = db.BooleanProperty()                      #Access to all reports?
  initialized = db.BooleanProperty()                      #Has the ally been fully initialized in the app?
  
# Items such as planets, SS, and stars, which have a fixed Cartesian location
class Locatable(polymodel.PolyModel):
  body_id       = db.IntegerProperty(required=True)      #TLE ID for object
  x_pos         = db.IntegerProperty(required=True)      #X coordinate
  y_pos         = db.IntegerProperty(required=True)      #Y coordinate
  created       = db.DateTimeProperty(auto_now_add=True) #record creation
  updated       = db.DateTimeProperty(auto_now_add=True) #record update
  created_by    = db.UserProperty()                      #Google user ID of record creator
  updated_by    = db.UserProperty()                      #Google user ID of last updater

#Stars
class Star(Locatable):
  star_name     = db.StringProperty(required=True)       #TLE star name
  color         = db.StringProperty()                    #Star color
  bodies        = db.ListProperty(long)                  #List of IDs of orbiting bodies

#Space stations
class Station(Locatable):
  station_name  = db.StringProperty(required=True)      #Name of station
  alliance_id   = db.IntegerProperty()               #TLE ID of owning alliance
  alliance      = db.ReferenceProperty(Alliance,
                                        collection_name="station_alliance")        #Alliance DB object
  inf_total     = db.IntegerProperty()                  #Total influence
  inf_spent     = db.IntegerProperty()                  #Influence spent
  
#Planets and asteroids
class Planet(Locatable):
  id     = db.IntegerProperty(required=True)     #TLE ID of planet
  name   = db.StringProperty()                    #Name of planet 
  type   = db.StringProperty()                   #inhabitable, gg, asteroid
  orbit         = db.IntegerProperty()                   #orbit slot
  empire_id     = db.IntegerProperty()                   #TLE ID of owning empire
  empire        = db.ReferenceProperty(Player,
                                        collection_name="planet_owner")           #Ref to owner DB object   
  station_id    = db.IntegerProperty()                   #TLE ID of controlling station
  station       = db.ReferenceProperty(Station,
                                        collection_name="planet_station")          #Ref to controlling station DB object
  plots         = db.IntegerProperty()                   #number of buildable plots
  buildings     = db.IntegerProperty()                   #number of buildings
  obs_id        = db.IntegerProperty()                   #TLE ID of observatory, if any
  obs_probes    = db.IntegerProperty()                   #Number of probes controlled by observatory
  obs_max       = db.IntegerProperty()                   #Max number of probes obs can control
  water         = db.IntegerProperty()                   #water rating
  #Ratings of different types of ore
  anthracite    = db.IntegerProperty()
  bauxite       = db.IntegerProperty()
  beryl         = db.IntegerProperty()
  chalcopyrite  = db.IntegerProperty()
  chromite      = db.IntegerProperty()
  fluorite      = db.IntegerProperty()
  galena        = db.IntegerProperty()
  goethite      = db.IntegerProperty()
  gold          = db.IntegerProperty()
  gypsum        = db.IntegerProperty()
  halite        = db.IntegerProperty()
  kerogen       = db.IntegerProperty()
  magnetite     = db.IntegerProperty()
  methane       = db.IntegerProperty()
  monazite      = db.IntegerProperty()
  rutile        = db.IntegerProperty()
  sulfur        = db.IntegerProperty()
  trona         = db.IntegerProperty()
  uraninite     = db.IntegerProperty()
  zircon        = db.IntegerProperty()

