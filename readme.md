# Deploy fastAPI to Heroku using Docker

[FastAPI](https://fastapi.tiangolo.com/) Modern, fast, web framework for Python  
[Docker](https://www.docker.com/) Containerization software  
[Heroku](https://www.heroku.com/) Hosting platform

## Requirements

[Git](https://git-scm.com/) (or just download the repo)  
[Heroku cli](https://devcenter.heroku.com/articles/heroku-cli) (to run the heroku commands)


## db backend

https://github.com/vicogarcia16/fastapi_airtable


## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/wanghaisheng/fastapi-docker-heroku)

## Instructions


>https://link-discovery.herokuapp.com/sitemap/?url=


https://link-discovery.herokuapp.com/sitemap/?url=https://x.hacking8.com/



#
https://github.com/sfu-db/connector-x/discussions/270

https://github.com/juanretamales/DataframeToDB




import connectorx as cx

postgres_url = "postgresql://username:password@server:port/database"
query = "SELECT * FROM lineitem"

cx.read_sql(postgres_url, query)





import pandas as pd
import dataframetodb
from dataframetodb import Table, refactor
from datetime import datetime
import os

nametable = "nameTable"
engine = dataframetodb.create_engine('sqlite:///{}.sqlite'.format(nametable)) #create engine for use SQLAlchemy
df = pd.read_csv("./dataset/data.csv") # Get the DataFrame
df = refactor(df) # Returns a dataframe with the correct dtype compatible with DataframeToDB.
table_class = Table(name=nametable, df=df) #create Table instance
table_class.toDb(df, engine, 'append') #insert data in database, in this example sqlite



$ pip install sqlmodel
## supabase


https://app.supabase.io/


## firebase

from flask import Flask, render_template, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)
# app.config['SECRET_KEY']= os.getenv('key')
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()


links = (
    ('/', 'Homepage'),
    ('/add_form', 'Add new country'),
    ('/list', 'View all countries'),
)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    heading = 'Flask Country Application'
    description = 'Flask application for countries adding and listing with Firebase.'
    return render_template('index.html', heading=heading, description=description, links=links)


@app.route('/add_form', methods=['GET', 'HEAD'])
def add_form():
    # TODO: Add Flask-WTF for form validation
    heading = 'Add country'
    description = 'Fill in the form and press Create butoon'
    return render_template('add_form.html', heading=heading,
                           description=description, links=links), 200


@app.route('/add', methods=['POST'])
def add_country():
    try:
        c = {
            'name': request.form['name'],
            'area': request.form['area'],
            'population': request.form['population'],
            'density': request.form['density'],
        }
        country_ref = db.collection(u'Countries').document(c['name'])
        country_ref.set(c)
        return render_template('success.html', country=c,
                               heading='Country created successfully!',
                               description='Your country was added to database',
                               links=links), 200
    except Exception as e:
        return f"An Error occured: {e}"


@app.route('/list')
def list_all_countries():
    try:
        country_ref = db.collection(u'Countries')
        # Check if ID was passed to URL query
        # country_id = request.args.get('id')
        # if country_id:
        #     c = country_ref.document(country_id).get()
        #     return jsonify(c.to_dict()), 200
        countries = [doc.to_dict() for doc in country_ref.stream()]
        return render_template('list.html', countries=countries,
                                heading='All countries',
                                description='Table displays all countries in a database',
                                   inks=links), 200
    except Exception as e:
        return f"An Error Occured: {e}"


if __name__ == '__main__':
    app.run()



```
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter

class Potato(BaseModel):
    id: int
    color: str
    mass: float

app = FastAPI()
app.include_router(CRUDRouter(schema=Potato))
```
https://github.com/awtkns/fastapi-crudrouter



https://github.com/tokusumi/fastapi-cloudauth

