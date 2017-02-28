# -*- coding: cp1252 -*-

from Bot import Bot 
import cPickle as pickle
from os.path import isfile
import pprint
pp = pprint.PrettyPrinter(indent=3)
import requests


bot=Bot()

print "AOKey= ", bot.AOKey
print "AOToken=", bot.AOToken
print "Bot logado?=", bot.IsLoggedIn()

api_url='https://webapi.asianodds88.com/AsianOddsService/'
command='PlaceBet'
params={'GameId':130721120,
	'GameType': 'H',
	'IsFullTime': 1,
	'MarketTypeId': 0,
	'OddsFormat': '00',
	'OddsName': 'AwayOdds',
	'SportsType': 1,
	'Amount':5,
	'BookieOdds':'SIN:2.480' }
	
headers={'AOToken': bot.AOToken} 
	
print requests.post(api_url + command, json=params,   headers=headers).json()

quit()


#pp.pprint(  bot.PlaceBet(1035445197,'H',1, 0,  )    )

#print bot.Jogos[0].tempo, bot.Jogos[0].home
#for jogo in bot.Jogos:
#	print jogo.GameId, "'"+jogo.home+"'",jogo.etapa, jogo.tempo, jogo.AH_home, jogo.AH_away, jogo.ind, jogo.ind2, jogo.gH, jogo.gA, '|', jogo.EvaluateGame(), jogo.BookieOdds_BEST
#	if jogo.GameId==-276724192: pp.pprint( bot.ApostaEmHandicap(jogo,-1) )
		#pp.pprint(jogo.feed)	
pp.pprint( bot.GetBets() )
#pp.pprint(bot.GetMatchesTotalcorner())

#for jogo in bot.GetMatchesTotalcorner():
#	if jogo['stats'] != {}: 
#	        if (jogo['stats']['ind']>=0 and  jogo['stats']['ind2']>=0) or (jogo['stats']['ind']<=-0 and  jogo['stats']['ind2']<=0): 
#			print jogo['Home'] +' v ' +jogo['Away'] + " @ " + jogo['LeagueName']+'|     ind:' +  str(jogo['stats']['ind']) + ' |     ind2:' + str(jogo['stats']['ind2'])
		
		
