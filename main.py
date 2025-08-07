# app.py - Backend Python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Configuração do Flask
app = Flask(__name__)
app.template_folder = 'templates'
app.static_folder = 'static'
app.css_folder = 'static/css'

# Importa as rotas do arquivo views.py
from views import *

# Inicia o servidor
if __name__ == '__main__':
    socketio = SocketIO(app)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)