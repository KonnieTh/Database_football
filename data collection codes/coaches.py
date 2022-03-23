from bs4 import BeautifulSoup
import requests
import xlsxwriter as xw

#setting the headers in the .xlsx file
headers = ['coach_ID','first_name','last_name','contract_start_date','contract_end_date','team_code']

#creating the .xlsx file
workbook = xw.Workbook('Coach.xlsx')
worksheet = workbook.add_worksheet()

row=0
col=0
#writting the name of the headers in the first row of the .xlsx file
for count,l in enumerate(headers):
    worksheet.write(row, count,l)
row=row+1

#the list of teams to make it easier to find the team code
list_teams=["Manchester City","Manchester United","Liverpool","Chelsea","Leicester City","West Ham United",\
            "Tottenham Hotspur","Arsenal","Leeds United","Everton","Aston Villa","Newcastle United",\
            "Wolverhampton Wanderers","Crystal Palace","Southampton","Brighton & Hove Albion",\
            "Burnley","Fulham","West Bromwich Albion", "Sheffield United"]#teams of premier league 2020-2021

coach_id=0
#getting the html code from the site that contains the coaches of the teams
link='https://en.wikipedia.org/wiki/List_of_Premier_League_managers'
html_text = requests.get(link).text
coaches_soup = BeautifulSoup(html_text,'lxml')
coaches = coaches_soup.find_all("tbody")[1].find_all("tr")#contains all the rows of the table
for count,coach in enumerate(coaches):
    if(count==0):#the first row were the headers
        continue
    team=coach.find_all("td")[1].text.strip()#team of the current coach
    if team in list_teams: #if he is a coach of a team that participated in Premier League 2020-2021
        general=coach.find_all("td") 
        try:
            #we wanted to gather the coaches that were active during the Premier League 2020-2021
            #so if his contract ended before the start of the championship he wasn't included or if the contract
            #started after the end of the championship
            if(int(general[2].span.get('data-sort-value')[13:15])>5 and int(general[2].span.get('data-sort-value')[8:12])==2021):
                    continue #not accepted
            if(int(general[3].span.get('data-sort-value')[8:12])>=2020):
                if(int(general[3].span.get('data-sort-value')[8:12])==2020 and int(general[3].span.get('data-sort-value')[13:15])<9):#not accepted
                    continue
                name=coach.th.text.split(" ") #full name of the coach
                fname=name[0].strip() #first name of the coach
                lname=name[1].strip() #last name of the coach
                contract_end=general[3].span.get('data-sort-value')[8:18] #date the contract of the coach ended
                if(contract_end[0:4]=='2021' and (contract_end[5:7]=='05' or contract_end[5:7]=='06')):
                    contract_end='2021-06-30' #there were some gaps in the end of the championship so we extended their contract
                contract_start=general[2].span.get('data-sort-value')[8:18] #date the contract of the coach began 
                try:
                    team_code=list_teams.index(general[1].text.strip()) #team code he was the coach of
                except:
                    team_code='NULL'
                #writting the information we gathered to the .xlsx file
                worksheet.write(row,col,coach_id)   
                worksheet.write(row,col+1,fname)
                worksheet.write(row,col+2,lname)
                worksheet.write(row,col+3,contract_start)
                worksheet.write(row,col+4,contract_end)
                worksheet.write(row,col+5,team_code)
                coach_id=coach_id+1
                row=row+1
        except:#accepted because he remains a coach to this date (the contract end was null)
            try:
                team_code=list_teams.index(general[1].text.strip()) #team code he was the coach of
            except:
                team_code='NULL'
            name=coach.th.text.split(" ") #full name of the coach
            fname=name[0].strip() #first name of the coach
            lname=name[1].strip() #last name of the coach
            contract_end='NULL' #he's still coach for this team
            contract_start=general[2].span.get('data-sort-value')[8:18] #date the contract of the coach began
            #writting the information we gathered to the .xlsx file
            worksheet.write(row,col,coach_id)   
            worksheet.write(row,col+1,fname)
            worksheet.write(row,col+2,lname)
            worksheet.write(row,col+3,contract_start)
            worksheet.write(row,col+4,contract_end)
            worksheet.write(row,col+5,team_code)
            coach_id=coach_id+1
            row=row+1
workbook.close()
