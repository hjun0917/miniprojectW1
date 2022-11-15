from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi

from flask import Flask, render_template, jsonify

from routes.login import login
from routes.main import main
from routes.sign_up import sign_up

app.register_blueprint(login, url_prefix="/login")
app.register_blueprint(main, url_prefix="/main")
app.register_blueprint(sign_up, url_prefix="/sign_up")

load_dotenv()
DB = os.getenv('DB')
client = MongoClient(DB, tlsCAFile=certifi.where())

db = client.dbminiW1


print("success")

@app.route('/')
def home():
    return render_template('main.html')

@app.route("/todo", methods=["POST"])
def todo_post():
    todo_tesk = request.form['todo_tesk']
    num = len(list(db.todo.find({},{'_id':False}))) + 1
    done = 0
    doc = {'todo_tesk': todo_tesk, 'num': num, 'done': done}
    db.todo.insert_one(doc)

    return jsonify({'msg': '작성 완료!'})

@app.route("/todo", methods=["GET"])
def sample_get():
    todoList = list(db.todo.find({}, {'_id': False}))
    return jsonify(todoList)

@app.route("/tododone", methods=["POST"])
def done_post():
    item_num = request.form['give_itemNum']
    type(item_num)
    db.todo.update_one({'num':item_num},{'$set':{'done':1}})

    return jsonify({'msg': '목표 달성!'});

if __name__ == '__main__':
    app.run('0.0.0.0', port=1500, debug=True)