import requests
from bs4 import BeautifulSoup
import re

baseURL = "http://www.basketball-reference.com"

# return a list of the day's games
def getGameURLs(month, day, year):
    games = requests.get(baseURL + "/boxscores/index.cgi?month=" + str(month) + "&day=" + str(day) + "&year=" + str(year))
    gameSoup = BeautifulSoup(games.text, 'html.parser')
    scores = gameSoup.find_all('a', href=re.compile('^/boxscores'))
    boxscores = []
    for score in scores:
        if score.text == "Final":
            boxscores.append(score.attrs['href'])
    return boxscores


# list of stats for the given date
def getGameStats(boxscores):
    statList = []
    for gameURL in boxscores:
        r = requests.get(baseURL + gameURL)
        soup = BeautifulSoup(r.text, 'html.parser')
        # stats are found in the tbody tag
        name = soup.find_all("tbody")
        away = name[0].contents[1].find("a").text
        home = name[0].contents[3].find("a").text
        # only do 1 and 3 because 2 and 4 are advanced stats
        for i in [1, 3]:
            for row in name[i].contents[1::2]:
                if i == 1:
                    playerStats = [away]
                elif i == 3:
                    playerStats = [home]
                else:
                    playerStats = ["No team"]
                space = 0 # Need to count spaces because some players do not have certain stats. 
                for string in row.strings:
                    if string.isspace():
                        space += 1
                        if space > 1: # If more than one space, it means a stat is missing. Insert None to keep columns aligned
                            playerStats.append(None)
                        continue
                    else:
                        space = 0
                    if string == "Did Not Play":
                        for val in xrange(20):
                            playerStats.append(None)
                        break
                    playerStats.append(string)
                playerStats.append(baseURL + gameURL)
                if playerStats[1] != "Reserves":
                    statList.append(playerStats)
    return statList

test = getGameURLs(12,25,2015)
test2 = getGameStats(test)
for i in test2:
    print i
