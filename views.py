#Imports
from datetime import datetime, timedelta
from main import *
from flask import flash, redirect, request, render_template
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import requests

#variavel do env
load_dotenv()  

#Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    try:
        email_remetente = request.form['email']
        assunto = request.form['subject']
        mensagem = request.form['message']

        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        smtp_user = os.getenv('SMTP_USER')
        smtp_password = os.getenv('SMTP_PASSWORD')
        destinatario = os.getenv('DESTINATARIO')

        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = destinatario
        msg['Subject'] = f"{assunto} (De: {email_remetente})"
        msg['Reply-To'] = email_remetente  # Para facilitar resposta direta ao visitante

        corpo = f"""
        Nova mensagem do formulário:

        De: {email_remetente}
        Assunto: {assunto}

        Mensagem:
        {mensagem}
        """

        msg.attach(MIMEText(corpo, 'plain'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)

        return redirect('/')

    except Exception as e:
        return redirect('/')
    
@app.route('/api/github-contributions')
def github_contributions():
    try:
        username = "JoaoKraideM"  # Substitua pelo seu username
        token = os.getenv('GITHUB_TOKEN')  # Token do .env
        
        # Configuração básica de headers
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Python-Flask-App'  
        }
        
        # Adiciona token se existir
        if token:
            headers['Authorization'] = f'token {token}'
        
        # 1. Verifica primeiro se o usuário existe
        user_url = f'https://api.github.com/users/{username}'
        user_response = requests.get(user_url, headers=headers, timeout=10)
        
        if user_response.status_code != 200:
            return jsonify({
                "error": "Usuário não encontrado no GitHub",
                "status": user_response.status_code
            }), 404
        
        # 2. Obtém os eventos públicos
        events_url = f'https://api.github.com/users/{username}/events/public'
        events_response = requests.get(events_url, headers=headers, timeout=10)
        
        if events_response.status_code != 200:
            return generate_simulated_data(username)
        
        events = events_response.json()
        
        # 3. Processa os eventos
        contributions = process_github_events(events)
        
        return jsonify({
            "username": username,
            "year": datetime.now().year,
            "total": sum(c['count'] for c in contributions),
            "contributions": contributions,
            "source": "GitHub API"
        })
        
    except requests.exceptions.Timeout:
        return jsonify({
            "error": "Timeout ao conectar com a API do GitHub",
            "solution": "Tente novamente mais tarde"
        }), 504
    except Exception as e:
        print(f"Erro interno: {str(e)}")

def process_github_events(events):
    """Processa eventos reais do GitHub para o formato do gráfico"""
    contributions = {}
    
    # Processa cada evento
    for event in events:
        if 'created_at' not in event:
            continue
            
        date_str = event['created_at'][:10] 
        
        # Contabiliza o tipo de evento
        if event['type'] in ['PushEvent', 'PullRequestEvent', 'IssueCommentEvent']:
            contributions[date_str] = contributions.get(date_str, 0) + 1
    
    # Preenche os últimos 371 dias (53 semanas)
    today = datetime.now()
    full_contributions = []
    
    for i in range(371):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        count = contributions.get(date_str, 0)
        
        full_contributions.append({
            "date": date_str,
            "count": count,
            "intensity": min(count // 7, 4)  
        })
    
    return full_contributions[::-1]  

