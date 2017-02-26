# -*- coding: cp1252 -*-
import requests
import json
from distance import nlevenshtein as distance

class Jogo(object):
   def __init__(self, feed):
      """
      Método __init__
      Inicializa o objeto. É chamado quando o objeto é criado.
      
      Assim que o objeto é criado, ele atribui os dados relevantes.
      
      Args:
         feed é um dicionáro com o dados provenientes do método Bot.GetFeeds() e por posteriormente alterado por Bot.GetMatchesTotalcorner()   
      """
      self.Update(feed)
      
      
   
   def Update(self, feed):
      

      if feed['InGameMinutes']==60: self.etapa='HT'
      elif feed['InGameMinutes']>120: self.etapa='2H'
      elif feed['InGameMinutes']>60: self.etapa='1H'
      else: self.etapa='0'
      
      self.tempo=feed['InGameMinutes']-60 if self.etapa=='1H' else (45+feed['InGameMinutes']-120 if self.etapa=='2H' else -1)
      self.ativo=feed['IsActive']
      self.home=feed['HomeTeam']['Name']
      self.InGameMinutes=feed['InGameMinutes']
      
      #self.AH_home=feed['HalfTimeHdpfeed']['Handicap'] 
      

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
   global ODDSFORMAT_DECIMAL

   

   SPORTS_TYPE_SOCCER = 1 # 1 = Futebol. 2 = Basquete, etc...
   MARKETTYPE_LIVE = 0  #0 : Live Market. É esse!
   MARKETTYPE_TODAY = 1 #1 : Today Market
   MARKETTYPE_EARLY = 2 #2 : Early Market
   ODDSFORMAT_DECIMAL ='00'
   
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
	FIRST_ITEM = 0
	return self.API('GetFeeds',  params={'sportsType': SPORTS_TYPE_SOCCER, 'marketTypeId': MARKETTYPE_LIVE, 'oddsFormat': ODDSFORMAT_DECIMAL }, headers={'AOToken': self.AOToken} )['Sports'][FIRST_ITEM]['MatchGames']
		
   def GetMatchesTotalcorner(self):
      """
       Método GetMatchesTotalcorner
       Retorna a lista com os jogos de futebol ativos no momento com correspondente no Totalcorner
         são adicionadas as chaves  'Home_totalcorner', 'Away_totalcorner' e 'stats' (provenientes de http://aposte.me/live)
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
       
      """  
      def jogoMaisProximo(jogo, lista_de_jogos):
         jogo['Home_totalcorner']=''
         jogo['Away_totalcorner']=''
         min_distance=0.7
         j_atual={}
         for j in lista_de_jogos:
            dis_atual=distance( j['home']+j['away'], jogo['Home']+jogo['Away'] )
            if dis_atual<min_distance:
               j_atual=j
               min_distance=dis_atual
         if j_atual != {}: 
            jogo['Home_totalcorner']=j_atual['home']	
            jogo['Away_totalcorner']=j_atual['away']
         return jogo
         

      #Função que ajusta o nome da equipe do AsianOdds88 para ficar mais parecida com o padrão do TotalCorner	
      def normalizaNome(nome): return nome.replace('(N)','').replace('(W)','Women').replace('(R)','Reserves')


      #Carrega os jogos do totalcorner que provem de um script do phantomjs que fica o rodando, gerando o arquivo a cada 1 minuto
      with open('jogos_totalcorner.json') as data_file: jogos_totalcorner = json.load(data_file)  

      #Gera um dicionario cujas chaves são os distintos timestamps e o valores são listas com todos os jogos_totalcorner que começam nesses timestamps
      jogos_por_timestamp={}
      for timestamp in set([jogo['timestamp'] for jogo in  jogos_totalcorner ]):
         jogos_por_timestamp[timestamp]=[jogo for jogo in jogos_totalcorner if jogo['timestamp']==timestamp]
            
         
      #Remove os matches com 'No. of Corners' e Fantasy Matches que não são o foco do Bot
      matches=[ match for match in self.GetFeeds() if 'No. of Corners' not in match['HomeTeam']['Name']  and match['LeagueName']!='FANTASY MATCH' ]


      #Cada jogo do AsianOdss ao vivo no momento 
      for i in range(len(matches)):      
         #Ajusta o nome das equipes para ficarem mais proximas do padrão do TotalCorner
         matches[i]['Home']=normalizaNome(matches[i]['HomeTeam']['Name'])
         matches[i]['Away']=normalizaNome(matches[i]['AwayTeam']['Name'])
         
         #Preenche matches[i]['Home_totalcorner'] e matches[i]['Home_totalcorner'] através da comparação da distancia entre strings  
         matches[i]=jogoMaisProximo(matches[i], jogos_por_timestamp[ matches[i]['StartTime'] ] if matches[i]['StartTime'] in jogos_por_timestamp else [] )

      #Remove os jogos que que não houve não encontrados no Totalcorenr
      matches= [match for match in matches if match['Home_totalcorner']!='' ] 

      #Adiciona as estatisticas provenientes do aposte.me
      stats=requests.get('http://aposte.me/live/stats.php').json() 
      for i in range(len( matches )):
         matches[i]['stats']={}
         for stat in stats:	      
            if (stat['home']==matches[i]['Home_totalcorner'] and stat['away']==matches[i]['Away_totalcorner']): matches[i]['stats']=stat   				 
      return matches  

	
   
   def __init__(self):
     """
       Método __init__
       Inicializa o objeto. É chamado quando o objeto é criado.
       
       Assim que o objeto é criado, o login é efetuado. E o AOKey e AOToken são guardados. E depois ele se registra.
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
        
     """
     self.LoginAndRegister()
     self.Jogos=[Jogo(feed) for feed in self.GetMatchesTotalcorner()]