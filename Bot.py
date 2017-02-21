# -*- coding: cp1252 -*-
import requests


class Bot(object):
   """
      
      Atributos:
         username: Nome de usuário para acessar o WebService
         password: Senha para acessar o WebService
      
      Constantes:
         SPORTS_TYPE_SOCCER: Esporte alvo no caso é o futebol. = 1.
         MARKETTYPE_LIVE: Mercado alvo é o ao vivo. = 0.
   """
   username='webapiuser40'
   password='b59c5d190b12d5b7fa3b425aa69dcb8d'
   global SPORTS_TYPE_SOCCER
   global MARKETTYPE_LIVE
   global MARKETTYPE_TODAY
   global MARKETTYPE_EARLY
   
   SPORTS_TYPE_SOCCER = 1 # 1 = Futebol. 2 = Basquete, etc...
   MARKETTYPE_LIVE = 0  #0 : Live Market. É esse!
   MARKETTYPE_TODAY = 1 #1 : Today Market
   MARKETTYPE_EARLY = 2 #2 : Early Market
   
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
      if method=='GET':  return requests.get(api_url  + command, params=params, headers=headers).json()['Result']
      if method=='POST': return requests.post(api_url + command, data=params,   headers=headers).json()['Result']
   	   	
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
	
   def IsLoggedIn(self):
      """
         Método que verifica se o usuário está logado ou não no site Asianodds88.
         
         Args:
            Não há parâmetros. Ele meio que já sabe o que fazer.
         
      """
      return self.API('IsLoggedIn', headers={'AOToken': self.AOToken} )  
   
   def GetAccountSummary(self):
      return self.API('GetAccountSummary', headers={'AOToken': self.AOToken} )
   
   def GetLeagues(self):
      """
         Método GetLeagues
         Retorna uma lista com todas as ligas que de futebol que jogos acontecendo no momento
         
         Args:
            Não há parâmetros. Ele meio que já sabe o que fazer.
         
      """
      FIRST_ITEM = 0
      return self.API('GetLeagues',  params={'sportsType': SPORTS_TYPE_SOCCER, 'marketTypeId': MARKETTYPE_LIVE}, headers={'AOToken': self.AOToken} )['Sports'][FIRST_ITEM]['League']
   
   def GetMatches(self):
      """
         Método GetMatches
         Retorna a lista com os jogos de futebol ativos no momento.
         
         Args:
            Não há parâmetros. Ele meio que já sabe o que fazer.
         
      """
      FIRST_ITEM = 0
      return self.API('GetMatches',  params={'sportsType': SPORTS_TYPE_SOCCER, 'marketTypeId': MARKETTYPE_LIVE}, headers={'AOToken': self.AOToken} )['EventSportsTypes'][FIRST_ITEM]['Events']
   	
   	
   def __init__(self):
      """
         Método __init__
         Inicializa o objeto. É chamado quando o objeto é criado.
         
         Assim que o objeto é criado, o login é efetuado. E o AOKey e AOToken são guardados. E depois ele se registra.
         
         Args:
            Não há parâmetros. Ele meio que já sabe o que fazer.
         
      """
      login_result=self.Login()	     
      self.AOKey=login_result['Key']
      self.AOToken=login_result['Token']      
      self.Register()



   
