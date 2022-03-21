import tkinter as tk
from tkinter import ttk
import sqlite3
import time

class DataModel(): #class that connects to the database and creates a cursor
    def __init__(self, filename):
        self.filename = filename
        try:
            self.con = sqlite3.connect(filename)
            self.con.row_factory = sqlite3.Row
            self.cursor = self.con.cursor()
            print("Successful connection to database", filename)
        except sqlite3.Error as error:
            print("Error connecting to the database sqlite", error)
    
    def close(self): #stop the connection to the database
        self.con.commit()
        self.con.close()

    
    def executeSQL(self, query, show=False): #execute SQL queries
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)
                    sql_time = time.perf_counter() - t1
                    print(f'The code was executed {statement[:40]}... in {sql_time:.5f} sec')
            
            if show:
                d=[]
                for row in self.cursor.fetchall():
                    #print(", ".join([str(item)for item in row]))
                    d.append([str(item)for item in row])
            self.con.commit()
            return d
        except sqlite3.Error as error:
            print(f"Error while trying to execute SQL", error)
            return False

    def readTable(self, table):
        '''Φόρτωμα ενός πίνακα, όταν το προαιρετικό όρισμα machine πάρει τιμή, τότε επιστρέφει μόνο 
        τις εγγραφές που αφορούν τη συγκεκριμένη μηχανή'''
        try:
            query = f'''SELECT * FROM {table};'''
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            result = []
            for row in records:
                result.append(dict(row))
            return result
        except sqlite3.Error as error:
            print(f"Σφάλμα φόρτωσης πίνακα {table}", error)
    
    def _insertIntoTable(self, table, row_dict):
        ''' Εισαγωγή εγγραφής σε μορφή λεξικού σε πίνακα'''
        try:
            query_param = f"""INSERT INTO {table} ({",".join(row_dict.keys())}) VALUES ({", ".join((len(row_dict)-1) * ["?"])}, ?);"""
            data = tuple(row_dict.values())
            self.cursor.execute(query_param, data)
            self.con.commit()
            return True
        except sqlite3.Error as error:
            print(f"Σφάλμα εισαγωγής στοιχείων στον πίνακα {table}", error)
            return False


