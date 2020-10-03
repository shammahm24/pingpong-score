from flask import Flask,render_template,request,redirect,url_for
import dbconnect as db

app=Flask(__name__)
#temporary storage for user names
player1=""
player2=""
score1=0
score2=0
#get index page
@app.route('/')
def get_index():
    #get all players for leader board
    players=db.get_all()
    return render_template('index.html',player1=player1,player2=player2,players=players,score1=score1,score2=score2)
#update score
@app.route('/update_score',methods=['POST'])
def update_score():
    global player1
    global player2
    global score1
    global score2

            #end game logic
    def check_winner():
        if score1>10 and score1>(score2+2) or score2>10 and score2>(score1+2):
            if score1>score2:
                db.update_games(player1)
            else:
                db.update_games(player2)
            db.reset_score(player1)
            db.reset_score(player2)

    if request.method=='POST':
        pname=request.form['pname']
        if pname=="p1":
            db.update_score(player1)
            score1=db.get_score(player1)
            check_winner()
        else:
            db.update_score(player2)
            score2=db.get_score(player2)
            check_winner()

    return redirect(url_for('get_index'))





#update games

#add player
@app.route('/add_player',methods=['POST'])
def add_player():
    if request.method=='POST':
        db.add_player(request.form['pname'])

    return redirect(url_for('get_index'))

#player join
@app.route('/player1_join',methods=['POST'])
def join1():
    global player1
    global score1
    if request.method=='POST':
        if len(request.form['p1name'])>1:
            res=db.get_player(request.form['p1name'])
            if res is not -1:
                player1=res[0]
                score1=res[2]

    return redirect(url_for('get_index'))

#player join
@app.route('/player2_join',methods=['POST'])
def join2():
    global player2
    global score2
    if request.method=='POST':
        if len(request.form['p2name'])>1:
            res=db.get_player(request.form['p2name'])
            if res is not -1:
                player2=res[0]
                score2=res[2]

    return redirect(url_for('get_index'))

if __name__=='__main__':
     app.run(host='127.0.0.1', port=8080, debug=True)
