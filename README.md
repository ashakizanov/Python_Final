## TITLE

Final Project
## Installation

To get started with the application you need to intsall following PyPl:
``` bash 
pip install flask
pip install flask-sqlalchemy
pip install bs4
pip install requests
pip install transformers
```

## Usage
```
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
from sqlalchemy import desc
```

## Create table in your database
```
Create table Coin()
```

## connect to DataBase
```bash
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:PASSWORD@localhost/CoinMarket'
db = SQLAlchemy(app)

Examples:
postgresql://user:passwoed@localhost/mydatabase
mysql://user:passwoed@localhost/mydatabase
oracle://user:passwoed@127.0.0.1:1521/mydatabase
```

```shell
$ python3 src/app.py
```

##Sources
```bash
pyjwt (https://pyjwt.readthedocs.io/en/stable/)
flask (https://flask.palletsprojects.com/en/2.0.x/)
flask_sqlalchemy (https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
requests  (https://pypi.org/project/requests/)
beautifulSoup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
transformers (https://huggingface.co/transformers/installation.html)
```

# Done by
Amirkhan Shakizan, Altair Tussupov, Ayan Aitkulov
