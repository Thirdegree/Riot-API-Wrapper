'''This product is not endorsed, certified, or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.'''
import requests
import Errors


class Riot(object):
	def __init__(self, key):
		self.key = key
		test = requests.get("http://prod.api.pvp.net/api/lol/na/v1.1/champion?api_key=%s"%self.key)
		if test.status_code == 401:
			raise Errors.API_Key_Error("Invalid API Key \"%s\""%key)

	def get_all_champions(self, region='na'):
		champions = requests.get("http://prod.api.pvp.net/api/lol/%s/v1.1/champion?api_key=%s"%(region, self.key)).json()
		champion_list = []
		for champ in champions['champions']:
			champion_list.append(champ['name'])
		return champion_list

	def get_champion(self, champ_name,region='na'):
		champion = requests.get("http://prod.api.pvp.net/api/lol/%s/v1.1/champion?api_key=%s"%(region, self.key)).json()['champions']
		for champ in champion:
			if champ['name'] == champ_name:
				return champ
		return None