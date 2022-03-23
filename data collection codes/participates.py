from bs4 import BeautifulSoup
import requests
import random as rd
import xlsxwriter as xw
import pandas as pd

#setting the headers in the .xlsx file 
headers = ['player_ID','match_ID','start','goals','participation_in_match','saves','shots','shots_on_target','assists','tackles','passes','position']

#creating the .xlsx file
workbook = xw.Workbook('participates.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0
#writting the name of the headers in the first row of the .xlsx file
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#an array that contains the names of the teams to make it easier to find the right match ids
t=['Manchester City','Manchester Utd','Liverpool','Chelsea','Leicester City','West Ham','Tottenham','Arsenal','Leeds United','Everton','Aston Villa','Newcastle Utd','Wolves','Crystal Palace','Southampton','Brighton','Burnley','Fulham','West Brom','Sheffield Utd']
d=[]
matches=pd.read_excel("matches2.xlsx")#loading the .xlsx file
df=pd.DataFrame(matches) #df contains the information about the matches and the two teams that participated in the match

player_id=-1
#getting the html code from the site that contains the teams that took part in Premier League 2020-2021
link='https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
html_text = requests.get(link).text
teams_soup = BeautifulSoup(html_text,'lxml')
teams = teams_soup.find("tbody").find_all('a')#it contains all the teams
for team in teams:
    part_link=team.get('href').split('/')
    if(part_link[2]=='squads'):
        print("done") #the program is slow so we needed to know if it was getting close to the end 
        new_link='https://fbref.com'+'/'.join(part_link) #link of the list of players of each team
        #getting the html code of the list of players
        html_text2=requests.get(new_link).text
        players_soup=BeautifulSoup(html_text2,'lxml')
        players1=players_soup.find("tbody")
        players2=players1.find_all("td",{"data-stat":"matches"}) #contains each player of the list
        for count1,player in enumerate(players2):
            player_id=player_id+1
            split=player.a.get('href').split('/')
            position2=players1.find_all("tr")[count1].find("td",{"class":"center"}).text.strip() #the position the player is playing
            stats_link='https://fbref.com/en/players/'+split[3]+'/matchlogs/s10728/summary/'+split[-1] #the link of the stats of the player for Premier League 2020-2021
            #getting the html code of the stats of the player
            html_text3=requests.get(stats_link).text
            stats_soup=BeautifulSoup(html_text3,'lxml')
            stats=stats_soup.find("tbody").find_all("tr")
            for stat in stats: #the stats for each match that he took part
                if(position2!="GK"):
                    saves="NULL"#only goalkeepers have "saves"
                else:
                    saves=rd.randint(4,8)#saves weren't provided in the site
                position=stat.find("td",{"data-stat":"position"})#position for the specific match
                if(position==None):#there were blank lines and we wanted to skip them
                    continue
                else:
                    venue=stat.find("td",{"data-stat":"venue"}).text #venue of the match to make it easier to find match ids
                    if venue=="Home":
                        venue=1
                    else:
                        venue=0
                    squad=stat.find("td",{"data-stat":"squad"}).text #team of the player
                    opponent=stat.find("td",{"data-stat":"opponent"}).text #the opponent in that match
                    d.append([venue,squad,opponent])#helping list for the match ids
                    minutes=stat.find("td",{"data-stat":"minutes"}).text.strip()#minutes the player participated in the match
                    starterr=stat.find("td",{"data-stat":"game_started"}).text #if he was one of the main players in the match
                    goals=stat.find("td",{"data-stat":"goals"}).text #how many goals he scored
                    shots=stat.find("td",{"data-stat":"shots_total"}).text #how many shots
                    shots_on_target=stat.find("td",{"data-stat":"shots_on_target"}).text #how many shots on target
                    assists=stat.find("td",{"data-stat":"assists"}).text #how many assists
                    tackles=stat.find("td",{"data-stat":"tackles"}).text #how many tackles
                    passes=stat.find("td",{"data-stat":"passes_completed"}).text #how many passes
                    row=row+1
                    #writting the information we gathered to the .xlsx file
                    worksheet.write(row,col,player_id)
                    worksheet.write(row,col+2,starterr)
                    worksheet.write(row,col+3,goals)
                    worksheet.write(row,col+4,minutes)
                    worksheet.write(row,col+5,saves)
                    worksheet.write(row,col+6,shots)
                    worksheet.write(row,col+7,shots_on_target)
                    worksheet.write(row,col+8,assists)
                    worksheet.write(row,col+9,tackles)
                    worksheet.write(row,col+10,passes)
                    worksheet.write(row,col+11,position2)
row=0
#finding the correct ids for each match and writting them to the .xlsx file
for x in range(0,len(d)):
    for y in range(0,len(df)):
        if d[x][0]==1 and df.at[y,'squad_a']==d[x][1] and df.at[y,'squad_b']==d[x][2]:
            match_ID=df.at[y,'match_ID']
        elif d[x][0]==0 and df.at[y,'squad_b']==d[x][1] and df.at[y,'squad_a']==d[x][2]:
            match_ID=df.at[y,'match_ID']
    row+=1
    worksheet.write(row,col+1,match_ID)
workbook.close()
