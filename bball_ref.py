import requests
from bs4 import BeautifulSoup
import re

# ------------------ Get Game URLs ----------------------
baseGame = "http://www.basketball-reference.com"
games = requests.get('http://www.basketball-reference.com/boxscores/index.cgi?month=12&day=25&year=2015')
gameSoup = BeautifulSoup(games.text, 'html.parser')
#print(soup.prettify())

scores = gameSoup.find_all('a', href=re.compile('^/boxscores'))
boxscores = []
for score in scores:
    if score.text == "Final":
        boxscores.append(score.attrs['href'])


# ------------------ Get Stats ---------------------------
statList = []
for gameURL in boxscores:
    r = requests.get(baseGame + gameURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find_all("tbody")

    # this is how to get the stats. return list of name and stats
    away = name[0].contents[1].find("a").text
    home = name[0].contents[3].find("a").text
    for i in [1, 3]:
        for row in name[i].contents[1::2]:
            if i == 1:
                playerStats = [away]
            elif i == 3:
                playerStats = [home]
            else:
                playerStats = ["No team"]
            for string in row.stripped_strings:
                playerStats.append(string)
            statList.append(playerStats)

for i in statList:
    print i
