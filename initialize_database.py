import sqlite3
import time
import pandas as pd

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
                    d.append([str(item)for item in row])
            self.con.commit()
            return d
        except sqlite3.Error as error:
            print(f"Error while trying to execute SQL", error)
            return False

if __name__ == "__main__":
    dbfile = "project.db" #name of the database file that will be created
    d = DataModel(dbfile) #connecting to the database
    
    #create each table of the database:
    sql='''CREATE TABLE "Coach" (
	"coach_ID"	INTEGER,
	"first_name"	TEXT,
	"last_name"	TEXT NOT NULL,
	"contract_start_date"	TEXT CHECK(contract_start_date IS strftime('%Y-%m-%d',contract_start_date)),
	"contract_end_date"	TEXT CHECK(contract_end_date IS strftime('%Y-%m-%d',contract_end_date)),
	"team_code"	INTEGER,
	FOREIGN KEY("team_code") REFERENCES "Team"("team_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("coach_ID" AUTOINCREMENT)
        );''' #creating the table Coach
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "Match_" (
	"match_ID"	INTEGER,
	"score"	TEXT,
	"datetime_"	TEXT CHECK(datetime_ IS strftime('%Y-%m-%d %H:%M',datetime_)),
	"matchweek"	INTEGER CHECK(matchweek>=1 AND matchweek<=38),
	"stadium_code"	INTEGER,
	PRIMARY KEY("match_ID" AUTOINCREMENT),
	FOREIGN KEY("stadium_code") REFERENCES "Stadium"("stadium_ID") ON UPDATE CASCADE ON DELETE SET NULL
        );'''#creating the table Match_
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "Player" (
	"player_ID"	INTEGER,
	"shirt_number"	INTEGER CHECK(shirt_number>0),
	"height"	INTEGER CHECK(height>0),
	"date_of_birth"	TEXT CHECK(date_of_birth IS strftime('%Y-%m-%d',date_of_birth)), 
	"first_name"	TEXT,
	"last_name"	TEXT NOT NULL,
	PRIMARY KEY("player_ID" AUTOINCREMENT)
        );'''#creating the table Player
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "Referee" (
	"referee_ID"	INTEGER,
	"last_name"	TEXT NOT NULL,
	"first_name"	TEXT,
	"yellow_cards"	INTEGER CHECK(yellow_cards>=0),
	"red_cards"	INTEGER CHECK(red_cards>=0),
	"number_of_matches"	INTEGER CHECK(number_of_matches>=0),
	PRIMARY KEY("referee_ID" AUTOINCREMENT)
        );'''#creating the table Referee
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "Stadium" (
	"stadium_ID"	INTEGER,
	"name"	TEXT NOT NULL,
	"date_built"	INTEGER,
	"place"	TEXT,
	"capacitance"	INTEGER CHECK(capacitance>0),
	PRIMARY KEY("stadium_ID" AUTOINCREMENT)
        );'''#creating the table Stadium
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "Team" (
	"team_ID"	INTEGER,
	"name"	TEXT NOT NULL,
	"founded"	TEXT,
	"wins"	INTEGER CHECK(wins>=0),
	"ties"	INTEGER CHECK(ties>=0),
	"losses"	INTEGER CHECK(losses>=0),
	"points"	INTEGER CHECK(points>=0),
	"stadium_ID"	INTEGER,
	FOREIGN KEY("stadium_ID") REFERENCES "Stadium"("stadium_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("team_ID" AUTOINCREMENT)
        );'''#creating the table Team
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "attributes_violation" (
	"violation_ID"	INTEGER,
	"match_ID"	INTEGER,
	"player_ID"	INTEGER,
	"disqualification"	INTEGER CHECK(disqualification IN (0,1)),
	"minute_in_match"	INTEGER CHECK(minute_in_match>=0 AND minute_in_match<=90),
	"card"	TEXT CHECK(card IN ('Yellow','Second Yellow','Red')),
	FOREIGN KEY("match_ID") REFERENCES "Match_"("match_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY("player_ID") REFERENCES "Player"("player_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("match_ID","player_ID","violation_ID")
        );'''#creating the table attributes_violation
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "belongs" (
	"player_ID"	INTEGER,
	"team_ID"	INTEGER,
	"contract_start_day"	TEXT CHECK(contract_start_day IS strftime('%Y-%m-%d',contract_start_day)),
	"contract_end_day"	TEXT CHECK(contract_end_day IS strftime('%Y-%m-%d',contract_end_day)),
	"salary"	INTEGER CHECK(salary>0),
	FOREIGN KEY("team_ID") REFERENCES "Team"("team_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY("player_ID") REFERENCES "Player"("player_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("player_ID","team_ID")
        );'''#creating the table belongs
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "enters" (
	"match_ID"	INTEGER,
	"team_ID"	INTEGER,
	"home"	INTEGER CHECK(home IN (0,1)),
	FOREIGN KEY("team_ID") REFERENCES "Team"("team_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY("match_ID") REFERENCES "Match_"("match_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("match_ID","team_ID")
        );'''#creating the table enters
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "inspects" (
	"match_ID"	INTEGER,
	"referee_ID"	INTEGER,
	"status"	TEXT CHECK(status IN ('Referee','AR1','AR2','4th')),
	FOREIGN KEY("match_ID") REFERENCES "Match_"("match_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY("referee_ID") REFERENCES "Referee"("referee_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("match_ID","referee_ID")
        );'''#creating the table inspects
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "participates" (
        "player_ID"	INTEGER,
	"match_ID"	INTEGER,
	"start"	TEXT CHECK(start IN ('Y','Y*','N')),
	"goals"	INTEGER CHECK(goals>=0),
	"participation_in_match"	INTEGER CHECK(participation_in_match>0 AND participation_in_match<91),
	"saves"	INTEGER CHECK(saves>=0),
	"shots"	INTEGER CHECK(shots>=0),
	"shots_on_target"	INTEGER CHECK(shots_on_target>=0),
	"assists"	INTEGER CHECK(assists>=0),
	"tackles"	INTEGER CHECK(tackles>=0),
	"passes"	INTEGER CHECK(passes>=0),
	"position"	TEXT,
	"start_of_participation"	INTEGER CHECK(start_of_participation>=0 AND start_of_participation<90),
	"end_of_participation"	INTEGER CHECK(end_of_participation>0 AND end_of_participation<=90),
	PRIMARY KEY("match_ID","player_ID"),
	FOREIGN KEY("match_ID") REFERENCES "Match_"("match_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY("player_ID") REFERENCES "Player"("player_ID") ON UPDATE CASCADE ON DELETE SET NULL
        );'''#creating the table participates
    d.executeSQL(sql, show=True)

    sql='''CREATE TABLE "substitutes" (
	"substitution_ID"	INTEGER,
	"match_ID"	INTEGER,
	"player_ID"	INTEGER,
	"minute_in_match"	INTEGER CHECK(minute_in_match>0 AND minute_in_match<90),
	FOREIGN KEY("player_ID") REFERENCES "Player"("player_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY("match_ID") REFERENCES "Match_"("match_ID") ON UPDATE CASCADE ON DELETE SET NULL,
	PRIMARY KEY("substitution_ID","player_ID","match_ID")
        );'''#creating the table substitutes
    d.executeSQL(sql, show=True)

    #inserting excel and csv files to the database
    players = pd.read_excel(r'excel_csv\Players.xlsx', sheet_name='Sheet1',header=0) #Player
    players.to_sql('Player',d.con, if_exists='append', index=False)

    coaches = pd.read_excel(r'excel_csv\Coach.xlsx', sheet_name='Sheet1',header=0) #Coach
    coaches.to_sql('Coach',d.con, if_exists='append', index=False)

    stadiums = pd.read_excel(r'excel_csv\Stadiums.xlsx', sheet_name='Sheet1',header=0) #Stadium
    stadiums.to_sql('Stadium',d.con, if_exists='append', index=False)

    matches = pd.read_excel(r'excel_csv\matches.xlsx', sheet_name='Sheet1',header=0) #Match_
    matches.to_sql('Match_',d.con, if_exists='append', index=False)

    referees = pd.read_excel(r'excel_csv\referee.xlsx', sheet_name='Sheet1',header=0) #Referee
    referees.to_sql('Referee',d.con, if_exists='append', index=False)

    teams = pd.read_csv(r'excel_csv\Team.csv', header=0) #Team
    teams.to_sql('Team',d.con, if_exists='append', index=False)
    
    violations = pd.read_excel(r'excel_csv\attributes_violation_fixed.xlsx', sheet_name='Sheet1',header=0) #attributes_violation
    violations.to_sql('attributes_violation',d.con, if_exists='append', index=False)

    belongs = pd.read_excel(r'excel_csv\Belongs.xlsx', sheet_name='Sheet1',header=0) #belongs
    belongs.to_sql('belongs',d.con, if_exists='append', index=False)

    enters = pd.read_excel(r'excel_csv\enters.xlsx', sheet_name='Sheet1',header=0) #enters
    enters.to_sql('enters',d.con, if_exists='append', index=False)

    inspects = pd.read_excel(r'excel_csv\inspects.xlsx', sheet_name='Sheet1',header=0) #inspects
    inspects.to_sql('inspects',d.con, if_exists='append', index=False)

    participates = pd.read_excel(r'excel_csv\participates_fixed.xlsx', sheet_name='Sheet1',header=0) #participates
    participates.to_sql('participates',d.con, if_exists='append', index=False)

    substitutes = pd.read_excel(r'excel_csv\substitutes_fixed.xlsx', sheet_name='Sheet1',header=0) #substitutes
    substitutes.to_sql('substitutes',d.con, if_exists='append', index=False)

    d.executeSQL('''create index position_index on participates(position);''', show=True)
    d.executeSQL('''create index status_index on inspects(status);''', show=True)
    d.executeSQL('''create index card_index on attributes_violation(card);''', show=True)
    d.executeSQL('''create index matchweek_index on Match_(matchweek);''', show=True)
    d.executeSQL('''create index f_lname_index on Player(first_name,last_name);''', show=True)
    
    sql="""SELECT count(*),T.team_ID
        FROM Match_ AS M,enters AS E,Team AS T 
        WHERE M.match_ID=E.match_ID AND T.team_ID=E.team_ID AND ((CAST(SUBSTR(score, 1, 1) AS INTEGER)>CAST(SUBSTR(score, 3, 3) AS INTEGER) AND home=1)
        OR (CAST(SUBSTR(score, 1, 1) AS INTEGER)<CAST(SUBSTR(score, 3, 3) AS INTEGER) AND home=0))
        GROUP BY T.team_ID;""" #sql code for computing the number of wins of each team
    wins=d.executeSQL(sql, show=True)

    sql="""SELECT count(*),T.team_ID
        FROM Match_ AS M,enters AS E,Team AS T 
        WHERE M.match_ID=E.match_ID AND T.team_ID=E.team_ID AND CAST(SUBSTR(score, 1, 1) AS INTEGER)==CAST(SUBSTR(score, 3, 3) AS INTEGER)
        GROUP BY T.team_ID;""" #sql code for computing the number of ties of each team
    ties=d.executeSQL(sql, show=True)

    sql="""SELECT count(*),T.team_ID
        FROM Match_ AS M,enters AS E,Team AS T 
        WHERE M.match_ID=E.match_ID AND T.team_ID=E.team_ID AND ((CAST(SUBSTR(score, 1, 1) AS INTEGER)<CAST(SUBSTR(score, 3, 3) AS INTEGER) AND home=1)
        OR (CAST(SUBSTR(score, 1, 1) AS INTEGER)>CAST(SUBSTR(score, 3, 3) AS INTEGER) AND home=0))
        GROUP BY T.team_ID;""" #sql code for computing the number of losses of each team
    losses=d.executeSQL(sql, show=True)

    sql='''SELECT sum(IIF((CAST(SUBSTR(score, 1, 1) AS INTEGER))==(CAST(SUBSTR(score, 3, 3) AS INTEGER)),1,IIF(home,IIF((CAST(SUBSTR(score, 1, 1) AS INTEGER))
        >(CAST(SUBSTR(score, 3, 3) AS INTEGER)),3,0),IIF((CAST(SUBSTR(score, 1, 1) AS INTEGER))>(CAST(SUBSTR(score, 3, 3) AS INTEGER)),0,3)))) AS pointss,T.team_ID
        FROM Match_ AS M,enters AS E,Team AS T 
        WHERE M.match_ID=E.match_ID AND T.team_ID=E.team_ID
        GROUP BY T.team_ID
        ORDER BY pointss DESC;''' #sql code for computing the points of each team
    points=d.executeSQL(sql, show=True)
    
    #update wins/losses/ties of each team
    for i in range(20):
        sql="""UPDATE Team
        SET wins={},ties={},losses={},points={}
        WHERE team_ID={};""".format(wins[i][0],ties[i][0],losses[i][0],points[i][0],i)
        d.executeSQL(sql, show=True)

    sql='''SELECT referee_ID,count(*) as appearances
        FROM Referee NATURAL JOIN inspects
        GROUP BY referee_ID
        ORDER BY referee_ID'''
    appearances=d.executeSQL(sql, show=True)

    sql='''SELECT referee_ID,count(*) as yellow_cards
        FROM (Referee NATURAL JOIN inspects)NATURAL JOIN attributes_violation
        WHERE card="Yellow" AND status="Referee"
        GROUP BY referee_ID'''
    yellow=d.executeSQL(sql, show=True)

    sql='''SELECT referee_ID,count(*) as red_cards
        FROM (Referee NATURAL JOIN inspects)NATURAL JOIN attributes_violation
        WHERE (card="Red" OR card="Second Yellow") AND status="Referee"
        GROUP BY referee_ID'''
    red=d.executeSQL(sql, show=True)

    for i in range(len(appearances)):
        sql="""UPDATE Referee
        SET number_of_matches={}
        WHERE referee_ID={};""".format(appearances[i][1],appearances[i][0])
        d.executeSQL(sql, show=True)

    for i in range(len(yellow)):
        sql="""UPDATE Referee
        SET yellow_cards={}
        WHERE referee_ID={};""".format(yellow[i][1],yellow[i][0])
        d.executeSQL(sql, show=True)

    for i in range(len(red)):
        sql="""UPDATE Referee
        SET red_cards={}
        WHERE referee_ID={};""".format(red[i][1],red[i][0])
        d.executeSQL(sql, show=True)
    d.close()#closing the connection to the database
