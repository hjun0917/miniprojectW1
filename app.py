from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://spartaA5:99a5@todomini.88lewxp.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

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

@app.route("/sample", methods=["GET"])
def sample_get():
    cheer_comments = list(db.fancomments.find({}, {'_id': False}))
    return jsonify(cheer_comments)

if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)