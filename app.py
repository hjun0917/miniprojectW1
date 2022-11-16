from flask import Flask, render_template, request, jsonify

from dotenv import load_dotenv
import os
from pymongo import MongoClient
import certifi

####유튜브 크롤링 관련 모듈#####
# html 예쁘게 긁어오기 bs4
from bs4 import BeautifulSoup
# 동적페에지 크롤링 selenium
from selenium import webdriver

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


#유튜브 키워드 크롤링
@app.route('/crawling', methods=["POST"])
def web_crawling_youtube():
    #### 1. 사용자 키워드 및 크롤링 대상 url 세팅 ####
    keyword = '건강'
    target_url = 'https://www.youtube.com/results?search_query=' + keyword

    #### 2. 동적페이지 크롤링 ####
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가(백그라운드로 실행, 이걸 하지 않으면 브라우저 열어서 탐색하게 됨)
    options.add_argument("headless")

    # driver 실행
    driver = webdriver.Chrome(options=options)
    driver.get(target_url)

    #html 가져오기
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # driver 종료
    driver.quit()

    #### 3. 링크주소 추출 및 json 배열화 ####
    youtube_links = []
    if soup != None:
        i = 0
        j = 0
        for i in  range(0, 3, 1):
            j += 1
            crawling_link = soup.select_one('#contents > ytd-video-renderer:nth-child('+str(j)+') > #dismissible > ytd-thumbnail > #thumbnail')['href'].strip()
            crawling_link = crawling_link.replace('/watch?v=', '') #링크 식별값만 추출
            youtube_links.append({i:crawling_link}) #append : 배열 뒤로 추가

    return jsonify({'ytb_links':youtube_links})


if __name__ == '__main__':
    app.run('0.0.0.0', port=1500, debug=True)