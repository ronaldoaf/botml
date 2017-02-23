# -*- coding: cp1252 -*-
import requests

class KickOffBot(object):
   def doLogin(self):
      payload = {'Username': 'webapiuser40', 'Password': 'b59c5d190b12d5b7fa3b425aa69dcb8d'}
      r = requests.get('https://webapi.asianodds88.com/AsianOddsService/Login', params=payload)
      return r.json()['Result']['SuccessfulLogin']
   def doPlaceBet(self):
      parameters = {
         "AcceptChangedOdds":2147483647,
         "Amount":1.26743233E+15,
         "BookieOdds":"String content",
         "GameId":9223372036854775807,
         "GameType":"String content",
         "IsFullTime":2147483647,
         "MarketTypeId":"String content",
         "OddsFormat":"String content",
         "OddsName":"String content",
         "PlaceBetId":"String content",
         "SportsType":2147483647 
      }
      r = requests.post('https://webapi.asianodds88.com/AsianOddsService/PlaceBet', data = parameters)
      return True #Alterar depois
      
#Começando a testar (ficará em um arquivo separado futuramente)
import unittest
class TestKickOffBot(unittest.TestCase):
   def testLoginResponse(self):
      kob = KickOffBot()
      self.assertTrue( kob.doLogin()  )
   def testPlaceBet(self):
      kob = KickOffBot()
      self.assertTrue( kob.doPlaceBet() )
if __name__ == '__main__':
   unittest.main()

print 'teste commmit'
