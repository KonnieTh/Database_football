from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter as xw

#Here we get data for the substitutions of every match

#We import the matches2 excel file that we created in the matches.py file
matches=pd.read_excel("matches2.xlsx")
df=pd.DataFrame(matches)

#We import the Players excel file that we created in the Player.py file
data=pd.read_excel('Players.xlsx',na_filter=False)
df1=pd.DataFrame(data,columns=['player_ID','first_name','last_name'])

#Create of substitution excel file
headers = ['substitution_ID','match_ID','player_ID','minute_in_match']
workbook = xw.Workbook('substitutes.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)


num_subs=0#substitution_ID
#special minutes
special_minutes=["90+1","90+2","90+3","90+4","90+5","90+6","90+7","90+8","90+9","90+10","90+11","45+1","45+2","45+3","45+4","45+5","45+6"]
#fixed special minutes
fixed_special_minutes=["91","92","93","94","95","96","97","98","99","100","101","46","47","48","49","50","51"]
#Requesting and inserting data in the excel file using BeautifulSoup
#Requesting the html text of the Match Report of every match using the requests.get() function
for x in range(0,len(df)):
    html_text = requests.get('{}'.format(df.at[x,'Match_Report']))
    soup = BeautifulSoup(html_text.text,'html.parser')
    #We get the substitutions for one of the two teams that take part in the match
    events=soup.find('div',{"id":"events_wrap"}).find_all("div",{"class":"event a"})
    for event in events:
        #Because the site had some problems determining the substitutions he had to put more conditions in order for this code to work as expected
        if len(event.find_all('small'))>1 and "Penalty" not in event.find_all('small')[1].text and "Own Goal" not in event.find_all('small')[1].text  and "Substitute" in event.find('div',{"style":"display: none;"}).text :
            for sub in event.find_all('a'):
                player_ID=0
                row+=1
                minute_in_match=event.find('div').text
                minute_in_match=minute_in_match.replace(" ","")
                minute_in_match=minute_in_match.split("’")
                minute_in_match=minute_in_match[0]
                minute_in_match=minute_in_match.replace('\n',"")
                minute_in_match=minute_in_match.replace('\t',"")
                minute_in_match=minute_in_match.replace('\xa0',"")
                minute_in_match=minute_in_match.replace("’","")#minute in match 
                for z in range(len(special_minutes)):#if a minute is in special minutes we need to fix it in order to be readable in python as an integer number
                    if special_minutes[z]==minute_in_match:
                        minute_in_match=fixed_special_minutes[z]# fixed minute in match 
                #Here we get the the player_ID using the Players excel file
                name=sub.text
                name=name.split(" ")
                lastname=""
                firstname=""
                if len(name)==1:
                    firstname=""
                    lastname=name[0]
                elif len(name)==2:
                    firstname=name[0]
                    lastname=name[1]
                elif len(name)>2:
                    firstname=name[0]
                    for z in range(1,len(name)-1):
                        lastname+=name[z]+" "
                    lastname+=name[-1]
                for y in range(len(df1['first_name'])):
                    if lastname=="Smith Rowe":
                        player_ID=230
                    elif len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                        player_ID=df1['player_ID'][y]
                    elif len(name)==1 and df1['last_name'][y]==lastname:
                        player_ID=df1['player_ID'][y]
                    
                worksheet.write(row,col,num_subs)
                worksheet.write(row,col+1,df.at[x,'match_ID'])
                worksheet.write(row,col+2,player_ID)
                worksheet.write(row,col+3,minute_in_match)
            num_subs+=1
    #We do here the same thing for the second team   
    events=soup.find('div',{"id":"events_wrap"}).find_all("div",{"class":"event b"})
    for event in events:
        if len(event.find_all('small'))>1 and "Penalty" not in event.find_all('small')[1].text and "Own Goal" not in event.find_all('small')[1].text  and "Substitute" in event.find('div',{"style":"display: none;"}).text :
            for sub in event.find_all('a'):
                player_ID=0
                row+=1
                minute_in_match=event.find('div').text
                minute_in_match=minute_in_match.replace(" ","")
                minute_in_match=minute_in_match.split("’")
                minute_in_match=minute_in_match[0]
                minute_in_match=minute_in_match.replace('\n',"")
                minute_in_match=minute_in_match.replace('\t',"")
                minute_in_match=minute_in_match.replace('\xa0',"")
                minute_in_match=minute_in_match.replace("’","")
                for z in range(len(special_minutes)):
                    if special_minutes[z]==minute_in_match:
                        minute_in_match=fixed_special_minutes[z]# fixed minute in match 
                name=sub.text
                name=name.split(" ")
                lastname=""
                firstname=""
                if len(name)==1:
                    firstname=""
                    lastname=name[0]
                elif len(name)==2:
                    firstname=name[0]
                    lastname=name[1]
                elif len(name)>2:
                    firstname=name[0]
                    for z in range(1,len(name)-1):
                        lastname+=name[z]+" "
                    lastname+=name[-1]
                for y in range(len(df1['first_name'])):
                    if lastname=="Smith Rowe":
                        player_ID=230
                    elif len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                        player_ID=df1['player_ID'][y]
                    elif len(name)==1 and df1['last_name'][y]==lastname:
                        player_ID=df1['player_ID'][y]
                worksheet.write(row,col,num_subs)
                worksheet.write(row,col+1,df.at[x,'match_ID'])
                worksheet.write(row,col+2,player_ID)
                worksheet.write(row,col+3,minute_in_match)
            num_subs+=1
#We finish creating the excel file.
workbook.close()

