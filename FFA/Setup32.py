#Backing up (and switching?) from jupyter notebook to visual studio code and github


import numpy as np
import os,glob
import pandas as pd
import gc
import random
import string



class Files: #used for making global variables of file path locations
    pass


               

class Player:
#Has to do with the player PK and their absolute and relative scores 
    player_list = []
    
    
    player_old_dict = {} #creates a dictioanry of player scores from file
    player_old_last = {} #creates a dictionary of player last played game from file
    player_old_stand_score = {}  
    player_new_dict = {} #createsa a dictionary of player scores from file, but from new game
    player_new_last = {} #creates a dictionary of player's last played game from new game
    player_new_stand_score = {}
    
    all_new_games_player_dict = {}
    all_new_games_player_standard_dict = {}
    all_new_games_player_last_dict = {}
    
    
    def __init__(self, player_key,xscore=0,standardized_score=0,last_game_played=None):
        self.score = xscore
        self.standard_score = standardized_score
        self.pkey = player_key
        self.last_game = last_game_played
        Player.player_list.append(self)
        

    def last_played(self):
        self.rounds_ago_player = 0
        try:
            self.version = self.last_game[3:5]
            self.series = self.last_game[5:7]
            self.round = self.last_game[7:9]
            self.group = self.last_game[9:10]
            self.num_players = self.last_game[10:11]
            print("or print this")
        except:
            self.version = Game.current_round[0].version
            self.series = Game.current_round[0].series
            self.group = list(string.ascii_uppercase)[len(Round.next_round_players) // 5]
            print(self.group)

        
        
class Group:
#Group size and order of groups. This is class is for both proscriptive computing and will be used for both past and future groups.
    group_bonus_dict = {"A":1.2,"B":1.1, "C":1.0, "D":.9, "E":.8, "F":.7, "G":.6, "H":.5, "I":.4, "J":.3, "K":.2, "L":.1}
    
    group_min = 3
    group_max = 6 
    go = True # This is a status variable for creating more groups or not
    groups_made = []

    def __init__(self, name):
        self.name = name #A, B, C etc.
        Group.groups_made.append(self) #will this make a list of objects?


    def contenders(self,one, two, three, four = None, five = None, six = None):
        self.one = one
        self.two = two
        self.three = three
        self.four = four
        self.five = five
        self.six = six

    def num_players_decide(): #use random for now, we'll use a statistic method to find nearby scores later
        pass



            

class Round:
#info about a round. Every new series restarts counting rounds. Dealing with past and future so maybe could be seperate classes?
    next_round_players = []
    last_series_round_penalty = 8
    last_version_round_penalty = 20

    def __init__(self, number):
        self.number = number
        self.groups_played = []
        self.players_played = []
        self.is_complete = "No"
        
    def update_games_played(): # a list of the gameTags in this round
        pass
    def update_groups_played(): # a list of groups played in this round
        pass
    def update_players_played(): # a list of players played in this round
        pass
    
    
class Series:
#info about a series. Series is a portion of, or a full tournament. Each new series restarts the rounds
    def __init__(self, number):
        self.number = number


        
        
        
        
class Game:
#Game log files and their attributes. Game logs have the meta data in its name.
    all_games =[]
    gsorted = []
    current_round = []
    
    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.group = "none"
        self.round = 0
        self.series = 0
        self.version = 0
        self.num_players = 0
        self.xscore_dict = {}
        self.stand_score_dict = {}
        self.last_game_dict = {}
        Game.all_games.append(self)

    def __str__(self):
        return self.name
    
#    def __repr__(self):
#        return {'name':self.name, 'df':self.df}
        
    def classify(self): #turn the group name into meta data
        self.version = self.name[3:5]
        self.series = self.name[5:7]
        self.round = self.name[7:9]
        self.group = self.name[9:10]
        self.num_players = self.name[10:11]
    
    def player_scores(self): # returns a dictionary of all player:scores in this file
        #i ="player_key", b ="stand_score"
        df = self.df
        self.xscore_dict =  dict([(i,b) for i, b in zip(df.player_key, df.XScore)]) #df.player_key and df.XScore are not variables or methods

    def player_stand_scores(self): # returns a dictionary of all player:scores in this file
        #i ="player_key", b ="stand_score"
        df = self.df
        self.stand_score_dict =  dict([(i,b) for i, b in zip(df.player_key, df.stand_score)]) #df.player_key and df.stand_score are not variables or methods


    def player_lastgame(self): # returns a dictionary of all player:scores in this file
        #i ="player_key", b ="gameTag"
        df = self.df
        self.last_game_dict =  dict([(i,b) for i, b in zip(df.player_key, df.gameTag)]) #df.player_key and df.gameTag are not variables or methods


    
class NewGame(Game):
    games_to_update = [] #a list of games than need that player scores need to be updated
    
    
    def __init__(self, name,df):
        Game.__init__(self, name, df) #tried using super() but I couldn't get the right number of arguments
        NewGame.games_to_update.append(self)
        
    def apply_group_bonus(self):    
        self.bonus = Group.group_bonus_dict[self.group]
        #self.xscore_dict.update((k, v*self.bonus) for k, v in self.xscore_dict) *I can't get this to work even though it should
        for key in self.xscore_dict: #wow this feels so elementry
            y = self.xscore_dict[key]
            z = self.bonus*y
            self.xscore_dict[key]= z
        
class OldGame(Game):
    old_games = []

    def __init__(self, name,df):
        Game.__init__(self, name, df) #tried using super() but I couldn't get the right number of arguments
        OldGame.old_games.append(self)
        
        
class Bids:

    recency_dict = {}

    def __init__(self):
        self.bid = 0
    
    def set_dict():
        for i in range(10):
            Bids.recency_dict.update({i : (i/10 -1)**2})

    def deviation_weight(self, dev_score, k=0.3):
        y = (-(dev_score**2)*(-dev_score)*k)
        return y

    def group_relation_mod(self,group_diff, m = 0.2):
        x = (-(group_diff**2)*(-group_diff)*m)
        return x


    def get_bid(self, standard_deviation, rounds_ago, group_diff,):
        Bids.recency_dict.get(group_diff)
        self.bid = Bids.deviation_weight(standard_deviation) * Bids.recency_dict.get(rounds_ago) + Bids.group_relation_mod(group_diff)



####### END CLASS DEFINITONS




def main():
    open_records()
    make_games_metadata()
    get_player_records()
    get_player_new_scores()
    get_player_new_stand_scores()
    get_player_lastgames()
    merge_newscore_dic()
    add_scores_dict()
    player_dictionary_managed() #All have been added to class Player
#   determine_num_groups_last() #For now, the group bonus will be static: not dependent on number of players
    writeGame() #write all the gameTags that have been record to file
    writePlayers() #write all the player objects from Player class to csv file
    assign_sorted()
    groups_reporting()
    Bids.set_dict() # Sets formula for value of last game played recency 
    get_players_for_next() #After manually donwloading a file from google sheets to location as .csv import primary keys of players that wish to play the next round
    FFA_limit() #is thre more than 2 players? if True, go ahead
    check_if_players_have_record() #Check if any of these player keys are new, if they are, create a new instance of Player for each with default values
    calc_recency_played() #Find the difference between current round and when each individual player last played. outside round or series, there is a default variable.


    
#########
        
# Begin open_records()        
def open_records(): # open every file in this folder that ends in csv. Add the new games to a list in Game
    glist = rgames()
    for filename in glob.glob(os.path.join(game_folder_path, '*.csv')):
        df = pd.read_csv(filename)
        gameTag = df["gameTag"][2]
        Game(gameTag,df)
        checkGame(gameTag,glist,df) 
        
def rgames(): #open a text file and read it
    f = GameList1.location
    with open(f, "r") as file:
        glist =  (file.readline())
        return glist

    
    
def checkGame(gameTag,glist,df): #if a gameTag isn't on in the master games list, add it to a new list
    if gameTag in glist:
        OldGame(gameTag,df)
        print("Game "+gameTag+" already recorded")
    else:
        NewGame(gameTag,df)
        print("Found " +gameTag+" as new game. Added to records.")
        
        
##end open_records()
        
def make_games_metadata():
    for instance in Game.all_games:
        instance.classify() #now all the metadata is taken from the name of the game an applied to the game information on class Game
    

#
##Below is 2 different methods to do the same thing. One for old records and one is for new games
def get_player_records(): #open a csv file and read it
    df_oldp = pd.read_csv(GameList2.location)
    for index, row in df_oldp.iterrows():
        #print(str(row['player_key'])+"   "+str(row['XScore']))
        Player.player_old_dict[(row['player_key'])] = int(row['XScore'])
        Player.player_old_last[(row['player_key'])] = row['gameTag']
        Player.player_old_stand_score[(row['player_key'])] = row['stand_score']
        
def get_player_new_scores():
    for games in NewGame.games_to_update:
        games.player_scores()
        ##don't worry about duplicate keys for now 

def get_player_new_stand_scores():
    for games in NewGame.games_to_update:
        games.player_stand_scores()
        ##don't worry about duplicate keys for now 
        
def get_player_lastgames():
    for games in NewGame.games_to_update:
        games.player_lastgame()
        ##don't worry about duplicate keys for now 
               
        
def merge_newscore_dic():#merge dictionaries together
    all_new_scores = {}
    all_new_standardized_scores = {}
    all_new_last_games = {}
    for obj in gc.get_objects():
        if isinstance(obj, NewGame):
            all_new_scores.update(obj.xscore_dict)
            all_new_standardized_scores.update(obj.stand_score_dict)
            #last game also needs to be done like thsi here!!!!
            all_new_last_games.update(obj.last_game_dict)
            obj.apply_group_bonus() #apply group bonus
    Player.all_new_games_player_dict.update(all_new_scores)
    Player.all_new_games_player_standard_dict.update(all_new_standardized_scores) #might not need this
    Player.all_new_games_player_last_dict.update(all_new_last_games)
##
        
def determine_num_groups_last():
    pass


##    
    
def add_scores_dict(): # add new scores to existing keys of players
    #for all keys in Player.player_old_dict, check if the key exists in NewGame.all_new_games_dict
    #if the key exists, add the values together and update old dictionary with added value, remove new key:value from new dictionary
    #repeat for last game played, but update, then remove the last game played from the new game list
    for key in Player.player_old_dict:
        if key in Player.all_new_games_player_dict:
            Player.player_old_dict[key] = Player.player_old_dict[key]+Player.all_new_games_player_dict[key] #add scores
            del Player.all_new_games_player_dict[key] #now that the scores are added, remove key from new list

            

            

def player_dictionary_managed():
    old = Player.player_old_dict, Player.player_old_stand_score, Player.player_old_last
    new = Player.all_new_games_player_dict, Player.all_new_games_player_standard_dict, Player.all_new_games_player_last_dict #herefix
    for inputs in [old, new]:
        _scoredict, _standscoredict, _lastgamedict = inputs
        try:
            for primary_key in _scoredict: 
                score = _scoredict[primary_key]
                standscore = _standscoredict[primary_key]
                lastgame = _lastgamedict[primary_key]
                Player(primary_key, score, standscore, lastgame)
        except KeyError:
            pass

            
###
def check_if_duplicates(list_of_elems):
    for elem in list_of_elems:
        if list_of_elems.count(elem) > 1:
            list_of_elems.remove(elem)


#Writing the games list and player records to file


def writeGame():
    #write the list of all games logged to file 
    write_list =[]
    for obj in gc.get_objects():
        if isinstance(obj, NewGame):
            write_list.append(obj.name)
        elif isinstance(obj, OldGame):
            write_list.append(obj.name)
    with open(GameList1.location, 'w') as f:
        f.write("["+",".join(map(str, write_list))+"]")



def writePlayers(): #Take all the player objects from Player class and using pandas dataframe, write to csv
    prepare_to_df_players = []
    for obj in gc.get_objects(): #creating a datafram of players and writing to file
        if isinstance(obj, Player):
            prepare_to_df_players.append([obj.pkey, obj.score, obj.standard_score, obj.last_game])
    df_players_to_write = pd.DataFrame(prepare_to_df_players,  columns = ["player_key", "XScore", "stand_score", "gameTag"])
    df_players_to_write.to_csv(GameList2.location, index = False)
        
###

def sort_games(list_of_games): # sort by version, then series, then round, then group
    games_sorted = []
    for obj in list_of_games:
        games_sorted.append(obj)
    games_sorted.sort(key=lambda obj: obj.group)
    games_sorted.sort(key=lambda obj: obj.round)
    games_sorted.sort(key=lambda obj: obj.series)
    games_sorted.sort(key=lambda obj: obj.version)  
    return games_sorted

def getallgames():
    glist1 = []
    for obj in gc.get_objects():
        if isinstance(obj, NewGame) or isinstance(obj, OldGame):
            glist1.append(obj)
    return glist1
  
  
def assign_sorted():
    Game.gsorted = sort_games(getallgames())

def find_like_latest(): # Go to the lastest game and find alike games 
    version_alike = [Game.gsorted[-1]]
    for x in Game.gsorted[0:-1]:
        if x.version == Game.gsorted[-1].version:
            version_alike.append(x)
    version_alike = sort_games(version_alike) #sort and drill down again

    series_alike = [version_alike[-1]] 
    for y in version_alike[0:-1]:
        if y.series == version_alike[-1].series:
            series_alike.append(y)
    series_alike = sort_games(series_alike)

    round_alike = [series_alike[-1]]
    for z in series_alike[0:-1]:
        if z.round == series_alike[-1].round:
            round_alike.append(z)
    return round_alike

def groups_reporting():
    Game.current_round = find_like_latest() #shows which round we are on.
    groups_reporting =[]
    for v in Game.current_round:
        groups_reporting.append(v.group)
    groups_reporting = sorted(groups_reporting)
    print("Groups reporting: "+', '.join(groups_reporting)+" for round "+str(Game.current_round[0].round))


##
# Get Players for next Round

def get_players_for_next(): #open a csv that has been downloaded from google sheets and read it
    df_next_up = pd.read_csv(NextRound1.location)
    for index, row in df_next_up.iterrows():
        Round.next_round_players.append(row['Player_Key']) # Creates a list of player_keys that will play in the next round. These are not connencted to the player objects yet

def check_if_players_have_record():
    pkeys_list = []
    for each in Player.player_list:
        pkeys_list.append(each.pkey)
    for i in Round.next_round_players:
        if i not in pkeys_list:
            Player(i)  #This adds a new player instance with default values. This instance won't be written to file.


##
# Find When players last played
def calc_recency_played():
    temp_list = []
    for i in Round.next_round_players:
        for obj in gc.get_objects():
            if isinstance(obj, Player):
                if obj.pkey == i:
                    temp_list.append(obj)
    Round.next_round_players = temp_list
    for u in Round.next_round_players:
        try:
            u.last_played()
            if u.version == Game.current_round[0].version:
                if u.series == Game.current_round[0].series:
                    u.rounds_ago_player = Game.current_round[0].round - u.round
                else:
                    u.rounds_ago_player = Round.last_series_round_penalty
            else:
                u.rounds_ago_player = Round.last_version_round_penalty
        except: #creates and exception for new players that haven't played before
            u.rounds_ago_player = Game.current_round[0].round

            



def FFA_limit():
    if len(Round.next_round_players) < 3:
        print("Not enough players for any games of FFA")
        Group.go = False
        return False
    else:
        Group.go = True
        return True

#######
GameList1 = Files()
GameList1.location ="/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/GamesList.txt" 
GameList2 = Files()
GameList2.location = "/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/player_records.csv"
game_folder_path = "/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/game_results/"
NextRound1 = Files()
NextRound1.location = "/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/Next_Round - Export.csv"



##RUN     
main()


print("     ")
print("you're doing good buddy")
print("     ")
print("     ")


def make_group():
    while Group.go == True:
        uppers = list(string.ascii_uppercase) #create a list of upper case letters
        temp_next_players = Round.next_round_players
        conditions = True
        while conditions == True:
            if len(temp_next_players) > 2:
                try:
                    Group(uppers[0])
                    uppers.pop(0)

                    #all players place bids
                    for p in Player.player_list:
                        print(p.group) #determine distance from last group to this group
                        #bid on this group.
                        pass
                    #add players with winning bid to group
                    #remove players from temp_next list
                except: #reached end of alphabet
                    break
            elif 2 >= len(temp_next_players) > 0:
                for obj in gc.get_objects(): #delete all objects of class Group
                    if isinstance(obj, Group):
                        del obj
                conditions = False
                break #start over with setting conditions to false
            elif temp_next_players == 0:
                conditions = False #not sure if this is necessary either?
                Group.go = False
                break #not sure if this is necessary, maybe just chaning the conditions cuases it to break


#make_group()





# if number of players still in next to play list is greater than three, create a new instance of group starting from A and working down the list
# create a Player method that sets a bid price for each group
# create a list of playes still bidding
# create a random.int method of selecting between 3-6 players ina group
# take the highest rated players until a group is full
# remove the players that have succesfully bid, out from the still bidding list
#
        
