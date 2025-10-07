
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
# Ajustando tipos de dados
df["dia"] = pd.to_datetime(df["dia"], format="%Y-%m-%d")
# Extrair apenas a parte da hora como string para evitar problemas de fuso horário e facilitar o mapeamento
df["hora_str"] = pd.to_datetime(df["hora"]).dt.strftime("%H:%M")

# Criar uma coluna de data e hora combinada para facilitar a extração de features
df["data_hora"] = df.apply(lambda row: pd.to_datetime(str(row["dia"]).split(" ")[0] + " " + row["hora_str"]), axis=1)

# Extrair features de tempo
df["dia_semana_num"] = df["data_hora"].dt.dayofweek # 0=Segunda, 6=Domingo
df["hora_do_dia"] = df["data_hora"].dt.hour
df["mes"] = df["data_hora"].dt.month
df["ano"] = df["data_hora"].dt.year

# Codificação de variáveis categóricas
# Usaremos Label Encoding para simplicidade, mas One-Hot Encoding pode ser considerado para mais precisão
# Para a API, precisaremos manter os mapeamentos

bairros_map = {bairro: i for i, bairro in enumerate(df["bairro"].unique())}
cidades_map = {cidade: i for i, cidade in enumerate(df["cidade"].unique())}
tipos_crime_map = {tipo: i for i, tipo in enumerate(df["tipo_de_crime"].unique())}
status_investigacao_map = {status: i for i, status in enumerate(df["status_investigacao"].unique())}

df["bairro_encoded"] = df["bairro"].map(bairros_map)
df["cidade_encoded"] = df["cidade"].map(cidades_map)
df["tipo_crime_encoded"] = df["tipo_de_crime"].map(tipos_crime_map)
df["status_investigacao_encoded"] = df["status_investigacao"].map(status_investigacao_map)

# Salvar os mapeamentos para uso na API
joblib.dump(bairros_map, "../api/bairros_map.pkl")
joblib.dump(cidades_map, "../api/cidades_map.pkl")
joblib.dump(tipos_crime_map, "../api/tipos_crime_map.pkl")
joblib.dump(status_investigacao_map, "../api/status_investigacao_map.pkl")

# ---------------------------
# 3️⃣ Criar dataset para Classificação
# ---------------------------
# Definir as features que representam um 'contexto' para a previsão
context_features = ['dia_semana_num', 'hora_do_dia', 'mes', 'ano', 'bairro_encoded', 'cidade_encoded', 'tipo_crime_encoded']

# Criar um DataFrame com contextos únicos onde crimes ocorreram (target = 1)
positive_contexts = df[context_features].drop_duplicates().copy()
positive_contexts['target'] = 1

# Para criar contextos onde *não* houve crime (target = 0), precisamos de um conjunto de dados mais amplo.
# Uma abordagem comum é gerar amostras aleatórias de contextos válidos (dia, hora, local, tipo de crime)
# e assumir que, se não estão nos dados de ocorrências, não houve crime.
# Isso é uma simplificação e pode ser refinado com dados de 'não-ocorrências' reais se disponíveis.

# Gerar contextos negativos aleatórios (ex: 2x o número de positivos para balancear)
all_bairros = df['bairro_encoded'].unique()
all_cidades = df['cidade_encoded'].unique()
all_tipos_crime = df['tipo_crime_encoded'].unique()
all_dias_semana = df['dia_semana_num'].unique()
all_horas_dia = df['hora_do_dia'].unique()
all_meses = df['mes'].unique()
all_anos = df['ano'].unique()

num_negative_samples = len(positive_contexts) * 2 # Exemplo: 2x mais amostras negativas

np.random.seed(42) # Para reprodutibilidade
negative_data = {
    'dia_semana_num': np.random.choice(all_dias_semana, num_negative_samples),
    'hora_do_dia': np.random.choice(all_horas_dia, num_negative_samples),
    'mes': np.random.choice(all_meses, num_negative_samples),
    'ano': np.random.choice(all_anos, num_negative_samples),
    'bairro_encoded': np.random.choice(all_bairros, num_negative_samples),
    'cidade_encoded': np.random.choice(all_cidades, num_negative_samples),
    'tipo_crime_encoded': np.random.choice(all_tipos_crime, num_negative_samples),
}
negative_contexts = pd.DataFrame(negative_data)
negative_contexts['target'] = 0

# Remover duplicatas de contextos negativos
negative_contexts = negative_contexts.drop_duplicates(subset=context_features)

# Filtrar contextos negativos que também aparecem como positivos
# Convertendo DataFrames para tuples para usar em set operations
positive_contexts_tuples = set(tuple(row) for row in positive_contexts[context_features].itertuples(index=False))
negative_contexts_tuples = set(tuple(row) for row in negative_contexts[context_features].itertuples(index=False))

# Encontrar contextos que estão em negative_contexts_tuples mas não em positive_contexts_tuples
unique_negative_contexts_tuples = list(negative_contexts_tuples - positive_contexts_tuples)

# Converter de volta para DataFrame
negative_contexts_filtered = pd.DataFrame(unique_negative_contexts_tuples, columns=context_features)
negative_contexts_filtered['target'] = 0

# Combinar os datasets
classification_df = pd.concat([positive_contexts, negative_contexts_filtered], ignore_index=True)

# Features e target para o modelo de classificação
X = classification_df[context_features]
y = classification_df['target']

# Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# ---------------------------
# 4️⃣ XGBoost Classifier
# ---------------------------
xgb_classifier_model = XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, n_estimators=200, random_state=42)
xgb_classifier_model.fit(X_train, y_train)

# Previsões e avaliação
y_pred_xgb_class = xgb_classifier_model.predict(X_test)
y_proba_xgb_class = xgb_classifier_model.predict_proba(X_test)[:, 1] # Probabilidade da classe positiva

accuracy = accuracy_score(y_test, y_pred_xgb_class)
precision = precision_score(y_test, y_pred_xgb_class)
recall = recall_score(y_test, y_pred_xgb_class)
f1 = f1_score(y_test, y_pred_xgb_class)
roc_auc = roc_auc_score(y_test, y_proba_xgb_class)

print("\n=== XGBoost Classifier ===")
print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1-Score: {f1:.3f}")
print(f"ROC AUC: {roc_auc:.3f}")

# ---------------------------
# 5️⃣ Salvar o modelo treinado
# ---------------------------
joblib.dump(xgb_classifier_model, "../api/model.pkl")
print("Modelo XGBoost Classifier salvo como ../api/model.pkl")

