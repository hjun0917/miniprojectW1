from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi

app = Flask(__name__)

load_dotenv()
DB = os.getenv('DB')
client = MongoClient(DB, tlsCAFile=certifi.where())

db = client.dbminiW1


@app.route("/")
def home():
    return render_template('cover.html')

@app.route("/main/")
def main_home():
    return render_template('main.html') 

@app.route("/main/todo", methods=["POST"])
def todo_post():
    todo_tesk = request.form['todo_tesk']
    today = request.form['today']

    num = len(list(db.todo.find({},{'_id':False}))) + 1
    done = 0
    doc = {'today': today, 'todo_tesk': todo_tesk, 'num': num, 'done': done}
    db.todo.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})

@app.route("/main/todo", methods=["GET"])
def sample_get():
    todoList = list(db.todo.find({}, {'_id': False}))
    return jsonify(todoList)

@app.route("/main/tododone", methods=["POST"])
def done_post():
    item_num = int(request.form['give_itemNum'])
    doneNum = db.todo.find_one({'num':item_num})['done']
    
    if doneNum == 1:
        db.todo.update_one({'num':item_num},{'$set':{'done':0}})
    elif doneNum == 0:
        db.todo.update_one({'num':item_num},{'$set':{'done':1}})
        

    return jsonify({'msg': 'Todo 갱신'});

if __name__ == '__main__':
    app.run('0.0.0.0', port=1500, debug=True)