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


#pp.pprint(bot.GetPlacementInfo( GameId=-1658651957, IsFullTime=1,OddsName='HomeOdds') )

#PlaceBet(self, GameId,  IsFullTime, MarketTypeId, OddsName, BookieOdds, Amount, GameType=GAME_TYPE_HANDCAP)
#pp.pprint(bot.PlaceBet( GameId=-1919729884, IsFullTime=1,OddsName='HomeOdds', BookieOdds='IBC:1.960', Amount=10) )



#pp.pprint(['Balance',bot.GetBalance()] )



#print requests.post(api_url + command, json=params,   headers=headers).json()

#quit()


#pp.pprint(  bot.PlaceBet(1035445197,'H',1, 0,  )    )

#print bot.Jogos[0].tempo, bot.Jogos[0].home
c=0
for jogo in bot.Jogos:
	print c,bot.jaFoiApostadoAH(jogo),jogo.GameId, "'"+jogo.home+"'",jogo.etapa, jogo.tempo, jogo.AH_home, jogo.AH_away, jogo.ind, jogo.ind2, jogo.gH, jogo.gA, '|', jogo.EvaluateGame(), jogo.BookieOdds_BEST
        c+=1
        
print "-------------------"
c=5
#for jogo in [bot.Jogos[c]]:
#	print c,jogo.GameId, "'"+jogo.home+"'",jogo.etapa, jogo.tempo, jogo.AH_home, jogo.AH_away, jogo.ind, jogo.ind2, jogo.gH, jogo.gA, '|', jogo.EvaluateGame(), jogo.BookieOdds_BEST
	#pp.pprint(   bot.ApostarAH(jogo=jogo, selecao=1, valor=10)   )
	
	
#	if jogo.GameId==-276724192: pp.pprint( bot.ApostaEmHandicap(jogo,-1) )
		#pp.pprint(jogo.feed)	
pp.pprint( bot.GetBets() )
#pp.pprint(bot.GetMatchesTotalcorner())

#for jogo in bot.GetMatchesTotalcorner():
#	if jogo['stats'] != {}: 
#	        if (jogo['stats']['ind']>=0 and  jogo['stats']['ind2']>=0) or (jogo['stats']['ind']<=-0 and  jogo['stats']['ind2']<=0): 
#			print jogo['Home'] +' v ' +jogo['Away'] + " @ " + jogo['LeagueName']+'|     ind:' +  str(jogo['stats']['ind']) + ' |     ind2:' + str(jogo['stats']['ind2'])
		
		
