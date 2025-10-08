import os
import io
import pickle
import joblib
import random
import string
import numpy as np
import pandas as pd
from functools import wraps
from datetime import datetime
from captcha.image import ImageCaptcha
# REMOVIDO: werkzeug.security não é mais necessário
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS

# --- 1. CONFIGURAÇÃO INICIAL DA APLICAÇÃO ---
app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)
app.secret_key = 'chave-secreta-para-manter-a-sessao-segura'

# --- 2. SISTEMA DE LOGIN E SEGURANÇA (SIMPLIFICADO) ---
# Usuário: admin, Senha: senha123
# MODIFICADO: A senha agora está em texto plano, sem hash.
users = {
    "admin": {
        "password": "senha123"
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- 3. CARREGAMENTO DE DADOS E MODELOS DE ML ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(BASE_DIR, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    bairros_map = joblib.load(os.path.join(BASE_DIR, 'bairros_map.pkl'))
    cidades_map = joblib.load(os.path.join(BASE_DIR, 'cidades_map.pkl'))
    tipos_crime_map = joblib.load(os.path.join(BASE_DIR, 'tipos_crime_map.pkl'))
    df_bairros_geo = pd.read_csv(
        os.path.join(BASE_DIR, 'coords_bairros_geocoded.csv'),
        dtype={"latitude": float, "longitude": float} 
    )
    df_bairros_geo.dropna(inplace=True)
except FileNotFoundError as e:
    raise RuntimeError(f"Erro ao carregar arquivos .pkl ou .csv: {e}. Execute o script de treino primeiro.")

cidades_unicas = sorted(cidades_map.keys())
tipos_crime_unicos = sorted(tipos_crime_map.keys())

# --- 4. ROTAS DA APLICAÇÃO ---

# 4.1 Rotas de Autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        captcha_input = request.form['captcha']
        user_data = users.get(username)
        if 'captcha_text' not in session or captcha_input.lower() != session['captcha_text'].lower():
            return "Erro: CAPTCHA incorreto! Volte e tente novamente."
        
        # MODIFICADO: Comparação direta de senhas, sem hash.
        if user_data is None or user_data['password'] != password:
            return "Erro: Usuário ou senha inválidos! Volte e tente novamente."
            
        session['user_id'] = username
        session.pop('captcha_text', None)
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/captcha.png')
def generate_captcha():
    try:
        captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        session['captcha_text'] = captcha_text
        
        image = ImageCaptcha()
        data = image.generate(captcha_text) # 'data' já é o objeto de imagem em memória (_io.BytesIO)
        
        return send_file(data, mimetype='image/png')
        
    except Exception as e:
        app.logger.error(f"ERRO AO GERAR IMAGEM DO CAPTCHA: {e}")
        return "Erro interno ao gerar CAPTCHA", 500

# 4.2 Rotas do Sistema Principal (Protegidas)
@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/metadata')
@login_required
def get_metadata():
    bairros_com_coords = df_bairros_geo.to_dict('records')
    metadata = {
        "cidades": cidades_unicas,
        "bairros": bairros_com_coords, 
        "tipos_crime": tipos_crime_unicos
    }
    return jsonify(metadata)

@app.route('/predict', methods=['POST'])
@login_required
def predict_risk():
    try:
        data = request.get_json()
        if not data: return jsonify({"error": "Corpo da requisição JSON ausente."}), 400
        bairro_req = data.get('bairro')
        cidade_req = data.get('cidade')
        tipo_crime_req = data.get('tipo_crime')
        data_str = data.get('dia')
        hora_str = data.get('hora', '00:00')
        if not all([bairro_req, cidade_req, tipo_crime_req, data_str]):
             return jsonify({"error": "Dados insuficientes para predição."}), 400
        data_obj = datetime.strptime(data_str, '%Y-%m-%d')
        hora_obj = datetime.strptime(hora_str, '%H:%M')
        input_data = pd.DataFrame([{'dia_semana_num': data_obj.weekday(),'hora_do_dia': hora_obj.hour,'mes': data_obj.month,'ano': data_obj.year,'bairro_encoded': bairros_map.get(bairro_req, -1),'cidade_encoded': cidades_map.get(cidade_req, -1),'tipo_crime_encoded': tipos_crime_map.get(tipo_crime_req, -1)}])
        features_para_prever = ['dia_semana_num', 'hora_do_dia', 'mes', 'ano', 'bairro_encoded', 'cidade_encoded', 'tipo_crime_encoded']
        X_pred = input_data[features_para_prever]
        raw_prediction = model.predict_proba(X_pred)
        probabilidade = raw_prediction[0][1]
        probabilidade_percent = round(float(probabilidade) * 100, 2)
        return jsonify({"probabilidade_crime": probabilidade_percent})
    except Exception as e:
        app.logger.error(f"Erro na rota /predict: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor.", "details": str(e)}), 500

# --- 5. EXECUÇÃO DA APLICAÇÃO ---
if __name__ == '__main__':
    # MODIFICADO: Removida a lógica de geração de hash.
    app.run(debug=True)

