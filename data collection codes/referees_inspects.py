from bs4 import BeautifulSoup
import requests
import random as rd
import xlsxwriter as xw
import pandas as pd

#Here we get the data of the referees of our Championship and the who referee plays in which match and the status of the referee
#The status can be Referee or AR1(Assistant Referee 1) or AR2(Assistant Referee 2) or 4th (4th Referee)

#We import the matches2 excel file that we created in the matches.py file
matches=pd.read_excel("matches2.xlsx")
df=pd.DataFrame(matches)

#Creation of the excel file for the referees
headers = ['referee_ID','last_name','first_name','yellow_cards','red_cards','number_of_matches']
workbook = xw.Workbook('referee.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#Requesting and inserting data in the excel file using BeautifulSoup
referee=[]#We use this list in order to save the referees ones in  the database
referee_ID=0#This is used in order to determine the ID of the referees
#Requesting the html text of the Match Report of every match using the requests.get() function 
for x in range(0,len(df)):
    html_text = requests.get(df.at[x,'Match_Report'])
    soup = BeautifulSoup(html_text.text,'html.parser')
    ref=soup.find('div',{'class':'scorebox_meta'})
    ref=ref.find_all('span',{'style':'display:inline-block'})
    i=0
    for r in ref:# for every match get the name of the first 4 referees of every match and we put it in the excel file
        if i<4:
            k=r.text.index(' (')
            text=r.text[:k].replace('\xa0',' ')
            text=text.split(' ')
            if text not in referee:
                row+=1#increase of row of the excel file 
                referee.append(text)
                worksheet.write(row,col,referee_ID)
                worksheet.write(row,col+1,text[1])
                worksheet.write(row,col+2,text[0])
                worksheet.write(row,col+3,"NULL")
                worksheet.write(row,col+4,"NULL")
                worksheet.write(row,col+5,"NULL")
                referee_ID+=1#increase of referee_ID by one every time a referee is saved
            i+=1
#We finish creating the excel file.
workbook.close()

#Creation of the excel file of relation inspects
headers = ['match_ID','referee_ID','status']
workbook = xw.Workbook('inspects.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#Doing the same thing as above with get not only the name of the referees in every match, but also the match_ID and the status of every referee
for x in range(0,len(df)):
    html_text = requests.get(df.at[x,'Match_Report'])
    soup = BeautifulSoup(html_text.text,'html.parser')
    ref=soup.find('div',{'class':'scorebox_meta'})
    ref=ref.find_all('span',{'style':'display:inline-block'})
    i=0
    for r in ref:
        if i<4:
            row+=1
            worksheet.write(row,col,df.at[x,'match_ID'])
            k1=r.text.index(' (')
            k2=r.text.index(')')
            worksheet.write(row,col+1,referee.index(r.text[:k1].replace('\xa0',' ').split(' ')))
            worksheet.write(row,col+2,r.text[k1+2:k2])
            i+=1
#We finish creating the excel file.
workbook.close()    


