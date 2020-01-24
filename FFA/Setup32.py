#Backing up (and switching?) from jupyter notebook to visual studio code and github


import numpy as np
import os,glob
import pandas as pd
import gc



class Files:
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
    
    
    def __init__(self, player_key,xscore=0,standardized_score=0,last_game_played=None):
        self.score = xscore
        self.standard_score = standardized_score
        self.pkey = player_key
        self.last_game = last_game_played
        Player.player_list.append(self)
        

        
        
        
class Group:
#Group size and order of groups. This is class is for both proscriptive computing and will be used for both past and future groups.
    group_bonus_dict = {"A":1.2,"B":1.1, "C":1.0, "D":.9, "E":.8, "F":.7, "G":.6, "H":.5, "I":.4, "J":.3, "K":.2, "L":.1}
    
    def __init__(self):
        self.min = 3
        self.max = 6

class Round:
#info about a round. Every new series restarts counting rounds.
    def __init__(self, number):
        self.number = number
        self.groups_played = []
        self.players_played = []
        
    def update_games_played():
        pass
    def update_groups_played():
        pass
    def update_players_played():
        pass
    
    
class Series:
#info about a series. Series is a portion of, or a full tournament. Each new series restarts the rounds
    def __init__(self, number):
        self.number = number


        
        
        
        
class Game:
#Game log files and their attributes. Game logs have the meta data in its name.
    all_games =[]
    
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
    pass



####### END CLASS DEFINITONS




def main():
    open_records()
    make_games_metadata()
    get_player_records()
    get_player_new_scores()
    get_player_new_stand_scores()
    merge_newscore_dic()
    add_scores_dict()
    player_dictionary_managed() #All have been added to class Player
#   determine_num_groups_last() #For now, the group bonus will be static: not dependent on number of players
    writeGame() #write all the gameTags that have been record to file

    

    
    
    
#########
        
# Begin open_records()        
def open_records(): # open every file in this folder that ends in csv. Add the new games to a list in Game
    glist = rgames()
    for filename in glob.glob(os.path.join(game_folder_path, '*.csv')):
        df = pd.read_csv(filename)
        gameTag = df["gameTag"][2]
        instance1 = Game(gameTag,df)
        checkGame(gameTag,glist,df) 
        
def rgames(): #open a text file and read it
    f = GameList1.location
    with open(f, "r") as file:
        glist =  (file.readline())
        return glist

    
    
def checkGame(gameTag,glist,df): #if a gameTag isn't on in the master games list, add it to a new list
    if gameTag in glist:
        instance2 = OldGame(gameTag,df)
        print("Game "+gameTag+" already recorded")
    else:
        instance3 = NewGame(gameTag,df)
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
        
def merge_newscore_dic():#merge dictionaries together
    all_new_scores = {}
    all_new_standardized_scores = {}
    for obj in gc.get_objects():
        if isinstance(obj, NewGame):
            all_new_scores.update(obj.xscore_dict)
            all_new_standardized_scores.update(obj.stand_score_dict)
            obj.apply_group_bonus() #apply group bonus
    Player.all_new_games_player_dict.update(all_new_scores)
    Player.all_new_games_player_standard_dict.update(all_new_standardized_scores) #might not need this
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
            #Player.player_old_last[key].update(Player.player_new_last[key]) #update the last game played to this current one
            #del Player.player_new_last[key] #now that has been updated, remove the key and value from the new list
            #Player.player_old_stand_score[key].update(Player.all_new_games_player_standard_dict[key]) #might not need this
            #del Player.all_new_games_player_standard_dict[key] #might not need this
            ##What is left is 2 dictionaries of players. One is an updated list of records that we had before, the other is any new players that haven't been in the records yet
            ##Now, each dictionary can be seperately applied to the class Player in order to complete information about the player
            

            
#Using Dictionaries, create instance of every player
def create_player_instance(player_key,XScore,stand_score,last_game):
    Player(player_key,XScore,stand_score,last_game)
    
def player_dict_to_instance(dictionary_score,dictionary_stand_score,last_game_dictionary):
    for key in dictionary_score:
        XScore = dictionary_score.get(str(key))
        stand_score = dictionary_stand_score.get(str(key))
        last_game = last_game_dictionary.get(str(key))
        create_player_instance(key,XScore,stand_score,last_game)
          
def player_dictionary_managed():
    old = [Player.player_old_dict, Player.player_old_stand_score, Player.player_old_last]
    new = [Player.all_new_games_player_dict, Player.player_new_stand_score, Player.player_new_last]
    for x in (old,new):
        score,standscore,lastgame = x[0], x[1], x[2]
        player_dict_to_instance(score,standscore,lastgame)
            
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
        
###
GameList1 = Files()
GameList1.location ="/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/GamesList.txt" 
GameList2 = Files()
GameList2.location = "/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/player_records.csv"
game_folder_path = "/Users/SteveGlenMBPGoodVibe/Program/dok/FFA/game_results/"



##RUN     
main()
    
    






# write player dataframe to file.
# Celebrate a milestone. phase 1 complete

# create a formula map for standard deviatoin score; like a x^2 function, where x is the standard_dev score and y is the bid index weight
#    make it dependent on how many players were in the match
# create a schedule for rounds since last played bid weight modifier
# create a Player method that sets a bid price for each group
        
