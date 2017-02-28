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
      #Converte o handicap para decimaol 0.25. Exemplo:   0-0.5 para -0.25
      def handicapStrToFloat(h_str, favorito):
         arr=h_str.split('-') 
         if arr[0]=='': return ''
         if len(arr)==1: arr+=arr   
         arr[0]=float(arr[0])
         arr[1]=float(arr[1])
         return (-1 if favorito else 1)*sum(arr)/2.0

      self.GameId=feed['GameId']
      
      if feed['InGameMinutes']==60: self.etapa='HT'
      elif feed['InGameMinutes']>120: self.etapa='2H'
      elif feed['InGameMinutes']>60: self.etapa='1H'
      else: self.etapa='0'
      
      #self.feed=feed
      
      if (feed['stats']=={}) or (self.etapa=='HT') or (self.etapa=='0'): return None
      
      self.tempo=feed['InGameMinutes']-60 if self.etapa=='1H' else (45+feed['InGameMinutes']-120 if self.etapa=='2H' else -1)
      self.ativo=feed['IsActive']
      self.home=feed['HomeTeam']['Name']
      self.away=feed['AwayTeam']['Name'] 
      
      self.AH_home=handicapStrToFloat(feed['HalfTimeHdp']['Handicap'], feed['Favoured']==1) if self.etapa=='1H' else handicapStrToFloat(feed['FullTimeHdp']['Handicap'], feed['Favoured']==1) 
      self.AH_away=handicapStrToFloat(feed['HalfTimeHdp']['Handicap'], feed['Favoured']==2) if self.etapa=='1H' else handicapStrToFloat(feed['FullTimeHdp']['Handicap'], feed['Favoured']==2) 
  
      if self.AH_home=='': return None
      
      self.ind=feed['stats']['ind']
      self.ind2=feed['stats']['ind2']
      self.gH=feed['stats']['gH']
      self.gA=feed['stats']['gA']

   def EvaluateGame(self):
      """
         Método para avaliar se uma aposta será feita ou não.
         
         args:
            
         return:
            true quando deve-se apostar
            false quando nao se deve apostar
            
         TODO: mudar parâmetros para um objeto do tipo Jogo. 
               Ao invés de retornar true ou false, chamar o método da aposta.
      """
      def primeroTempo(): return self.etapa=='1H'
      def segundoTempo(): return self.etapa=='2H'
      
      #Apostar no Home
      if ( ( self.ind>=3.50 ) and  ( self.ind2>=2.5) and ( self.AH_Home==-0.5) and ( self.gH<=1) and ( (primeiroTempo() and (self.tempo>=25)) or (segundoTempo() and (self.tempo>=70)) ) ): return 1
      if ( ( self.ind>=2.50 ) and  ( self.ind2>=1.50) and ( self.AH_Home==-0.25)  and  ( self.gH==0.0) and  ( (primeiroTempo() and (self.tempo>=25)) or  (segundoTempo() and (self.tempo>=70))) ): return 1
      if ( ( self.ind>=2.00 ) and  ( self.ind2>=1.00) and ( self.AH_Home>=0)  and  ( self.gH==0.0) and  ( (primeiroTempo() and (self.tempo>=25)) or  (segundoTempo() and (self.tempo>=70))    ) ): return 1
      
      #Apostar em away
      if ( ( self.ind<=-3.50 ) and  ( self.ind2<=-2.5) and ( self.AH_Away==-0.5)  and  ( self.gA<=1)  and  ( (primeiroTempo() and (self.tempo>=25)) or  (segundoTempo() and (self.tempo>=70))    ) ): return -1
      if ( ( self.ind<=-2.50 ) and  ( self.ind2<=-1.50) and ( self.AH_Away==-0.25)  and  ( self.gA==0.0)  and  ( (primeiroTempo() and (self.tempo>=25)) or  (segundoTempo() and (self.tempo>=70))    ) ): return -1
      if ( ( self.ind<=-2.00 ) and  ( self.ind2<=-1.00) and ( self.AH_Away>=0)  and  ( self.gA==0.0) and  ( (primeiroTempo() and (self.tempo>=25)) or  (segundoTempo() and (self.tempo>=70))    ) ): return -1
      
      return 0

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
   global IS_FULL_TIME
   global IS_NOT_FULL_TIME
   global GAME_TYPE_HANDCAP
   global GAME_TYPE_OVERUNDER
   global GAME_TYPE_1X2GAME
   global CHANGE_ODDS_YES 
   global CHANGE_ODDS_NO

   

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

   def UpateJogos(self):
      Jogos=[Jogo(feed) for feed in self.GetMatchesTotalcorner()]
      Jogos=[jogo for jogo in Jogos if hasattr(jogo, 'tempo') ]
      self.Jogos=[jogo for jogo in Jogos if jogo.AH_home!='' ]
   
   
   
   
   def GetBets(self):
      return self.API('GetBets',headers={'AOToken': self.AOToken} )  
   
   def PlaceBet(self, GameId, GameType, IsFullTime, MarketTypeId, oddsName, AcceptChangedOdds, amount):
      """
      Método que faz a aposta.
      
      Args:
            oddsName: pode ser 'AwayOdds', 'HomeOdds', ou 'DrawOdds' em mercados 1x2.
            Qual é o tipo de odds a ser apostado "ISN:-0.84,SBO:-0.75,.."
            amount: quantidade a ser apostada.
         
      """

      return self.API('PlaceBet',  params=	{
                                    #"PlaceBetId":"{uniqueID (optional)}", #Não precisa passar
                                    "GameId": GameId,
                                    "GameType": GameType,
                                    "IsFullTime":IsFullTime,
                                    'MarketTypeId':MarketTypeId,
                                    "OddsFormat": ODDSFORMAT_DECIMAL, #optional parameter
                                    "OddsName":oddsName,
                                    "SportsType":SPORTS_TYPE_SOCCER,
                                    "AcceptChangedOdds":CHANGE_ODDS_YES,
                                    #"BookieOdds":bookieOdds,    #Para todos os bookies não precisa passar o paremtro
                                    "Amount":amount}
      , method='POST'                              
      , headers={'AOToken': self.AOToken} )   
   
   def ApostaEmHandicap(self, jogo, selecao):
      """
      Método que faz a aposta no Asian Handicap Live de acordo com a seleção
         selecao: 1 aposta no home
         selecao: 2 aposta no away
      
      Args:
            jogo é objeto do tipo Jogoo

            amount: quantidade a ser apostada.
            
      """
      return self.PlaceBet(jogo.GameId,GAME_TYPE_HANDCAP, IS_FULL_TIME if jogo.etapa=='2H' else IS_NOT_FULL_TIME, MARKETTYPE_LIVE, 'FullTimeHdp' if  jogo.etapa=='2H' else 'HalfTimeHdp', CHANGE_ODDS_YES, 5.00   )
      
   def __init__(self):
      """
       Método __init__
       Inicializa o objeto. É chamado quando o objeto é criado.
       
       Assim que o objeto é criado, o login é efetuado. E o AOKey e AOToken são guardados. E depois ele se registra.
       
       Args:
         Não há parâmetros. Ele meio que já sabe o que fazer.
        
      """

      self.LoginAndRegister()

      self.UpateJogos()