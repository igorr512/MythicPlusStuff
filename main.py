import pickle

from blizzard_api_handler import BlizzardApiHandler
from statistics import MythicPlusStatistics
clientid = 'ecee19a8f928461c8d0ffa8e045543aa'
clientpass = '8YRMgZDn3d2Tx0hqeIyw4vdjT0noJZi8'
gh1 = BlizzardApiHandler(clientid,clientpass)
#aa = gh1.get_max_level_players_from_guild("the-venture-co","dont-release")
#bb = gh1.get_best_runs("defias-brotherhood","lightnning",6)
#bb = bb = gh1.get_best_runs("the-venture-co","razlom",6)
#bb = gh1.get_best_runs_from_raiderio("razlom","the-venture-co")
#cc = gh1.get_guild_members_list("the-venture-co","dont-release")
object_stuff = MythicPlusStatistics(clientid,clientpass)

#b = object_stuff.get_most_played_players_for_character("razlom","the-venture-co")
#c= object_stuff.get_most_played_players_for_guild("dont-release","the-venture-co")
#a_file = open("data.pkl","wb")
#pickle.dump(c,a_file)
#a_file.close()

a_file = open("data.pkl","rb")
c = pickle.load(a_file)
object_stuff.get_teams_from_guild_only(c)
#temp check
print ("x")


#gh1.get_recent_runs("razlom","the-venture-co")
#aa = object_stuff.get_weekly_keys("razlom","the-venture-co")
bb = object_stuff.get_guilds_recent_runs('no-pressure','doomhammer')
a_file = open("data4.pkl","wb")
pickle.dump(bb,a_file)
a_file.close()

#a_file = open("data3.pkl","rb")
#c = pickle.load(a_file)

print ("BB")