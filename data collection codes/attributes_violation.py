from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter as xw
#Here we get data for the cards of that were given in every match

#We import the matches2 excel file that we created in the matches.py file
matches=pd.read_excel("matches2.xlsx")
df=pd.DataFrame(matches)

#We import the Players excel file that we created in the Player.py file
data=pd.read_excel('Players.xlsx',na_filter=False)
df1=pd.DataFrame(data,columns=['player_ID','first_name','last_name'])


#list of cards
cards=[]
#special minutes
special_minutes=["90+1","90+2","90+3","90+4","90+5","90+6","90+7","90+8","90+9","90+10","90+11","45+1","45+2","45+3","45+4","45+5","45+6"]
#fixed special minutes
fixed_special_minutes=["91","92","93","94","95","96","97","98","99","100","101","46","47","48","49","50","51"]
#Requesting and inserting data in the excel file using BeautifulSoup
#Requesting the html text of the Match Report of every match using the requests.get() function
for x in range(0,len(df)):
    html_text = requests.get('{}'.format(df.at[x,'Match_Report']))
    soup = BeautifulSoup(html_text.text,'html.parser')
    tl=soup.find('div',{'id':'events_wrap'})
    #We get the cards for one of the two teams that take part in the match
    tl=tl.find_all('div',{'class':'event a'})
    for l in tl:
        tex=l.find('div',{'style':'display: none;'}).text
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        #Here we get the the player_ID using the Players excel file
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if('Second Yellow Card' in tex):#If a player gets a Second Yellow Card he gets disqualified
            dq=1
            #We save the data in 
            cards.append([df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Second Yellow"])  
        elif('Yellow Card' in tex):#If a player gets a Yellow Card he is not disqualified
            dq=0
            cards.append([df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"])
        elif('Red Card' in tex):#If a player gets a Red Card he gets disqualified
            dq=1
            cards.append([df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Red"])
    #Here because the site had some problems determining the Cards, he had to include more conditions in order to delete them from the list cards
    #We save the flaws of the site in a list c and we delete them from the list cards
    c=[]
    #We do the same thing as above
    for l in tl:
        dq=0
        a=l.find_all("small")
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if len(a)>1 and "Penalty Kick" in a[1]:
            c=[df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"]
            if c in cards:#If flaw(c) is in cards then we delete it from cards
                cards.remove(c)
    #Same here
    c=[]
    for l in tl:
        dq=0
        a=l.find_all("small")
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if len(a)>1 and "Own Goal" in a[1]:
            c=[df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"]
            if c in cards:#If flaw(c) is in cards then we delete it from cards
                cards.remove(c)
    #Same here
    for l in tl:
        dq=0
        a=l.find_all("small")
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if len(a)>1 and "Penalty saved by " in a[1]:
            c=[df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"]
            if c in cards:
                cards.remove(c)
    #Now we do the same thing for the second team that takes part in a match
    tl=soup.find('div',{'id':'events_wrap'})
    tl=tl.find_all('div',{'class':'event b'})
    for l in tl:
        tex=l.find('div',{'style':'display: none;'}).text
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        #Here we get the the player_ID using the Players excel file
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if('Second Yellow Card' in tex):
            dq=1
            cards.append([df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Second Yellow"])   
        elif('Yellow Card' in tex):
            dq=0
            cards.append([df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"])
        elif('Red Card' in tex):
            dq=1
            cards.append([df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Red"])
    c=[]
    for l in tl:
        dq=0
        a=l.find_all("small")
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if len(a)>1 and "Penalty Kick" in a[1]:
            c=[df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"]
            if c in cards:
                cards.remove(c)
    c=[]
    for l in tl:
        dq=0
        a=l.find_all("small")
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if len(a)>1 and "Own Goal" in a[1]:
            c=[df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"]
            if c in cards:
                cards.remove(c)
    for l in tl:
        dq=0
        a=l.find_all("small")
        minute_in_match=l.find('div').text
        minute_in_match=minute_in_match.replace(" ","")
        minute_in_match=minute_in_match.split("’")
        minute_in_match=minute_in_match[0]
        minute_in_match=minute_in_match.replace('\n',"")
        minute_in_match=minute_in_match.replace('\t',"")
        minute_in_match=minute_in_match.replace('\xa0',"")
        minute_in_match=minute_in_match.replace("’","")#minute in match
        name=l.find('a').text
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
            if len(name)>1 and df1['first_name'][y]==firstname and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
            elif len(name)==1 and df1['last_name'][y]==lastname:
                player_ID=df1['player_ID'][y]
        if len(a)>1 and "Penalty saved by " in a[1]:
            c=[df.at[x,'match_ID'],player_ID,dq,minute_in_match,"Yellow"]
            if c in cards:
                cards.remove(c)

#Create of attributes_violation excel file
headers = ['violation_ID','match_ID','player_ID','disqualification','minute_in_match','card']
workbook = xw.Workbook('attributes_violation.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

violation_ID=0#ID of violation
#We pass the insides of the list into an excel file
for x in range(len(cards)):
    row+=1
    worksheet.write(row,col,violation_ID)
    worksheet.write(row,col+1,cards[x][0])
    worksheet.write(row,col+2,cards[x][1])
    worksheet.write(row,col+3,cards[x][2])
    for z in range(len(special_minutes)):
        if special_minutes[z]==cards[x][3]:
            cards[x][3]=fixed_special_minutes[z]# fixed minute in match
    worksheet.write(row,col+4,cards[x][3])
    worksheet.write(row,col+5,cards[x][4])
    violation_ID+=1

#We finish creating the excel file.
workbook.close()



    
