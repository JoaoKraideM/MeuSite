#Imports
from main import *

#Rotas
@app.route('/')
def index():
    return render_template('index.html')

