import requests
import json


class BlizzardApiHandler:
    def __init__(self, client_id, client_pass):
        self.client_id = client_id
        self.client_pass = client_pass
        self.max_level = 60
        self.token_bearer = self.__get_token()

    def __get_token(self):
        token_url = "https://eu.battle.net/oauth/token"
        payload = {'grant_type': 'client_credentials'}
        files = [

        ]
        response = requests.request("POST", token_url, data=payload, files=files,
                                    auth=(self.client_id, self.client_pass))
        if response.status_code == 200:
            return json.loads(response.text)["access_token"]

    def get_guild_members_list(self, realm_name, guild_name, ):

        guild_members_url = 'https://eu.api.blizzard.com/data/wow/guild/' + realm_name + '/' + guild_name + \
                            '/roster?namespace=profile-eu&locale=en_US&access_token=' + self.token_bearer
        response = requests.request("GET", guild_members_url)
        if response.status_code != 200:
            return 0
        response_content = json.dumps(response.json())
        roster_object = json.loads(response_content)
        roster = roster_object["members"]
        return roster

    def sort_max_level_players(self, roster):
        max_level_players_list = []
        for member in roster:
            if member["character"]["level"] == self.max_level:
                max_level_players_list.append({
                    'name': member["character"]["name"],
                    'realm': member["character"]["realm"]["slug"],
                    'guild_rank': member["rank"]
                })
        return max_level_players_list

    def get_max_level_players_from_guild(self, realm_name, guild_name):
        return self.sort_max_level_players(self.get_guild_members_list(realm_name, guild_name))

    def get_best_runs(self, realm, character_name, season_id):
        mythic_keystone_season_details_url = 'https://eu.api.blizzard.com/profile/wow/character/' + realm + \
                                             '/' + character_name + '/mythic-keystone-profile/season/' + str(season_id) + \
                                             '?namespace=profile-eu&locale=en_us&access_token=' + self.token_bearer
        response = requests.request("GET", mythic_keystone_season_details_url)
        if response.status_code != 200:
            return 0
        response_content = json.dumps(response.json())
        response_content = json.loads(response_content)
        return response_content['best_runs']

    def get_best_runs_from_raiderio(self,character_name,realm_name):
        a_dict={}
        url = "https://raider.io/api/v1/characters/profile?region=eu&realm=" + realm_name +"&name=" + character_name + "&fields=mythic_plus_best_runs"
        response = requests.request("GET", url)
        if response.status_code != 200:
            return 0
        response_content = json.dumps(response.json())
        response_content = json.loads(response_content)
        a_dict = {'name':character_name,'realm':realm_name}

        print ("bluh")

    def get_recent_runs(self,character_name,character_realm):
        url = "https://raider.io/api/v1/characters/profile?region=eu&realm=" + character_realm +\
              "&name=" + character_name + "&fields=mythic_plus_recent_runs"
        try:
            response = requests.request("GET", url)
        except:
            response.status_code = 404
        if response.status_code != 200:
            return 0
        response_content = json.dumps(response.json())
        response_content = json.loads(response_content)
        recent_runs = response_content["mythic_plus_recent_runs"]
        return recent_runs



