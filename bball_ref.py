import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import time
import datetime

baseURL = "http://www.basketball-reference.com"
dbWriteBool = True # set this to true if results are to be written to a db

# return a list of the day's games
def getGameURLs(month, day, year):
    boxscores = []
    try:
        games = requests.get(baseURL + "/boxscores/index.cgi?month=" + str(month) + "&day=" + str(day) + "&year=" + str(year))
        gameSoup = BeautifulSoup(games.text, 'html.parser')
        scores = gameSoup.find_all('a', href=re.compile('^/boxscores'))
        for score in scores:
            if score.text == "Final":
                boxscores.append(score.attrs['href'])
    except Exception as e:
        print "URL Error ----------> " + str(e)
    return boxscores


# list of stats for the given date
def getGameStats(statList, boxscores, year, db=dbWriteBool):
    for gameURL in boxscores:
        try:
            r = requests.get(baseURL + gameURL)
            soup = BeautifulSoup(r.text, 'html.parser')
            # stats are found in the tbody tag
            name = soup.find_all("tbody")
            away = name[0].contents[1].find("a").text
            home = name[0].contents[3].find("a").text
            # only do 1 and 3 because 2 and 4 are advanced stats. Advanced stats added after 1984
            if year > 1984:
                homeTable = 3
            else:
                homeTable = 2
            for i in [1, homeTable]:
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
                        if string == "Did Not Play" or string == "Player Suspended":
                            for val in xrange(20):
                                playerStats.append(None)
                            break
                        playerStats.append(string)
                    while len(playerStats) < 22:
                        playerStats.append(None)
                    playerStats.append(baseURL + gameURL) 
                    if playerStats[1] != "Reserves":
                        if db:
                            c.execute('''insert into boxscores(team, name, minutes, FG, FGA, FG_Percent, ThreePt, ThreePtA, ThreePt_Percent, FT, FTA, FT_Percent, ORB, DRB, TRB, AST, STL, BLK, TOV, PF, PTS, plus_minus, game_url)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', playerStats)
                        statList.append(playerStats)
        except Exception as e:
            print "Error --------> " + str(e)
            pass
    return statList

# Enter starting and ending year of NBA season. Use 4 digits.
# Ex: getSeason(2015, 2016)
def getSeason(startYear, endYear):
    if endYear != startYear + 1:
        print "Invalid years"
        return
    stats = []
    year = startYear
    for month in [10, 11, 12, 1, 2, 3, 4, 5, 6]:
        if month == 1:
            year = endYear
        for day in range(1, 32):
            print "Getting %s/%s/%s" % (str(month), str(day), str(year))
            games = getGameURLs(month, day, year)
            if games:
                stats = getGameStats(stats, games, year)
    return stats

def getDay(month, day, year):
    stats = []
    print "Getting %s/%s/%s" % (str(month), str(day), str(year))
    games = getGameURLs(month, day, year)
    if games:
        stats = getGameStats(stats, games, year)
    return stats

# enter dates as 'mm-dd-yyyy'
def getRange(start, end):
    startDate = datetime.datetime.strptime(start, '%m-%d-%Y')
    endDate = datetime.datetime.strptime(end, '%m-%d-%Y')
    step = datetime.timedelta(days=1)
    while startDate <= endDate:
        getDay(startDate.month, startDate.day, startDate.year)
        startDate += step

def createTable(db=dbWriteBool):
    if db:
        c.execute('''create table if not exists boxscores
            (team text,
            name text,
            minutes text,
            FG integer,
            FGA integer,
            FG_Percent real,
            ThreePt integer, 
            ThreePtA integer,
            ThreePt_Percent real,
            FT integer, 
            FTA integer, 
            FT_Percent real,
            ORB integer, 
            DRB integer, 
            TRB integer, 
            AST integer, 
            STL integer,
            BLK integer,
            TOV integer,
            PF integer,
            PTS integer,
            plus_minus text, 
            game_url text)''')

def getRows(query):
    db = sqlite3.connect("bball-ref-dataset.db")
    c = db.cursor()
    c.execute(str(query))
    rows = c.fetchall()
    c.close
    return rows

# Ex: Get all of NBA history
"""
for year in range(1946, 2017):
    getSeason(year, year+1)
    time.sleep(60)
"""

# Ex: Get range of dates
"""
getRange('01-01-2016', '01-13-2016')
"""

if __name__ == '__main__':
    db = sqlite3.connect("bball-ref-dataset.db")
    c = db.cursor()
    db.commit()
    c.close()

