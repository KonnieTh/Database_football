from bs4 import BeautifulSoup
import requests
import xlsxwriter as xw

#setting the headers in the .xlsx file 
headers = ['stadium_ID','name','date_built','place','capacitance']

#creating the .xlsx file
workbook = xw.Workbook('Stadiums.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0
#writting the name of the headers in the first row of the .xlsx file
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

stadium_id=0
#getting the html code from the site that contains the stadiums
link='https://www.worldfootball.net/venues/eng-premier-league-2020-2021/'
html_text = requests.get(link).text
stadiums_soup = BeautifulSoup(html_text,'lxml')
stadiums_part = stadiums_soup.find("table", {"class": "standard_tabelle"})
stadiums=stadiums_part.find_all("tr") #it contains all the rows of the table
#iterating through the stadiums we gathered
for count,stadium in enumerate(stadiums):
    if(count==0):#the first tr is the headers and we want to skip that one
        continue
    row=row+1
    name=stadium.a.text #name of the stadium
    capacitance=stadium.text.strip().split("\n")[-1]#capacitance of the stadium
    city=stadium.text.strip().split("\n")[1]#the city the stadium is located
    #getting the html code of the stadium to get more information about it
    new_link='https://www.worldfootball.net'+stadium.find("a").get('href')+'1/' 
    html_text2=requests.get(new_link).text
    opening_soup=BeautifulSoup(html_text2,'lxml')
    openingg=opening_soup.find("table", {"class": "standard_tabelle"}).text
    posi=openingg.find("Opening:")
    if(posi==-1): 
        opening='NULL' #if the year the stadium opened isn't provided 
    else:
        opening=int(openingg[posi+9:posi+13])#the year the stadium opened
    #writting the information we gathered to the .xlsx file
    worksheet.write(row,col,stadium_id)   
    worksheet.write(row,col+1,name)
    worksheet.write(row,col+2,opening)
    worksheet.write(row,col+3,city)
    worksheet.write(row,col+4,capacitance)
    stadium_id=stadium_id+1
workbook.close()