class MyApp:
    #Creation of the root window
    def __init__(self,root):
        self.root=root
        root.title("Premier League 2020-2021")#title of the root window
        root.iconbitmap(r'images\premier_league_logo.ico')#icon of the window
        root.state('zoomed')
        self.bg=tk.PhotoImage(file=r'images\pr.png')#here we put as a background of the root window this png file
        self.bg_label = tk.Label(root, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        #Configuration of the sizes of the columns of the root window
        for i in [0,6,7,8]:
            root.rowconfigure(i, weight=0)
        for i in[1,2,3,4,5]:
            root.rowconfigure(i, weight=3)
        #Creation of the Table,Matches,Players,Teams,Referees,Stadiums,More Stats and Exit Buttons and a Frame in the right side of the root window
        self.b1=tk.Button(self.root,text='Table',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed1)
        self.b1.grid(row=0,column=0,padx=10,pady=10,sticky='ns')
        self.b2=tk.Button(root,text='Matches',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed2)
        self.b2.grid(row=1,column=0,padx=10,pady=10,sticky='ns')
        self.b3=tk.Button(root,text='Players',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed3)
        self.b3.grid(row=2,column=0,padx=10,sticky='ns',pady=10)
        self.b4=tk.Button(root,text='Teams',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed4)
        self.b4.grid(row=3,column=0,padx=10,sticky='ns',pady=10)
        self.b5=tk.Button(root,text='Referees',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed5)
        self.b5.grid(row=4,column=0,padx=10,sticky='ns',pady=10)
        self.b6=tk.Button(root,text='Managers',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed6)
        self.b6.grid(row=5,column=0,padx=10,sticky='ns',pady=10)
        self.b7=tk.Button(root,text='Stadiums',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed7)
        self.b7.grid(row=6,column=0,padx=10,sticky='ns',pady=10)
        self.b8=tk.Button(root,text='More Stats',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed8)
        self.b8.grid(row=7,column=0,padx=10,sticky='ns',pady=10)
        self.b11=tk.Button(root,text='Exit',width=50,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed)
        self.b11.grid(row=8,column=0,padx=10,sticky='ns',pady=10)
        self.f1=tk.Frame(root,height=900,width=930,bg='#FFFFFF')
        self.f1.grid(row=1,column=2,padx=10,ipady=10,rowspan=7,columnspan=2)
        self.f1.grid_propagate(0)

    #When the button Table is pushed, then in the Frame right of the root, The Table of the Championship is being created and the user can select the matchweek in which the points are being calculated
    def buttonPushed1(self):
        labels=[]
        #import of database
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(7):#Configuration of columns of Frame
            self.f1.columnconfigure(i, weight=1)
        def selected(event):
            for x in labels:#Destruction of previous labels
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            s=self.myCombo.get().split(" ")#We get the selection of the user
            self.label=tk.Label(self.f1,text="matchweek {}".format(s[1]),bg='#873ec7',font="Arial 13")#Label of matchweek
            sql='''SELECT name,count(*) as number_of_matches,sum(IIF(CAST(SUBSTR(score,1,1) as integer)>CAST(SUBSTR(score,3,3) as integer) and e.home=1,1,0)) + sum(IIF(CAST(SUBSTR(score,1,1) as integer)<CAST(SUBSTR(score,3,3) as integer) and e.home=0,1,0))  as wins, sum(IIF(CAST(SUBSTR(score,1,1) as integer)=CAST(SUBSTR(score,3,3) as integer) and (e.home=1 or e.home=0),1,0)) as ties, sum(IIF(CAST(SUBSTR(score,1,1) as integer)<CAST(SUBSTR(score,3,3) as integer) and e.home=1,1,0)) + sum(IIF(CAST(SUBSTR(score,1,1) as integer)>CAST(SUBSTR(score,3,3) as integer) and e.home=0,1,0))  as losses,sum(IIF((CAST(SUBSTR(score, 1, 1) AS INTEGER))==(CAST(SUBSTR(score, 3, 3) AS INTEGER)),1,IIF(home,IIF((CAST(SUBSTR(score, 1, 1) AS INTEGER))>(CAST(SUBSTR(score, 3, 3) AS INTEGER)),3,0),IIF((CAST(SUBSTR(score, 1, 1) AS INTEGER))>(CAST(SUBSTR(score, 3, 3) AS INTEGER)),0,3)))) AS pointss
                   FROM Match_ AS M,enters AS E,Team AS T 
                   WHERE M.match_ID=E.match_ID AND T.team_ID=E.team_ID AND matchweek<={}
                   GROUP BY T.team_ID
                   ORDER BY pointss DESC,wins DESC,ties DESC ,losses DESC;'''.format(s[1])##We get the number of games,wins,ties,losses and points of every team until the matchweek that was selected
            l=d.executeSQL(sql,show=True)
            #Creation of the table     
            self.label.grid(row=8,column=0,columnspan=8,sticky='ew')
            labels.append(self.label)
            self.label1=tk.Label(self.f1,text="Position",bg='#873ec7',font="Arial 13")
            self.label1.grid(row=9,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f1,text="Club",bg='#873ec7',width=20,font="Arial 13")
            self.label2.grid(row=9,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f1,text="Played",bg='#873ec7',font="Arial 13")
            self.label3.grid(row=9,column=2,sticky='ew')
            labels.append(self.label3)
            self.label4=tk.Label(self.f1,text="Wins",bg='#873ec7',font="Arial 13")
            self.label4.grid(row=9,column=3,sticky='ew')
            labels.append(self.label4)
            self.label5=tk.Label(self.f1,text="Draws",bg='#873ec7',font="Arial 13")
            self.label5.grid(row=9,column=4,sticky='ew')
            labels.append(self.label5)
            self.label6=tk.Label(self.f1,text="Loses",bg='#873ec7',font="Arial 13")
            self.label6.grid(row=9,column=5,sticky='ew')
            labels.append(self.label6)
            self.label7=tk.Label(self.f1,text="Points",bg='#873ec7',font="Arial 13")
            self.label7.grid(row=9,column=6,sticky='ew')
            labels.append(self.label7)
            row1=10
            #For every team we create labels for the position of the team in the table,the name of the team,the number of wins,draws and losses and the points of the team
            for i in range(0,20):
                self.label=tk.Label(self.f1,text="{}".format(i+1),bg='#dbbfbf',font="Arial 12")
                self.label.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label1)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][0]),bg='#dbbfbf',width=20,font="Arial 12")
                self.label1.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label1)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][1]),bg='#dbbfbf',width=8,font="Arial 12")
                self.label1.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label1)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][2]),bg='#dbbfbf',width=8,font="Arial 12")
                self.label1.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label1)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][3]),bg='#dbbfbf',width=8,font="Arial 12")
                self.label1.grid(row=row1,column=4,sticky='ew')
                labels.append(self.label1)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][4]),bg='#dbbfbf',width=8,font="Arial 12")
                self.label1.grid(row=row1,column=5,sticky='ew')
                labels.append(self.label1)
                self.label2=tk.Label(self.f1,text="{}".format(l[i][5]),bg='#dbbfbf',width=8,font="Arial 12")
                self.label2.grid(row=row1,column=6,sticky='ew')
                labels.append(self.label2)
                row1+=1
        for widget in self.f1.winfo_children():#Destruction of what was happening already in the Frame
            widget.destroy()
        self.label=tk.Label(self.f1,text="Table of Premier League",bg='#873ec7',font="Arial 15")
        options=[]
        for i in range(1,39):
            options.append("matchweek "+str(i))#Creation of a Combobox in which the user selects the matchweek of the Championship
        self.myCombo=ttk.Combobox(self.f1,value=options)
        self.myCombo.current(37)
        
        self.myCombo.bind("<<ComboboxSelected>>",selected)#if an option is selected, function selected happens
        self.label.grid(row=1,column=0,columnspan=8,sticky='ew')
        self.myCombo.grid(row=2,column=2,ipadx=10,ipady=5)

    #When the button Matches is pushed, then in the Frame right of the root, The Matches of the Championship are being created and the user can select the matchweek in which the Matches are being shown
    def buttonPushed2(self):
        #import of database
        dbfile = "project.db"
        d = DataModel(dbfile)
        labels=[]#list of labels
        buttons=[]#list of buttons
        self.image=[]#list of images
        self.violation_id=1200
        options=['Manchester City','Manchester Utd','Liverpool','Chelsea','Leicester City','West Ham','Tottenham','Arsenal','Leeds United','Everton','Aston Villa','Newcastle Utd','Wolves','Crystal Palace','Southampton','Brighton','Burnley','Fulham','West Brom','Sheffield Utd']
        for i in range(0,20):#Import of the images of every team
            self.image.append(tk.PhotoImage(file=r'images\{}.png'.format(options[i])))
        for i in range(7):#Configuration of columns of the Frame
            self.f1.columnconfigure(i, weight=1)
        def selected(event):#When the user selects the matchweek, selected function happens
            def Match_Report(datetime_,stadium,match_ID,matchweek):#When a button Match Report is being pushed, we create a new window, where analytic stats are being shown
               def Update():#Creation of a window in which we insert the Team in which we want to update the stats. Finally we press the Submit button and we get to the UpdateStats function
                  c=tk.Toplevel()
                  self.c=c
                  self.label=tk.Label(self.c,text="Updating Statistics of Match {} vs {}".format(self.l1[0][1],self.l1[0][3]))
                  self.label.grid(row=0,column=0)
                  self.label1=tk.Label(self.c,text="For which of the two teams do you want to update the stastistics:")
                  self.label1.grid(row=1,column=0)
                  self.entry=tk.Entry(self.c,borderwidth=2)
                  self.entry.grid(row=1,column=1)
                  self.entry.insert(0,"Enter name of team")
                  self.button=tk.Button(self.c,text="Submit",command=UpdateStats)
                  self.button.grid(row=1,column=3)  

               def UpdateButton(match_ID):#Here first we see if the inserted Player plays in the Match and if it does , we update his stats
                      p=[]
                      for i in range(len(self.entries)):
                          p.append(self.entries[i].get())
                      print(p)
                      #query in witch we see if the player plays in the match 
                      if p[0]=="":
                          sql='''Select p1.player_ID from Player as p1,participates as p2 where p1.player_ID=p2.player_ID and last_name="{}" and p2.match_ID={}'''.format(p[1],match_ID)
                      else:
                          sql='''Select p1.player_ID from Player as p1,participates as p2 where p1.player_ID=p2.player_ID and first_name="{}" and last_name="{}" and p2.match_ID={}'''.format(p[0],p[1],match_ID)
                      l1=d.executeSQL(sql,show=True)
                      print(l1)
                      if len(l)==0:#if its not, this label is being created
                          self.label=tk.Label(self.c,text="This player is not in this match.Try again")
                          self.label.grid(row=15,column=0,columnspan=2)
                      else:#else We update the stats of the Player in the Match
                          sql1='''update participates set start={},participation_in_match={},position="{}",shots={},shots_on_target={},assists={},saves={},passes={},tackles={},end_of_participation=start_of_participation+participation_in_match where player_ID={} and match_ID={}'''.format(p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],l1[0][0],match_ID)
                          l2=d.executeSQL(sql1,show=True)
               def UpdateStats():#Creation of a window in which we can insert the name of the player and the new stats of the player that plays in the match
                      team=self.entry.get()
                      if(';' in team or 'drop' in team or 'delete' in team): #checking if someone tried to erase the database through the input
                          self.label0=tk.Label(self.c,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
                          self.label0.grid()
                      elif team==self.l1[0][1] or team==self.l1[0][3]:
                          for widget in self.c.winfo_children():
                             widget.destroy()
                          self.label=tk.Label(self.c,text="Player firstname")
                          self.label1=tk.Label(self.c,text="Player lastname")
                          self.label12=tk.Label(self.c,text="start")
                          self.label3=tk.Label(self.c,text="participation")
                          self.label4=tk.Label(self.c,text="position")
                          self.label6=tk.Label(self.c,text="shots")
                          self.label7=tk.Label(self.c,text="shots on target")
                          self.label8=tk.Label(self.c,text="assists")
                          self.label9=tk.Label(self.c,text="saves")
                          self.label10=tk.Label(self.c,text="passes")
                          self.label11=tk.Label(self.c,text="tackles")
                          #self.labels=[self.label,self.label1]
                          self.labels=[self.label,self.label1,self.label12,self.label3,self.label4,self.label6,self.label7,self.label8,self.label9,self.label10,self.label11]
                          self.entry=tk.Entry(self.c,borderwidth=2)
                          self.entry1=tk.Entry(self.c,borderwidth=2)
                          self.entry12=tk.Entry(self.c,borderwidth=2)
                          self.entry3=tk.Entry(self.c,borderwidth=2)
                          self.entry4=tk.Entry(self.c,borderwidth=2)
                          self.entry6=tk.Entry(self.c,borderwidth=2)
                          self.entry7=tk.Entry(self.c,borderwidth=2)
                          self.entry8=tk.Entry(self.c,borderwidth=2)
                          self.entry9=tk.Entry(self.c,borderwidth=2)
                          self.entry10=tk.Entry(self.c,borderwidth=2)
                          self.entry11=tk.Entry(self.c,borderwidth=2)
                          #self.entries=[self.entry,self.entry1]
                          self.entries=[self.entry,self.entry1,self.entry12,self.entry3,self.entry4,self.entry6,self.entry7,self.entry8,self.entry9,self.entry10,self.entry11]
                          for i in range(len(self.labels)):
                              self.labels[i].grid(row=i+1,column=0)
                              self.entries[i].grid(row=i+1,column=1)
                          #Pressing the Button Update we process the information and we go to function UpdateButton
                          self.Button1=tk.Button(self.c,text="Update",command= lambda match_ID=self.l1[0][0]:UpdateButton(match_ID))
                          self.Button1.grid(row=13,column=0)
                      else:
                          self.label=tk.Label(self.c,text="Team Not in match!! Try again")
                          self.label.grid(row=2,column=1)
               def Update_Match(match_id):#Pressing the Submit Button we update the information of the Match
                   p=[]
                   flag=0
                   for i in range(len(self.entries2)):
                       if(';' in self.entries2[i].get() or 'drop' in self.entries2[i].get() or 'delete' in self.entries2[i].get()): #checking if someone tried to erase the database through the input
                            flag=1
                       p.append(self.entries2[i].get())
                   if flag==0:
                       sql='''select stadium_ID from Stadium where name="{}" '''.format(p[2])#query in which we see if the inserted stadium is in the database
                       s=d.executeSQL(sql,show=True)
                       if len(p[0])!=10:#if the date is not well inserted,the following label is being created
                            self.label=tk.Label(self.a,text="Invalid Date")
                            self.label.grid(row=7,column=0,columnspan=2)
                       elif len(p[1])!=5:#if the time is not well inserted,the following label is being created
                            self.label=tk.Label(self.a,text="Invalid Time")
                            self.label.grid(row=7,column=0,columnspan=2)
                       elif len(s)==0:# if the inserted stadium is not in the database, then the following label is being created
                            self.label=tk.Label(self.a,text="Invalid Stadium Name")
                            self.label.grid(row=7,column=0,columnspan=2)
                       else:#else we update the Match information with the following query
                            datetime_=p[0]+" "+p[1]
                            self.a.destroy()
                            sql='''update Match_ set datetime_="{}",stadium_code={} where match_ID={}'''.format(datetime_,s[0][0],match_id)
                            d.executeSQL(sql,show=True)
                   else:
                       self.label0=tk.Label(self.a,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
                       self.label0.grid()
               def Update3(match_id):#Pressing the Update Match Button, the user can insert values for the score, the date and time of the match and the Stadium of the match
                   a=tk.Toplevel()
                   self.a=a
                   self.label=tk.Label(self.a,text="Update Match {} vs {}".format(self.l1[0][1],self.l1[0][3]))
                   self.label.grid(row=0,column=0,columnspan=2)
                   self.label1=tk.Label(self.a,text="date")
                   self.label2=tk.Label(self.a,text="time")
                   self.label5=tk.Label(self.a,text="stadium")
                   self.labels2=[self.label,self.label1,self.label2,self.label5]
                   self.entry1=tk.Entry(self.a,borderwidth=2)
                   self.entry2=tk.Entry(self.a,borderwidth=2)
                   self.entry5=tk.Entry(self.a,borderwidth=2)
                   self.entries2=[self.entry1,self.entry2,self.entry5]
                   #Button in which the inserting information are getting processed
                   self.button=tk.Button(self.a,text="Submit",command= lambda match_id=match_id : Update_Match(match_id))
                   for i in range(1,len(self.labels2)):
                         self.labels2[i].grid(row=i,column=0)
                         self.entries2[i-1].grid(row=i,column=1)
                   self.button.grid(row=6,column=0)
                   
               b=tk.Toplevel()#creation of a new window
               self.b=b
               b.state('zoomed')
               my_canvas= tk.Canvas(self.b)
               my_canvas.pack(side="left",fill="both",expand=1)
               my_scrollbar=ttk.Scrollbar(self.b,orient="vertical",command=my_canvas.yview)#creation of a scrollbar
               my_scrollbar.pack(side="right",fill="y")
               my_canvas.configure(yscrollcommand=my_scrollbar.set)
               my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
               a=tk.Frame(my_canvas)#creation of a Frame in the window
               self.a=a
               my_canvas.create_window((0,0),window=a,anchor='nw')
               for i in range(15):#Configuration of columns of the Frame
                   a.columnconfigure(i, weight=2)
               #Teams that take part in the match,the goals that they made,the number of autogoals(if they were autogoals)
               sql='''select a1.match_ID,a1.team1,a1.team_ID,a2.team2,a2.team_ID,a1.goals1,a1.goals,IIF(a1.goals1==a1.goals,0,a1.goals1-a1.goals) as autogoals1,a2.goals2,a2.goals,IIF(a2.goals2==a2.goals,0,a2.goals2-a2.goals) as autogoals2,IIF(a1.goals1==a1.goals,0,a1.goals1-a1.goals) +a1.goals as total_goals1,a2.goals+IIF(a2.goals2==a2.goals,0,a2.goals2-a2.goals)  as total_goals2
                      from(select m.match_ID,IIF(e.home==1,t.name,NULL) as team1,t.team_ID,sum(goals) as goals,cast(substr(score,1,1) as integer) as goals1 
                      from Match_ as m,enters as e,Team as t,belongs as b,participates as p1     
                      where m.match_ID=e.match_ID and t.team_ID=e.team_ID and b.team_ID=e.team_ID and p1.match_ID=m.match_ID and p1.player_ID=b.player_ID and e.home=1 and b.contract_end_day>m.datetime_ and m.match_ID={}
                      group by m.match_ID,t.team_ID 
                      order by m.match_ID) as a1 left join 
                      (select m.match_ID,IIF(e.home==0,t.name,NULL) as team2,t.team_ID,sum(goals) as goals,cast(substr(score,3,3) as integer) as goals2 
                      from Match_ as m,enters as e,Team as t,belongs as b,participates as p1  
                      where m.match_ID=e.match_ID and t.team_ID=e.team_ID and b.team_ID=e.team_ID and p1.match_ID=m.match_ID and p1.player_ID=b.player_ID and e.home=0 and b.contract_end_day>m.datetime_ and m.match_ID={}
                      group by m.match_ID,t.team_ID
                      order by m.match_ID) as a2 on a1.match_ID=a2.match_ID 
                      where a1.team1 is not NULL and a2.team2 is not NULL
                      order by a1.match_ID
                '''.format(match_ID,match_ID)
               self.l1=d.executeSQL(sql,show=True)
               self.label=tk.Label(a,text="{} vs {} Match Report - {} matchweek: {} Stadium:{} ".format(self.l1[0][1],self.l1[0][3],datetime_,matchweek,stadium),font="Arial 14",bg='#873ec7',width=140)
               self.label.grid(row=0,column=0,columnspan=15,sticky="ew")
               #Import of images of the teams in the specific columns
               self.label=tk.Label(a,image=self.image[int(self.l1[0][2])])  
               self.label.grid(row=1,column=6)
               self.Label=tk.Label(a,text=" vs ",font="Arial 12")
               self.Label.grid(row=1,column=7)
               self.label=tk.Label(a,image=self.image[int(self.l1[0][4])])         
               self.label.grid(row=1,column=8)
               #labels of the names of the teams
               self.label=tk.Label(a,text="{}".format(self.l1[0][1]),font="Arial 12")
               self.label.grid(row=2,column=6)
               self.label=tk.Label(a,text="{}".format(self.l1[0][3]),font="Arial 12")
               self.label.grid(row=2,column=8)
               #Coaches of the teams in the match
               sql11='''select first_name,last_name from Coach where team_code={} and (contract_end_date>"{}" or contract_end_date is NULL) '''.format(self.l1[0][2],datetime_)
               l11=d.executeSQL(sql11,show=True)
               sql12='''select first_name,last_name from Coach where team_code={} and (contract_end_date>"{}" or contract_end_date is NULL) '''.format(self.l1[0][4],datetime_)
               l12=d.executeSQL(sql12,show=True)
               #Goals of the teams
               self.label=tk.Label(a,text="{}".format(self.l1[0][-2]),font="Arial 12")       
               self.label.grid(row=3,column=6)
               self.Label=tk.Label(a,text=" : ",font="Arial 12")
               self.Label.grid(row=3,column=7)
               self.label=tk.Label(a,text="{}".format(self.l1[0][-1]),font="Arial 12")         
               self.label.grid(row=3,column=8)
               #Labels of the coaches of the teams
               self.label=tk.Label(a,text="Coach: {} {}".format(l11[0][0],l11[0][1]),font="Arial 12")
               self.label.grid(row=4,column=6)
               self.label=tk.Label(a,text="Coach: {} {}".format(l12[0][0],l12[0][1]),font="Arial 12")
               self.label.grid(row=4,column=8)
               #Referees that ispect the match
               sql13='''select  r.first_name,r.last_name,i.status
                        from Referee as r,inspects as i,Match_ as m
                        where r.referee_ID=i.referee_ID and m.match_ID=i.match_ID and m.match_ID={}
                        order by i.status DESC'''.format(match_ID)
               l13=d.executeSQL(sql13,show=True)
               self.label=tk.Label(a,text="Officials: {} {} ({}), {} {} ({}),{} {} ({}),{} {} ({})".format(l13[0][0],l13[0][1],l13[0][2],l13[2][0],l13[2][1],l13[2][2],l13[1][0],l13[1][1],l13[1][2],l13[3][0],l13[3][1],l13[3][2]))
               self.label.grid(row=5,column=4,columnspan=8)
               #Button in which the user can update information about the match, the score,the date and time and the Stadium 
               self.button=tk.Button(a,text="Update Match",command= lambda match_id=self.l1[0][0] : Update3(match_id))
               self.button.grid(row=5,column=14)
               #Scorers of the first team
               self.label=tk.Label(a,text="Scorers",font="Arial 12",bg='#873ec7',width=140)
               self.label.grid(row=6,column=0,columnspan=15,sticky="ew")
               sql3='''select p2.first_name,p2.last_name,p1.goals
                       from participates as p1,Player as p2,belongs as b,Match_ as m
                       where p1.player_ID=p2.player_ID and b.player_ID=p2.player_ID and  m.match_ID=p1.match_ID and m.match_ID={} and p1.goals>0 and b.team_ID={} and b.contract_end_day > m.datetime_
                        '''.format(match_ID,self.l1[0][2])
               l3=d.executeSQL(sql3,show=True)
               row1=7
               goals1=0#goals for team1 
               for i in range(len(l3)):
                   if l3[i][0]=='None':
                       l3[i][0]=l3[i][0].replace('None','')
                   self.label1=tk.Label(a,text="{} {} goals:{}".format(l3[i][0],l3[i][1],l3[i][2]))         
                   self.label1.grid(row=row1,column=6)
                   goals1+=int(l3[i][2])
                   row1+=1
               #Checking for auto-goals
               if int(self.l1[0][7])!=0:
                   self.label1=tk.Label(a,text="Own-goals: {}".format(int(self.l1[0][7])))   
                   self.label1.grid(row=row1,column=6)
                   goals1=int(self.l1[0][-2])
               #Scorers of the second team
               sql4='''select p2.first_name,p2.last_name,p1.goals
                       from participates as p1,Player as p2,belongs as b,Match_ as m
                       where p1.player_ID=p2.player_ID and b.player_ID=p2.player_ID and  m.match_ID=p1.match_ID and m.match_ID={} and p1.goals>0 and b.team_ID={} and b.contract_end_day > m.datetime_
                        '''.format(match_ID,self.l1[0][4])
               l4=d.executeSQL(sql4,show=True)
               row2=7
               goals2=0 #goals for the team2
               for i in range(len(l4)):
                   if l4[i][0]=='None':
                      l4[i][0]=l4[i][0].replace('None','')
                   self.label1=tk.Label(a,text="{} {} goals:{}".format(l4[i][0],l4[i][1],l4[i][2]))         
                   self.label1.grid(row=row2,column=8)
                   goals2+=int(l4[i][2])    
                   row2+=1
               #Checking for auto-goals
               if int(self.l1[0][10])!=0:
                   self.label1=tk.Label(a,text="Own-goals: {}".format(int(self.l1[0][10])))       
                   self.label1.grid(row=row2,column=8)
                   goals2=int(self.l1[0][-1])
               if goals1==0 and goals2==0:
                   self.label=tk.Label(a,text=" ")
                   self.label.grid(row=row2,column=0,columnspan=15,sticky='ew')
               #Creation of labels for the players that got a card for both teams
               sql5='''select p1.first_name,p1.last_name,a.minute_in_match,a.card
                            from Player as p1,attributes_violation as a,belongs as b,Match_ as m 
                            where p1.player_ID=a.player_ID and b.player_ID=p1.player_ID and m.match_ID=a.match_ID and b.team_ID={} and a.match_ID={} and b.contract_end_day > m.datetime_
                            order by a.minute_in_match'''.format(self.l1[0][2],match_ID)
               l5=d.executeSQL(sql5,show=True)
               row3=max(row1,row2)+1
               self.label=tk.Label(a,text="Cards",font="Arial 12",bg='#873ec7',width=140)
               self.label.grid(row=row3,column=0,columnspan=15,sticky='ew')
               row3+=1
               cards1=0
               for i in range(len(l5)):
                    if l5[i][0]=='None':
                       l5[i][0]=l5[i][0].replace('None','')
                    self.label1=tk.Label(a,text="{} {}:{} card({}')".format(l5[i][0],l5[i][1],l5[i][3],l5[i][2]))         
                    self.label1.grid(row=row3,column=6)
                    cards1+=1
                    row3+=1
               sql5='''select p1.first_name,p1.last_name,a.minute_in_match,a.card
                            from Player as p1,attributes_violation as a,belongs as b,Match_ as m
                            where p1.player_ID=a.player_ID and b.player_ID=p1.player_ID and m.match_ID=a.match_ID and b.team_ID={} and a.match_ID={} and b.contract_end_day > m.datetime_
                            order by a.minute_in_match'''.format(self.l1[0][4],match_ID)
               l5=d.executeSQL(sql5,show=True)
               row4=max(row1,row2)+1
               row4+=1
               cards2=0
               for i in range(len(l5)):
                    if l5[i][0]=='None':
                        l5[i][0]=l5[i][0].replace('None','')
                    self.label1=tk.Label(a,text="{} {}:{} card({}')".format(l5[i][0],l5[i][1],l5[i][3],l5[i][2]))         
                    self.label1.grid(row=row4,column=8)
                    row4+=1
                    cards2+=1
               if cards1==0 and cards2==0:
                   self.label=tk.Label(a,text=" ")
                   self.label.grid(row=row4,column=0,columnspan=15,sticky="ew")
               #Creation of labels for the players that took part in a substitution
               sql6='''select p1.first_name,p1.last_name,s.minute_in_match
                        from Player as p1,substitutes as s,belongs as b,Match_ as m
                        where p1.player_ID=s.player_ID and b.player_ID=p1.player_ID and m.match_ID=s.match_ID and b.team_ID={} and s.match_ID={} and b.contract_end_day > m.datetime_
                        order by s.minute_in_match'''.format(self.l1[0][2],match_ID)
               l6=d.executeSQL(sql6,show=True)
               row5=max(row3,row4)+1
               #self.button=tk.Button(a,text="Update cards",command= lambda match_id=self.l1[0][0]: Update1(match_id))
               #self.button.grid(row=row5,column=14)
               row5+=1
               self.label=tk.Label(a,text="Substitutions",font="Arial 12",bg='#873ec7',width=140)
               self.label.grid(row=row5,column=0,columnspan=15,sticky='ew')
               row5+=1
               for i in range(0,len(l6),2):
                    if l6[i][0]=='None':
                       l6[i+1][0]=l6[i+1][0].replace('None','')
                    if l6[i+1][0]=='None':
                       l6[i+1][0]=l6[i+1][0].replace('None','')
                    self.label1=tk.Label(a,text="Substitution: {} {} <-- {} {}({}')".format(l6[i][0],l6[i][1],l6[i+1][0],l6[i+1][1],l6[i][2]))         
                    self.label1.grid(row=row5,column=6)
                    row5+=1
               sql6='''select p1.first_name,p1.last_name,s.minute_in_match
                        from Player as p1,substitutes as s,belongs as b,Match_ as m
                        where p1.player_ID=s.player_ID and b.player_ID=p1.player_ID and m.match_ID=s.match_ID and b.team_ID={} and s.match_ID={} and b.contract_end_day > m.datetime_
                        order by s.minute_in_match'''.format(self.l1[0][4],match_ID)
               l7=d.executeSQL(sql6,show=True)
               row6=max(row3,row4)+1
               row6+=2
               for i in range(0,len(l7),2):
                    if l7[i][0]=='None':
                       l7[i][0]=l7[i][0].replace('None','')
                    if l7[i+1][0]=='None':
                       l7[i+1][0]=l7[i+1][0].replace('None','')
                    self.label1=tk.Label(a,text="Substitution: {} {} <-- {} {}({}')".format(l7[i][0],l7[i][1],l7[i+1][0],l7[i+1][1],l7[i][2]))         
                    self.label1.grid(row=row6,column=8)
                    row6+=1 
               row7=max(row5,row6)+1
               #Creation of a Frame for the stats of players for both teams that took part in the game
               self.t=tk.Frame(a,height=740,width=900,bg='#FFFFFF')
               self.t.grid(row=row7,column=3,padx=10,ipady=10,rowspan=7,columnspan=10)
               self.t.grid_propagate(0)
               for i in range(12):
                   self.f1.columnconfigure(i, weight=1)
               sql7='''select p1.first_name,p1.last_name,shirt_number,start,participation_in_match,position,goals,shots,shots_on_target,assists,saves,passes,tackles
                        from Player as p1,participates as p2,belongs as b,Match_ as m
                        where p1.player_ID=p2.player_ID and p2.player_ID=b.player_ID and m.match_ID=p2.match_ID and b.team_ID={} and p2.match_ID={} and b.contract_end_day>m.datetime_
                        order by participation_in_match'''.format(self.l1[0][2],match_ID)#Stats of players for team1
               l8=d.executeSQL(sql7,show=True)
               row8=0
               self.label=tk.Label(self.t,text="{}-Stats".format(self.l1[0][1]),font="Arial 13",bg='#873ec7')
               self.label.grid(row=row8,column=0,sticky='ew',columnspan=12)
               row8+=1
               for i in range(12):
                    self.t.columnconfigure(i, weight=1)
               self.label1=tk.Label(self.t,text="Player",bg='#873ec7')
               self.label2=tk.Label(self.t,text="shirt_number",bg='#873ec7')  
               self.label3=tk.Label(self.t,text="start",bg='#873ec7')
               self.label4=tk.Label(self.t,text="participation",bg='#873ec7')
               self.label5=tk.Label(self.t,text="position",bg='#873ec7')
               self.label6=tk.Label(self.t,text="goals",bg='#873ec7')
               self.label7=tk.Label(self.t,text="shots",bg='#873ec7')
               self.label8=tk.Label(self.t,text="shots on target",bg='#873ec7')
               self.label9=tk.Label(self.t,text="assists",bg='#873ec7')
               self.label10=tk.Label(self.t,text="saves",bg='#873ec7')
               self.label11=tk.Label(self.t,text="passes",bg='#873ec7')
               self.label12=tk.Label(self.t,text="tackles",bg='#873ec7')
               self.label1.grid(row=row8,column=0,sticky='ew')
               self.label2.grid(row=row8,column=1,sticky='ew')
               self.label3.grid(row=row8,column=2,sticky='ew')
               self.label4.grid(row=row8,column=3,sticky='ew')
               self.label5.grid(row=row8,column=4,sticky='ew')
               self.label6.grid(row=row8,column=5,sticky='ew')
               self.label7.grid(row=row8,column=6,sticky='ew')
               self.label8.grid(row=row8,column=7,sticky='ew')
               self.label9.grid(row=row8,column=8,sticky='ew')
               self.label10.grid(row=row8,column=9,sticky='ew')
               self.label11.grid(row=row8,column=10,sticky='ew')
               self.label12.grid(row=row8,column=11,sticky='ew')
               row8+=1
               for i in range(0,len(l8)):
                   if l8[i][0]=='None':
                        l8[i][0]=l8[i][0].replace('None','')
                   for j in range(1,len(l8[i])):
                       if l8[i][j]=='None':
                           l8[i][j]=l8[i][j].replace('None','0')
                   self.label=tk.Label(self.t,text="{} {}".format(l8[i][0],l8[i][1]))#Name of Player
                   self.label.grid(row=row8,column=0,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][2]))#shirt_number  
                   self.label.grid(row=row8,column=1,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][3]))#start
                   self.label.grid(row=row8,column=2,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][4]))#participation
                   self.label.grid(row=row8,column=3,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][5]))#position
                   self.label.grid(row=row8,column=4,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][6]))#goals
                   self.label.grid(row=row8,column=5,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][7]))#shots
                   self.label.grid(row=row8,column=6,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][8]))#shots_on_target
                   self.label.grid(row=row8,column=7,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][9]))#assists
                   self.label.grid(row=row8,column=8,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][10]))#saves
                   self.label.grid(row=row8,column=9,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][11]))#passes
                   self.label.grid(row=row8,column=10,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][12]))#tackles
                   self.label.grid(row=row8,column=11,sticky='ew')
                   row8+=1
               sql8='''select count(p1.player_ID),sum(participation_in_match),sum(goals),sum(shots),sum(shots_on_target),sum(assists),sum(saves),sum(passes),sum(tackles)
                        from Player as p1,participates as p2,belongs as b,Match_ as m
                        where p1.player_ID=p2.player_ID and p2.player_ID=b.player_ID and m.match_ID=p2.match_ID and b.team_ID={} and p2.match_ID={} and b.contract_end_day>m.datetime_
                        '''.format(self.l1[0][2],match_ID)#Total stats of players of team1
               l9=d.executeSQL(sql8,show=True)
               self.label=tk.Label(self.t,text="Total:{}".format(l9[0][0]))#number of players
               self.label.grid(row=row8,column=0,sticky='ew')
               self.label=tk.Label(self.t,text="")
               self.label.grid(row=row8,column=1,sticky='ew')
               self.label=tk.Label(self.t,text="")
               self.label.grid(row=row8,column=2,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][1]))#total number of minutes
               self.label.grid(row=row8,column=3,sticky='ew')
               self.label=tk.Label(self.t,text="")
               self.label.grid(row=row8,column=4,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][2]))#total number of goals
               self.label.grid(row=row8,column=5,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][3]))#total number of shots
               self.label.grid(row=row8,column=6,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][4]))#total number of shots on target
               self.label.grid(row=row8,column=7,sticky='ew')    
               self.label=tk.Label(self.t,text="{}".format(l9[0][5]))#total number of assists
               self.label.grid(row=row8,column=8,sticky='ew')    
               self.label=tk.Label(self.t,text="{}".format(l9[0][6]))#total number of saves
               self.label.grid(row=row8,column=9,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][7]))#total numberof passes
               self.label.grid(row=row8,column=10,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][8]))#total number of tackles
               self.label.grid(row=row8,column=11,sticky='ew')
               row8+=1
               self.label=tk.Label(self.t,text="{}-Stats".format(self.l1[0][3]),font="Arial 13",bg='#873ec7')
               self.label.grid(row=row8,column=0,sticky='ew',columnspan=12)
               row8+=1
               sql7='''select p1.first_name,p1.last_name,shirt_number,start,participation_in_match,position,goals,shots,shots_on_target,assists,saves,passes,tackles
                        from Player as p1,participates as p2,belongs as b,Match_ as m
                        where p1.player_ID=p2.player_ID and p2.player_ID=b.player_ID and m.match_ID=p2.match_ID and b.team_ID={} and p2.match_ID={} and b.contract_end_day>m.datetime_
                        order by participation_in_match'''.format(self.l1[0][4],match_ID)#Stats of players for team2
               l8=d.executeSQL(sql7,show=True)
               for i in range(12):
                    self.t.columnconfigure(i, weight=1)
               self.label1=tk.Label(self.t,text="Player",bg='#873ec7')
               self.label2=tk.Label(self.t,text="shirt_number",bg='#873ec7')
               self.label3=tk.Label(self.t,text="start",bg='#873ec7')
               self.label4=tk.Label(self.t,text="participation",bg='#873ec7')
               self.label5=tk.Label(self.t,text="position",bg='#873ec7')
               self.label6=tk.Label(self.t,text="goals",bg='#873ec7')
               self.label7=tk.Label(self.t,text="shots",bg='#873ec7')
               self.label8=tk.Label(self.t,text="shots on target",bg='#873ec7')
               self.label9=tk.Label(self.t,text="assists",bg='#873ec7')
               self.label10=tk.Label(self.t,text="saves",bg='#873ec7')
               self.label11=tk.Label(self.t,text="passes",bg='#873ec7')
               self.label12=tk.Label(self.t,text="tackles",bg='#873ec7')
               self.label1.grid(row=row8,column=0,sticky='ew')
               self.label2.grid(row=row8,column=1,sticky='ew')
               self.label3.grid(row=row8,column=2,sticky='ew')
               self.label4.grid(row=row8,column=3,sticky='ew')
               self.label5.grid(row=row8,column=4,sticky='ew')
               self.label6.grid(row=row8,column=5,sticky='ew')
               self.label7.grid(row=row8,column=6,sticky='ew')
               self.label8.grid(row=row8,column=7,sticky='ew')
               self.label9.grid(row=row8,column=8,sticky='ew')
               self.label10.grid(row=row8,column=9,sticky='ew')
               self.label11.grid(row=row8,column=10,sticky='ew')
               self.label12.grid(row=row8,column=11,sticky='ew')
               row8+=1
               for i in range(0,len(l8)):
                   if l8[i][0]=='None':
                        l8[i][0]=l8[i][0].replace('None','')
                   for j in range(1,len(l8[i])):
                       if l8[i][j]=='None':
                           l8[i][j]=l8[i][j].replace('None','0')
                   self.label=tk.Label(self.t,text="{} {}".format(l8[i][0],l8[i][1]))#Name of Player
                   self.label.grid(row=row8,column=0,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][2]))#shirt_number
                   self.label.grid(row=row8,column=1,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][3]))#start
                   self.label.grid(row=row8,column=2,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][4]))#participation
                   self.label.grid(row=row8,column=3,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][5]))#position
                   self.label.grid(row=row8,column=4,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][6]))#goals
                   self.label.grid(row=row8,column=5,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][7]))#shots
                   self.label.grid(row=row8,column=6,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][8]))#shots on target
                   self.label.grid(row=row8,column=7,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][9]))#assists
                   self.label.grid(row=row8,column=8,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][10]))#saves
                   self.label.grid(row=row8,column=9,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][11]))#passes
                   self.label.grid(row=row8,column=10,sticky='ew')
                   self.label=tk.Label(self.t,text="{}".format(l8[i][12]))#tackles
                   self.label.grid(row=row8,column=11,sticky='ew')
                   row8+=1
               sql8='''select count(p1.player_ID),sum(participation_in_match),sum(goals),sum(shots),sum(shots_on_target),sum(assists),sum(saves),sum(passes),sum(tackles)
                        from Player as p1,participates as p2,belongs as b,Match_ as m
                        where p1.player_ID=p2.player_ID and p2.player_ID=b.player_ID and m.match_ID=p2.match_ID and b.team_ID={} and p2.match_ID={} and b.contract_end_day>m.datetime_
                        '''.format(self.l1[0][4],match_ID)#Total Stats of players for team2
               l9=d.executeSQL(sql8,show=True)
               self.label=tk.Label(self.t,text="Total:{}".format(l9[0][0]))#Total number of players
               self.label.grid(row=row8,column=0,sticky='ew')
               self.label=tk.Label(self.t,text="")
               self.label.grid(row=row8,column=1,sticky='ew')
               self.label=tk.Label(self.t,text="")
               self.label.grid(row=row8,column=2,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][1]))#total number of minutes
               self.label.grid(row=row8,column=3,sticky='ew')
               self.label=tk.Label(self.t,text="")
               self.label.grid(row=row8,column=4,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][2]))#total number of goals
               self.label.grid(row=row8,column=5,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][3]))#total number of shots 
               self.label.grid(row=row8,column=6,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][4]))#total number of shots on target
               self.label.grid(row=row8,column=7,sticky='ew')    
               self.label=tk.Label(self.t,text="{}".format(l9[0][5]))#total number of passes
               self.label.grid(row=row8,column=8,sticky='ew')    
               self.label=tk.Label(self.t,text="{}".format(l9[0][6]))#total number of saves
               self.label.grid(row=row8,column=9,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][7]))#total number of passes
               self.label.grid(row=row8,column=10,sticky='ew')
               self.label=tk.Label(self.t,text="{}".format(l9[0][8]))#total number of tackles
               self.label.grid(row=row8,column=11,sticky='ew')
               #Update button in which we can update the statline of a player that plays in the match
               self.button=tk.Button(a,text="Update",command=Update)
               self.button.grid(row=row8+1,column=12)

            
            s=self.myCombo.get().split(" ")#We get the selection of the user
            self.label=tk.Label(self.f1,text="matchweek {}".format(s[1]),bg='#873ec7',font="Arial 13")#Creation of a label that contains the matchweek
            self.label.grid(row=2,column=0,columnspan=5,sticky='ew')
            sql='''select a1.datetime_,a1.score,a1.name,a2.name,a1.stadium_name,a1.team_ID,a2.team_ID,a1.match_ID
                    from (select m.datetime_,m.score,s.name as stadium_name,t.name,m.Match_ID,e.home,t.team_ID,m.match_ID
                    from Match_ as m,enters as e,Team as t,Stadium as s
                    where m.match_ID=e.match_ID and t.team_ID=e.team_ID and m.stadium_code=s.stadium_ID and matchweek={}
                    ) as a1 left join 
                    (select m.datetime_,m.score,s.name as stadium_name,t.name,m.Match_ID,e.home,t.team_ID,m.match_ID
                    from Match_ as m,enters as e,Team as t,Stadium as s
                    where m.match_ID=e.match_ID and t.team_ID=e.team_ID and m.stadium_code=s.stadium_ID and matchweek={}
                    ) as a2 on a1.match_ID=a2.match_ID
                    where a1.home=1 and a2.home=0
                    order by a1.datetime_'''.format(s[1],s[1])#Here get the matches of a matchweek, the date,the teams that take part in every team, the score and the stadium
            l=d.executeSQL(sql,show=True)
            labels.append(self.label)
            self.label1=tk.Label(self.f1,text="datetime",width=20,bg='#873ec7',font="Arial 12")
            self.label1.grid(row=4,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f1,text="Fixtures",width=40,bg='#873ec7',font="Arial 12")
            self.label2.grid(row=4,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f1,text="Score",width=20,bg='#873ec7',font="Arial 12")
            self.label3.grid(row=4,column=2,sticky='ew')
            labels.append(self.label3)
            self.label4=tk.Label(self.f1,text="Stadium",width=30,bg='#873ec7',font="Arial 12")
            self.label4.grid(row=4,column=3,sticky='ew')
            labels.append(self.label4)
            self.label5=tk.Label(self.f1,text="Match Report",width=30,bg='#873ec7',font="Arial 12")
            self.label5.grid(row=4,column=4,sticky='ew')
            labels.append(self.label5)
            row1=4
            #Creation of the matches. In every match we have the datetime_ of the match, the teams that play in a game of the specific matchweek,the score, the stadium and also we create a button for the Match Report
            for i in range(0,len(l)):
                row1+=1
                self.label=tk.Label(self.f1,text="{}".format(l[i][0]),width=20,bg='#dbbfbf',font="Arial 9")
                self.label.grid(row=row1,column=0,sticky='ew')#datetime_
                labels.append(self.label)
                self.label1=tk.Label(self.f1,text="{} vs {}".format(l[i][2],l[i][3]),width=45,bg='#dbbfbf',font="Arial 9")
                self.label1.grid(row=row1,column=1,sticky='ew')#teams that took part in the match
                labels.append(self.label1)
                self.label2=tk.Label(self.f1,text="{}".format(l[i][1]),width=20,bg='#dbbfbf',font="Arial 9")
                self.label2.grid(row=row1,column=2,sticky='ew')#score
                labels.append(self.label2)
                self.label3=tk.Label(self.f1,text="{}".format(l[i][4]),width=20,bg='#dbbfbf',font="Arial 9")
                self.label3.grid(row=row1,column=3,sticky='ew')#Stadium that this match happened
                labels.append(self.label3)
                datetime_=l[i][0]
                score=l[i][1]
                stadium=l[i][4]
                team1=l[i][5]
                team2=l[i][6]
                match_ID=l[i][7]
                matchweek=s[1]
                self.button=tk.Button(self.f1,text="Match Report",width=10,bg='#dbbfbf',font="Arial 9",command=lambda datetime_=datetime_,stadium=stadium,match_ID=match_ID,matchweek=matchweek:Match_Report(datetime_,stadium,match_ID,matchweek))
                self.button.grid(row=row1,column=4,sticky='ew')
                buttons.append(self.button)
        for widget in self.f1.winfo_children():#Destruction of what was happening already in the Frame
            widget.destroy()
        self.label=tk.Label(self.f1,text="Matches of Premier League",bg='#873ec7',font="Arial 15")
        options=[]
        for i in range(1,39):
            options.append("matchweek "+str(i))#Creation of a Combobox where the user can select the matchweek of his choosing
        self.myCombo=ttk.Combobox(self.f1,value=options)
        self.myCombo.current(37)
        self.myCombo.bind("<<ComboboxSelected>>",selected)
        self.label.grid(row=0,column=0,columnspan=8,sticky='ew')
        self.myCombo.grid(row=1,column=2,ipadx=10,ipady=5)
    #When the button Players is pushed, then in the Frame right of the root, The Players of the selected team of the Championship are being created 
    def buttonPushed3(self):
        buttons=[]#List of buttons
        labels=[]#List of labels
        #Importing the database
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(5):#configuration of the columns of the Frame
            self.f1.columnconfigure(i, weight=1)
        def Player_info(firstname,lastname,team,player_ID,height,date_of_birth):#If the user presses a Player Button, a window opens which shows information and stats of the player in every match that he plays
            b=tk.Toplevel()
            self.b=b
            b.state('zoomed')
            my_canvas= tk.Canvas(self.b)
            my_canvas.pack(side="left",fill="both",expand=1)
            my_scrollbar=ttk.Scrollbar(self.b,orient="vertical",command=my_canvas.yview)
            my_scrollbar.pack(side="right",fill="y")
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>',lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
            a=tk.Frame(my_canvas)
            self.a=a
            my_canvas.create_window((0,0),window=a,anchor='nw')
            for i in range(11):
                self.a.columnconfigure(i, weight=1)
            sql='''select b.team_ID from Belongs as b,Player as p where b.player_ID=p.player_ID and p.player_ID={}'''.format(player_ID)
            l=d.executeSQL(sql,show=True)
            if len(l)==1:#Here we see if a player plays in a team the whole season or if he in two or more teams. In any case, we find the stats of the player in every match that he plays
                sql1='''select *
                from Player as p1,participates as p2,enters as e,Team as t,Match_ as m
                where p1.player_ID=p2.player_ID and p2.match_ID=e.match_ID and e.team_ID=t.team_ID and m.match_ID=e.match_ID and  p1.player_ID={} and t.team_ID!={}'''.format(player_ID,team)
                l1=d.executeSQL(sql1,show=True)
            else:
                sql1='''select *
                        from(select * from Player as p1,participates as p2,enters as e,Team as t,Match_ as m
                        where p1.player_ID=p2.player_ID  and p2.match_ID=e.match_ID and e.team_ID=t.team_ID and m.match_ID=e.match_ID  and  p1.player_ID={}) as a1 
                        left join (select * from Player as p1,participates as p2,enters as e,Team as t,Match_ as m
                        where p1.player_ID=p2.player_ID  and p2.match_ID=e.match_ID and e.team_ID=t.team_ID and m.match_ID=e.match_ID  and  p1.player_ID={} ) as a2
                        on a1.match_ID=a2.match_ID
                        where a1.team_ID={} and a2.team_ID!=a1.team_ID'''.format(player_ID,player_ID,team)
                l1=d.executeSQL(sql1,show=True)
            sql2='''select contract_start_day,contract_end_day
                    from belongs as b,Player as p,Team as t
                    where b.player_ID=p.player_ID and t.team_ID=b.team_ID and p.player_ID={} and t.team_ID={}'''.format(player_ID,team)
            l2=d.executeSQL(sql2,show=True)
            if firstname!="None":
                self.label=tk.Label(a,text="{} {}".format(firstname,lastname),bg='#873ec7',font="Arial 15")
                self.label.grid(row=8,column=0,columnspan=12,sticky='ew')
            else:
                self.label=tk.Label(a,text="{}".format(lastname),bg='#873ec7')
                self.label.grid(row=8)
            self.label1=tk.Label(a,text="Info",bg='#dbbfbf')
            self.label1.grid(row=9,column=0,sticky='ew')
            self.labe2=tk.Label(a,text="height: {}cm".format(height),bg='#dbbfbf')
            self.labe2.grid(row=9,column=1,sticky='ew')
            self.labe3=tk.Label(a,text="date_of_birth: {}".format(date_of_birth),bg='#dbbfbf')
            self.labe3.grid(row=9,column=2,sticky='ew')
            self.labe5=tk.Label(a,text="      contract start date: {}".format(l2[0][0]),bg='#dbbfbf')
            self.labe5.grid(row=9,column=3,sticky='ew')
            self.labe6=tk.Label(a,text="      possible contract end date: {}".format(l2[0][1]),bg='#dbbfbf')
            self.labe6.grid(row=9,column=4,sticky='ew')
            row1=11
            if len(l1)>0:
                self.label=tk.Label(a,text="datetime",bg='#873ec7')
                self.label11=tk.Label(a,text="Opponent",bg='#873ec7')
                self.label1=tk.Label(a,text="Position",bg='#873ec7')
                self.label2=tk.Label(a,text="starter",bg='#873ec7')
                self.label3=tk.Label(a,text="participation",bg='#873ec7')
                self.label4=tk.Label(a,text="goals",bg='#873ec7')
                self.label5=tk.Label(a,text="saves",bg='#873ec7')
                self.label6=tk.Label(a,text="shots",bg='#873ec7')
                self.label7=tk.Label(a,text="shots on target",bg='#873ec7')
                self.label8=tk.Label(a,text="assists",bg='#873ec7')
                self.label9=tk.Label(a,text="tackles",bg='#873ec7')
                self.label10=tk.Label(a,text="passes",bg='#873ec7')
                self.label.grid(row=row1,column=0,sticky='ew')
                self.label11.grid(row=row1,column=1,sticky='ew')
                self.label1.grid(row=row1,column=2,sticky='ew')
                self.label2.grid(row=row1,column=3,sticky='ew')
                self.label3.grid(row=row1,column=4,sticky='ew')
                self.label4.grid(row=row1,column=5,sticky='ew')
                self.label5.grid(row=row1,column=6,sticky='ew')
                self.label6.grid(row=row1,column=7,sticky='ew')
                self.label7.grid(row=row1,column=8,sticky='ew')
                self.label8.grid(row=row1,column=9,sticky='ew')
                self.label9.grid(row=row1,column=10,sticky='ew')
                self.label10.grid(row=row1,column=11,sticky='ew')
                row1=12
            for i in range(0,len(l1)):
                self.label=tk.Label(a,text="{}".format(l1[i][-3]),width=16,bg='#dbbfbf')
                if len(l)==1:
                    self.label11=tk.Label(a,text="{}".format(l1[i][-12]),width=20,bg='#dbbfbf')
                else:
                    self.label11=tk.Label(a,text="{}".format(l1[i][-12]),width=20,bg='#dbbfbf')
                self.label1=tk.Label(a,text="{}".format(l1[i][17]),width=16,bg='#dbbfbf')
                self.label2=tk.Label(a,text="{}".format(l1[i][8]),width=16,bg='#dbbfbf')
                self.label3=tk.Label(a,text="{}".format(l1[i][10]),width=16,bg='#dbbfbf')
                self.label4=tk.Label(a,text="{}".format(l1[i][9]),width=10,bg='#dbbfbf')
                self.label5=tk.Label(a,text="{}".format(l1[i][11]),width=16,bg='#dbbfbf')
                self.label6=tk.Label(a,text="{}".format(l1[i][12]),width=16,bg='#dbbfbf')
                self.label7=tk.Label(a,text="{}".format(l1[i][13]),width=16,bg='#dbbfbf')
                self.label8=tk.Label(a,text="{}".format(l1[i][14]),width=16,bg='#dbbfbf')
                self.label9=tk.Label(a,text="{}".format(l1[i][15]),width=10,bg='#dbbfbf')
                self.label10=tk.Label(a,text="{}".format(l1[i][16]),width=10,bg='#dbbfbf')
                self.label.grid(row=row1,column=0,sticky='ew')
                self.label11.grid(row=row1,column=1,sticky='ew')
                self.label1.grid(row=row1,column=2,sticky='ew')
                self.label2.grid(row=row1,column=3,sticky='ew')
                self.label3.grid(row=row1,column=4,sticky='ew')
                self.label4.grid(row=row1,column=5,sticky='ew')
                self.label5.grid(row=row1,column=6,sticky='ew')
                self.label6.grid(row=row1,column=7,sticky='ew')
                self.label7.grid(row=row1,column=8,sticky='ew')
                self.label8.grid(row=row1,column=9,sticky='ew')
                self.label9.grid(row=row1,column=10,sticky='ew')
                self.label10.grid(row=row1,column=11,sticky='ew')
                row1+=1
        def selected(event):#When the user selects the team of his choosing this function creates a Button with the name of every player of Team on it
            def UpdateButton(team_id):#Pressing the Button Submit, we see if the new information is valid, and if it is we insert the player in the new team or update the players information
                p=[]
                flag=0
                #We get the inserted data
                for i in range(len(self.entries)):
                    if(';' in self.entries[i].get() or 'drop' in self.entries[i].get() or 'delete' in self.entries[i].get()):#No to this invalid characters 
                        flag=1
                    p.append(self.entries[i].get())
                if flag==0:
                    if p[0]=="":
                        sql='''select team_ID,p.player_ID from Player as p,belongs as b where p.player_ID=b.player_ID and p.last_name="{}" and team_ID={}'''.format(p[1],team_id)
                    #we see if the Player is in the selected Team
                    else:
                        sql='''select team_ID,p.player_ID from Player as p,belongs as b where p.player_ID=b.player_ID and p.first_name="{}" and p.last_name="{}" and team_ID={}'''.format(p[0],p[1],team_id)
                    d1=d.executeSQL(sql,show=True)
                    #name of the Team
                    sql1='''select name from Team where team_ID={}'''.format(team_id)
                    d2=d.executeSQL(sql1,show=True)
                    if len(p[3])!=3 and len(p[3])!=4:#If the height of the Player is invalid, then this label is being created
                        self.label=tk.Label(self.s,text="Invalid height.Try again!!")
                        self.label.grid(row=11,column=0,columnspan=2)
                    #If one of the dates are invalid, then this label is being created
                    elif len(p[4])!=10 and len(p[5])!=10 and len(p[6])!=10 and len(p[4])!=4 and len(p[5])!=4 and len(p[6])!=4:
                        self.label=tk.Label(self.s,text="Invalid date.Try again!!")
                        self.label.grid(row=11,column=0,columnspan=2)
                    else:#else we check if the inserted Player is in the selected Team
                        self.s.destroy()
                        if len(d1)==0:#if he is not, then we insert him in the Team
                            #Here we check if the Player is in the database
                            if p[0]=="":
                                sql='''select player_ID from Player where last_name="{}"'''.format(p[1])
                            else:
                                sql='''select player_ID from Player where first_name="{}" and last_name="{}"'''.format(p[0],p[1])
                            d3=d.executeSQL(sql,show=True)
                            if len(d3)==0:#If we he is not , we insert him into the database(Player relation)
                                if p[0]=="":
                                    sql='''insert into Player(shirt_number,height,date_of_birth,first_name,last_name)
                                values({},{},"{}",NULL,"{}") '''.format(p[2],p[3],p[4],p[1])
                                else:
                                    sql='''insert into Player(shirt_number,height,date_of_birth,first_name,last_name)
                                    values({},{},"{}","{}","{}") '''.format(p[2],p[3],p[4],p[0],p[1])
                                if d.executeSQL(sql,show=True)==False:#if the inputs are invalid,this label is being created
                                    print("Wrong Input.Try again!!!") 
                                if p[0]=="":
                                    sql='''select player_ID from Player where last_name="{}"'''.format(p[1])
                                else:
                                    sql='''select player_ID from Player where first_name="{}" and last_name="{}"'''.format(p[0],p[1])
                                d3=d.executeSQL(sql,show=True)
                                player_id=d3[0][0]#player_ID of the player
                            else:player_id=d3[0][0]#player_ID of the player
                            #Then we insert the Player into the belongs relation
                            sql='''insert into belongs(player_ID,team_ID,contract_start_day,contract_end_day,salary)
                            values({},{},"{}","{}",{}) '''.format(player_id,team_id,p[5],p[6],p[7])
                            if d.executeSQL(sql,show=True)==False:#if the inputs are invalid,this label is being created
                                print("Wrong Input.Try again!!!")
                                
                        else:#If the Player is in the Team, We update his information in the Player and belongs relation
                            sql=''' update Player set shirt_number={},height={},date_of_birth="{}" where player_ID={} '''.format(p[2],p[3],p[4],d1[0][1])
                            if d.executeSQL(sql,show=True)==False:#if the inputs are invalid,this label is being created
                                print("Wrong Input.Try again!!!")
                            sql=''' update belongs set team_ID={},contract_start_day="{}",contract_end_day="{}",salary={} where player_ID={} and team_ID={}'''.format(team_id,p[5],p[6],p[7],d1[0][1],team_id)
                            if d.executeSQL(sql,show=True)==False:#if the inputs are invalid,this label is being created
                                print("Wrong Input.Try again!!!")
                else:
                    self.label0=tk.Label(self.s,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
                    self.label0.grid(row=0,column=0,columnspan=12,sticky='ew',ipady=5)
            def Update_Players(team_id):#If the Update Button is being pushed,a window is being created in which we can import  new information of the player that we want to update/insert
                self.s=tk.Toplevel()
                self.label10=tk.Label(self.s,text="Update Players")
                self.label10.grid(row=0,column=0,columnspan=2)
                self.label=tk.Label(self.s,text="Player firstname")
                self.label1=tk.Label(self.s,text="Player lastname")
                self.label2=tk.Label(self.s,text="shirt number")
                self.label3=tk.Label(self.s,text="height")
                self.label4=tk.Label(self.s,text="date of birth")
                self.label5=tk.Label(self.s,text="Contract start date:")
                self.label6=tk.Label(self.s,text="Contract end date:")
                self.label7=tk.Label(self.s,text="Salary:")
                self.labels=[self.label,self.label1,self.label2,self.label3,self.label4,self.label5,self.label6,self.label7]
                self.entry=tk.Entry(self.s,borderwidth=2)
                self.entry1=tk.Entry(self.s,borderwidth=2)
                self.entry2=tk.Entry(self.s,borderwidth=2)
                self.entry3=tk.Entry(self.s,borderwidth=2)
                self.entry4=tk.Entry(self.s,borderwidth=2)
                self.entry5=tk.Entry(self.s,borderwidth=2)
                self.entry6=tk.Entry(self.s,borderwidth=2)
                self.entry7=tk.Entry(self.s,borderwidth=2)
                self.entries=[self.entry,self.entry1,self.entry2,self.entry3,self.entry4,self.entry5,self.entry6,self.entry7]
                for i in range(len(self.labels)):
                    self.labels[i].grid(row=i+1,column=0)
                    self.entries[i].grid(row=i+1,column=1)
                #Pushing the Button Submit we process the given information
                self.Button1=tk.Button(self.s,text="Submit",command= lambda team_id=team_id : UpdateButton(team_id))
                self.Button1.grid(row=10,column=1)

            def startpage():#Is the user pushes the Return Button , the user can see the previous players of the team
                for x in buttons:#Destruction of previous labels and buttons
                    if len(buttons)==0:
                        break
                    else:
                        x.destroy()
                for x in labels:
                    if len(labels)==0:
                        break
                    else:
                        x.destroy()
                self.label=tk.Label(self.f1,text="Club: {}".format(self.myCombo.get()),bg='#873ec7',width=40)
                self.label.grid(row=10,column=2)
                labels.append(self.label)
                row1=11
                sql='''select p.first_name,p.last_name,t.team_ID,p.player_ID,p.height,p.date_of_birth
                        from Player as p,belongs as b,Team as t
                        where p.player_ID=b.player_ID and t.team_ID=b.team_ID and b.team_ID={}
                        order by p.last_name;'''.format(options.index(self.myCombo.get()))
                l=d.executeSQL(sql,show=True)
                i=0
                while i<20:
                    firstname=l[i][0]
                    lastname=l[i][1]
                    team=l[i][2]
                    height=l[i][4]
                    date_of_birth=l[i][5]
                    player_ID=l[i][3]
                    if l[i][0]!="None":
                        self.button=tk.Button(self.f1,text="{} {}".format(l[i][0],l[i][1]),bg='#dbbfbf',width=40,command= lambda firstname=firstname,lastname=lastname,team=team,player_ID=player_ID,height=height,date_of_birth=date_of_birth : Player_info(firstname,lastname,team,player_ID,height,date_of_birth))
                        self.button.grid(row=row1,column=2)
                        buttons.append(self.button)
                    else:
                        self.button=tk.Button(self.f1,text="{}".format(l[i][1]),bg='#dbbfbf',width=40,command= lambda firstname=firstname,lastname=lastname,team=team,player_ID=player_ID,height=height,date_of_birth=date_of_birth : Player_info(firstname,lastname,team,player_ID,height,date_of_birth))
                        self.button.grid(row=row1,column=2)
                        buttons.append(self.button)
                    row1+=1
                    i+=1
                if len(l)>20:
                    self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                    self.button1.grid(row=row1,column=0)
                    buttons.append(self.button1)
                
            def nextpage():#If the user presses the Next Page button, the rest players of the Team are being shown
                 for x in buttons:#Destruction of previous labels and buttons
                     if len(buttons)==0:
                         break
                     else:
                         x.destroy()
                 for x in labels:
                     if len(labels)==0:
                         break
                     else:
                         x.destroy()
                 self.label=tk.Label(self.f1,text="Club: {}".format(self.myCombo.get()),bg='#873ec7',width=40)
                 self.label.grid(row=10,column=2)
                 labels.append(self.label)
                 row1=11
                 sql='''select p.first_name,p.last_name,t.team_ID,p.player_ID,p.height,p.date_of_birth
                        from Player as p,belongs as b,Team as t
                        where p.player_ID=b.player_ID and t.team_ID=b.team_ID and b.team_ID={}
                        order by p.last_name;'''.format(options.index(self.myCombo.get()))
                 l=d.executeSQL(sql,show=True)
                 i=20
                 while i<len(l):
                    firstname=l[i][0]
                    lastname=l[i][1]
                    team=l[i][2]
                    height=l[i][4]
                    date_of_birth=l[i][5]
                    player_ID=l[i][3]
                    if l[i][0]!="None":
                        self.button=tk.Button(self.f1,text="{} {}".format(l[i][0],l[i][1]),bg='#dbbfbf',width=40,command= lambda firstname=firstname,lastname=lastname,team=team,player_ID=player_ID,height=height,date_of_birth=date_of_birth: Player_info(firstname,lastname,team,player_ID,height,date_of_birth))
                        self.button.grid(row=row1,column=2)
                        buttons.append(self.button)
                    else:
                        self.button=tk.Button(self.f1,text="{}".format(l[i][1]),bg='#dbbfbf',width=40,command= lambda firstname=firstname,lastname=lastname,team=team,player_ID=player_ID,height=height,date_of_birth=date_of_birth : Player_info(firstname,lastname,team,player_ID,height,date_of_birth))
                        self.button.grid(row=row1,column=2)
                        buttons.append(self.button)
                    row1+=1
                    i+=1
                 if len(l)-20>20:#Again if the players are more than 40 we create button for rest players
                    self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                    self.button1.grid()
                    buttons.append(self.button1)
                 else:#Else we create a button in order to see the previous players
                    self.button2=tk.Button(self.f1,text="Return",command=startpage)
                    self.button2.grid()
                    buttons.append(self.button2)
            for x in buttons:#Destruction of previous labels and buttons
                if len(buttons)==0:
                    break
                else:
                    x.destroy()
            for x in labels:
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            self.label=tk.Label(self.f1,text="Club: {}".format(self.myCombo.get()),bg='#873ec7',width=40)
            self.label.grid(row=10,column=2)
            labels.append(self.label)
            row1=11
            sql='''select p.first_name,p.last_name,t.team_ID,p.player_ID,p.height,p.date_of_birth
                        from Player as p,belongs as b,Team as t
                        where p.player_ID=b.player_ID and t.team_ID=b.team_ID and b.team_ID={}
                        order by p.last_name;'''.format(options.index(self.myCombo.get()))#Players of the team that the user selectes
            l=d.executeSQL(sql,show=True)
            i=0
            while i<20:#We limit the  creation of button to 20
                    firstname=l[i][0]
                    lastname=l[i][1]
                    team=l[i][2]
                    height=l[i][4]
                    date_of_birth=l[i][5]
                    player_ID=l[i][3]
                    if l[i][0]!="None":
                        self.button=tk.Button(self.f1,text="{} {}".format(l[i][0],l[i][1]),bg='#dbbfbf',width=40,command= lambda firstname=firstname,lastname=lastname,team=team,player_ID=player_ID,height=height,date_of_birth=date_of_birth: Player_info(firstname,lastname,team,player_ID,height,date_of_birth))
                        self.button.grid(row=row1,column=2)
                        buttons.append(self.button)
                    else:
                        self.button=tk.Button(self.f1,text="{}".format(l[i][1]),bg='#dbbfbf',width=40,command= lambda firstname=firstname,lastname=lastname,team=team,player_ID=player_ID,height=height,date_of_birth=date_of_birth : Player_info(firstname,lastname,team,player_ID,height,date_of_birth))
                        self.button.grid(row=row1,column=2)
                        buttons.append(self.button)
                    row1+=1
                    i+=1
            if len(l)>20:#If a team has more than 20 players we create a button that shows the rest of the players
                    self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                    self.button1.grid()
                    buttons.append(self.button1)
            #Button in which we can Insert Players to a Team or Update the information of a Player         
            self.button=tk.Button(self.f1,text="Update/Insert",command= lambda team_id= options.index(self.myCombo.get()): Update_Players(team_id))
            self.button.grid(row=row1,column=5)        
        for widget in self.f1.winfo_children():#Destruction of what was happening in the Frame
            widget.destroy()
        self.label=tk.Label(self.f1,text="Players",font="Arial 15",bg='#873ec7')
        options=[]
        options=['Manchester City','Manchester United','Liverpool','Chelsea','Leicester City','West Ham United','Tottenham Hotspur','Arsenal','Leeds United','Everton','Aston Villa','Newcastle United','Wolverhampton Wonderers','Crystal Palace','Southampton','Brighton & Hove Albion','Burnley','Fulham','West Bromwich Albion','Sheffield United']
        self.myCombo=ttk.Combobox(self.f1,value=options,width=30)#Combobox in which the user can select the team of his choosing
        self.myCombo.current(0)
        self.myCombo.bind("<<ComboboxSelected>>",selected)
        self.label.grid(row=1,column=0,columnspan=12,sticky='ew')
        self.myCombo.grid(row=2,column=2,ipadx=10,ipady=5)  
    #If the Teams Button is selected, in the frame right to the root, Images and buttons of the Teams are being created and and the user can select Team of his choosing and see Information for that Team
    def buttonPushed4(self):
        buttons=[]
        labels=[]
        #import the database
        dbfile = "project.db"
        d = DataModel(dbfile)
        def UpdateButton(team_id):
            p=[]
            flag=0
            #We get the inserted data
            for i in range(len(self.entries6)):
                if (';' in self.entries6[i].get() or 'drop' in self.entries6[i].get() or 'delete' in self.entries6[i].get()):#no to his invalid characters
                    flag=1
                p.append(self.entries6[i].get())
            if flag==0:
                if len(p[1])!=4:#IF date is invalid,then this label is being created
                    self.label=tk.Label(self.s,text="Invalid date.Try again!!")
                    self.label.grid(row=11,column=0,columnspan=2)
                else:#We update the data of the selected Team
                    self.s.destroy()
                    sql='''update Team set name="{}",founded="{}" where team_ID={}'''.format(p[0],p[1],team_id)
                    q=d.executeSQL(sql,show=True)
            else:
                self.label0=tk.Label(self.s,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
                self.label0.grid(row=0,column=0,columnspan=12,sticky='ew',ipady=5)
        def Update_Team(team_name):#Here pressing the Button Update, we can insert the new data of the Team
            self.s=tk.Toplevel()
            self.label10=tk.Label(self.s,text="Update Team: {}".format(team_name))
            self.label10.grid(row=0,column=0,columnspan=2)
            self.label=tk.Label(self.s,text="Team name:")
            self.label1=tk.Label(self.s,text="Date of foundation:")
            self.labels6=[self.label,self.label1]
            self.entry=tk.Entry(self.s,borderwidth=2)
            self.entry1=tk.Entry(self.s,borderwidth=2)
            self.entries6=[self.entry,self.entry1]
            for i in range(len(self.labels6)):
                self.labels6[i].grid(row=i+1,column=0)
                self.entries6[i].grid(row=i+1,column=1)
                #Pushing the Button Submit we process the given information
            sql='''select team_id from Team where name="{}"'''.format(team_name)
            l=d.executeSQL(sql,show=True)
            self.Button1=tk.Button(self.s,text="Submit",command= lambda team_id=l[0][0] :UpdateButton(team_id))
            self.Button1.grid(row=6,column=1)
        def Team_info(team_name,x):#If the user presses the button, a new window pops in which we can Information of the Team
            a=tk.Toplevel(bg='#dbbfbf')
            self.a=a
            sql1='''select * from Team where name="{}"'''.format(team_name)
            l1=d.executeSQL(sql1,show=True)
            self.label=tk.Label(a,text="Team name: {}".format(team_name),bg='#dbbfbf',font="Arial 14")
            self.label.grid(row=0)
            self.label4=tk.Label(a,image=self.image[x])         
            self.label4.grid(row=1)
            self.label1=tk.Label(a,text="Founded: {}".format(l1[0][2]),bg='#dbbfbf',font="Arial 12")
            self.label1.grid(row=2,column=0)
            self.label2=tk.Label(a,text="Total Record in season: {}-{}-{} (Position:{})".format(l1[0][3],l1[0][4],l1[0][5],int(l1[0][0])+1),bg='#dbbfbf',font="Arial 12")
            self.label2.grid(row=3,column=0)                     
            self.label3=tk.Label(a,text="Total points: {}".format(l1[0][6]),bg='#dbbfbf',font="Arial 12")
            self.label3.grid(row=4,column=0)
            sql2='''select s.name from Team as t,Stadium as s where t.stadium_ID=s.stadium_ID and t.name="{}"'''.format(team_name)
            l2=d.executeSQL(sql2,show=True)
            self.label4=tk.Label(a,text="Stadium: {}".format(l2[0][0]),bg='#dbbfbf',font="Arial 12")
            self.label4.grid(row=5,column=0)
            self.button=tk.Button(self.a,text="Update",command=lambda team_name=team_name: Update_Team(team_name))#Pressing the button Update function Update_Team runs in which we can update some of the data of the Team
            self.button.grid(row=6,column=3)
        def selected(event):
            for x in buttons:
                if len(buttons)==0:
                    break
                else:
                    x.destroy()
            for x in labels:
                if len(labels)==0:
                    break
                else:
                    x.destroy()
        for widget in self.f1.winfo_children():#Destruction of what was happening previously in the Frame
            widget.destroy()
        options=['Manchester City','Manchester Utd','Liverpool','Chelsea','Leicester City','West Ham','Tottenham','Arsenal','Leeds United','Everton','Aston Villa','Newcastle Utd','Wolves','Crystal Palace','Southampton','Brighton','Burnley','Fulham','West Brom','Sheffield Utd']
        row1=10
        self.image=[]
        #Import the images of Teams
        for i in range(0,20):
            self.image.append(tk.PhotoImage(file=r'images\{}.png'.format(options[i])))
        sql='''Select name,team_ID from Team;'''
        l=d.executeSQL(sql,show=True)
        #We put the images and the Buttons of the Team in the right place in the Frame so that we can have the 20 teams in 4 rows
        for x in range(0,20):
            self.label=tk.Label(self.f1,image=self.image[x])         
            self.label.grid(row=row1+int(x/5),column=x%5)
            team_name=l[x][0]
            self.button=tk.Button(self.f1,text="{}".format(l[x][0]),bg='#dbbfbf',width=25,command=lambda team_name=team_name,x=x: Team_info(team_name,x))
            self.button.grid(row=row1+int(x/5)+1,column=x%5)
            buttons.append(self.button)
            if (x%5)==4:
                row1+=1   
    #If the Referees Button is selected, in the frame right to the root, we can see the Referees of the Championship and their and information about them
    def buttonPushed5(self):
        buttons=[]
        labels=[]
        #importing the database
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(5):#Configuration of the columns of the Frame
            self.f1.columnconfigure(i, weight=1)
        self.b=0#variable which determines whether we are going to have a Next Button or a Return Button or both of them
        def startpage():#If the Return Button is being pushed, it shows the previous 20 referees.We have a Next Page Button and also if we are not on the 1st page , we have a Return Button too
                for x in buttons:
                    if len(buttons)==0:
                        break
                    else:
                        x.destroy()
                for x in labels:
                    if len(labels)==0:
                        break
                    else:
                        x.destroy()
                row1=12
                i=0
                self.b-=1
                lnew=l[20*self.b:]
                while i<20:
                    self.label=tk.Label(self.f1,text="{} {}".format(lnew[i][1],lnew[i][0]),bg='#dbbfbf',width=30,font="Arial 10")
                    self.label.grid(row=row1,column=0,sticky='ew')
                    labels.append(self.label)
                    self.label1=tk.Label(self.f1,text="{}".format(lnew[i][3]),bg='#dbbfbf',width=20,font="Arial 10")
                    self.label1.grid(row=row1,column=1,sticky='ew')
                    labels.append(self.label1)
                    self.label2=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                    self.label2.grid(row=row1,column=2,sticky='ew')
                    labels.append(self.label2)
                    self.label3=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                    self.label3.grid(row=row1,column=3,sticky='ew')
                    labels.append(self.label3)
                    self.label4=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                    self.label4.grid(row=row1,column=4,sticky='ew')
                    labels.append(self.label4)
                    for x in range(0,len(l1)):
                        if l1[x][0]==lnew[i][0]:
                            self.label2=tk.Label(self.f1,text="{}".format(l1[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                            self.label2.grid(row=row1,column=2,sticky='ew')
                            labels.append(self.label2)
                            break
                    for x in range(0,len(l2)):
                        if l2[x][0]==lnew[i][0]:
                            self.label3=tk.Label(self.f1,text="{}".format(l2[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                            self.label3.grid(row=row1,column=3,sticky='ew')
                            labels.append(self.label3)
                            break
                    for x in range(0,len(l3)):
                        if l3[x][0]==lnew[i][0]:
                            self.label4=tk.Label(self.f1,text="{}".format(l3[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                            self.label4.grid(row=row1,column=4,sticky='ew')
                            labels.append(self.label4)
                            break
                    row1+=1
                    i+=1
                if len(lnew)>20 and len(lnew)!=len(l):
                    self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                    self.button1.grid()
                    buttons.append(self.button1)
                    self.button2=tk.Button(self.f1,text="Return",command=startpage)
                    self.button2.grid()
                    buttons.append(self.button2)
                elif len(lnew)<20:
                    self.button2=tk.Button(self.f1,text="Return",command=startpage)
                    self.button2.grid()
                    buttons.append(self.button2)
                else:
                    self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                    self.button1.grid()
                    buttons.append(self.button1)
                    
        def nextpage():#if the Next Page Button is being pushed, the next 20 referees are being shown and we create a Return Button, and also if there are more than 20*i referees , where i=1,2,3.... we have a Next Button too
            for x in buttons:
                if len(buttons)==0:
                    break
                else:
                    x.destroy()
            for x in labels:
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            row1=12
            i=0
            self.b+=1
            lnew=l[20*self.b:]
            while (i<20 and i<len(lnew)):
                self.label=tk.Label(self.f1,text="{} {}".format(lnew[i][1],lnew[i][0]),bg='#dbbfbf',width=30,font="Arial 10")
                self.label.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label)
                self.label1=tk.Label(self.f1,text="{}".format(lnew[i][3]),bg='#dbbfbf',width=20,font="Arial 10")
                self.label1.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label1)
                self.label2=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                self.label2.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label2)
                self.label3=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                self.label3.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label3)
                self.label4=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                self.label4.grid(row=row1,column=4,sticky='ew')
                labels.append(self.label4)
                for x in range(0,len(l1)):
                    if l1[x][0]==lnew[i][0]:
                        self.label2=tk.Label(self.f1,text="{}".format(l1[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                        self.label2.grid(row=row1,column=2,sticky='ew')
                        labels.append(self.label2)
                        break
                for x in range(0,len(l2)):
                    if l2[x][0]==lnew[i][0]:
                        self.label3=tk.Label(self.f1,text="{}".format(l2[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                        self.label3.grid(row=row1,column=3,sticky='ew')
                        labels.append(self.label3)
                        break
                for x in range(0,len(l3)):
                    if l3[x][0]==lnew[i][0]:
                        self.label4=tk.Label(self.f1,text="{}".format(l3[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                        self.label4.grid(row=row1,column=4,sticky='ew')
                        labels.append(self.label4)
                        break
                row1+=1
                i+=1
            if len(lnew)>20:
                self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                self.button1.grid()
                buttons.append(self.button1)
                self.button2=tk.Button(self.f1,text="Return",command=startpage)
                self.button2.grid()
                buttons.append(self.button2)
            elif len(lnew)<20:
                self.button2=tk.Button(self.f1,text="Return",command=startpage)
                self.button2.grid()
                buttons.append(self.button2)
                
        for widget in self.f1.winfo_children():#Destruction of what was happening previously in the frame
            widget.destroy()
        #Creation of Labels for the referees in which we can see their names, the number of appearances, and the number of Yellow,Second Yellow and Red Cards that they have given in the Championship(only for the referees that had at least at once status = Referee)
        self.label=tk.Label(self.f1,text="Referees",font="Arial 20",bg='#873ec7')
        self.label1=tk.Label(self.f1,text="Name",bg='#873ec7',font="Arial 13")
        self.label2=tk.Label(self.f1,text="Appearances",bg='#873ec7',font="Arial 13")
        self.label3=tk.Label(self.f1,text="Yellow Cards",bg='#873ec7',font="Arial 13")
        self.label4=tk.Label(self.f1,text="Second Yellow Cards",bg='#873ec7',font="Arial 13")
        self.label5=tk.Label(self.f1,text="Red Cards",bg='#873ec7',font="Arial 13")
        self.label.grid(row=1,column=0,columnspan=12,sticky='ew')
        self.label1.grid(row=10,column=0,sticky='ew')
        self.label2.grid(row=10,column=1,sticky='ew')
        self.label3.grid(row=10,column=2,sticky='ew')
        self.label4.grid(row=10,column=3,sticky='ew')
        self.label5.grid(row=10,column=4,sticky='ew')
        row1=12
        sql='''select r.last_name,r.first_name,r.referee_ID,count(*) as appearances
                from Referee as r, inspects as i 
                where r.referee_ID=i.referee_ID
                group by r.referee_ID
                order by r.referee_ID;'''
        l=d.executeSQL(sql,show=True)
        sql1='''select r.last_name,r.first_name,r.referee_ID,count(*) as yellow_cards
                from Referee as r, attributes_violation as a,inspects as i 
                where r.referee_ID=i.referee_ID and i.match_ID=a.match_ID and (a.card="Yellow") and i.status="Referee"
                group by r.referee_ID
                order by r.referee_ID'''
        l1=d.executeSQL(sql1,show=True)
        sql2='''select r.last_name,r.first_name,r.referee_ID,count(*) as second_yellow_cards
                from Referee as r, attributes_violation as a,inspects as i 
                where r.referee_ID=i.referee_ID and i.match_ID=a.match_ID and a.card="Second Yellow" and i.status="Referee"
                group by r.referee_ID
                order by r.referee_ID'''
        l2=d.executeSQL(sql2,show=True)
        sql3='''select r.last_name,r.first_name,r.referee_ID,count(*) as red_cards
                from Referee as r, attributes_violation as a,inspects as i 
                where r.referee_ID=i.referee_ID and i.match_ID=a.match_ID and a.card="Red" and i.status="Referee"
                group by r.referee_ID
                order by r.referee_ID'''
        l3=d.executeSQL(sql3,show=True)
        i=0
        while i<20:#We limit the creation of the labels to 20 referees and then we create a Next Page Button
                self.label=tk.Label(self.f1,text="{} {}".format(l[i][1],l[i][0]),bg='#dbbfbf',width=30,font="Arial 10")
                self.label.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][3]),bg='#dbbfbf',width=20,font="Arial 10")
                self.label1.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label1)
                self.label2=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                self.label2.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label2)
                self.label3=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                self.label3.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label3)
                self.label4=tk.Label(self.f1,text="-",bg='#dbbfbf',width=20,font="Arial 10")
                self.label4.grid(row=row1,column=4,sticky='ew')
                labels.append(self.label4)
                for x in range(0,len(l1)):
                    if l1[x][0]==l[i][0]:
                        self.label2=tk.Label(self.f1,text="{}".format(l1[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                        self.label2.grid(row=row1,column=2,sticky='ew')
                        labels.append(self.label2)
                        break
                for x in range(0,len(l2)):
                    if l2[x][0]==l[i][0]:
                        self.label3=tk.Label(self.f1,text="{}".format(l2[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                        self.label3.grid(row=row1,column=3,sticky='ew')
                        labels.append(self.label3)
                        break
                for x in range(0,len(l3)):
                    if l3[x][0]==l[i][0]:
                        self.label4=tk.Label(self.f1,text="{}".format(l3[x][3]),bg='#dbbfbf',width=20,font="Arial 10")
                        self.label4.grid(row=row1,column=4,sticky='ew')
                        labels.append(self.label4)
                        break
                        
                row1+=1
                i+=1
        if len(l)>20:
                self.button1=tk.Button(self.f1,text="Next Page",command=nextpage)
                self.button1.grid()
                buttons.append(self.button1)
    #If the Coaches Button is selected, in the frame right to the root, Coaches of every team and information for their contract informations are being shown
    def buttonPushed6(self):
        buttons=[]
        labels=[]
        #Importing the database
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(5):#Configuration of the columns in the Frame right to the root window
            self.f1.columnconfigure(i, weight=1)
        def UpdateButton():#pressing the button UpdateButton, We process the data
            p=[]
            flag=0
            #We get the inserted data
            for i in range(len(self.entries4)):
                if(';' in self.entries4[i].get() or 'drop' in self.entries4[i].get() or 'delete' in self.entries4[i].get()):#NO invalid characters
                    flag=1
                p.append(self.entries4[i].get())
            if flag==0:
                sql='''select team_ID from Team where name="{}"'''.format(p[2])
                l1=d.executeSQL(sql,show=True)
                sql1='''select coach_ID from Coach where first_name="{}" and last_name="{}"'''.format(p[0],p[1])
                l2=d.executeSQL(sql1,show=True)
                if len(l1)==0:#If the name of the Team doesnt exist in the database, then this label is being created
                    self.label=tk.Label(self.s,text="Invalid Team name.Try again!!")
                    self.label.grid(row=11,column=0,columnspan=2)
                elif len(p[3])!=10 and len(p[4])!=10 and len(p[4])!=4 and len(p[3])!=4:#If the dates of contract is invalid, then this label is being created
                        self.label=tk.Label(self.s,text="Invalid date.Try again!!")
                        self.label.grid(row=11,column=0,columnspan=2)
                elif len(l2)!=0:#If the coach exists in the database, then we update his data
                    self.s.destroy()
                    sql='''update Coach set team_code={},contract_start_date="{}",contract_end_date="{}" where coach_ID={}'''.format(l1[0][0],p[3],p[4],l2[0][0])
                    d.executeSQL(sql,show=True)
                else:#If the coach doesnt exist in the database, then we insert them in the database
                    self.s.destroy()
                    sql='''insert into Coach(first_name,last_name,team_code,contract_start_date,contract_end_date) values("{}","{}",{},"{}","{}")'''.format(p[0],p[1],l1[0][0],p[3],p[4])
                    d.executeSQL(sql,show=True)
            else:
                self.label0=tk.Label(self.s,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
                self.label0.grid(row=0,column=0,columnspan=12,sticky='ew',ipady=5)
        def Update_Manager():#pressing the Update/Insert Button, a window pops in which we can insert data for the manager
            self.s=tk.Toplevel()
            self.label10=tk.Label(self.s,text="Update Manager")
            self.label10.grid(row=0,column=0,columnspan=2)
            self.label=tk.Label(self.s,text="Manager firstname")
            self.label1=tk.Label(self.s,text="Manager lastname")
            self.label2=tk.Label(self.s,text="Team")
            self.label3=tk.Label(self.s,text="Contract start date:")
            self.label4=tk.Label(self.s,text="Contract end date:")
            self.labels4=[self.label,self.label1,self.label2,self.label3,self.label4]
            self.entry=tk.Entry(self.s,borderwidth=2)
            self.entry1=tk.Entry(self.s,borderwidth=2)
            self.entry2=tk.Entry(self.s,borderwidth=2)
            self.entry3=tk.Entry(self.s,borderwidth=2)
            self.entry4=tk.Entry(self.s,borderwidth=2)
            self.entries4=[self.entry,self.entry1,self.entry2,self.entry3,self.entry4]
            for i in range(len(self.labels4)):
                self.labels4[i].grid(row=i+1,column=0)
                self.entries4[i].grid(row=i+1,column=1)
                #Pushing the Button Submit we process the given information
            self.Button1=tk.Button(self.s,text="Submit",command= UpdateButton)#Pressing the Button Submi, the data are being processed
            self.Button1.grid(row=6,column=1)
        def StartWindow(self):#Creation of the first page
            #Here we create labels of the coaches that are currently in a team and they are not fired or their contract hasn't expired (for the season 2020-2021)
            for widget in self.f1.winfo_children():
                widget.destroy()       
            self.label=tk.Label(self.f1,text="Managers",font="Arial 20",bg='#873ec7')
            self.label1=tk.Label(self.f1,text="Name",bg='#873ec7',font="Arial 15")
            self.label2=tk.Label(self.f1,text="Team",bg='#873ec7',font="Arial 15")
            self.label3=tk.Label(self.f1,text="Start of Contract",bg='#873ec7',font="Arial 15")
            self.label4=tk.Label(self.f1,text="Possible end of Contract",bg='#873ec7',font="Arial 15")
            self.label.grid(row=1,column=0,columnspan=12,sticky='ew')
            self.label1.grid(row=9,column=0,sticky='ew')
            self.label2.grid(row=9,column=1,sticky='ew')
            self.label3.grid(row=9,column=2,sticky='ew')
            self.label4.grid(row=9,column=3,sticky='ew')
            sql='''select c.first_name,c.last_name,t.name,c.contract_start_date,c.contract_end_date
                    from Coach as c, Team as t
                    where c.team_code=t.team_ID 
                    EXCEPT
                    select c.first_name,c.last_name,t.name,c.contract_start_date,c.contract_end_date
                    from Coach as c, Team as t
                    where c.team_code=t.team_ID and (c.contract_end_date is not NULL and c.contract_end_date<"2021-05-23")
                    order by c.contract_end_date;'''
            l=d.executeSQL(sql,show=True)
            row1=11
            for i in range(len(l)):
                self.label=tk.Label(self.f1,text="{} {}".format(l[i][0],l[i][1]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][2]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label1.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label1)
                self.label2=tk.Label(self.f1,text="{}".format(l[i][3]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label2.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label2)
                self.label3=tk.Label(self.f1,text="{}".format(l[i][4]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label3.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label3)
                row1+=1
            self.button1=tk.Button(self.f1,text="Released Managers",command=nextpage)#And creation of a Released Managers button
            self.button1.grid()
            self.button3=tk.Button(self.f1,text="Update/Insert",command=Update_Manager)#Pressing the button Update/Insert, the function Update_Manager runs where we can insert new data for the Manager
            self.button3.grid(row=row1,column=3)
            buttons.append(self.button1)
        def Return():#If Return Button is being pushed, then we get back to the starting page
            for x in buttons:#Destruction of previous labels and buttons
                if len(buttons)==0:
                    break
                else:
                    x.destroy()
            for x in labels:
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            StartWindow(self)
        def nextpage():#if the Button Released Managers is being pushed, the second page is being created
            #Here we create labels of the coaches that have been released in the middle of the Season
            for x in buttons:
                if len(buttons)==0:#Destruction of previous labels and buttons
                    break
                else:
                    x.destroy()
            for x in labels:
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            row1=11
            sql='''select c.first_name,c.last_name,t.name,c.contract_start_date,c.contract_end_date
                    from Coach as c, Team as t
                    where c.team_code=t.team_ID and (c.contract_end_date is not NULL and c.contract_end_date<"2021-05-23")
                    order by c.contract_end_date'''
            l=d.executeSQL(sql,show=True)
            for i in range(len(l)):
                self.label=tk.Label(self.f1,text="{} {}".format(l[i][0],l[i][1]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label)
                self.label1=tk.Label(self.f1,text="{}".format(l[i][2]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label1.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label1)
                self.label2=tk.Label(self.f1,text="{}".format(l[i][3]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label2.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label2)
                self.label3=tk.Label(self.f1,text="{}".format(l[i][4]),bg='#dbbfbf',width=30,font="Arial 13")
                self.label3.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label3)
                row1+=1
            self.button2=tk.Button(self.f1,text="Return",command=Return)#And creation of return button
            self.button2.grid()
            buttons.append(self.button2)

        StartWindow(self)
    #If the Teams Stadiums is selected, in the frame right to the root, Stadiums of every team and informations for them are being shown
    def buttonPushed7(self):
        #Importing the database
        dbfile = "project.db"
        d = DataModel(dbfile)
        def UpdateButton():#If the button is being pushed, the data of the Stadium are being proccesed
            p=[]
            flag=0
            #We get the inserted data
            for i in range(len(self.entries5)):
                if (';' in self.entries5[i].get() or 'drop' in self.entries5[i].get() or 'delete' in self.entries5[i].get()):#No invalid caharcters
                    flag=1
                p.append(self.entries5[i].get())
            if flag==0:
                sql='''select team_ID from Team where name="{}"'''.format(p[4])
                l1=d.executeSQL(sql,show=True)
                sql1='''select stadium_ID from Stadium where name="{}"'''.format(p[0])
                l2=d.executeSQL(sql1,show=True)
                if len(l1)==0:#If the name of the team doesnt not exist in the datebase, this label is being created
                    self.label=tk.Label(self.s,text="Invalid Team name.Try again!!")
                    self.label.grid(row=11,column=0,columnspan=2)
                elif len(p[1])!=4:#If the date is invalid, this label is being created
                        self.label=tk.Label(self.s,text="Invalid date.Try again!!")
                        self.label.grid(row=11,column=0,columnspan=2)
                elif len(l2)!=0:#If the Stadium exists in the database, then we update the data of the Stadium and the Team
                    self.s.destroy()
                    sql='''update Stadium set name="{}",date_built="{}",place="{}",capacitance={} where stadium_ID={}'''.format(p[0],p[1],p[2],p[3],l2[0][0])
                    d.executeSQL(sql,show=True)
                    sql='''update Team set stadium_ID={} where name="{}"'''.format(l2[0][0],p[4])
                    d.executeSQL(sql,show=True)
                else:#If the Stadium doesnt exist in the database, then we insert the new Stadium in the database, and update the data of the Team
                    self.s.destroy()
                    sql='''insert into Stadium(name,date_built,place,capacitance) values("{}","{}","{}","{}")'''.format(p[0],p[1],p[2],p[3])
                    d.executeSQL(sql,show=True)
                    sql='''select stadium_id from Stadium where name="{}"'''.format(p[0])
                    l3=d.executeSQL(sql,show=True)
                    sql='''update Team set stadium_ID={} where name="{}"'''.format(l3[0][0],p[4])
                    d.executeSQL(sql,show=True)
            else:
                self.label0=tk.Label(self.s,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
                self.label0.grid(row=0,column=0,columnspan=12,sticky='ew',ipady=5)    
        def Update_Stadium():#If the button is being pushed, then a window pops, in which the user can Insert the new data for the Stadium
            self.s=tk.Toplevel()
            self.label10=tk.Label(self.s,text="Update Stadium")
            self.label10.grid(row=0,column=0,columnspan=2)
            self.label=tk.Label(self.s,text="Name of Stadium")
            self.label1=tk.Label(self.s,text="Date of Built")
            self.label2=tk.Label(self.s,text="Place")
            self.label3=tk.Label(self.s,text="Capacitance")
            self.label4=tk.Label(self.s,text="Team")
            self.labels5=[self.label,self.label1,self.label2,self.label3,self.label4]
            self.entry=tk.Entry(self.s,borderwidth=2)
            self.entry1=tk.Entry(self.s,borderwidth=2)
            self.entry2=tk.Entry(self.s,borderwidth=2)
            self.entry3=tk.Entry(self.s,borderwidth=2)
            self.entry4=tk.Entry(self.s,borderwidth=2)
            self.entries5=[self.entry,self.entry1,self.entry2,self.entry3,self.entry4]
            for i in range(len(self.labels5)):
                self.labels5[i].grid(row=i+1,column=0)
                self.entries5[i].grid(row=i+1,column=1)
            #Pushing the Button Submit we process the given information
            self.Button1=tk.Button(self.s,text="Submit",command= UpdateButton)#If the button is being pushed, the data are being processed
            self.Button1.grid(row=10,column=1)
        for i in range(5):#configuration of columns of the Frame
            self.f1.columnconfigure(i, weight=1)
        for widget in self.f1.winfo_children():#Destruction of what was happening previously in the Frame
                widget.destroy()
        #Here we create Labels of the Stadiums of every team in the Championship and Information about them
        self.label=tk.Label(self.f1,text="Stadiums",font="Arial 20",bg='#873ec7')
        self.label1=tk.Label(self.f1,text="Name",bg='#873ec7',width=30,font="Arial 15")
        self.label2=tk.Label(self.f1,text="Date Built",bg='#873ec7',width=25,font="Arial 15")
        self.label3=tk.Label(self.f1,text="Place",bg='#873ec7',width=25,font="Arial 15")
        self.label4=tk.Label(self.f1,text="Capacitance",bg='#873ec7',width=25,font="Arial 15")
        self.label5=tk.Label(self.f1,text="Team",bg='#873ec7',width=30,font="Arial 15")
        self.label.grid(row=1,column=0,columnspan=12,sticky='ew')
        self.label1.grid(row=9,column=0,sticky='ew')
        self.label2.grid(row=9,column=1,sticky='ew')
        self.label3.grid(row=9,column=2,sticky='ew')
        self.label4.grid(row=9,column=3,sticky='ew')
        self.label5.grid(row=9,column=4,sticky='ew')
        row1=11
        sql='''select s.name,date_built,place,capacitance,t.name
                    from Stadium as s,Team as t
                    where s.stadium_ID=t.stadium_ID;'''
        l=d.executeSQL(sql,show=True)
        for i in range(len(l)):
            stadium_name=l[i][0]
            self.label6=tk.Label(self.f1,text="{}".format(l[i][0]),bg='#dbbfbf',width=30,font="Arial 13")
            self.label6.grid(row=row1,column=0,sticky='ew')
            self.label7=tk.Label(self.f1,text="{}".format(l[i][1]),bg='#dbbfbf',width=25,font="Arial 13")
            self.label7.grid(row=row1,column=1,sticky='ew')
            self.label8=tk.Label(self.f1,text="{}".format(l[i][2]),bg='#dbbfbf',width=25,font="Arial 13")
            self.label8.grid(row=row1,column=2,sticky='ew')
            self.label9=tk.Label(self.f1,text="{}".format(l[i][3]),bg='#dbbfbf',width=25,font="Arial 13")
            self.label9.grid(row=row1,column=3,sticky='ew')
            self.label10=tk.Label(self.f1,text="{}".format(l[i][4]),bg='#dbbfbf',width=30,font="Arial 13")
            self.label10.grid(row=row1,column=4,sticky='ew')
            row1+=1
        self.button3=tk.Button(self.f1,text="Update/Insert",command=Update_Stadium)#If the button Update/Insert is being pressed, then the function Update_Stadium runs
        self.button3.grid()
    def buttonPushed8(self):
        root1=tk.Toplevel() #if button 8 is pushed it opens a new window
        self.root1=root1
        root1.title('Premier League 2020-2021') #title of the new window
        root1.iconbitmap(r'images\premier_league_logo.ico') #icon of the new window
        root1.state('zoomed') #the new window is in full-screen
        self.bg=tk.PhotoImage(file=r'images\pr.png') #the background is an image of the logo of Premier League
        self.bg_label = tk.Label(root1, image=self.bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        #root1.rowconfigure(0, weight=0)
        for i in range(0,8):
            root1.rowconfigure(i, weight=1) #we want all the rows except the first one to have the same height
        #we add three columns with differences in length
        root1.columnconfigure(0, weight=1)
        root1.columnconfigure(1, weight=5)
        root1.columnconfigure(2, weight=4)
        #with grid we place the buttons in certain positions
        #when the button b1 is pushed it shows the referees that inspected the most matches
        self.b1=tk.Button(self.root1,text='Referees that inspected the most matches',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed9)
        self.b1.grid(row=0,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b2 is pushed it shows the Top Scorers
        self.b2=tk.Button(self.root1,text='Top Scorers',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed10)
        self.b2.grid(row=1,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b3 is pushed it shows the Players with the most assists
        self.b3=tk.Button(root1,text='Players with the most assists',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed11)
        self.b3.grid(row=2,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b4 is pushed it shows the Players that were given the most cards
        self.b4=tk.Button(root1,text='Players that were given the most cards',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed12)
        self.b4.grid(row=3,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b5 is pushed it shows the Referees that gave the most cards
        self.b5=tk.Button(root1,text='Referees that gave the most cards',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed13)
        self.b5.grid(row=4,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b6 is pushed it shows the most goals in one match
        self.b6=tk.Button(root1,text='Most goals in one match',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed14)
        self.b6.grid(row=5,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b7 is pushed it shows the Players that scored the most goals in one match
        self.b7=tk.Button(root1,text='Players that scored the most goals in one match',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed15)
        self.b7.grid(row=6,column=0,padx=10,pady=10,sticky='ns')
        
        #when the button b8 is pushed it shows the Goalkeepers with the most goals received
        self.b8=tk.Button(root1,text='Goalkeepers with the most goals received',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed16)
        self.b8.grid(row=7,column=0,padx=10,pady=10,sticky='ns')

        #when the button b11 is pushed it shows the Best scorer
        self.b11=tk.Button(root1,text='Best scorers',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed17)
        self.b11.grid(row=6,column=1,padx=10,pady=10,sticky='ns')
        
        #when the button b12 is pushed it shows the Best goalkeepers
        self.b12=tk.Button(root1,text='Best goalkeepers',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed18)
        self.b12.grid(row=7,column=1,padx=10,pady=10,sticky='ns')
        
        #when the button b13 is pushed it shows the players that scored in two different teams
        self.b13=tk.Button(root1,text='Players that scored in two different teams',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed19)
        self.b13.grid(row=6,column=2,columnspan=2,padx=10,pady=10,sticky='ns')
        
        #when the button b14 is pushed it closes the windows
        self.b14=tk.Button(root1,text='Exit',width=50,height=3,fg='#FFFFFF',bg='#551A8B',font=12,command=self.buttonPushed)
        self.b14.grid(row=7,column=2,columnspan=2,padx=10,pady=10,sticky='ns')
        
        #when the button b10 is pushed it submits the name of the player that was written
        self.b10=tk.Button(root1,text='Submit',width=10,height=2,fg='#FFFFFF',bg='#551A8B',font=12,command=self.submit)
        self.b10.grid(row=0,column=2,padx=10,pady=10)
        
        #creates a window to get input from the user (name of the player)
        self.e=tk.Entry(root1,width=100,borderwidth=5)
        self.e.grid(row=0,column=1,padx=10,ipady=10)
        self.f2=tk.Frame(root1,height=500,width=930,bg='#FFFFFF')
        self.f2.grid(row=1,column=1,padx=10,ipady=10,rowspan=5,columnspan=2)
        self.f2.grid_propagate(0)
        self.e.insert(0,"Enter player's name")
    #when submit button is pushed
    def submit(self):
        flag=0
        for widget in self.f2.winfo_children(): #clears the window where the results appeared from the previous results
            widget.destroy()
        player_=self.e.get().strip() #gets the player's name from the input window
        player=player_.split(" ")
        dbfile = "project.db" 
        d = DataModel(dbfile) #connecting to our database
        if(';' in player_ or 'drop' in player_ or 'delete' in player_): #checking if someone tried to erase the database through the input
            flag=1
        if(flag!=1):
            #if the player has only his last name registered in our database
            if(len(player)==1):
                sql='''SELECT first_name,last_name,shirt_number,height,date_of_birth,sum(goals) AS total_goals,sum(saves) AS total_saves,sum(passes) AS total_passes,sum(assists) AS total_assists,sum(shots) AS total_shots,sum(shots_on_target) AS total_shots_ot,sum(tackles) AS total_tackles
                    FROM player AS P1, participates AS P2
                    WHERE P1.player_ID=P2.player_ID AND last_name=="{}";
                    '''.format(player[0])
                results=d.executeSQL(sql,show=True)
            #if the player has his first and last name (his last name consists of one or two words joined with -) registered in our database
            if(len(player)==2):
                sql='''SELECT first_name,last_name,shirt_number,height,date_of_birth,sum(goals) AS total_goals,sum(saves) AS total_saves,sum(passes) AS total_passes,sum(assists) AS total_assists,sum(shots) AS total_shots,sum(shots_on_target) AS total_shots_ot,sum(tackles) AS total_tackles
                    FROM player AS P1, participates AS P2
                    WHERE P1.player_ID=P2.player_ID AND first_name=="{}" AND last_name=="{}";
                '''.format(player[0],player[1])
                results=d.executeSQL(sql,show=True)
            #if the player has his first and last name (his last name consists of two or more words joined with a space) registered in our database
            if(len(player)>2):
                sql='''SELECT first_name,last_name,shirt_number,height,date_of_birth,sum(goals) AS total_goals,sum(saves) AS total_saves,sum(passes) AS total_passes,sum(assists) AS total_assists,sum(shots) AS total_shots,sum(shots_on_target) AS total_shots_ot,sum(tackles) AS total_tackles
                    FROM player AS P1, participates AS P2
                    WHERE P1.player_ID=P2.player_ID AND first_name=="{}" AND last_name=="{}";
                '''.format(player[0],' '.join(player[1:]))
                results=d.executeSQL(sql,show=True)
            #if the player is found we print his stats and information on the window
            if(results[0][1]!="None"):
                #we print the header for each result
                self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 13')
                self.label1.grid(row=1,column=0,sticky='ew')
                self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 13')
                self.label2.grid(row=1,column=1,sticky='ew')
                self.label3=tk.Label(self.f2,text="Shirt Number",bg='#873ec7',font='Arial 13')
                self.label3.grid(row=1,column=2,sticky='ew')
                self.label4=tk.Label(self.f2,text="Height",bg='#873ec7',font='Arial 13')
                self.label4.grid(row=1,column=3,sticky='ew')
                self.label5=tk.Label(self.f2,text="Date of birth",bg='#873ec7',font='Arial 13')
                self.label5.grid(row=1,column=4,sticky='ew')
                self.label6=tk.Label(self.f2,text="Goals",bg='#873ec7',font='Arial 13')
                self.label6.grid(row=1,column=5,sticky='ew')
                self.label7=tk.Label(self.f2,text="Saves",bg='#873ec7',font='Arial 13')
                self.label7.grid(row=1,column=6,sticky='ew')
                self.label8=tk.Label(self.f2,text="Passes",bg='#873ec7',font='Arial 13')
                self.label8.grid(row=1,column=7,sticky='ew')
                self.label9=tk.Label(self.f2,text="Assists",bg='#873ec7',font='Arial 13')
                self.label9.grid(row=1,column=8,sticky='ew')
                self.label10=tk.Label(self.f2,text="Shots",bg='#873ec7',font='Arial 13')
                self.label10.grid(row=1,column=9,sticky='ew')
                self.label11=tk.Label(self.f2,text="Shots on target",bg='#873ec7',font='Arial 13')
                self.label11.grid(row=1,column=10,sticky='ew')
                self.label12=tk.Label(self.f2,text="Tackles",bg='#873ec7',font='Arial 13')
                self.label12.grid(row=1,column=11,sticky='ew')
                column1=0
                if(len(results[0])==11):
                    results[0].insert(5,' ')
                #we print the results on the window
                for i in range(12):
                    self.label13=tk.Label(self.f2,text=results[0][i],bg='#dbbfbf',font='Arial 12')
                    self.label13.grid(row=2,column=column1,sticky='ew')
                    column1+=1
                self.e.delete(0,'end') #clears the input window
            else: #if the name of the player isn't found
                self.label0=tk.Label(self.f2,text="THE NAME YOU ENTERED WAS WRONG",bg='#873ec7',font='Arial 16')
                self.label0.grid(row=0,column=0,columnspan=12,sticky='ew',ipady=5)
        else: #if someone tried to erase the database
            self.label0=tk.Label(self.f2,text="Did you think it would be that easy to erase our database;",bg='#873ec7',font='Arial 16')
            self.label0.grid(row=0,column=0,columnspan=12,sticky='ew',ipady=5)
    #when the Referees that inspected the most matches button is pushed
    def buttonPushed9(self):
        for widget in self.f2.winfo_children():
            widget.destroy() #clears the window where results appear from the previous results
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many referees:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="REFEREES WITH THE MOST INSPECTIONS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip()) #we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,count(*) AS inspections
                FROM Referee AS r, inspects AS i 
                WHERE r.referee_ID=i.referee_ID
                GROUP BY r.referee_ID
                ORDER BY inspections DESC
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Inspections",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the Top Scorers button is pushed
    def buttonPushed10(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many players do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="TOP SCORERS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip()) #we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,sum(goals) AS goals_sum 
                FROM player AS P1,participates AS P2 
                WHERE P1.player_ID=P2.player_ID AND position<>'GK' 
                GROUP BY P2.player_ID 
                ORDER BY goals_sum DESC 
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Goals scored",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the Players with the most assists button is pushed
    def buttonPushed11(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many players do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="PLAYERS WITH THE MOST ASSISTS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip()) #we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,sum(assists) AS assists_sum
                FROM player AS P1,participates AS P2 
                WHERE P1.player_ID=P2.player_ID
                GROUP BY P2.player_ID 
                ORDER BY assists_sum DESC
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Total assists",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the Players that were given the most cards button is pushed
    def buttonPushed12(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many players do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="PLAYERS WITH THE MOST CARDS RECEIVED PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip())#we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,count(card) AS cards_sum 
                FROM player AS P1,attributes_violation AS P2 
                WHERE P1.player_ID=P2.player_ID 
                GROUP BY P2.player_ID 
                ORDER BY cards_sum DESC  
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Cards Received",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the Referees that gave the most cards button is pushed
    def buttonPushed13(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many referees do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="REFEREES THAT GAVE THE MOST CARDS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip())#we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,count(*) AS cards
                FROM Referee AS r, attributes_violation AS a,inspects AS i 
                WHERE r.referee_ID=i.referee_ID AND i.match_ID=a.match_ID AND i.status="Referee"
                GROUP BY r.referee_ID
                ORDER BY cards DESC  
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Cards",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the most goals in one match button is pushed
    def buttonPushed14(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many matches do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="MATCHES WITH THE MOST GOALS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip())#we get the choice of the user from the combo box
            sql='''SELECT IIF(E.home,T1.name,T2.name) AS team1,IIF(E.home!=1,T1.name,T2.name) AS team2,score,matchweek,(CAST(SUBSTR(score, 1, 1) AS INTEGER)+CAST(SUBSTR(score, 3, 3) AS INTEGER)) AS total_goals 
                FROM (enters AS E1 LEFT JOIN (SELECT match_ID,team_ID AS team_ID2,home AS home2 FROM enters) AS E2 ON E1.match_ID=E2.match_ID AND E1.team_ID<>E2.team_ID2) AS E,Match_ AS M,Team AS T1,Team AS T2
                WHERE E.match_ID=M.match_ID AND T1.team_ID=E.team_ID AND T2.team_ID=E.team_ID2
                GROUP BY E.match_ID
                ORDER BY total_goals DESC  
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="Team1 vs Team2",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Score",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="matchweek",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            self.label4=tk.Label(self.f2,text="Total goals",bg='#873ec7',font='Arial 14')
            self.label4.grid(row=2,column=3,sticky='ew')
            labels.append(self.label4)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label5=tk.Label(self.f2,text="{} vs {}".format(results[i][0],results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label6)
                self.label7=tk.Label(self.f2,text="{}".format(results[i][3]),bg='#dbbfbf',font='Arial 12')
                self.label7.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label7)
                self.label8=tk.Label(self.f2,text="{}".format(results[i][4]),bg='#dbbfbf',font='Arial 12')
                self.label8.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label8)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=4,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the Players that scored the most goals in one match button is pushed
    def buttonPushed15(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile) 
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many players do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="THE MOST GOALS SCORED BY A PLAYER IN ONE MATCH PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip())#we get the choice of the user from the combo box
            sql='''SELECT IIF(E.home,T1.name,T2.name) AS team1,IIF(E.home!=1,T1.name,T2.name) AS team2,score,matchweek,first_name,last_name,max(goals) as goals,IIF(T1.team_ID=B.team_ID,T1.name,T2.name) AS his_team
                FROM participates AS P1, Player AS P2,(enters AS E1 LEFT JOIN (SELECT match_ID,team_ID AS team_ID2,home AS home2 FROM enters) AS E2 ON E1.match_ID=E2.match_ID AND E1.team_ID<>E2.team_ID2) AS E,Team AS T1,Team AS T2,Match_ AS M,belongs AS B
                WHERE P1.player_ID=P2.player_ID AND position<>'GK' AND T1.team_ID=E.team_ID AND T2.team_ID=E.team_ID2 AND E.match_ID=M.match_ID AND P1.match_ID=E.match_ID AND B.player_ID=P1.player_ID
                GROUP BY P1.player_ID
                ORDER BY goals DESC
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="Team 1 vs Team2",bg='#873ec7',font='Arial 13')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Score",bg='#873ec7',font='Arial 13')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Matchweek",bg='#873ec7',font='Arial 13')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            self.label4=tk.Label(self.f2,text="First name",bg='#873ec7',font='Arial 13')
            self.label4.grid(row=2,column=3,sticky='ew')
            labels.append(self.label4)
            self.label5=tk.Label(self.f2,text="Last name",bg='#873ec7',font='Arial 13')
            self.label5.grid(row=2,column=4,sticky='ew')
            labels.append(self.label5)
            self.label6=tk.Label(self.f2,text="Goals scored",bg='#873ec7',font='Arial 13')
            self.label6.grid(row=2,column=5,sticky='ew')
            labels.append(self.label6)
            self.label7=tk.Label(self.f2,text="Team of the player",bg='#873ec7',font='Arial 13')
            self.label7.grid(row=2,column=6,sticky='ew')
            labels.append(self.label7)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label8=tk.Label(self.f2,text="{} vs {}".format(results[i][0],results[i][1]),bg='#dbbfbf',font='Arial 11')
                self.label8.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label8)
                self.label9=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 11')
                self.label9.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label9)
                self.label10=tk.Label(self.f2,text="{}".format(results[i][3]),bg='#dbbfbf',font='Arial 11')
                self.label10.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label10)
                self.label11=tk.Label(self.f2,text="{}".format(results[i][4]),bg='#dbbfbf',font='Arial 11')
                self.label11.grid(row=row1,column=3,sticky='ew')
                labels.append(self.label11)
                self.label12=tk.Label(self.f2,text="{}".format(results[i][5]),bg='#dbbfbf',font='Arial 11')
                self.label12.grid(row=row1,column=4,sticky='ew')
                labels.append(self.label12)
                self.label13=tk.Label(self.f2,text="{}".format(results[i][6]),bg='#dbbfbf',font='Arial 11')
                self.label13.grid(row=row1,column=5,sticky='ew')
                labels.append(self.label13)
                self.label14=tk.Label(self.f2,text="{}".format(results[i][7]),bg='#dbbfbf',font='Arial 11')
                self.label14.grid(row=row1,column=6,sticky='ew')
                labels.append(self.label14)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=7,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,columnspan=2,sticky='ew')
        self.choices.grid(row=1,column=2,ipadx=5,ipady=3)
    #when the Goalkeepers with the most goals received button is pushed
    def buttonPushed16(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many goalkeepers do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="GOALKEEPERS THAT RECEIVED THE MOST GOALS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip())#we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,sum(IIF(home!=1,(CAST(SUBSTR(score, 1, 1) AS INTEGER)),(CAST(SUBSTR(score, 3, 3) AS INTEGER)))) AS goals_received 
                FROM participates AS P1, Player AS P2,Match_ AS M,enters AS E, belongs AS B 
                WHERE position=='GK' AND M.match_ID=P1.match_ID AND M.match_ID=E.match_ID AND B.team_ID=E.team_ID AND B.player_ID=P1.player_ID AND P1.player_ID=P2.player_ID 
                GROUP BY P1.player_ID 
                ORDER BY goals_received DESC 
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Goals Received",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when exit button is pushed
    def buttonPushed(self):
        self.root.destroy()

    #when the Best Scorers button is pushed
    def buttonPushed17(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many players do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="BEST SCORERS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip()) #we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,sum(participation_in_match)/sum(goals) AS minutes_per_goal 
                FROM player AS P1,participates AS P2 
                WHERE P1.player_ID=P2.player_ID AND position<>'GK'
                GROUP BY P2.player_ID
                HAVING minutes_per_goal IS NOT NULL
                ORDER BY minutes_per_goal 
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Minutes per goal",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    #when the Best Goalkeepers button is pushed
    def buttonPushed18(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        for i in range(3):
            self.f2.columnconfigure(i, weight=1) #we want each column to have the same length
        labels=[]
        self.choices=ttk.Combobox(self.f2) #creating a combo box
        self.choices['values'] = ('1','2','3','4','5','6','7','8','9','10') #the choices in the combo box that the user can choose from
        self.choices.current(0)
        #titles of the results
        self.label=tk.Label(self.f2,text="How many goalkeepers do you want to be shown:",bg='#FFFFFF',font='Arial 12')
        self.label0=tk.Label(self.f2,text="BEST GOALKEEPERS PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        #when a number is selected from the combo box
        def selected(event):
            for x in labels: #each time the user selects a number it deletes the previous results
                if len(labels)==0:
                    break
                else:
                    x.destroy()
            num=int(self.choices.get().strip())#we get the choice of the user from the combo box
            sql='''SELECT first_name,last_name,sum(participation_in_match)/sum(IIF(home!=1,(CAST(SUBSTR(score, 1, 1) AS INTEGER)),(CAST(SUBSTR(score, 3, 3) AS INTEGER)))) AS minutes_per_goal_received 
                FROM participates AS P1, Player AS P2,Match_ AS M,enters AS E, belongs AS B 
                WHERE position=='GK' AND M.match_ID=P1.match_ID AND M.match_ID=E.match_ID AND B.team_ID=E.team_ID AND B.player_ID=P1.player_ID AND P1.player_ID=P2.player_ID 
                GROUP BY P1.player_ID 
                ORDER BY minutes_per_goal_received DESC  
                LIMIT {};'''.format(num)
            results=d.executeSQL(sql,show=True) #the results we got from the query
            #the headers for the results
            self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
            self.label1.grid(row=2,column=0,sticky='ew')
            labels.append(self.label1)
            self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
            self.label2.grid(row=2,column=1,sticky='ew')
            labels.append(self.label2)
            self.label3=tk.Label(self.f2,text="Minutes per Goal Received",bg='#873ec7',font='Arial 14')
            self.label3.grid(row=2,column=2,sticky='ew')
            labels.append(self.label3)
            row1=3
            #putting the results we got on the window
            for i in range(num):
                self.label4=tk.Label(self.f2,text="{}".format(results[i][0]),bg='#dbbfbf',font='Arial 12')
                self.label4.grid(row=row1,column=0,sticky='ew')
                labels.append(self.label4)
                self.label5=tk.Label(self.f2,text="{}".format(results[i][1]),bg='#dbbfbf',font='Arial 12')
                self.label5.grid(row=row1,column=1,sticky='ew')
                labels.append(self.label5)
                self.label6=tk.Label(self.f2,text="{}".format(results[i][2]),bg='#dbbfbf',font='Arial 12')
                self.label6.grid(row=row1,column=2,sticky='ew')
                labels.append(self.label6)
                row1+=1
        self.choices.bind("<<ComboboxSelected>>",selected)
        self.label0.grid(row=0,column=0,columnspan=3,sticky='ew',ipady=5)
        self.label.grid(row=1,column=0,sticky='ew')
        self.choices.grid(row=1,column=1,ipadx=5,ipady=3)
    def buttonPushed19(self):
        for widget in self.f2.winfo_children(): #clears the window where results appear from the previous results
            widget.destroy()
        dbfile = "project.db"
        d = DataModel(dbfile)
        #title of the results
        self.label0=tk.Label(self.f2,text="PLAYERS THAT SCORED IN TWO DIFFERENT TEAMS DURING PREMIER LEAGUE 2020-2021",bg='#873ec7',font='Arial 16')
        self.label0.grid(row=0,column=0,columnspan=6,sticky='ew',ipady=5)
        sql='''CREATE VIEW IF NOT EXISTS players_that_changed_teams
            AS 
            SELECT player_ID,team_ID,SUM(goals) AS total_goals
            FROM (participates NATURAL JOIN Match_) NATURAL JOIN belongs
            WHERE strftime("%Y-%m-%d",datetime_)<contract_end_day AND strftime("%Y-%m-%d",datetime_)>contract_start_day AND player_ID IN(
            SELECT player_ID
            FROM belongs
            GROUP BY player_ID
            HAVING COUNT(*)>1
            )GROUP BY player_ID,team_ID;
            SELECT first_name,last_name,name AS team1,total_goals AS total_goals_at_team1,name2 AS team2,total_goals2 AS total_goals_at_team2
            FROM (Player NATURAL JOIN players_that_changed_teams NATURAL JOIN(SELECT team_ID AS team_ID2,player_ID,total_goals AS total_goals2 FROM players_that_changed_teams) NATURAL JOIN Team) AS T1 JOIN (SELECT name AS name2,team_ID FROM Team) AS T2 ON T1.team_ID2=T2.team_ID  
            WHERE T1.team_ID<>team_ID2 AND player_ID IN(
            SELECT player_ID
            FROM players_that_changed_teams
            WHERE total_goals>0
            GROUP BY player_ID
            HAVING COUNT(*)>1
            )LIMIT 1;'''
        results=d.executeSQL(sql,show=True) #the results we got from the query
        #the headers for the results
        self.label1=tk.Label(self.f2,text="First Name",bg='#873ec7',font='Arial 14')
        self.label1.grid(row=1,column=0,sticky='ew')
        self.label2=tk.Label(self.f2,text="Last Name",bg='#873ec7',font='Arial 14')
        self.label2.grid(row=1,column=1,sticky='ew')
        self.label3=tk.Label(self.f2,text="Team1",bg='#873ec7',font='Arial 14')
        self.label3.grid(row=1,column=2,sticky='ew')
        self.label4=tk.Label(self.f2,text="Total goals scored for team1",bg='#873ec7',font='Arial 14')
        self.label4.grid(row=1,column=3,sticky='ew')
        self.label5=tk.Label(self.f2,text="Team2",bg='#873ec7',font='Arial 14')
        self.label5.grid(row=1,column=4,sticky='ew')
        self.label6=tk.Label(self.f2,text="Total goals scored for team2",bg='#873ec7',font='Arial 14')
        self.label6.grid(row=1,column=5,sticky='ew')
        #putting the results we got on the window
        self.label7=tk.Label(self.f2,text="{}".format(results[0][0]),bg='#dbbfbf',font='Arial 12')
        self.label7.grid(row=2,column=0,sticky='ew')
        self.label8=tk.Label(self.f2,text="{}".format(results[0][1]),bg='#dbbfbf',font='Arial 12')
        self.label8.grid(row=2,column=1,sticky='ew')
        self.label9=tk.Label(self.f2,text="{}".format(results[0][2]),bg='#dbbfbf',font='Arial 12')
        self.label9.grid(row=2,column=2,sticky='ew')
        self.label10=tk.Label(self.f2,text="{}".format(results[0][3]),bg='#dbbfbf',font='Arial 12')
        self.label10.grid(row=2,column=3,sticky='ew')
        self.label11=tk.Label(self.f2,text="{}".format(results[0][4]),bg='#dbbfbf',font='Arial 12')
        self.label11.grid(row=2,column=4,sticky='ew')
        self.label12=tk.Label(self.f2,text="{}".format(results[0][5]),bg='#dbbfbf',font='Arial 12')
        self.label12.grid(row=2,column=5,sticky='ew')

root=tk.Tk()
myapp=MyApp(root)
root.mainloop()
