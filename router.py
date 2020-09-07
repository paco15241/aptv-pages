from app import app
from app.views.aptv import views

@app.route('/', methods=['GET'])
def index():
    return views.index()
