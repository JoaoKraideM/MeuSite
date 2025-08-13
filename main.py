# app.py - Backend Python
from flask import Flask, render_template, request, flash, redirect, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO, emit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.template_folder = 'templates'
app.static_folder = 'static'

# Initialize extensions
csrf = CSRFProtect(app)
socketio = SocketIO(app)

# Import routes after app is created to avoid circular imports
from views import *

# Inicia o servidor
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)