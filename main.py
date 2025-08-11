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
csrf = CSRFProtect(app)
app.secret_key = os.getenv('SECRET_KEY')
app.template_folder = 'templates'
app.static_folder = 'static'
app.css_folder = 'static/css'

# Importa as rotas do arquivo views.py
from views import *

# Inicia o servidor
