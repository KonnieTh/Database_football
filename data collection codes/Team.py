from bs4 import BeautifulSoup
import requests
import random as rd
import xlsxwriter as xw
import pandas as pd

#Here we get the Teams that take part in the Championship

#Creation of Team relation file
headers = ['team_ID','name','founded','wins','ties','losses','points','stadium_id']
workbook = xw.Workbook('Team.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#Requesting data from this link https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats
df=pd.read_html('https://fbref.com/en/comps/9/10728/2020-2021-Premier-League-Stats')
#Here we get the name of the teams and their ids, the rest we input it ourselves 
p1=df[0].loc[:,'Squad']
for i in range(len(p1)):
    row+=1
    worksheet.write(row,col,i)
    worksheet.write(row,col+1,p1[i])
    worksheet.write(row,col+2,"NULL")
    worksheet.write(row,col+3,"NULL")
    worksheet.write(row,col+4,"NULL")
    worksheet.write(row,col+5,"NULL")
    worksheet.write(row,col+6,"NULL")
    worksheet.write(row,col+7,"NULL")

#We finish creating the excel file.
workbook.close()
