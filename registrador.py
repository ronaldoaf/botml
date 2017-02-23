# -*- coding: cp1252 -*-

from Bot import Bot 
import cPickle as pickle
from os.path import isfile
import pprint
pp = pprint.PrettyPrinter(indent=4)

#Se existir o arquivo 'bot.pickle', carrega o bot do arquivo sen�o cria uma nova inst�ncia
if isfile('bot.pickle'):
    with open('bot.pickle', 'rb') as handle:
        bot = pickle.load(handle)
        
        #Se o bot n�o estiver logado tenta uma nova sess�o.
        if bot.IsLoggedIn()['CurrentlyLoggedIn']==False: bot=Bot()          
else:
    #Se n�o existir o arquivo bot.pickle, cria uma nova inst�ncia
    bot=Bot()

#salva para o arquivo
with open('bot.pickle', 'wb') as handle:
    pickle.dump(bot, handle)

print "AOKey= ", bot.AOKey
print "AOToken=", bot.AOToken
print "Bot logado?=", bot.IsLoggedIn()

#pp.pprint(bot.GetMatches())

for jogo in bot.GetMatchesTotalcorner():
	if jogo['stats'] != {}: 
		print jogo['Home'] +' v ' +jogo['Away'] + " @ " + jogo['LeagueName']+'|     ind:' +  str(jogo['stats']['ind']) + ' |     ind2:' + str(jogo['stats']['ind2'])
		
		
