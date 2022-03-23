from bs4 import BeautifulSoup
import requests
import random as rd
import xlsxwriter as xw
import pandas as pd

#Here we write a code order to fix the particapation time of every player in every team in a match, so that the team has a total participation time in match equal to 990 minutes

#We import the Player_statistics excel file that we created 
players_stats = pd.read_excel('participates.xlsx')
df1=pd.DataFrame(players_stats).sort_values(by='match_ID',ascending=False,ignore_index=True)
#We import the substitutions excel file that we created in the subs.py file
subs = pd.read_excel('substitutes.xlsx',header=0)
df2=pd.DataFrame(subs)
#We import the attributes_violation excel file that we created in the card.py file
cards = pd.read_excel('attributes_violation.xlsx',header=0)
df3=pd.DataFrame(cards)

p=[]
participation_ID=0
#To fix the participation time of the substitutes 
for j in range(0,len(df2)):# For every player in the substitutions file
    for i in range(0,len(df1)):#For every player in the Player_statistics file
        if(j%2==1):#For the players that leave the game
            if(int(df1.at[i,'player_ID'])==int(df2.at[j,'player_ID']) and int(df1.at[i,'match_ID'])==int(df2.at[j,'match_ID'])):
                end=int(df2.at[j,'minute_in_match'])-1#end of participation time is when the substitution happens
                if end>=90:#if the substitution happens after the 90 minutes we make it happen in the 89' minute
                    end=89
                start=0#initialization of start of participation as 0 minutes
                match_ID=int(df1.at[i,'match_ID'])#match_ID
                player_ID=int(df2.at[j,'player_ID'])#player_ID
                participation=int(df1.at[i,'participation_in_match'])#participation in match for that player
                #Here we fix the participation time and start and end time of the players
                if participation+p[participation_ID-1][6] > 90:#if that condition is true, 
                    if participation>p[participation_ID-1][6]:# then if the participation of the Player that left is more than that of the Player that got in, then that means that he was a substitute and we need to fix his participation and start time
                        participation-=participation+p[participation_ID-1][6]-90
                        start=end-participation
                    else:#else if the participation of the Player that left is less than that of the Player that got in, then we need to fix the participation time of the player that got in
                        p[participation_ID-1][6]-=participation+p[participation_ID-1][6]-90                  
                        p[participation_ID-1][4]=p[participation_ID-1][5]-p[participation_ID-1][6]
                end=participation#participation time determines finally the end time of the player that left the game
                try:
                    p.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),df1.at[i,'saves'],\
                              int(df1.at[i,'shots']),int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
                except:
                    p.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),'NULL',int(df1.at[i,'shots']),\
                              int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
                participation_ID+=1
                continue
        elif(j%2==0):#For the players that got into the game
            if(int(df1.at[i,'player_ID'])==int(df2.at[j,'player_ID']) and int(df1.at[i,'match_ID'])==int(df2.at[j,'match_ID'])):
                end=int(df2.at[j,'minute_in_match'])+int(df1.at[i,'participation_in_match'])-1#end of participation time is when the substitution happens plus the participation of the player in the matchs
                if end>=90:#if hiw end time is over 90 make it 90.
                    end=90
                match_ID=int(df1.at[i,'match_ID'])#match_ID
                player_ID=int(df2.at[j,'player_ID'])#player_ID
                participation=int(df1.at[i,'participation_in_match'])#participation in match for the Player
                start=end-participation#Initialization of start time as end time-participation
                starter=0#he is not a starter, starter=0
                try:
                    p.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),df1.at[i,'saves'],\
                              int(df1.at[i,'shots']),int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
                except:
                    p.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),'NULL',int(df1.at[i,'shots']),\
                              int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
                participation_ID+=1
                continue


#To delete the players who have multiple ids
L=[]
M=[[22,263],[79,328],[84,221],[86,533],[89,493],[95,394],[126,639],[225,144],[235,533],[237,396],[238,118],[259,630],[277,263],[290,600],[307,632],[349,226]]
flags=[]
flag1=0
for i in range(len(M)):
    flags.append(0)
