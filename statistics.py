import time
from blizzard_api_handler import BlizzardApiHandler
import copy
from datetime import date
from datetime import timedelta
from calendar import WEDNESDAY
from datetime import datetime

class MythicPlusStatistics:
    def __init__(self, client_id, client_pass):
        self.client_id = client_id
        self.client_pass = client_pass
        self.blizzard_api_handler = BlizzardApiHandler(self.client_id, self.client_pass)
        self.season = 6
        self.min_key_level = 18
        self.num_of_members_in_team = 3
    teams = []

    def get_most_played_players_for_guild(self,guild_name,guild_realm):
        members = self.blizzard_api_handler.get_max_level_players_from_guild(guild_realm,guild_name)
        guild_members_num_of_runs ={}
        num = 0
        if members:
            for member in members:
                if num%10==0 and num != 0:
                    print ("Sleep started")
                    time.sleep(10)
                    print ("Sleep ended")
                print (member['name'])
                participants =  self.get_most_played_players_for_character(member['name'].lower(),member['realm'].lower())
                if participants:
                    guild_members_num_of_runs[member['name']+'_'+member['realm']] = participants
                num=num+1
            return guild_members_num_of_runs
        return 0

    def get_most_played_players_for_character(self, character_name, character_realm):
        runs = self.blizzard_api_handler.get_best_runs(character_realm, character_name, self.season)
        members_num_of_runs = {}
        if runs:
            for run in runs:
                if run['keystone_level'] < self.min_key_level:
                    continue
                members = run["members"]
                for member in members:
                    if member['character']['name'].lower() == character_name and member['character']['realm']['slug'].lower() == character_realm:
                        continue
                    members_num_of_runs[member['character']['name'] + '_' + member['character']['realm']['slug']] \
                        = members_num_of_runs.get(member['character']['name'] + '_' +
                                                   member['character']['realm']['slug'], 0) + 1
            return members_num_of_runs
        return 0

    def sort_teams(self,a_dict):
        a_dict = self.sort_top_participants(a_dict)
        a_dict = self.remove_single_encounter(a_dict)
        return a_dict

    def sort_top_participants(self,members_dict):
        a_dict = {}
        for key in members_dict:

            values = members_dict[key]
            top_participants = self.get_top_number_of_participants(values,self.num_of_members_in_team)
            a_dict[key] = top_participants
        return a_dict

    def remove_single_encounter(self,a_dict):
        b_dict = copy.copy(a_dict)
        for key in a_dict:
            number_of_removes = 0
            temp_arr = copy.copy(a_dict[key])
            for index,value in enumerate(a_dict[key]):
                if value['num'] == 1:
                    temp_arr.pop(index-number_of_removes)
                    number_of_removes = number_of_removes+1
            b_dict[key] = copy.copy(temp_arr)
            if len(b_dict[key]) ==0:
                del b_dict[key]
        return b_dict

    def get_top_number_of_participants(self, a_dict, num_of_participants):
        top_participants = [{}] * num_of_participants
        index_to_insert = -1
        for key in a_dict:
            for index,array_member in enumerate(top_participants):
                if key == array_member.get("name",0):
                    break
                if a_dict[key] > array_member.get("num",0):
                    index_to_insert = index
                else:
                    if index == 0:
                        break
            if index_to_insert != -1:
                top_participants.pop(0)
                top_participants.insert(index_to_insert,{"name":key,"num":a_dict[key]})
                index_to_insert = -1
        return top_participants

    def get_teams_from_guild_only(self,a_dict):
        teams = []
        stripped_dict = self.sort_teams(a_dict)
        for key in stripped_dict:
            members = []
            for member in stripped_dict[key]:
                member_name = member['name']
                if stripped_dict.get(member_name,None) is None :
                    continue
                if self.check_if_exist_at_top_members(key,stripped_dict[member_name]):
                    members.append(member_name)
            if len(members) > 0:
                members.append(key)
                teams.append(members)
        print ("X")
    def eliminate_duplicates(self,teams_list):
        for i,team in enumerate(teams_list):
            for j,team in enumerate(teams_list):
                return




    def check_if_exist_at_top_members(self,name,list_members):
        for member in list_members:
            member_name = member['name']
            if member_name.lower() == name.lower():
                return 1
        return 0

    def get_weekly_keys(self,character,realm):
        last_wednesday = self.get_last_reset_date()
        num_of_weekly_runs = 0
        recent_runs = self.blizzard_api_handler.get_recent_runs(character,realm)
        if recent_runs:
            for run in recent_runs:
                run_date= run["completed_at"]
                run_date = datetime.strptime(run_date,"%Y-%m-%dT%H:%M:%S.%fZ")
                if run_date > last_wednesday:
                    num_of_weekly_runs = num_of_weekly_runs + 1
        return num_of_weekly_runs

    def get_last_reset_date(self):
        today = date.today()
        offset = (today.weekday() - WEDNESDAY) % 7
        last_wednesday = today - timedelta(days=offset)
        last_wednesday = datetime.strftime(last_wednesday,"%Y-%m-%dT%H:%M:%S.%fZ")
        last_wednesday = datetime.strptime(last_wednesday, "%Y-%m-%dT%H:%M:%S.%fZ")
        return last_wednesday

    def get_guilds_recent_runs(self,guild_name,realm):
        roster = self.blizzard_api_handler.get_max_level_players_from_guild(realm,guild_name)

        arr = []
        if roster:
            for player in roster:
                print ("Running on " + player['name'] + "\n")
                num_of_weekly_keys = self.get_weekly_keys(player['name'].lower(),player['realm'])
                if num_of_weekly_keys > 0:
                    a_dict = {"name":player['name'].lower() + "_" + player['realm'],"num_of_weekly_keys":num_of_weekly_keys}
                    arr.append(a_dict)
                    print ("appended: " + player['name'] + "\n")
                time.sleep(1)
            return arr



