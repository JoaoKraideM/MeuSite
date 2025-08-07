# app.py - Backend Python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Configuração do Flask
app = Flask(__name__)
app.template_folder = 'Statics/templates'
app.static_folder = 'Statics/imgs'

# Importa as rotas do arquivo views.py
from views import *

# Inicia o servidor
if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)