for x in range(len(p)):
    for y in range(len(M)):# If a player gets/leaves a match with more than one ids (p[x][2]) in the match p[x][0] dont include the other id 
        if p[x][1]==M[y][0] and p[x][2]==M[y][1]:
            flags[y]+=1
            flag1=1
            if flags[y]==2:
                continue
            elif flags[y]==1:
                L.append(p[x])
    if flag1==0:
        L.append(p[x])
    else:
        flag1=0


#To fix the participation time of the attributes_violation relationship when a player gets a Second Yellow or a Red card 
for j in range(0,len(df3)):
    for i in range(0,len(df1)):
        if("Y" in df1.at[i,'start'] and int(df1.at[i,'player_ID'])==int(df3.at[j,'player_ID']) and int(df1.at[i,'match_ID'])==int(df3.at[j,'match_ID']) and (df3.at[j,'card']=="Red" or\
        df3.at[j,'card']=="Second Yellow") and (df1.at[i,'player_ID']!=596 or df1.at[i,'player_ID']!=538 or df1.at[i,'player_ID']!=172 or df1.at[i,'player_ID']!=370\
        or df1.at[i,'player_ID']!=495 or df1.at[i,'player_ID']!=601 or df1.at[i,'player_ID']!=331 or df1.at[i,'player_ID']!=409 or df1)):
            start=0#initialization of start of participation as 0 minutes
            end=int(df3.at[j,'minute_in_match'])-1#initialization of end of participation as minute_in_match of attributes violation
            if end>90:#if the attribution happens after the 90 minutes we make it happen in the 89' minute
                end=89
            match_ID=int(df1.at[i,'match_ID'])
            player_ID=int(df3.at[j,'player_ID'])
            participation=end
            starter=df1.at[i,'start']
            try:
                L.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),df1.at[i,'saves'],\
                          int(df1.at[i,'shots']),int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
            except:
                L.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),'NULL',int(df1.at[i,'shots']),\
                          int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
            participation_ID+=1

#To get the participation time of the players that participate the whole 90 minutes
for i in range(0,len(df1)):
    if(int(df1.at[i,'participation_in_match'])==90 and (df1.at[i,'player_ID']!=596 or df1.at[i,'player_ID']!=538 or df1.at[i,'player_ID']!=172 or df1.at[i,'player_ID']!=370\
    or df1.at[i,'player_ID']!=495 or df1.at[i,'player_ID']!=601 or df1.at[i,'player_ID']!=331 or df1.at[i,'player_ID']!=409\
    or df1.at[i,'player_ID']!=463 or df1.at[i,'player_ID']!=559 or df1.at[i,'player_ID']!=458)):
        match_ID=int(df1.at[i,'match_ID'])
        player_ID=int(df1.at[i,'player_ID'])
        start=0#start_time
        end=90#end_tim
        starter=1
        participation=90
        try:
            L.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),df1.at[i,'saves'],\
                      int(df1.at[i,'shots']),int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
        except:
            L.append([participation_ID,match_ID,player_ID,starter,start,end,participation,df1.at[i,'start'],int(df1.at[i,'goals']),'NULL',int(df1.at[i,'shots']),\
                      int(df1.at[i,'shots_on_target']),int(df1.at[i,'assists']),int(df1.at[i,'tackles']),int(df1.at[i,'passes']),df1.at[i,'position']])
        participation_ID+=1

    
headers = ['player_ID','match_ID','start','goals','participation_in_match','saves','shots','shots_on_target','assists','tackles','passes','position',\
           'start_of_participation','end_of_participation']
