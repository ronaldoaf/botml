# -*- coding: cp1252 -*-
import requests

class API(object):
   """
      Classe que acessar o API da AsianOdds88
   """

   global SPORTS_TYPE_SOCCER
   global MARKETTYPE_LIVE
   global MARKETTYPE_TODAY
   global MARKETTYPE_EARLY
   global ODDSFORMAT_DECIMAL
   global IS_FULL_TIME
   global IS_NOT_FULL_TIME
   global GAME_TYPE_HANDCAP
   global GAME_TYPE_OVERUNDER
   global GAME_TYPE_1X2GAME
   global CHANGE_ODDS_YES 
   global CHANGE_ODDS_NO
   global FIRST_ITEM
   

   SPORTS_TYPE_SOCCER = 1 # 1 = Futebol. 2 = Basquete, etc...
   MARKETTYPE_LIVE = 0  #0 : Live Market. É esse!
   MARKETTYPE_TODAY = 1 #1 : Today Market
   MARKETTYPE_EARLY = 2 #2 : Early Market
   ODDSFORMAT_DECIMAL ='00'
   IS_FULL_TIME = 1
   IS_NOT_FULL_TIME = 0
   GAME_TYPE_HANDCAP = "H" #AsianHandicap
   GAME_TYPE_OVERUNDER = "O" #OverUnder
   GAME_TYPE_1X2GAME = "X" #1X2game
   CHANGE_ODDS_YES = 1 #meaning that lower odds will be automatically accepted
   CHANGE_ODDS_NO = 0 #reject if the odds became lower
   FIRST_ITEM = 0
   
   def API(self,command, method='GET', params={}, headers={}):
     """
       Método API
       Efetua as chamadas para o WebService do site AsianOdds88.
       
       Args:
         comando: Nome do serviço a ser chamado. 'Login', por exemplo.
         method: Tipo de método. 'GET' ou 'POST'.
         params: Parâmetros necessários para chamar o WebService. {'Username': 'usuario', 'Password': '1234'} é um exemplo.
         headers: Header a ser passado, caso necessário. {'AOKey': 'd6c8064de65f13f84a17d3cd0d3d6a96', 'AOToken': '3220042181867839342977241801'} é um exemplo. 
     """
     api_url='https://webapi.asianodds88.com/AsianOddsService/'
     if method=='GET':  request_result=requests.get(api_url  + command, params=params, headers=headers).json()
     if method=='POST': request_result=requests.post(api_url + command, json=params,   headers=headers).json()
     return request_result['Result'] if  'Result' in request_result else request_result
     
   def Login(self):
     """
       Método Login
       Efetua Login no Asianodds88.
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
       
     """
     return self.API('Login', params={'Username': self.username, 'Password': self.password} )

   def Register(self):
     """
       Método Login
       Se registra no Asianodds88. Deve ser feito em até 60 segundos depois do login.
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
       
     """
     return self.API('Register', params={'Username': self.username}, headers={'AOKey': self.AOKey, 'AOToken': self.AOToken} )

   def LoginAndRegister(self):
      """
       Método Login
       Executar os métodos Login e Register e armazenas os tokens
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
       
      """
      login_result=self.Login()
      self.AOKey=login_result['Key']
      self.AOToken=login_result['Token']     
      self.Register()

      
   def IsLoggedIn(self):
     """
       Método que verifica se o usuário está logado ou não no site Asianodds88.
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
       
     """
     return self.API('IsLoggedIn', headers={'AOToken': self.AOToken} )  

   def GetAccountSummary(self):
     return self.API('GetAccountSummary', headers={'AOToken': self.AOToken} )


   def GetFeeds(self):
      """
       Método GetMatches
       Retorna a lista com os jogos de futebol ativos no momento.
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
       
      """
      
      return self.API('GetFeeds',  params={'sportsType': SPORTS_TYPE_SOCCER, 'marketTypeId': MARKETTYPE_LIVE, 'oddsFormat': ODDSFORMAT_DECIMAL }, headers={'AOToken': self.AOToken} )['Sports'][FIRST_ITEM]['MatchGames']
  
   
   
   def GetBets(self):
      return self.API('GetBets',headers={'AOToken': self.AOToken} )  
   
   def GetPlacementInfo(self,GameId, IsFullTime,OddsName, GameType=GAME_TYPE_HANDCAP ):
      return self.API('GetPlacementInfo',  method='POST', params={'GameId': GameId, 'GameType': GameType, 'IsFullTime': IsFullTime, 'Bookies': 'IBC,SBO,SIN,PIN,ISN,GA', 'OddsName': OddsName, 'OddsFormat': ODDSFORMAT_DECIMAL, 'SportsType': SPORTS_TYPE_SOCCER }, headers={'AOToken': self.AOToken} )
   
   
   #{u'Message': u'Bet has not been placed as an error occured.  Note : You must always call GetPlacementInfo prior to calling a PlaceBet. Did you call GetPlacementInfo before calling PlaceBet? If not, please do so. ', u'Code': -1, u'Result': {u'PlacementData': [{u'Bookie': u''}], u'Message': None, u'BetPlacementReference': None}}
   def PlaceBet(self, GameId,  IsFullTime, OddsName, BookieOdds, Amount, GameType=GAME_TYPE_HANDCAP,  MarketTypeId=MARKETTYPE_LIVE):
      """
      Método que faz a aposta.
      
      Args:
            oddsName: pode ser 'AwayOdds', 'HomeOdds', ou 'DrawOdds' em mercados 1x2.
            Qual é o tipo de odds a ser apostado 'ISN:-0.84,SBO:-0.75,..'
            amount: quantidade a ser apostada.
         
      """

      return self.API('PlaceBet',  params=	{
                                    #"PlaceBetId":"{uniqueID (optional)}", #Não precisa passar
                                    "GameId": GameId,
                                    "GameType": GameType,
                                    "IsFullTime":IsFullTime,
                                    'MarketTypeId':MarketTypeId,
                                    "OddsFormat": ODDSFORMAT_DECIMAL, #optional parameter
                                    "OddsName":OddsName,
                                    "SportsType":SPORTS_TYPE_SOCCER,
                                    "AcceptChangedOdds":CHANGE_ODDS_YES,
                                    "BookieOdds":BookieOdds,    
                                    "Amount":Amount}
      , method='POST'                              
      , headers={'AOToken': self.AOToken} )   
      
