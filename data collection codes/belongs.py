from bs4 import BeautifulSoup
import requests
import random as rd
import xlsxwriter as xw

#setting the headers in the .xlsx file
headers = ['player_ID','team_ID','contract_start_day','contract_end_day','salary']

#creating the .xlsx file
workbook = xw.Workbook('Belongs.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0
#writting the name of the headers in the first row of the .xlsx file
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#I added manually some transfers that we found but we couldn't find them gathered somewhere
transfers=[[596,241,"2021-02-01",7],[538,515,"2020-09-24",15],[172,64,"2021-01-29",1],[370,244,"2021-02-01",7]\
            ,[495,243,"2021-01-22",15],[601,184,"2021-01-08",5],[331,126,"2020-09-30",3],[409,77,"2020-09-19",12]\
            ,[463,88,"2021-02-01",2],[559,123,"2020-10-05",3],[458,309,"2020-10-05",9]]

countt=-1
player_id=-1
flag=0
#getting the html code from the site that contains the teams that took part in Premier League 2020-2021
link='https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats'
html_text = requests.get(link).text
teams_soup = BeautifulSoup(html_text,'lxml')
teams = teams_soup.find("tbody").find_all('a')#it contains all the teams
for team in teams:
    part_link=team.get('href').split('/')
    if(part_link[2]=='squads'):
        countt+=1
        new_link='https://fbref.com'+'/'.join(part_link) #link of the list of players of each team
        #getting the html code of the list of players
        html_text2=requests.get(new_link).text
        players_soup=BeautifulSoup(html_text2,'lxml')
        players=players_soup.find("tbody").find_all("td",{"data-stat":"matches"})
        for player in players:
            row+=1
            player_id+=1
            #we couldn't find the contracts of the players gathered somewhere so we put random dates
            year1=rd.randint(2018,2020)
            if(year1==2020):
                month=rd.randint(1,8)
            else:
                month=rd.randint(1,12)
            day=rd.randint(1,28)
            year2=year1+rd.randint(2,5)
            if(year2<2022):
                year2=2022
            contract_start=str(year1)+'-'+str(month)+'-'+str(day) #start of their contract
            contract_end=str(year2)+'-'+str(month)+'-'+str(day) #end of their contract
            salary=rd.randrange(10000,60000,5000)
            for j in range (len(transfers)): #if the player was transferred
                if (player_id==transfers[j][1]):
                    contract_end=transfers[j][2]
                    year=int(contract_end[0:4])
                    contract_start=str(year-2)+'-'+str(month)+'-'+str(day)
                if (player_id==transfers[j][0]):
                    player_id2=transfers[j][1]
                    contract_start=transfers[j][2]
                    year=int(contract_start[0:4])
                    contract_end=str(year+3)+'-'+str(month)+'-'+str(day)
                    flag=1
            #writting the information we gathered to the .xlsx file
            if(flag==0):
                worksheet.write(row,col,player_id)
            else:
                worksheet.write(row,col,player_id2) #players from the transfers
                flag=0
            #fixing the format of the dates to YYYY-MM-DD
            if(contract_start[6]=='-'):
                contract_start=contract_start[0:5]+'0'+contract_start[5:9]
            if(len(contract_start)==9):
                contract_start=contract_start[0:8]+'0'+contract_start[8]
            if(contract_end[6]=='-'):
                contract_end=contract_end[0:5]+'0'+contract_end[5:9]
            if(len(contract_end)==9):
                contract_end=contract_end[0:8]+'0'+contract_end[8]
            worksheet.write(row,col+1,countt)
            worksheet.write(row,col+2,contract_start)
            worksheet.write(row,col+3,contract_end)
            worksheet.write(row,col+4,salary)
workbook.close()
            
