
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Carregar o modelo e os mapeamentos
try:
    model = joblib.load("model.pkl")
    bairros_map = joblib.load("bairros_map.pkl")
    cidades_map = joblib.load("cidades_map.pkl")
    tipos_crime_map = joblib.load("tipos_crime_map.pkl")
    status_investigacao_map = joblib.load("status_investigacao_map.pkl") # Embora não usado na previsão, é bom ter
except Exception as e:
    print(f"Erro ao carregar arquivos do modelo: {e}")
    model = None
    bairros_map = {}
    cidades_map = {}
    tipos_crime_map = {}
    status_investigacao_map = {}

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Modelo não carregado. Verifique os logs do servidor."}), 500

    data = request.get_json(force=True)

    # Extrair e mapear features
    dia_str = data.get("dia") # Ex: "2024-10-27"
    hora_str = data.get("hora") # Ex: "14:30" ou None
    cidade = data.get("cidade")
    bairro = data.get("bairro")
    tipo_crime = data.get("tipo_crime")

    if not all([dia_str, cidade, bairro, tipo_crime]):
        return jsonify({"error": "Campos obrigatórios ausentes: dia, cidade, bairro, tipo_crime"}), 400

    try:
        # Processar data e hora
        data_hora_obj = pd.to_datetime(dia_str + " " + (hora_str if hora_str else "00:00"))
        dia_semana_num = data_hora_obj.dayofweek
        hora_do_dia = data_hora_obj.hour
        mes = data_hora_obj.month
        ano = data_hora_obj.year

        # Mapear variáveis categóricas
        bairro_encoded = bairros_map.get(bairro)
        cidade_encoded = cidades_map.get(cidade)
        tipo_crime_encoded = tipos_crime_map.get(tipo_crime)

        if any(val is None for val in [bairro_encoded, cidade_encoded, tipo_crime_encoded]):
            missing_maps = []
            if bairro_encoded is None: missing_maps.append(f"Bairro '{bairro}' não encontrado no mapeamento.")
            if cidade_encoded is None: missing_maps.append(f"Cidade '{cidade}' não encontrada no mapeamento.")
            if tipo_crime_encoded is None: missing_maps.append(f"Tipo de crime '{tipo_crime}' não encontrado no mapeamento.")
            return jsonify({"error": "Erro de mapeamento", "details": missing_maps}), 400

        # Criar DataFrame para previsão
        features = pd.DataFrame([[dia_semana_num, hora_do_dia, mes, ano, bairro_encoded, cidade_encoded, tipo_crime_encoded]],
                                columns=["dia_semana_num", "hora_do_dia", "mes", "ano", "bairro_encoded", "cidade_encoded", "tipo_crime_encoded"])

        # Fazer a previsão de probabilidade
        probability = model.predict_proba(features)[:, 1][0] # Probabilidade da classe positiva (crime)

        return jsonify({"probabilidade_crime": round(probability * 100, 2)})

    except Exception as e:
        return jsonify({"error": f"Erro no processamento da requisição: {e}"}), 500

@app.route("/metadata", methods=["GET"])
def metadata():
    return jsonify({
        "bairros": list(bairros_map.keys()),
        "cidades": list(cidades_map.keys()),
        "tipos_crime": list(tipos_crime_map.keys())
    })

if __name__ == "__main__":
    app.run(debug=True, host=\"0.0.0.0\", port=5000)

