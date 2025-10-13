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

# Converter coluna de data
df["dia"] = pd.to_datetime(df["dia"], format="%Y-%m-%d", errors="coerce")

# Converter hora em formato HH:MM (sem timezone)
df["hora_str"] = pd.to_datetime(df["hora"], format="%H:%M", errors="coerce").dt.strftime("%H:%M")

# Criar coluna combinada de data e hora
df["data_hora"] = df.apply(lambda row: pd.to_datetime(str(row["dia"].date()) + " " + row["hora_str"]), axis=1)

# Extrair features temporais
df["dia_semana_num"] = df["data_hora"].dt.dayofweek  # 0=Segunda, 6=Domingo
df["hora_do_dia"] = df["data_hora"].dt.hour
df["mes"] = df["data_hora"].dt.month
df["ano"] = df["data_hora"].dt.year

# ---------------------------
# 3️⃣ Codificação de variáveis categóricas
# ---------------------------

# Criar mapeamentos
bairros_map = {bairro: i for i, bairro in enumerate(df["bairro"].unique())}
cidades_map = {cidade: i for i, cidade in enumerate(df["cidade"].unique())}
tipos_crime_map = {tipo: i for i, tipo in enumerate(df["tipo_de_crime"].unique())}
status_investigacao_map = {status: i for i, status in enumerate(df["status_investigacao"].unique())}

# Aplicar codificação
df["bairro_encoded"] = df["bairro"].map(bairros_map)
df["cidade_encoded"] = df["cidade"].map(cidades_map)
df["tipo_crime_encoded"] = df["tipo_de_crime"].map(tipos_crime_map)
df["status_investigacao_encoded"] = df["status_investigacao"].map(status_investigacao_map)

# Salvar mapeamentos (para uso futuro na API)
joblib.dump(bairros_map, "../api/bairros_map.pkl")
joblib.dump(cidades_map, "../api/cidades_map.pkl")
joblib.dump(tipos_crime_map, "../api/tipos_crime_map.pkl")
joblib.dump(status_investigacao_map, "../api/status_investigacao_map.pkl")

# ---------------------------
# 4️⃣ Dataset para classificação
# ---------------------------

# Features contextuais
context_features = [
    "dia_semana_num", "hora_do_dia", "mes", "ano",
    "bairro_encoded", "cidade_encoded", "tipo_crime_encoded"
]

# Contextos positivos (onde crimes ocorreram)
positive_contexts = df[context_features].drop_duplicates().copy()
positive_contexts["target"] = 1

# Gerar contextos negativos aleatórios (2x o número de positivos)
np.random.seed(42)
num_negative_samples = len(positive_contexts) * 2

negative_data = {
    "dia_semana_num": np.random.choice(df["dia_semana_num"].unique(), num_negative_samples),
    "hora_do_dia": np.random.choice(df["hora_do_dia"].unique(), num_negative_samples),
    "mes": np.random.choice(df["mes"].unique(), num_negative_samples),
    "ano": np.random.choice(df["ano"].unique(), num_negative_samples),
    "bairro_encoded": np.random.choice(df["bairro_encoded"].unique(), num_negative_samples),
    "cidade_encoded": np.random.choice(df["cidade_encoded"].unique(), num_negative_samples),
    "tipo_crime_encoded": np.random.choice(df["tipo_crime_encoded"].unique(), num_negative_samples),
}
negative_contexts = pd.DataFrame(negative_data)
negative_contexts["target"] = 0

# Remover duplicatas e sobreposição entre positivos e negativos
positive_tuples = set(tuple(row) for row in positive_contexts[context_features].itertuples(index=False))
negative_tuples = set(tuple(row) for row in negative_contexts[context_features].itertuples(index=False))
unique_negative_tuples = list(negative_tuples - positive_tuples)

negative_contexts_filtered = pd.DataFrame(unique_negative_tuples, columns=context_features)
negative_contexts_filtered["target"] = 0

# Dataset final
classification_df = pd.concat([positive_contexts, negative_contexts_filtered], ignore_index=True)

# ---------------------------
# 5️⃣ Treino e Avaliação
# ---------------------------
X = classification_df[context_features]
y = classification_df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

xgb_classifier_model = XGBClassifier(
    objective="binary:logistic",
    eval_metric="logloss",
    use_label_encoder=False,
    n_estimators=200,
    random_state=42
)
xgb_classifier_model.fit(X_train, y_train)

# Avaliação
y_pred = xgb_classifier_model.predict(X_test)
y_proba = xgb_classifier_model.predict_proba(X_test)[:, 1]

print("\n=== XGBoost Classifier ===")
print(f"Accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall:    {recall_score(y_test, y_pred):.3f}")
print(f"F1-score:  {f1_score(y_test, y_pred):.3f}")
print(f"ROC AUC:   {roc_auc_score(y_test, y_proba):.3f}")

# ---------------------------
# 6️⃣ Salvar modelo treinado
# ---------------------------
joblib.dump(xgb_classifier_model, "../api/model.pkl")
print("✅ Modelo salvo como ../api/model.pkl")
