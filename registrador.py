# -*- coding: cp1252 -*-

from Bot import Bot 
import cPickle as pickle
from os.path import isfile
import pprint
pp = pprint.PrettyPrinter(indent=4)

bot=Bot()

print "AOKey= ", bot.AOKey
print "AOToken=", bot.AOToken
print "Bot logado?=", bot.IsLoggedIn()


#print bot.Jogos[0].tempo, bot.Jogos[0].home
for jogo in bot.Jogos:
	print jogo.home, jogo.etapa, jogo.tempo
#pp.pprint(bot.GetFeeds())

#for jogo in bot.GetMatchesTotalcorner():
#	if jogo['stats'] != {}: 
#	        if (jogo['stats']['ind']>=0 and  jogo['stats']['ind2']>=0) or (jogo['stats']['ind']<=-0 and  jogo['stats']['ind2']<=0): 
#			print jogo['Home'] +' v ' +jogo['Away'] + " @ " + jogo['LeagueName']+'|     ind:' +  str(jogo['stats']['ind']) + ' |     ind2:' + str(jogo['stats']['ind2'])
		
		
