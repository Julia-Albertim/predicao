import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from xgboost import XGBClassifier
import joblib

# ---------------------------
# 1️⃣ Carregar CSV
# ---------------------------
df = pd.read_csv("../ocorrencias.csv")

# ---------------------------
# 2️⃣ Pré-processamento e Feature Engineering
# ---------------------------
df["dia"] = pd.to_datetime(df["dia"], format="%Y-%m-%d")
df["hora_str"] = pd.to_datetime(df["hora"]).dt.strftime("%H:%M")
df["data_hora"] = df.apply(lambda row: pd.to_datetime(str(row["dia"]).split(" ")[0] + " " + row["hora_str"]), axis=1)
df["dia_semana_num"] = df["data_hora"].dt.dayofweek
df["hora_do_dia"] = df["data_hora"].dt.hour
df["mes"] = df["data_hora"].dt.month
df["ano"] = df["data_hora"].dt.year

# Garante uma ordem consistente para os mapeamentos
bairros_map = {bairro: i for i, bairro in enumerate(sorted(df["bairro"].unique()))}
cidades_map = {cidade: i for i, cidade in enumerate(sorted(df["cidade"].unique()))}
tipos_crime_map = {tipo: i for i, tipo in enumerate(sorted(df["tipo_de_crime"].unique()))}

df["bairro_encoded"] = df["bairro"].map(bairros_map)
df["cidade_encoded"] = df["cidade"].map(cidades_map)
df["tipo_crime_encoded"] = df["tipo_de_crime"].map(tipos_crime_map)

# Salvar os mapeamentos para uso na API
# Certifique-se de que o caminho '../api/' existe
import os
os.makedirs("../api", exist_ok=True)
joblib.dump(bairros_map, "../api/bairros_map.pkl")
joblib.dump(cidades_map, "../api/cidades_map.pkl")
joblib.dump(tipos_crime_map, "../api/tipos_crime_map.pkl")

# ... (Sua lógica de criação de contextos positivos e negativos continua a mesma) ...
# ---------------------------
# 3️⃣ Criar dataset para Classificação
# ---------------------------
context_features = ['dia_semana_num', 'hora_do_dia', 'mes', 'ano', 'bairro_encoded', 'cidade_encoded', 'tipo_crime_encoded']
positive_contexts = df[context_features].drop_duplicates().copy()
positive_contexts['target'] = 1

all_bairros = df['bairro_encoded'].unique()
all_tipos_crime = df['tipo_crime_encoded'].unique()
all_dias_semana = range(7)
all_horas_dia = range(24)
all_meses = range(1, 13)
all_anos = df['ano'].unique()

# Determinando cidade para cada bairro para gerar amostras negativas mais realistas
bairro_cidade_map = df.drop_duplicates(subset='bairro_encoded')[['bairro_encoded', 'cidade_encoded']].set_index('bairro_encoded')['cidade_encoded'].to_dict()

num_negative_samples = len(positive_contexts) * 2
np.random.seed(42)

# Gerando amostras negativas
neg_bairros = np.random.choice(all_bairros, num_negative_samples)
negative_data = {
    'dia_semana_num': np.random.choice(all_dias_semana, num_negative_samples),
    'hora_do_dia': np.random.choice(all_horas_dia, num_negative_samples),
    'mes': np.random.choice(all_meses, num_negative_samples),
    'ano': np.random.choice(all_anos, num_negative_samples),
    'bairro_encoded': neg_bairros,
    'cidade_encoded': [bairro_cidade_map.get(b, -1) for b in neg_bairros],
    'tipo_crime_encoded': np.random.choice(all_tipos_crime, num_negative_samples),
}
negative_contexts = pd.DataFrame(negative_data)
negative_contexts['target'] = 0
negative_contexts = negative_contexts.drop_duplicates(subset=context_features)
positive_contexts_tuples = {tuple(x) for x in positive_contexts[context_features].to_numpy()}
negative_contexts = negative_contexts[~negative_contexts[context_features].apply(tuple, axis=1).isin(positive_contexts_tuples)]

classification_df = pd.concat([positive_contexts, negative_contexts], ignore_index=True)
X = classification_df[context_features]
y = classification_df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ---------------------------
# 4️⃣ XGBoost Classifier com Correção
# ---------------------------

# CORREÇÃO: Calcular e usar o scale_pos_weight
# Isso diz ao modelo para dar mais importância à classe minoritária (crime)
count_neg = y_train.value_counts()[0]
count_pos = y_train.value_counts()[1]
scale_pos_weight_value = count_neg / count_pos
print(f"Scale Pos Weight: {scale_pos_weight_value:.2f}")

xgb_classifier_model = XGBClassifier(
    objective='binary:logistic', 
    eval_metric='logloss', 
    use_label_encoder=False, 
    n_estimators=200, 
    random_state=42,
    scale_pos_weight=scale_pos_weight_value  # <-- PARÂMETRO ADICIONADO
)
xgb_classifier_model.fit(X_train, y_train)

# ... (Sua avaliação e salvamento continuam os mesmos) ...
y_pred_xgb_class = xgb_classifier_model.predict(X_test)
y_proba_xgb_class = xgb_classifier_model.predict_proba(X_test)[:, 1]
print("\n=== XGBoost Classifier (Corrigido) ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred_xgb_class):.3f}")
print(f"Precision: {precision_score(y_test, y_pred_xgb_class):.3f}")
print(f"Recall: {recall_score(y_test, y_pred_xgb_class):.3f}")
print(f"F1-Score: {f1_score(y_test, y_pred_xgb_class):.3f}")
print(f"ROC AUC: {roc_auc_score(y_test, y_proba_xgb_class):.3f}")

joblib.dump(xgb_classifier_model, "../api/model.pkl")
print("Modelo XGBoost Classifier salvo como ../api/model.pkl")