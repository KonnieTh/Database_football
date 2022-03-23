from bs4 import BeautifulSoup
import requests
import random as rd
import xlsxwriter as xw

#setting the headers in the .xlsx file 
headers = ['player_ID','shirt_number','height','date_of_birth','first_name','last_name']

#creating the .xlsx file
workbook = xw.Workbook('Players.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0
#writting the name of the headers in the first row of the .xlsx file
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

player_id=0
#getting the html code from the site that contains the teams that took part in Premier League 2020-2021
link='https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
html_text = requests.get(link).text
teams_soup = BeautifulSoup(html_text,'lxml')
teams = teams_soup.find("tbody").find_all('a')#it contains all the teams
for team in teams:
    shirt_num=1#the shirt number of the players wasn't provided on the site so we used random numbers
    part_link=team.get('href').split('/')
    if(part_link[2]=='squads'):
        new_link='https://fbref.com'+'/'.join(part_link) #link of the list of players of each team
        html_text2=requests.get(new_link).text
        players_soup=BeautifulSoup(html_text2,'lxml')
        players=players_soup.find("tbody").find_all("tr") #contains all the players of a team
        for player in players:
            row=row+1
            player_link="https://fbref.com"+player.a.get('href') #link to find more info about the player
            html_text3=requests.get(player_link).text
            char_soup=BeautifulSoup(html_text3,'lxml')
            chars=char_soup.find("div",{"class":"players"}) #contains all the characteristics of a player
            name=chars.find("h1",{"itemprop":"name"}).text.strip().split(" ") #the full name of the player
            print(player_id)
            try:
                height=chars.find("span",{"itemprop":"height"}).text.strip()[:-2] #the height of the player
            except:
                height="NULL" #some heights weren't provided
            try:
                date_of_birth=chars.find("span",{"id":"necro-birth"}).get("data-birth").strip() #the date of birth of the player
            except:
                date_of_birth="NULL" #some dates weren't provided
            if (len(name)==1): #some players didn't have their first name on the site
                fname="NULL"
                lname=name[0]
            elif(len(name)==2): #if a player had a first name and one last name
                fname=name[0]
                lname=name[1]
            else: #if a player had a first name and 2 or more last names
                fname=name[0]
                lname=" ".join(name[1:len(name)])
            #writting the information we gathered to the .xlsx file
            worksheet.write(row,col,player_id)   
            worksheet.write(row,col+1,shirt_num)
            worksheet.write(row,col+2,height)
            worksheet.write(row,col+3,date_of_birth)
            worksheet.write(row,col+4,fname)
            worksheet.write(row,col+5,lname)
            player_id=player_id+1
            shirt_num=shirt_num+1
workbook.close()
