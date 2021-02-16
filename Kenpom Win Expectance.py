import csv
from plotly.offline import plot
import plotly.figure_factory as ff

neutralSite = input("Is it a neutral site (Y/N)?: ")
if neutralSite == 'Y':
    homeTeam = input("Team 1: ")
    awayTeam = input("Team 2: ")
else:
    #create user inputs for each team
    homeTeam = input("Home Team: ")
    awayTeam = input("Away Team: ")
#creates lists for stats of each team
homeTeamStats = []
awayTeamStats = []

with open('Kenpom Data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    #adds stats for the home and away team
    for row in csv_reader:
        if homeTeam == str(row[1]): 
            homeTeamStats.append(str(row[0]))
            homeTeamStats.append(str(row[1]))
            homeTeamStats.append(str(row[2]))
            homeTeamStats.append(str(row[3]))
            counter = 4
            for i in range (11):
                homeTeamStats.append(float(row[counter]))
                counter += 1
        if awayTeam == str(row[1]): 
            awayTeamStats.append(str(row[0]))
            awayTeamStats.append(str(row[1]))
            awayTeamStats.append(str(row[2]))
            awayTeamStats.append(str(row[3]))
            counter = 4
            for i in range (11):
                awayTeamStats.append(float(row[counter]))
                counter += 1
#overall average offensive rating
overallAvg = 102.675039633609
#average pace
pace = 68.2832834243438

if neutralSite == 'Y':
    #calculates the expected offensive ratings for each team
    homeProjOffRating = (((((homeTeamStats[5])-overallAvg)/overallAvg + 
                          ((awayTeamStats[7])-overallAvg)/overallAvg)+1) * overallAvg)
    
    awayProjOffRating = ((((awayTeamStats[5]-overallAvg)/overallAvg + 
                          ((homeTeamStats[7])-overallAvg)/overallAvg)+1) * overallAvg)
else:
    #calculates the expected offensive ratings for each team
    homeProjOffRating = (((((homeTeamStats[5]*1.014)-overallAvg)/overallAvg + 
                          ((awayTeamStats[7])-overallAvg)/overallAvg)+1) * overallAvg)
    
    awayProjOffRating = ((((awayTeamStats[5]-(awayTeamStats[5]*.014)-overallAvg)/overallAvg + 
                          ((homeTeamStats[7])-overallAvg)/overallAvg)+1) * overallAvg)

#adjusts the pace for the game
adjPace = (homeTeamStats[9] * awayTeamStats[9])/pace
homeProjPoints = (homeProjOffRating/100)*adjPace
awayProjPoints = (awayProjOffRating/100)*adjPace

#calculates pythagorean wins expected
homeWinExp = pow(homeProjOffRating, 10.25) / (pow(homeProjOffRating, 10.25)+
                                       pow(awayProjOffRating, 10.25))
awayWinExp = pow(awayProjOffRating, 10.25) / (pow(awayProjOffRating, 10.25)+
                                       pow(homeProjOffRating, 10.25))
sumWinExp = float(homeWinExp + awayWinExp)
#averages the expectances to add up to 1
homeWinExp = homeWinExp*100/sumWinExp
awayWinExp = awayWinExp*100/sumWinExp
#prints results
print('\nPredicted Score: ' + homeTeam + ' ' + str(round(homeProjPoints, 3)) 
      + ', ' + awayTeam + ' ' + str(round(awayProjPoints, 3)))
print('Projected Win %: ' + homeTeam + ' ' + str(round(homeWinExp, 3)) 
      + '%, ' + awayTeam + ' ' + str(round(awayWinExp, 3))+'%')
#creates data set to be put in a table
teamTable = [[] for i in range(3)]
teamTable[0] = ['Rnk','Team','Conf.','W-L','Adj. Eff. +/-', 
                'Adj. Off.','Off. Rnk','Adj. Def.','Def. Rnk',
                'Pace', 'Pace Rnk', 'Luck', 'Luck Rnk', 'Opp. Adj +/-', 'SOS Rnk']
teamTable[1] = homeTeamStats
teamTable[2] = awayTeamStats

userTable = input("Do you want a table (Y/N)?: ")
if userTable == 'Y':
    #creates the table
    fig = ff.create_table(teamTable)
    #plots the table
    plot(fig)