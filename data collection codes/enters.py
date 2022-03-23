from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter as xw

#List of teams that take part in the Championship in the order that they are in our database
teams=["Manchester City","Manchester Utd","Liverpool","Chelsea","Leicester City","West Ham","Tottenham","Arsenal","Leeds United","Everton","Aston Villa","Newcastle Utd","Wolves","Crystal Palace","Southampton","Brighton","Burnley","Fulham","West Brom","Sheffield Utd"]

#We import the matches2 excel file that we created in the matches.py file
matches=pd.read_excel("matches2.xlsx")
df=pd.DataFrame(matches)
#Creation of the excel file of the relation enters of our database 
headers = ['match_ID','team_ID','home']
workbook = xw.Workbook('enters.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#Here we insert in the excel file for every match the ID of the match, the teams that take part in the match and a bit that determines whether a team is playing in
#their stadium or in the opponent's stadium
for x in range(0,len(df)):
    row+=1
    match_ID=df.at[x,'match_ID']
    #The first team of every match is playing at home
    team_ID=teams.index(df.at[x,'squad_a'])
    home=1
    worksheet.write(row,col,match_ID)
    worksheet.write(row,col+1,team_ID)
    worksheet.write(row,col+2,home)
    row+=1
    match_ID=df.at[x,'match_ID']
    #The second team of every match is playing away
    team_ID=teams.index(df.at[x,'squad_b'])
    home=0
    worksheet.write(row,col,match_ID)
    worksheet.write(row,col+1,team_ID)
    worksheet.write(row,col+2,home)
    
#We finish creating the excel file.
workbook.close()