workbook = xw.Workbook('participates_fixed.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)


for i in range(len(df1)):
    for j in range(len(L)):
        if(int(df1.at[i,'player_ID'])==L[j][2] and int(df1.at[i,'match_ID'])==L[j][1]):
            row+=1
            #stats
            print(row)
            worksheet.write(row,col,L[j][2])#player ID
            worksheet.write(row,col+1,L[j][1])#match ID
            worksheet.write(row,col+2,L[j][7]) #starter
            worksheet.write(row,col+3,L[j][8]) #goals
            worksheet.write(row,col+4,L[j][6]) #participation in match
            try:
                worksheet.write(row,col+5,df1.at[i,'saves'])
            except:
                worksheet.write(row,col+5,"NULL")
            worksheet.write(row,col+6,L[j][10]) #shots
            worksheet.write(row,col+7,L[j][11]) #shots on target
            worksheet.write(row,col+8,L[j][12]) #assists
            worksheet.write(row,col+9,L[j][13]) #tackles
            worksheet.write(row,col+10,L[j][14]) #passes
            worksheet.write(row,col+11,L[j][15]) #position
            worksheet.write(row,col+12,L[j][4]) #start of participation
            worksheet.write(row,col+13,L[j][5]) #end of participation
#We finish creating the excel file.
workbook.close()


headers = ['substitution_ID','match_ID','player_ID','minute_in_match']
workbook = xw.Workbook('substitutions_fixed.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)
    
#We fix the minute_in_match in substitutes
for x in range(len(df2['player_ID'])):
    for y in range(len(L)):
        #If a player gets into a game, then his start time is the time when the substitution happens
        if (df2['player_ID'][x]==L[y][2] and df2['match_ID'][x]==L[y][1] and x%2==0):
            minute_in_match=L[y][4]
            match_ID=df2['match_ID'][x]
            substitution_ID=df2['substitution_ID'][x]
            player_ID=df2['player_ID'][x]
        #If a player leaves a game, then his end time is the time when the substitution happens
        elif (df2['player_ID'][x]==L[y][2] and df2['match_ID'][x]==L[y][1] and x%2==1):
            minute_in_match=L[y][5]    
            match_ID=df2['match_ID'][x]
            substitution_ID=df2['substitution_ID'][x]
            player_ID=df2['player_ID'][x]
    row+=1
    worksheet.write(row,col,substitution_ID)
    worksheet.write(row,col+1,match_ID)
    worksheet.write(row,col+2,player_ID)
    worksheet.write(row,col+3,minute_in_match)

#We finish creating the excel file.
workbook.close()


headers = ['violation_ID','match_ID','player_ID','disqualification','minute_in_match','card']
workbook = xw.Workbook('attributes_violation_fixed.xlsx')
worksheet = workbook.add_worksheet()
row=0
col=0
for count,l in enumerate(headers):
    worksheet.write(row, count,l)

#We fix the minute_in_match in attributes_violation
for x in range(len(df3['minute_in_match'])):
    for y in range(len(L)):#If the player gets a Red or a Second Yellow card,then set the minute in match as the end time of the Player
        if (df3['player_ID'][x]==L[y][2] and df3['match_ID'][x]==L[y][1] and (df3['card'][x]=="Red" or df3['card'][x]=="Second Yellow")):
            minute_in_match=L[y][5]
            row+=1
            worksheet.write(row,col,df3.at[x,'violation_ID'])
            worksheet.write(row,col+1,df3.at[x,'match_ID'])
            worksheet.write(row,col+2,df3.at[x,'player_ID'])
            worksheet.write(row,col+3,df3.at[x,'disqualification'])
            worksheet.write(row,col+4,minute_in_match)
            worksheet.write(row,col+5,df3.at[x,'card'])
        elif (df3['player_ID'][x]==L[y][2] and df3['match_ID'][x]==L[y][1] and df3['minute_in_match'][x]>=90):#If the minute in which the violation happens is over 90', then make 89
            minute_in_match=89
            row+=1
            worksheet.write(row,col,df3.at[x,'violation_ID'])
            worksheet.write(row,col+1,df3.at[x,'match_ID'])
            worksheet.write(row,col+2,df3.at[x,'player_ID'])
            worksheet.write(row,col+3,df3.at[x,'disqualification'])
            worksheet.write(row,col+4,minute_in_match)
            worksheet.write(row,col+5,df3.at[x,'card'])
        #else
        elif(df3['player_ID'][x]==L[y][2] and df3['match_ID'][x]==L[y][1] and df3['minute_in_match'][x]<90 and (df3['card'][x]!="Red" and df3['card'][x]!="Second Yellow")):
            row+=1
            worksheet.write(row,col,df3.at[x,'violation_ID'])
            worksheet.write(row,col+1,df3.at[x,'match_ID'])
            worksheet.write(row,col+2,df3.at[x,'player_ID'])
            worksheet.write(row,col+3,df3.at[x,'disqualification'])
            worksheet.write(row,col+4,df3.at[x,'minute_in_match'])
            worksheet.write(row,col+5,df3.at[x,'card'])

#Creation of new attributes violation relation file
workbook.close()

