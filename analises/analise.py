import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações para melhor visualização
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10

# Caminho do CSV
CSV_PATH = "../ocorrencias.csv"

# ---------------------------
# 1️⃣ Carregar dados e Pré-processamento
# ---------------------------
df = pd.read_csv(CSV_PATH)

# Conversão de tipos e extração de features temporais
df['dia'] = pd.to_datetime(df['dia'], errors='coerce')
df = df.dropna(subset=['dia']) # Remover linhas com datas inválidas
df['mes'] = df['dia'].dt.month
df['ano'] = df['dia'].dt.year
df['dia_semana'] = df['dia'].dt.day_name() # Nomes dos dias da semana em inglês por padrão # Nomes dos dias da semana em português
df['hora_int'] = pd.to_datetime(df['hora'], format="%H:%M", errors='coerce').dt.hour
df = df.dropna(subset=['hora_int']) # Remover linhas com horas inválidas

# Mapeamento para ordenar os dias da semana corretamente
dia_semana_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['dia_semana'] = pd.Categorical(df['dia_semana'], categories=dia_semana_ordem, ordered=True)

# Criar colunas auxiliares para crimes específicos (manter para análises específicas)
df['furto'] = df['tipo_de_crime'].apply(lambda x: 1 if x.lower() == 'furto' else 0)
df['estupro'] = df['tipo_de_crime'].apply(lambda x: 1 if x.lower() == 'estupro' else 0)

print("Pré-processamento concluído. Dados carregados e features temporais extraídas.")

# ---------------------------
# 2️⃣ Análise Exploratória Geral
# ---------------------------

# Distribuição de Crimes por Tipo
plt.figure(figsize=(14, 7))
sns.countplot(data=df, y='tipo_de_crime', order=df['tipo_de_crime'].value_counts().index, palette='viridis')
plt.title('Distribuição de Ocorrências por Tipo de Crime')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Tipo de Crime')
plt.tight_layout()
plt.savefig('distribuicao_crimes_tipo.png')
plt.show()

# Top 10 Bairros com Mais Ocorrências
plt.figure(figsize=(14, 7))
sns.countplot(data=df, y='bairro', order=df['bairro'].value_counts().head(10).index, palette='magma')
plt.title('Top 10 Bairros com Mais Ocorrências Criminais')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Bairro')
plt.tight_layout()
plt.savefig('top10_bairros_crimes.png')
plt.show()

# Ocorrências ao Longo dos Anos
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='ano', palette='cividis')
plt.title('Ocorrências Criminais por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('ocorrencias_por_ano.png')
plt.show()

print("Análises exploratórias gerais concluídas.")

# ---------------------------
# 3️⃣ Padrões Temporais
# ---------------------------

# Ocorrências de Lesão Corporal por Dia da Semana
lesao_por_dia_semana = (
    df[df['tipo_de_crime'] == 'Lesão Corporal']
    .groupby('dia_semana')
    .size()
    .reindex(dia_semana_ordem, fill_value=0)
)

plt.figure(figsize=(12, 6))
sns.barplot(x=lesao_por_dia_semana.index, y=lesao_por_dia_semana.values, palette='Purples')
plt.title('Ocorrências de Lesão Corporal por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('lesao_por_dia_semana.png')
plt.show()


# Ocorrências por Hora do Dia
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='hora_int', palette='viridis')
plt.title('Ocorrências Criminais por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('ocorrencias_por_hora_dia.png')
plt.show()

# Heatmap: Ocorrências por Dia da Semana e Hora (Geral)
heatmap_geral_data = df.groupby(['dia_semana', 'hora_int']).size().unstack(fill_value=0)
if not heatmap_geral_data.empty:
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_geral_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=.5)
    plt.title('Ocorrências Criminais por Dia da Semana e Hora (Geral)')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Dia da Semana')
    plt.tight_layout()
    plt.savefig('heatmap_geral_dia_hora.png')
    plt.show()
else:
    print("Não há dados suficientes para gerar o heatmap geral.")

print("Análises de padrões temporais concluídas.")

# ---------------------------
# 4️⃣ Análises Específicas (Melhorias nas análises existentes)
# ---------------------------

# Hora x Furto (Somente ocorrências de furto) - Melhorado
plt.figure(figsize=(12, 6))
sns.countplot(data=df[df['furto'] == 1], x='hora_int', color='red', palette='Reds_d')
plt.title('Crimes de Furto por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Quantidade de Ocorrências de Furto')
plt.tight_layout()
plt.savefig('furto_por_hora.png')
plt.show()

# Hora x Cidade x Furto (facetas) - Melhorado com melhor palette e ajuste de título
g = sns.catplot(
    data=df[df['furto'] == 1], 
    x='hora_int', 
    col='cidade', 
    kind='count', 
    col_wrap=2, 
    height=4, 
    aspect=1.2, 
    palette='Oranges_d', 
    sharey=False # Importante para ver a distribuição em cada cidade individualmente
)
g.set_axis_labels('Hora do Dia', 'Número de Furtos')
g.set_titles('Cidade: {col_name}')
plt.suptitle('Crimes de Furto por Hora do Dia em Cada Cidade', y=1.02) # Ajusta o título geral
plt.tight_layout(rect=[0, 0.03, 1, 0.98])
plt.savefig('furto_por_hora_cidade.png')
plt.show()

# Tipo de Crime x Status da Investigação - Melhorado com ordenação e percentual
status_counts = df.groupby(['tipo_de_crime', 'status_investigacao']).size().unstack(fill_value=0)
status_percentages = status_counts.apply(lambda x: x / x.sum(), axis=1)
status_percentages_flat = status_percentages.stack().reset_index(name='percentage')

plt.figure(figsize=(16, 8))
sns.barplot(data=status_percentages_flat, x='tipo_de_crime', y='percentage', hue='status_investigacao', palette='Set2', dodge=True)
plt.title('Proporção do Status da Investigação por Tipo de Crime')
plt.xlabel('Tipo de Crime')
plt.ylabel('Proporção')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Status da Investigação', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('status_investigacao_por_crime_proporcao.png')
plt.show()

print("Análises específicas aprimoradas concluídas.")

# ---------------------------
# 5️⃣ Análise de Correlação (Exemplo para features numéricas)
# ---------------------------
# Para esta análise, precisaremos de mais features numéricas ou codificar as categóricas
# Aqui, um exemplo simples com as features temporais e a 'target' se tivéssemos uma
# Como não temos uma 'target' numérica direta para correlação aqui, vamos focar em features existentes

# Exemplo de correlação entre features temporais (se fizesse sentido)
# corr_data = df[['mes', 'ano', 'hora_int']].corr()
# plt.figure(figsize=(8, 6))
# sns.heatmap(corr_data, annot=True, cmap='coolwarm', fmt='.2f')
# plt.title('Matriz de Correlação de Features Temporais')
# plt.tight_layout()
# plt.savefig('correlacao_features_temporais.png')
# plt.show()

print("Script de análise e visualização aprimorado criado.")

