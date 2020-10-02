import os
import psycopg2
from contextlib import closing
#connect to local postgresql database
try:
    PASSWORD = os.environ['PASSWORD']
    USERNAME = os.environ['USERNAME']
    conn=psycopg2.connect(database="mydb",user=USERNAME,password=PASSWORD,host="localhost",port="5432")
except:
    print("Failed to connect to database")

cursor=conn.cursor()

#create player Table
ptable_query="""CREATE TABLE IF NOT EXISTS Players(
            name varchar(50) UNIQUE,
            games_won int,
            current_points int
            )"""

with closing(conn.cursor())as c:
    c.execute(ptable_query)
    c.execute(current_players)
    conn.commit()



#add new player
def add_player(pname):
    query="""INSERT INTO Players(name,games_won,current_points) VALUES(%s,0,0)"""

    with closing(conn.cursor())as c:
        c.execute(query,(pname,))
        conn.commit()

#get current update_score
def get_score(pname):
    query="""SELECT current_points FROM Players WHERE name=%s"""

    with closing(conn.cursor())as c:
        c.execute(query,(pname,))
        score=c.fetchone()
        print(type(score[0]))
        return int(score[0])

#update current score
def update_score(pname):
    #get last score
    last_score=get_score(pname)
    new_score=last_score+1
    print(new_score)
    #add 1 and update score
    query="""UPDATE Players SET current_points=%s WHERE name=%s"""
    with closing(conn.cursor())as c:
        c.execute(query,(new_score,pname,))
        conn.commit()


#get current update_score
def get_games(pname):
    query="""SELECT games_won FROM Players WHERE name=%s"""

    with closing(conn.cursor())as c:
        c.execute(query,(pname,))
        score=c.fetchone()
        print(type(score[0]))
        return int(score[0])

#update games won
def update_games(pname):
    #get last score
    last_games=get_games(pname)
    new_games=last_games+1
    print(new_games)
    #add 1 and update score
    query="""UPDATE Players SET games_won=%s WHERE name=%s"""
    with closing(conn.cursor())as c:
        c.execute(query,(new_games,pname,))
        conn.commit()

#reset current score
def reset_score(pname):
        query="""UPDATE Players SET current_points=0 WHERE name=%s"""
        with closing(conn.cursor())as c:
            c.execute(query,(pname,))
            conn.commit()

#get player data
def get_player(pname):
    query="""SELECT * FROM Players WHERE name=%s"""

    try:
        with closing(conn.cursor())as c:
            c.execute(query,(pname,))
            player=c.fetchone()

            name=player[0]
            games_won=player[1]
            score=player[2]

            return (name,games_won,score)
    except:
        return -1 #when player is not in the database

#get sorted players
def get_all():
    query="""SELECT * FROM Players ORDER BY games_won DESC"""

    with closing(conn.cursor())as c:
        c.execute(query)
        players=c.fetchall()

        for player in players:
            print("{} {} {}".format(player[0],player[1],player[2]))

        return players

#delete a player
def delete_player(pname):
    query="""DELETE FROM Players WHERE name=%s"""
    with closing(conn.cursor())as c:
        c.execute(query,(pname,))
        conn.commit()



#DB tests
#add_player("John")
"""
update_score("John")
get_all()
reset_score("John")
get_all()
delete_player("Shammah")
delete_player("Peter")"""
#get_all()
