from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import pandas as pd
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///selectQ.db'
db = SQLAlchemy(app)

class selectQ(db.Model):
    __tablename__ = 'selectQ'
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(200), nullable = False)
    answer = db.Column(db.String(200), nullable = False)
    dummy_answer1 = db.Column(db.String(200), nullable = False)
    dummy_answer2 = db.Column(db.String(200), nullable = False)
    dummy_answer3 = db.Column(db.String(200), nullable = False)

"""clm = ["words", "meaning"]
df = pd.DataFrame(columns=clm)
df.to_csv('words.csv')"""

"""clm = ["date", "sum", "rate"]
df = pd.DataFrame(columns=clm)
df.to_csv('daily.csv')"""

@app.before_first_request
def init():
    db.create_all()

@app.route('/')
def index():
    clm = ["bool"]
    df = pd.DataFrame(columns=clm)
    df.to_csv('bool.csv')
    return render_template('index.html')

@app.route('/make')
def make():
    return render_template('make.html')

@app.route('/select', methods=['POST', 'GET'])
def select():
    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')
        dummy_answer1 = request.form.get('dummy_answer1')
        dummy_answer2 = request.form.get('dummy_answer2')
        dummy_answer3 = request.form.get('dummy_answer3')

        post = selectQ(question=question, answer=answer, dummy_answer1=dummy_answer1, dummy_answer2=dummy_answer2, dummy_answer3=dummy_answer3)

        db.session.add(post)
        db.session.commit()
        return redirect('/dblist')
    else:
        return render_template('select.html')

@app.route('/dblist', methods=['POST', 'GET'])
def dblist():
    if request.method == 'GET':
        posts = selectQ.query.all()
        return render_template('dblist.html', posts=posts)

@app.route('/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    post = selectQ.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.question = request.form.get('question')
        post.answer = request.form.get('answer')
        post.dummy_answer1 = request.form.get('dummy_answer1')
        post.dummy_answer2 = request.form.get('dummy_answer2')
        post.dummy_answer3 = request.form.get('dummy_answer3')

        db.session.commit()
        return redirect('/dblist')

@app.route('/answer')
def answer():
    return render_template('answer.html')

@app.route('/selectanswer', methods=['POST', 'GET'])
def marubatsu():
    rows = db.session.query(selectQ).count()
    num3 = random.randrange(1, rows+1, 1)
    selectans= selectQ.query.get(num3)
    if request.method == 'POST':
        kaitoo = request.form.get('answer')
        if kaitoo == 'true':
            df = pd.read_csv('bool.csv', index_col=0)
            a = "T"
            bools = df.append({'bool':a}, ignore_index=True)
            bools.to_csv('bool.csv')
            return render_template('maru.html')
        else:
            df = pd.read_csv('bool.csv', index_col=0)
            b = "F"
            bools = df.append({'bool':b}, ignore_index=True)
            bools.to_csv('bool.csv')
            return render_template('batsu.html')
    else:
        num2 = random.randrange(0, 4)
        if num2 == 0:
            return render_template('selectanswer.html', selectans=selectans)
        elif num2 == 1:
            return render_template('selectanswer1.html', selectans=selectans)
        elif num2 == 2:
            return render_template('selectanswer2.html', selectans=selectans)
        else:
            return render_template('selectanswer3.html', selectans=selectans)

@app.route('/word', methods=['POST', 'GET'])
def word():
    if request.method == 'POST':
        word = request.form.get('word')
        meaning = request.form.get('meaning')
        a = {'words' : word, 'meaning':meaning}
        df1 = pd.read_csv('words.csv',index_col=0)
        words = df1.append(a, ignore_index=True)
        words.to_csv('words.csv')
        df2 = pd.read_csv('words.csv',index_col=0)
        return render_template('wordslist.html', tbl=df2.values.tolist(), ind=df2.index.tolist())
    else:
        return render_template('word.html')

@app.route('/<int:id>/worddelete', methods=['GET'])
def worddelete(id):
    df2 = pd.read_csv('words.csv',index_col=0)
    words = df2.drop(id)
    words.to_csv('words.csv')
    wlist = pd.read_csv('words.csv',index_col=0)
    return render_template('wordslist.html', tbl=wlist.values.tolist(), ind=wlist.index.tolist())

@app.route('/temp')
def aaa():
    df = pd.read_csv('words.csv',index_col=0)
    rows = len(df)
    global num
    num = random.randrange(0, rows+1, 1)
    return redirect('/wordanswer')

@app.route('/wordanswer', methods=['POST', 'GET'])
def wordanswer():
    df = pd.read_csv('words.csv',index_col=0)
    randomlist = df.iloc[num]
    question = randomlist['words']
    answer = randomlist['meaning']
    if request.method == 'POST':
        kaitoo = request.form.get('answer')
        if kaitoo == answer:
            df = pd.read_csv('bool.csv', index_col=0)
            a = "T"
            bools = df.append({'bool':a}, ignore_index=True)
            bools.to_csv('bool.csv')
            return render_template('maru2.html')
        else:
            df = pd.read_csv('bool.csv', index_col=0)
            b = "F"
            bools = df.append({'bool':b}, ignore_index=True)
            bools.to_csv('bool.csv')
            return render_template('batsu2.html', answer=answer)
    else:
        return render_template('wordanswer.html', question=question)

@app.route('/result')
def result():
    df = pd.read_csv('bool.csv')
    all = len(df)
    T_num = (df == "T").sum().sum()
    rate = T_num*100 / all
    day = datetime.datetime.today().date()
    a = {'date':day,'sum':all,'rate':rate}
    df1 = pd.read_csv('daily.csv',index_col=0)
    daily = df1.append(a, ignore_index=True)
    daily.to_csv('daily.csv')
    return render_template('result.html', rate=rate)

@app.route('/daily')
def daily():
    df = pd.read_csv('daily.csv', index_col=0)
    return render_template('daily.html', tbl=df.values.tolist(), ind=df.index.tolist())
    

if __name__ == '__main__':
    app.run()