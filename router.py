from app import app
from app.views.aptv import views

@app.route('/')
def index():
    return views.index()

@app.route('/<country>/<lang>')
def landing_page(country, lang):
    return views.landing(country=country, lang=lang)

@app.route('/<country>/<lang>/collection/<collection_id>')
def collection_page(country, lang, collection_id):
    return views.collection(country=country, lang=lang, collection_id=collection_id)

