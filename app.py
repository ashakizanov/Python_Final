from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from sqlalchemy import desc
from transformers import pipeline

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Password@localhost/CoinMarket'
db = SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    login=db.Column(db.String(200), nullable=False )
    password=db.Column(db.String(200), nullable=False )

    def __repr__(self):
        return '<Users %r>' % self.id
class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(200000), nullable=True)

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<Coin %r>' % self.id

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not find the user', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = Users.query.filter_by(login=auth.username).first()

    if not user:
        return make_response('Could not find the user with login '+ auth.username, 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if user.password == auth.password:
        return redirect('/coin')

    return make_response('Could not find the user with login '+ auth.username, 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@app.route('/coin', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        coin_name = request.form['name']
        url = 'https://coinmarketcap.com/ru/currencies/{0}'.format(coin_name)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        coin_content = str(soup.find_all('p'))
        new_coin = Coin(name=coin_name, content=coin_content)
        try:
            db.session.add(new_coin)
            db.session.commit()
            return redirect('/coin')
        except:
            return 'error'
    else:
        coins = Coin.query.order_by(desc(Coin.id)).first()
        url = 'https://coinmarketcap.com/ru/currencies/{0}'.format(coins.name)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('p')
        summarizer = pipeline("summarization")
        soups=[]
        for result in results:
            ARTICLE = ''.join(result.text)
            max_chunk = 500
            ARTICLE = ARTICLE.replace('.', '.<eos>')
            ARTICLE = ARTICLE.replace('?', '?<eos>')
            ARTICLE = ARTICLE.replace('!', '!<eos>')
            sentences = ARTICLE.split('<eos>')
            current_chunk = 0
            chunks = []
            for sentence in sentences:
                if len(chunks) == current_chunk + 1:
                    if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                        chunks[current_chunk].extend(sentence.split(' '))
                    else:
                        current_chunk += 1
                        chunks.append(sentence.split(' '))
                else:
                    chunks.append(sentence.split(' '))

            for chunk_id in range(len(chunks)):
                chunks[chunk_id] = ''.join(chunks[chunk_id])
            res = summarizer(chunks, max_length=30, min_length=0, do_sample=False)
            text = ''.join([summ['summary_text'] for summ in res])
            soups.append(text)
        return render_template('coin.html',str=str, soupp=soup.p, soupfindall=soup.find_all('p'), nname=coins.name, summarizer= soups,len=len)


if __name__ == "__main__":
    app.run(debug=True)