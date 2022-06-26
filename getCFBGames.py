from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import csv

#1-317
d1Teams = []
with open('d1Teams.csv', newline='', mode='r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    print(reader)
    d1Teams = list(reader)
d1Teams = d1Teams[0]


print(d1Teams)
d1 = [2, 5, 6, 8, 9, 12, 21, 23, 24, 25, 26, 30, 36, 38, 41, 52, 57, 58, 59, 61, 62, 66, 68, 77, 84, 87, 96, 97, 98, 99, 103, 113, 120, 127, 130, 135, 142, 145, 150, 151, 152, 153, 154, 158, 164, 166, 167, 183, 189, 193, 194, 195, 197, 201, 202, 204, 213, 218, 221, 228, 235, 238, 239, 242, 245, 248, 249, 251, 252, 254, 258, 259, 264, 265, 275, 276, 277, 278, 290, 295, 309, 324, 326, 328, 333, 344, 349, 356, 2005, 2006, 2026, 2032, 2050, 2084, 2116, 2117, 2132, 2199, 2226, 2229, 2247, 2294, 2305, 2306, 2309, 2335, 2348, 2390, 2393, 2426, 2429, 2433, 2439, 2440, 2459, 2483, 2509, 2567, 2572, 2579, 2628, 2633, 2636, 2638, 2641, 2649, 2653, 2655, 2711, 2751]
#html_text = requests.get('https://www.espn.com/college-football/team/schedule/_/id/300/season/2021').text
#soup = BeautifulSoup(html_text, 'lxml')
#team = soup.find('span', 'db pr3 nowrap fw-bold')
ids = 0
year = 2000
idArr = []
while year < 2022:
    for d1ID in d1:
        print(year)
        html_text = requests.get('https://www.espn.com/college-football/team/schedule/_/id/' + str(d1ID) + '/season/' + str(year)).text
        soup = BeautifulSoup(html_text, 'lxml')
        team = soup.find('span', 'db pr3 nowrap fw-bold')
        teamName = ""
        if team != None:
            teamName = team.text
            teamName = teamName.replace("'", "")
            idArr.append(ids - 1)
            games = soup.find_all('tr', 'Table__TR--sm')
            print(teamName)
            if (len(games) != 0):
                schedule = {}
                dataFrameData = []
                for game in games:
                    gameTup = []
                    date = game.find_all('span')
                    if (len(date)!= 0):
                        if (date[0].text != "DATE"):
                            gameTup.append(date[0].text)
                        
                    winLoss = game.find_all('span', 'fw-bold')
                    wl = ""
                    if (len(winLoss)!= 0):
                        wl = winLoss[0].text
                        
                        
                    hA = game.find('div', "flex items-center opponent-logo")
                    if (hA != None):
                        horA = hA.find_all("span", "pr2")[0].text
                        #print(hA.find_all("span")[2].text)
                        if (hA.find_all("span")[2].text[-1] == "*"):
                            gameTup.append("Yes")
                        else:
                            gameTup.append("No")
                    oppInfo = game.find_all('a', 'AnchorLink')
                    
                    if (len(oppInfo)!= 0):
                        if(oppInfo[0].find('img') != None):
                        
                            oppName = oppInfo[0].find('img')["title"]
                            #print("Opponent Name: " + oppName)
                            date = game.span.text
                            #print("Date: " + date)
                            #print("Score: " + oppInfo[2].text + "\n")
                            winnerScore = ""
                            loserScore = ""
                            element = 0
                            if (len(oppInfo) >= 3 and "-" in oppInfo[2].text):
                                while(oppInfo[2].text[element] != "-"):
                                        loserScore = loserScore + oppInfo[2].text[element]
                                        element = element + 1
                                element = element + 1
                                while(oppInfo[2].text[element] != " " and element < len(oppInfo[2].text)):
                                        winnerScore = winnerScore + oppInfo[2].text[element]
                                        element = element + 1
                                title = teamName + " " + horA + " " + oppName
                                if "@" in title:
                                    gameTup.append(teamName)
                                    gameTup.append(oppName)
                                    if (wl == "W"):
                                        gameTup.append("W")
                                        gameTup.append(winnerScore)
                                        gameTup.append(loserScore)
                                    else:
                                        gameTup.append("L")
                                        gameTup.append(loserScore)
                                        gameTup.append(winnerScore)
                                else:
                                    gameTup.append(oppName)
                                    gameTup.append(teamName)
                                    if (wl == "W"):
                                        gameTup.append("W")
                                        gameTup.append(loserScore)
                                        gameTup.append(winnerScore)
                                    else:
                                        gameTup.append("L")
                                        gameTup.append(winnerScore)
                                        gameTup.append(loserScore)
                        
                                if ("OT" in oppInfo[2].text):
                                    gameTup.append("Yes")
                                else:
                                    gameTup.append("No")
                                    
                                    
                                
                                tupToAppend = tuple(gameTup)
                                dataFrameData.append(tupToAppend)
                                jsonGame = {}
                        else:
                                print("")
                                
                    else:
                            print("")
                        
                        
                df = pd.DataFrame(dataFrameData, columns = ['Date' , 'Neutral?', 'Away' , 'Home', "Win/Loss", "HomeScore", "AwayScore", "Overtime?"])
                df.to_excel(str(year) + "/" + teamName + ".xlsx")
    year = year + 1 
print("DONE")
                
                
        



