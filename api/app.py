import os
import pickle
import joblib # Usar joblib para carregar os mapeamentos
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# --- CARREGAMENTO DE DADOS E MODELOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    # Carrega o modelo de ML
    with open(os.path.join(BASE_DIR, 'model.pkl'), 'rb') as f:
        model = pickle.load(f)
    
    # CORREÇÃO: Carrega os mapeamentos salvos pelo script de treino
    bairros_map = joblib.load(os.path.join(BASE_DIR, 'bairros_map.pkl'))
    cidades_map = joblib.load(os.path.join(BASE_DIR, 'cidades_map.pkl'))
    tipos_crime_map = joblib.load(os.path.join(BASE_DIR, 'tipos_crime_map.pkl'))

    # Carrega os dados geográficos para o frontend
    df_bairros_geo = pd.read_csv(
        os.path.join(BASE_DIR, 'coords_bairros_geocoded.csv'),
        dtype={"latitude": float, "longitude": float} 
    )
    df_bairros_geo.dropna(inplace=True)

except FileNotFoundError as e:
    raise RuntimeError(f"Erro ao carregar arquivos .pkl ou .csv: {e}. Execute o script de treino primeiro.")


# Extrai as listas de nomes para o /metadata a partir dos mapeamentos carregados
cidades_unicas = sorted(cidades_map.keys())
tipos_crime_unicos = sorted(tipos_crime_map.keys())

# --- ROTAS DA APLICAÇÃO ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/metadata')
def get_metadata():
    bairros_com_coords = df_bairros_geo.to_dict('records')
    metadata = {
        "cidades": cidades_unicas,
        "bairros": bairros_com_coords, 
        "tipos_crime": tipos_crime_unicos
    }
    return jsonify(metadata)


# ... (A rota /predict e o resto do código permanecem os mesmos da versão anterior) ...
@app.route('/predict', methods=['POST'])
def predict_risk():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Corpo da requisição JSON ausente."}), 400

        bairro_req = data.get('bairro')
        cidade_req = data.get('cidade')
        tipo_crime_req = data.get('tipo_crime')
        data_str = data.get('dia')
        hora_str = data.get('hora', '00:00')

        if not all([bairro_req, cidade_req, tipo_crime_req, data_str]):
             return jsonify({"error": "Dados insuficientes para predição."}), 400

        data_obj = datetime.strptime(data_str, '%Y-%m-%d')
        hora_obj = datetime.strptime(hora_str, '%H:%M')

        input_data = pd.DataFrame([{
            'dia_semana_num': data_obj.weekday(),
            'hora_do_dia': hora_obj.hour,
            'mes': data_obj.month,
            'ano': data_obj.year,
            'bairro_encoded': bairros_map.get(bairro_req, -1),
            'cidade_encoded': cidades_map.get(cidade_req, -1),
            'tipo_crime_encoded': tipos_crime_map.get(tipo_crime_req, -1)
        }])

        features_para_prever = [
            'dia_semana_num', 'hora_do_dia', 'mes', 'ano', 
            'bairro_encoded', 'cidade_encoded', 'tipo_crime_encoded'
        ]
        X_pred = input_data[features_para_prever]
        
        # --- DEBUG PRINTS ---
        print("\n--- DADOS ENVIADOS PARA O MODELO ---")
        print(X_pred.to_string())
        
        raw_prediction = model.predict_proba(X_pred)
        
        print("\n--- RESPOSTA BRUTA DO MODELO ---")
        print(f"Probabilidades (Classe 0, Classe 1): {raw_prediction}")
        # --------------------

        probabilidade = raw_prediction[0][1]
        
        probabilidade_percent = round(float(probabilidade) * 100, 2)
        
        print(f"\nProbabilidade de CRIME (Classe 1) extraída: {probabilidade_percent}%\n")

        return jsonify({
            "probabilidade_crime": probabilidade_percent
        })

    except Exception as e:
        app.logger.error(f"Erro na rota /predict: {e}")
        return jsonify({"error": "Ocorreu um erro interno no servidor.", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)