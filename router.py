from app import app
from app.views.aptv import views
from flask import render_template

@app.route('/')
def index():
    return views.index()

@app.route('/<country>/<lang>')
def landing_page(country, lang):
    return views.landing(country=country, lang=lang)

@app.route('/<country>/<lang>/collection/<collection_id>')
def collection_page(country, lang, collection_id):
    return views.collection(country=country, lang=lang, collection_id=collection_id)

@app.route('/<country>/<lang>/bundle/<bundle_id>')
def bundle_page(country, lang, bundle_id):
    return views.bundle(country=country, lang=lang, bundle_id=bundle_id)

@app.route('/<country>/<lang>/room/<room_id>')
def room_page(country, lang, room_id):
    return views.room(country=country, lang=lang, room_id=room_id)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('aptv/404.html', title = '404'), 404
