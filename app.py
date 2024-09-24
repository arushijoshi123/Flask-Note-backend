
from flask import Flask,request,jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
app=Flask(__name__)
client =MongoClient("mongodb+srv://joshiarushi025:1234Arushi@cluster0.hiwfnvb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client["flaskDatabase"]
notesCollection =db['notes']
userCollection=db['users']

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello world"

@app.route("/one")
def one():
    return "you are on page one"

@app.route("/a/<id>")
def printId(id):
    return f"this is my id {id}"


@app.errorhandler(404)
def notFound(e):
    return e

# post request
@app.route("/submit",methods=["POST"])
def submit():
    data= request.get_json()
    return jsonify({
        "data":data,
        "message":"receiverdddddddd"


    })
    
#adding note
@app.route('/addNote',methods=['POST'])    
def addNote():
    
    data= request.json
 
    note={
        'noteTitle':data.get('title'),
        'noteDesc':data.get('desc'),
        'userId':data.get('userId')

    }
    result=notesCollection.insert_one(note)
    # note['_id']=str(result.inserted_id)
    note['_id']=str(note["_id"])
    return  note


# getting all notes
@app.route('/getAllNotes',methods=['GET'])
def getAllNotes():
    allNotes=list(notesCollection.find())
    for note in allNotes:
        note['_id']=str(note['_id'])
    return jsonify({
        'note':allNotes,
        'status':"202",
        "message":"notes retrieved successfullyyy!!!"
    })
# get notes by userid
@app.route("/note/<id>",methods=['GET'])
def getNoteById(id):
    try:
        notes=list(notesCollection.find({'userId':id}))
        for note in notes:
            note['_id']=str(note['_id'])
        return jsonify ({
            'note':notes,
           
            "status":"200"

        })
    except Exception as e:
        return e

# update note
@app.route("/updateNote/<id>",methods=['PUT'])
def updateNote(id):
    data= request.json
    try:
        updatedFieldDict={}
        for key in data:
            updatedFieldDict[key]=data[key]
           
        id = ObjectId(id)    #upar s id string format m aru h    
        print(id)
        result=notesCollection.find_one_and_update(
            {"_id":id},#kya cheez s find krna h
            {"$set":updatedFieldDict}#update specified field in the doc not affect other fields
            ,return_document= True
         )
        result["_id"]=str(result["_id"])
        return jsonify ({
            "noteUpdated":result,
            "message":"successfully updated !"
        })
    except Exception as e:
        return e
    

# delete note
@app.route("/deleteNote/<id>",methods=['DELETE'])
def deleteNote(id):
    id = ObjectId(id)
    result = notesCollection.find_one_and_delete({"_id":id})
    # result["_id"]=str(result["_id"])
   
    return jsonify({
    #   "deletedNote":result,
      "message":"Deleted successfully !!"
    })


# user signup function
@app.route("/signUp",methods=["POST"])
def signUp():
    data= request.json
    user={
        "userName":data.get("userName"),
        "password":data.get("password")
    }
    try:
        existingUser = userCollection.find_one({"userName":data.get("userName")})
        print(existingUser)
        if not existingUser:
            result=userCollection.insert_one(user)
            user['_id']=str(user['_id'])#here user]['_id'] is same as result.inserted_id
            return jsonify({
                "user":user,
                "message":" signup successfull !"
            })
        else:
            return "use exists already"
    except Exception as e:
        return e
# user signIn
@app.route("/signIn",methods=['POST'])
def signIn():
    data =request.json
    try:
        existingUser= userCollection.find_one({"userName":data['userName']})
        if (existingUser):
            if(data['password']==existingUser["password"]):
                return jsonify({
                    "message": "sign in successful",
                    "userId": str(existingUser['_id']),
                    "userName":existingUser['userName']
                })
            else:
               return jsonify({
                    "message": "wrong password"
                })
            
        else:
            return "user not found"
    except Exception as e:
        return e    
        
    
