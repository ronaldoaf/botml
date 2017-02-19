# -*- coding: cp1252 -*-
import requests


class Bot(object):
   username='webapiuser40'
   password='b59c5d190b12d5b7fa3b425aa69dcb8d'
   
   def API(self,command, method='GET', params={}, headers={}):
   	api_url='https://webapi.asianodds88.com/AsianOddsService/'
   	if method=='GET':  return requests.get(api_url  + command, params=params, headers=headers).json()['Result']
   	if method=='POST': return requests.post(api_url + command, data=params,   headers=headers).json()['Result']
   	
   	
   def Login(self):
   	return self.API('Login', params={'Username': self.username, 'Password': self.password} )
   
   def Register(self):
   	return self.API('Register', params={'Username': self.username}, headers={'AOKey': self.AOKey, 'AOToken': self.AOToken} )
	
   def IsLoggedIn(self):
   	return self.API('IsLoggedIn', headers={'AOToken': self.AOToken} )
   
   
   
   def GetAccountSummary(self):
   	return self.API('GetAccountSummary', headers={'AOToken': self.AOToken} )
   
   
   
   #Retorna uma lista com todas as ligas que de futebol que jogos acontecendo no momento
   def GetLeagues(self):
   	return self.API('GetLeagues',  params={'sportsType': 1, 'marketTypeId': 0}, headers={'AOToken': self.AOToken} )['Sports'][0]['League']
   
   #Retorna a lista com os jogos de futebol ativos no momento
   def GetMatches(self):
   	return self.API('GetMatches',  params={'sportsType': 1, 'marketTypeId': 0}, headers={'AOToken': self.AOToken} )['EventSportsTypes'][0]['Events']
   	
   	
   def __init__(self):
      login_result=self.Login()	     
      self.AOKey=login_result['Key']
      self.AOToken=login_result['Token']      
      self.Register()



   