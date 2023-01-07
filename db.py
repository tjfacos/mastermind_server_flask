import pymongo
import os

CLIENT_URI = os.environ["MONGO_URI"]
# print(CLIENT_URI)

client = pymongo.MongoClient(CLIENT_URI)
db = client["mastermindDB"]
users_collection = db["users"]
games_collection = db["games"]



def verifyUser(username, password): #Assess user exists, and password is correct
    
    query = {"username": username, "password": password}
    
    userdoc = users_collection.find_one(query)
    
    if userdoc:
        return True
    
    return False

def createUser(username, password): #Create new user (unique username)
    if not users_collection.find_one({
        "username": username
    }):
        users_collection.insert_one({
            "username": username,
            "password": password
        })
    
        return verifyUser(username, password)
    
    else:
        return "Error: username taken"

def changePassword(username, old_password, new_password):
    if verifyUser(username, old_password):
        users_collection.update_one(
            {"username": username},
            {
                "$set": {
                    "password": new_password
                }
            }
        )

        return verifyUser(username, new_password)

    else:
            return "Error: Invalid User"

def postScore(username, password, score):
    if verifyUser(username, password):
        games_collection.insert_one({
            "user": username,
            "score": score
        })

def getUserStats(username, password): #Return username, average score, and personal best
    if verifyUser(username, password):
        user_data = games_collection.find({
            "user": username
        })
        
        average = 0
        personal_best = 0
        num_entries = 0
        for entry in user_data:
            num_entries += 1
            score = entry["score"]
            if score > personal_best:
                personal_best = score

            average += score
        
        average = round(average / num_entries)

        return average, personal_best
    else:
        return "Error: Invalid User"


def getLeaderboard(): #Return usernames and score for top 5 scores in collection
    user_data = db.games.find(sort = [("score", -1)])
    user_array = []
    for x in user_data:
        user_array.append(x)
    print(len(user_array))
    leaderboard = []
    
    for i in range(5):
        print(i)
        print(i == len(user_array))
        if i == len(user_array):
            break
        
        leaderboard.append({
            "user": user_array[i]["user"],
            "score": user_array[i]["score"]
        })
        
    return leaderboard


if __name__ == "__main__":
       
    print(getLeaderboard())