from flask import Flask, request, jsonify
from db import *

app = Flask(__name__)

@app.route('/user/<name>/<password>', methods = ['GET', 'POST']) 
def userhandler(name, password):
    if request.method == "GET":
        #get user stats
        if verifyUser(name, password):
            data = getUserStats(name, password)

            return jsonify({
                "average": data[0],
                "personal_best": data[1]
            })
        else:
            return "401" #Not authorised
    
    elif request.method == "POST":
        
        if createUser(name, password) == True:
            return "200" #Success
        else:
            return "500" #Failure
    
    else:
        return "Error: method not available"

@app.route('/change_password/<name>/<current>/<new>', methods = ['GET']) 
def changeUserPassword(name, current, new):
    if verifyUser(name, current):
        changePassword(name, current, new)
        return "200"
    else:
        return "500"

@app.route('/verify/<name>/<password>', methods = ['GET']) 
def verify(name, password):
    if verifyUser(name, password):
        return "200"
    else:
        return "500"

@app.route('/leaderboard', methods = ['GET']) 
def leaderboard():
    leaderboard = getLeaderboard()
    board_dict = {}
    for i in range(len(leaderboard)):
        board_dict[i+1] = leaderboard[i]

    return jsonify(board_dict)

@app.route('/score/<name>/<password>/<score>', methods = ["POST"])
def postUserScore(name, password, score):
    if verifyUser(name, password):
        print("verified")
        postScore(name, password, int(score))
        return "200"

def main():
    app.run(host="0.0.0.0", port=5000)

main()