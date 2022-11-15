from flask import Flask, render_template, request, jsonify, url_for, redirect

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://test:sparta@cluster0.mapsk1p.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.test

import hashlib


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/signup')
def sign_up():
    return render_template('signup.html')


@app.route('/api/checkid', methods=['POST'])
def check_id():
    c_id = 0
    id_receive = request.form['id_give']
    users = list(db.user.find({}, {'_id': False}))
    for user in users:
        user_id = user['id']
        if user_id == id_receive:
            c_id = 1
    return jsonify({'result': 'success', 'status': c_id})


@app.route('/api/checkname', methods=['POST'])
def check_name():
    c_name = 0
    name_receive = request.form['name_give']
    users = list(db.user.find({}, {'_id': False}))
    for user in users:
        user_name = user['user_name']
        if user_name == name_receive:
            c_name = 1
    return jsonify({'result': 'success', 'status': c_name})


@app.route('/api/checkmail', methods=['POST'])
def check_mail():
    c_mail = 0
    mail_receive = request.form['mail_give']
    users = list(db.user.find({}, {'_id': False}))
    for user in users:
        user_mail = user['mail']
        if user_mail == mail_receive:
            c_mail = 1
    return jsonify({'result': 'success', 'status': c_mail})


@app.route('/api/signup', methods=['POST'])
def join():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    mail_receive = request.form['mail_give']
    pw_receive = request.form['pw_give']

    # 패스워드 단방향 암호화
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'user_name': name_receive, 'mail': mail_receive, 'pw': pw_hash})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=3000, debug=True)
