# -*- coding: cp1252 -*-
import requests
import json
from distance import nlevenshtein as distance

class Bot(object):
    """
      
      Atributos: 
         username: Nome de usu�rio para acessar o WebService
         password: Senha para acessar o WebService
      
      Constantes:
         SPORTS_TYPE_SOCCER: Esporte alvo no caso � o futebol. = 1.
         MARKETTYPE_LIVE: Mercado alvo � o ao vivo. = 0.
    """
    username='webapiuser40'
    password='b59c5d190b12d5b7fa3b425aa69dcb8d'
    global SPORTS_TYPE_SOCCER
    global MARKETTYPE_LIVE
    global MARKETTYPE_TODAY
    global MARKETTYPE_EARLY

    SPORTS_TYPE_SOCCER = 1 # 1 = Futebol. 2 = Basquete, etc...
    MARKETTYPE_LIVE = 0  #0 : Live Market. � esse!
    MARKETTYPE_TODAY = 1 #1 : Today Market
    MARKETTYPE_EARLY = 2 #2 : Early Market

    def API(self,command, method='GET', params={}, headers={}):
      """
         M�todo API
         Efetua as chamadas para o WebService do site AsianOdds88.
         
         Args:
            comando: Nome do servi�o a ser chamado. 'Login', por exemplo.
            method: Tipo de m�todo. 'GET' ou 'POST'.
            params: Par�metros necess�rios para chamar o WebService. {'Username': 'usuario', 'Password': '1234'} � um exemplo.
            headers: Header a ser passado, caso necess�rio. {'AOKey': 'd6c8064de65f13f84a17d3cd0d3d6a96', 'AOToken': '3220042181867839342977241801'} � um exemplo. 
      """
      api_url='https://webapi.asianodds88.com/AsianOddsService/'
      if method=='GET':  return requests.get(api_url  + command, params=params, headers=headers).json()['Result']
      if method=='POST': return requests.post(api_url + command, data=params,   headers=headers).json()['Result']
      

    def Login(self):
      """
         M�todo Login
         Efetua Login no Asianodds88.
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
      """
      return self.API('Login', params={'Username': self.username, 'Password': self.password} )

    def Register(self):
      """
         M�todo Login
         Se registra no Asianodds88. Deve ser feito em at� 60 segundos depois do login.
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
      """
      return self.API('Register', params={'Username': self.username}, headers={'AOKey': self.AOKey, 'AOToken': self.AOToken} )

    def LoginAndRegister(self):
        """
         M�todo Login
         Executar os m�todos Login e Register e armazenas os tokens
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
        """
        login_result=self.Login()
        self.AOKey=login_result['Key']
        self.AOToken=login_result['Token']      
        self.Register()

        
    def IsLoggedIn(self):
      """
         M�todo que verifica se o usu�rio est� logado ou n�o no site Asianodds88.
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
      """
      return self.API('IsLoggedIn', headers={'AOToken': self.AOToken} )  

    def GetAccountSummary(self):
      return self.API('GetAccountSummary', headers={'AOToken': self.AOToken} )

    def GetLeagues(self):
      """
         M�todo GetLeagues
         Retorna uma lista com todas as ligas que de futebol que jogos acontecendo no momento
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
      """
      FIRST_ITEM = 0
      return self.API('GetLeagues',  params={'sportsType': SPORTS_TYPE_SOCCER, 'marketTypeId': MARKETTYPE_LIVE}, headers={'AOToken': self.AOToken} )['Sports'][FIRST_ITEM]['League']

    def GetMatches(self):
      """
         M�todo GetMatches
         Retorna a lista com os jogos de futebol ativos no momento.
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
      """
      FIRST_ITEM = 0
      return self.API('GetMatches',  params={'sportsType': SPORTS_TYPE_SOCCER, 'marketTypeId': MARKETTYPE_LIVE}, headers={'AOToken': self.AOToken} )['EventSportsTypes'][FIRST_ITEM]['Events']

    def GetMatchesTotalcorner(self):
        """
         M�todo GetMatchesTotalcorner
         Retorna a lista com os jogos de futebol ativos no momento com correspondente no Totalcorner
            s�o adicionadas as chaves  'Home_totalcorner', 'Away_totalcorner' e 'stats' (provenientes de http://aposte.me/live)
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
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
            

        #Fun��o que ajusta o nome da equipe do AsianOdds88 para ficar mais parecida com o padr�o do TotalCorner	
        def normalizaNome(nome): return nome.replace('(N)','').replace('(W)','Women').replace('(R)','Reserves')


        #Carrega os jogos do totalcorner que provem de um script do phantomjs que fica o rodando, gerando o arquivo a cada 1 minuto
        with open('jogos_totalcorner.json') as data_file: jogos_totalcorner = json.load(data_file)  

        #Gera um dicionario cujas chaves s�o os distintos timestamps e o valores s�o listas com todos os jogos_totalcorner que come�am nesses timestamps
        jogos_por_timestamp={}
        for timestamp in set([jogo['timestamp'] for jogo in  jogos_totalcorner ]):
            jogos_por_timestamp[timestamp]=[jogo for jogo in jogos_totalcorner if jogo['timestamp']==timestamp]
                
            
        #Remove os matches com 'No. of Corners' e Fantasy Matches que n�o s�o o foco do Bot
        matches=[ match for match in self.GetMatches() if 'No. of Corners' not in match['Home']  and match['LeagueName']!='FANTASY MATCH' ]

        #Cada jogo do AsianOdss ao vivo no momento 
        for i in range(len(matches)):
                #Ajusta o nome das equipes para ficarem mais proximas do padr�o do TotalCorner
            matches[i]['Home']=normalizaNome(matches[i]['Home'])
            matches[i]['Away']=normalizaNome(matches[i]['Away'])
            
            #Preenche matches[i]['Home_totalcorner'] e matches[i]['Home_totalcorner'] atrav�s da compara��o da distancia entre strings  
            matches[i]=jogoMaisProximo(matches[i], jogos_por_timestamp[ matches[i]['StartTime'] ] if matches[i]['StartTime'] in jogos_por_timestamp else [] )

        #Remove os jogos que que n�o houve n�o encontrados no Totalcorenr
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
         M�todo __init__
         Inicializa o objeto. � chamado quando o objeto � criado.
         
         Assim que o objeto � criado, o login � efetuado. E o AOKey e AOToken s�o guardados. E depois ele se registra.
         
         Args:
            N�o h� par�metros. Ele meio que j� sabe o que fazer.
         
      """
      self.LoginAndRegister()
