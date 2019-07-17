import numpy as np
from matplotlib import pyplot as plt
import csv
def read_data():
    #textfile = input("Choose your file: ") # gets text file name
    myfile = open("battingData1950Present.csv") # Opens the file
    myfile_csv=csv.reader(myfile) # makes file more readible
    players = [] # List for the students
    for row in myfile_csv:
        players.append(row) # Adds the list of the student into another list
    #players.sort(key=lambda x: (x[0],x[1])) # Alphabetize the list by last name then firstname
    del players[0]
    myfile.close() # Closes the file
    return players

def get_menu_choice(players):
    choice = "100"
    while (choice!="0"):
        print("0: Exit")
        print("1: Histogram of runs scored in the lifetimes of all players (no cutoff, no postions")
        print("2: Histogram of runs scored in the lifetimes of all players (no cutoff)")
        print("3: Histogram of runs scored in the lifetimes of all players (cutoff = 100)")
        print("4: Graph team presence over time")
        print("5: Find the batters that had the best and worst seasons stealing bases")
        print("6: List the 10 best seasons that batters had by on base percentage")
        print("7: Plot on base percentage for the lifetimes of players with best seasons")
        print("8: Plot homeruns over time (percentiles)")
        print("9: Plot average team RBI over time (1950 - 1959)")
        print("10: Extra Credit")
        choice = input('> ')
        if ( choice == "1"):
            uniqueHist(unique(players))
        if ( choice == "2"):
            postitionHist(UniquePostions(players,1))
        if ( choice == "3"):
            postitionHist(UniquePostions(players,2))
        if ( choice == "4"):
            scat(teamPresence(players))
        if ( choice == "5"):
            pass
        if ( choice == "6"):
            pass
        if ( choice == "7"):
            pass
        if ( choice == "8"):
            pass
        if ( choice == "9"):
            pass
        if ( choice == "10"):
            pass

def unique(players):
    playerID = []
    runs = []
    for row in players:
        playerID.append(row[1])
        runs.append(row[7])
    NplayerID = np.array(playerID)
    Nruns = np.array(runs)
    unique_players = np.unique(NplayerID)
    sums = []
    for group in unique_players:
        sums.append(Nruns[NplayerID == group].astype(int).sum())
    Nsums = np.array(sums)
    return Nsums

def uniqueHist( Nlist ):
    plt.xlabel('Number of total runs')
    plt.ylabel('Number of players')
    plt.title('Total runs vs number of players having that many runs')
    plt.hist(Nlist.astype(int), bins = 100, stacked = True)
    plt.show()

def PositionList(list):
    playerID = []
    runs = []
    for row in list:
        playerID.append(row[0])
        runs.append(row[1])
    NplayerID = np.array(playerID)
    Nruns = np.array(runs)
    unique_players = np.unique(NplayerID)
    sums = []
    for group in unique_players:
        sums.append(Nruns[NplayerID == group].astype(int).sum())
    Nsums = np.array(sums)
    return Nsums

def PositionListCut(list): #need to edit so you can choose cutoff
    playerID = []
    runs = []
    for row in list:
        playerID.append(row[0])
        runs.append(row[1])
    NplayerID = np.array(playerID)
    Nruns = np.array(runs)
    unique_players = np.unique(NplayerID)
    sums = []
    for group in unique_players:
        if (Nruns[NplayerID == group].astype(int).sum() >=100):
            sums.append(Nruns[NplayerID == group].astype(int).sum())
    Nsums = np.array(sums)
    return Nsums

def UniquePostions(players, option):
    sums1B = []
    sums2B = []
    sums3B = []
    sumsC = []
    sumsNULL = []
    sumsOF = []
    sumsP = []
    sumsSS = []
    for row in players:
        if (row[19] == "1B"):
            sums1B.append([row[1],row[7]])
        if (row[19] == "2B"):
            sums2B.append([row[1],row[7]])
        if (row[19] == "3B"):
            sums3B.append([row[1],row[7]])
        if (row[19] == "C"):
            sumsC.append([row[1],row[7]])
        if (row[19] == "NULL"):
            sumsNULL.append([row[1],row[7]])
        if (row[19] == "OF"):
            sumsOF.append([row[1],row[7]])
        if (row[19] == "P"):
            sumsP.append([row[1],row[7]])
        if (row[19] == "SS"):
            sumsSS.append([row[1],row[7]])
    if option == 1:
        return np.array([PositionList(np.array(sums1B)),PositionList(np.array(sums2B)),PositionList(np.array(sums3B)),PositionList(np.array(sumsC)),PositionList(np.array(sumsNULL)),PositionList(np.array(sumsOF)),PositionList(np.array(sumsP)),PositionList(np.array(sumsSS))])
    if option == 2:
        return np.array([PositionListCut(np.array(sums1B)),PositionListCut(np.array(sums2B)),PositionListCut(np.array(sums3B)),PositionListCut(np.array(sumsC)),PositionListCut(np.array(sumsNULL)),PositionListCut(np.array(sumsOF)),PositionListCut(np.array(sumsP)),PositionListCut(np.array(sumsSS))])

def postitionHist(Nlist):
    plt.xlabel('Number of total runs')
    plt.ylabel('Number of players')
    plt.title('Total runs vs number of players having that many runs')
    plt.hist(Nlist, bins = 100, stacked = True, label=["1B","2B","3B","C","NULL","OF","P","SS"])
    plt.legend()
    plt.show()
    
def cutoffHist(Nlist,cut1,cut2):
    plt.xlabel('Number of total runs')
    plt.ylabel('Number of players')
    plt.title('Total runs vs number of players having that many runs')
    plt.hist(Nlist, bins = 100, stacked = True, range=(cut1,cut2),label=["1B","2B","3B","C","NULL","OF","P","SS"])
    plt.legend()
    plt.show()

def teamPresence(Nlist):
    tmpYear = Nlist[0][0]
    team = []
    year = []
    for row in Nlist:
        team.append(row[4])
        year.append(row[0])  
    teamList = np.array([np.array(team),np.array(year)])
    return np.unique(teamList,axis=0)
            
def scat(Nlist):
    print(Nlist)
    years = np.unique(Nlist[0])

    plt.figure(figsize=(12,12))
#    plt.scatter(Nlist[0].astype(np.int32),Nlist[1])
#    plt.show()
    
    np1 = np.asarray(Nlist[1])
    np0 = np.asarray(Nlist[0], dtype = np.int32)
    
    teams = np.unique(np1)
    
    print(teams)
    height = 0
    
    for team in teams:
        indicies = np.where(np1[:] == team)
        years = np.unique(np0[indicies])
        height_array = []
        for year in years:
            height_array.append(height)
        height += 1
        plt.scatter(years, height_array, marker = "s")
    
    plt.yticks(np.arange(len(teams)), teams)
    

    plt.show()
    


def main():
   playersData=np.array(read_data())
   get_menu_choice(playersData)
   
if __name__=='__main__':
    main()
