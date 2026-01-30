from flask import Flask, request, render_template, redirect
import json
import requests
import os
# importaciones locales
from models import db, Favorite


API_URL = 'https://rickandmortyapi.com/api/character'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "app.db")


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    page = request.args.get('page', 1)
    name = request.args.get('name')

    if name:
        response = requests.get(API_URL, params={'name':name})
        if response.status_code != 200:
            return render_template('index.html', caracters=[], search=True, error_message="Personaje no encontrado")
        data = response.json()
        return render_template('index.html', caracters=data['results'], search=True)

    else:
        response = requests.get(API_URL, params={'page':page})
        data = response.json() #call_api(API_URL, params={'page':2})
        return render_template(
            'index.html', 
            characters=data['results'], 
            info=data['info'],
            page=int(page),
            search=False
        )
    
@app.route('/save', methods=['POST'])
def save():
    api_id = request.form['api_id']
    name = request.form['name']
    image = request.form['image']
    page = request.form.get('page', 1)
    
    if not Favorite.query.filter_by(api_id).first():
        fav = Favorite(api_id=api_id, name=name, image=image)

        db.session.add(fav)
        db.seeion.commit()
    
    return redirect(f'/?page={page}')