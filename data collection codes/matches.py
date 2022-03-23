from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter as xw

#List of Stadiums of teams in the order that they are in our database
#Its going to be used in order to determine the stadium_ID in every match
pitches=["The American Express Community Stadium","Anfield","Bramall Lane","Craven Cottage","Elland Road","Emirates Stadium","Etihad Stadium","Goodison Park","King Power Stadium","London Stadium","Molineux Stadium","Old Trafford","St. Mary's Stadium","Selhurst Park","St. James' Park","Stamford Bridge","The Hawthorns","Tottenham Hotspur Stadium","Turf Moor","Villa Park"]

#Creation of the excel file of matches
headers = ['match_ID','score','datetime_','matchweek','stadium_code']
workbook = xw.Workbook('matches.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#Requesting and inserting data in the excel file using BeautifulSoup
print("##For matches")
#Requesting the html text of the link that's inside the the requests.get() function 
html_text = requests.get('https://fbref.com/en/comps/9/10728/schedule/2020-2021-Premier-League-Scores-and-Fixtures')
soup = BeautifulSoup(html_text.text,'html.parser')
#Searching in the html code the table that contains the matches of the Football Championship
table=soup.find('tbody')
#For every row of the table that contains data, we get from every match the score,the time and the date of the match,the matchday and the venue 
#and we insert them in the excel file.
matches=table.find_all('tr')
i=0
for match in matches:
   fixture=match.find_all('td')
   if(fixture[5].text!=""):
      row+=1
      score=fixture[5].text.strip()
      time=fixture[2].text.strip()
      date=fixture[1].text.strip()
      datetime=date+" "+time
      matchday=match.find('th',{"data-stat":"gameweek"}).text
      venue=pitches.index(fixture[9].text.strip())
      worksheet.write(row,col,i)#This is the ID in which we save the match in our database
      worksheet.write(row,col+1,score)
      worksheet.write(row,col+2,datetime)
      worksheet.write(row,col+3,matchday)
      worksheet.write(row,col+4,venue)
      i+=1
   else:
      continue
#We finish creating the excel file.
workbook.close()      


## We do the same thing as above, but we get also from every match the two teams that play in every match, and the link of match report
headers = ['match_ID','score','datetime','matchday','stadium_code','squad_a','squad_b','Match_Report']
workbook = xw.Workbook('matches2.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)
i=0    
for match in matches:
   fixture=match.find_all('td')
   if (fixture[5].text!=""):
      row+=1
      score=fixture[5].text.strip()
      time=fixture[2].text.strip()
      date=fixture[1].text.strip()
      datetime=date+" "+time
      matchday=match.find('th',{"data-stat":"gameweek"}).text
      venue=pitches.index(fixture[9].text.strip())
      squad_a=fixture[3].text.strip()
      squad_b=fixture[7].text.strip()
      link=match.find('td',{'data-stat':'match_report'})
      link=link.find('a')
      link='https://fbref.com'+link['href']
      worksheet.write(row,col,i)
      worksheet.write(row,col+1,score)
      worksheet.write(row,col+2,datetime)
      worksheet.write(row,col+3,matchday)
      worksheet.write(row,col+4,venue)
      worksheet.write(row,col+5,squad_a)
      worksheet.write(row,col+6,squad_b)
      worksheet.write(row,col+7,link)
      i+=1
   else:
      continue

workbook.close()
