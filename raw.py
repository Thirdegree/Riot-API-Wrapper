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

	def get_summoner_Id(self, summoner_name, region='na'):
		summoner_name = summoner_name.replace(" ", "")
		summoner = requests.get("http://prod.api.pvp.net/api/lol/%s/v1.1/summoner/by-name/%s?api_key=%s"%(region, summoner_name, self.key))
		if summoner.status_code == 404:
			raise Errors.Summoner_Error("Summoner does not exist")
		summoner_id = summoner.json()['id']
		return summoner_id

	def get_masteries(self, summoner_Id, page=None, region='na'):
		summoner_masteries = requests.get("http://prod.api.pvp.net/api/lol/%s/v1.1/summoner/%s/masteries?api_key=%s"%(region, summoner_Id, self.key))
		if summoner_masteries.status_code == 404:
			raise Errors.Summoner_Error("Summoner does not exist")
		masteries = {i['name']: i['talents'] for i in summoner_masteries.json()['pages']}
		if page:
			return masteries[page]
		else:
			return masteries

	def get_runes(self, summoner_Id, page=None, region='na'):
		summoner_runes = requests.get("http://prod.api.pvp.net/api/lol/%s/v1.1/summoner/%s/runes?api_key=%s"%(region, summoner_Id, self.key))
		if summoner_runes.status_code == 404:
			raise Errors.Summoner_Error("Summoner does not exist")
		slots = {summoner_runes.json()['pages'][i]['name']:summoner_runes.json()['pages'][i]['slots'] for i in range(len(summoner_runes.json()['pages']))}
		l = {i:[s['rune']['name'] for s in slots[i]] for i in slots}
		runes = {i:{m['rune']['name']:(m['rune']['description'], l[i].count(m['rune']['name'])) for m in slots[i]} for i in slots}
		return runes
