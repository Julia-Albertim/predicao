import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# ⚙️ CONFIGURAÇÕES GERAIS
# ---------------------------
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)
plt.rcParams["font.size"] = 10

CSV_PATH = "../ocorrencias.csv"  # Caminho do CSV

# ---------------------------
# 1️⃣ CARREGAR E PRÉ-PROCESSAR
# ---------------------------
df = pd.read_csv(CSV_PATH)

# Converter datas
df['dia'] = pd.to_datetime(df['dia'], errors='coerce')
df = df.dropna(subset=['dia'])
df['mes'] = df['dia'].dt.month
df['ano'] = df['dia'].dt.year

# Dia da semana já está em português no CSV
# Apenas criar a Categorical para ordenar corretamente
dia_semana_ordem = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira',
                    'Sexta-feira', 'Sábado', 'Domingo']
df['dia_semana'] = pd.Categorical(df['dia_semana'], categories=dia_semana_ordem, ordered=True)

# Converter hora (ex: "22:30" -> 22)
df['hora_int'] = pd.to_datetime(df['hora'], format="%H:%M", errors='coerce').dt.hour
df = df.dropna(subset=['hora_int'])

# Flags para crimes específicos
df['furto'] = df['tipo_crime'].apply(lambda x: 1 if str(x).lower() == 'furto' else 0)
df['estupro'] = df['tipo_crime'].apply(lambda x: 1 if str(x).lower() == 'estupro' else 0)

print("✅ Pré-processamento concluído com sucesso.")

# ---------------------------
# 2️⃣ ANÁLISE GERAL
# ---------------------------

# Distribuição de Crimes por Tipo
plt.figure(figsize=(14, 7))
sns.countplot(data=df, y='tipo_crime',
              order=df['tipo_crime'].value_counts().index,
              palette='viridis')
plt.title('Distribuição de Ocorrências por Tipo de Crime')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Tipo de Crime')
plt.tight_layout()
plt.savefig('distribuicao_crimes_tipo.png')
plt.show()

# Top 10 Bairros com Mais Ocorrências
plt.figure(figsize=(14, 7))
sns.countplot(data=df, y='bairro',
              order=df['bairro'].value_counts().head(10).index,
              palette='magma')
plt.title('Top 10 Bairros com Mais Ocorrências Criminais')
plt.xlabel('Número de Ocorrências')
plt.ylabel('Bairro')
plt.tight_layout()
plt.savefig('top10_bairros_crimes.png')
plt.show()
'''
# Ocorrências por Ano
plt.figure(figsize=(12, 6))
sns.countplot(data=df, x='ano', palette='cividis')
plt.title('Ocorrências Criminais por Ano')
plt.xlabel('Ano')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('ocorrencias_por_ano.png')
plt.show()
'''


# ---------------------------
# 3️⃣ PADRÕES TEMPORAIS
# ---------------------------

# Lesão Corporal por Dia da Semana
lesao_por_dia_semana = (
    df[df['tipo_crime'] == 'Lesão corporal']
    .groupby('dia_semana')
    .size()
    .reindex(dia_semana_ordem, fill_value=0)
)

plt.figure(figsize=(12, 6))
sns.barplot(x=lesao_por_dia_semana.index,
            y=lesao_por_dia_semana.values,
            palette='Purples')
plt.title('Lesões Corporais por Dia da Semana')
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

# Heatmap Dia da Semana x Hora
heatmap_data = df.groupby(['dia_semana', 'hora_int']).size().unstack(fill_value=0)
if not heatmap_data.empty:
    plt.figure(figsize=(14, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt='d', linewidths=.5)
    plt.title('Ocorrências por Dia da Semana e Hora')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Dia da Semana')
    plt.tight_layout()
    plt.savefig('heatmap_dia_hora.png')
    plt.show()

print("⏰ Análises temporais concluídas.")

# ---------------------------
# 4️⃣ ANÁLISES ESPECÍFICAS
# ---------------------------

# FURTO X HORA
plt.figure(figsize=(12, 6))
sns.countplot(data=df[df['furto'] == 1],
              x='hora_int',
              color='red',
              palette='Reds_d')
plt.title('Crimes de Furto por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Furtos')
plt.tight_layout()
plt.savefig('furto_por_hora.png')
plt.show()

# FURTO X HORA X CIDADE
g = sns.catplot(
    data=df[df['furto'] == 1],
    x='hora_int', col='cidade',
    kind='count', col_wrap=2, height=4, aspect=1.2,
    palette='Oranges_d', sharey=False
)
g.set_axis_labels('Hora do Dia', 'Número de Furtos')
g.set_titles('Cidade: {col_name}')
plt.suptitle('Crimes de Furto por Hora e Cidade', y=1.02)
plt.tight_layout(rect=[0, 0.03, 1, 0.98])
plt.savefig('furto_por_hora_cidade.png')
plt.show()

# STATUS DO CRIME X TIPO
status_counts = df.groupby(['tipo_crime', 'status_crime']).size().unstack(fill_value=0)
status_percent = status_counts.apply(lambda x: x / x.sum(), axis=1)
status_percent_flat = status_percent.stack().reset_index(name='percentual')

plt.figure(figsize=(16, 8))
sns.barplot(data=status_percent_flat,
            x='tipo_crime',
            y='percentual',
            hue='status_crime',
            palette='Set2', dodge=True)
plt.title('Proporção de Status do Crime por Tipo de Crime')
plt.xlabel('Tipo de Crime')
plt.ylabel('Proporção')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Status do Crime', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('status_crime_por_tipo.png')
plt.show()

print("🔍 Análises de furto e status concluídas.")

# ---------------------------
# 5️⃣ ANÁLISES DE ESTUPRO
# ---------------------------

# Estupro por Hora do Dia
plt.figure(figsize=(12, 6))
sns.countplot(data=df[df['estupro'] == 1],
              x='hora_int',
              color='purple',
              palette='Purples')
plt.title('Crimes de Estupro por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Ocorrências de Estupro')
plt.tight_layout()
plt.savefig('estupro_por_hora.png')
plt.show()

# Estupro por Dia da Semana
estupro_semana = (
    df[df['estupro'] == 1]
    .groupby('dia_semana')
    .size()
    .reindex(dia_semana_ordem, fill_value=0)
)

plt.figure(figsize=(12, 6))
sns.barplot(x=estupro_semana.index,
            y=estupro_semana.values,
            palette='pink')
plt.title('Crimes de Estupro por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('estupro_por_dia_semana.png')
plt.show()




# ---------------------------
# VIOLÊNCIA DOMÉSTICA E OUTROS PARÂMETROS
# ---------------------------

# Flag para Violência Doméstica
df['violencia_domestica'] = df['tipo_crime'].apply(lambda x: 1 if str(x).lower() == 'violência doméstica' else 0)

# Violência Doméstica por Dia da Semana
vd_semana = (
    df[df['violencia_domestica'] == 1]
    .groupby('dia_semana')
    .size()
    .reindex(dia_semana_ordem, fill_value=0)
)

plt.figure(figsize=(12, 6))
sns.barplot(x=vd_semana.index, y=vd_semana.values, palette='Reds')
plt.title('Violência Doméstica por Dia da Semana')
plt.xlabel('Dia da Semana')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('vd_por_dia_semana.png')
plt.show()

# Violência Doméstica por Hora do Dia
plt.figure(figsize=(12, 6))
sns.countplot(data=df[df['violencia_domestica'] == 1],
              x='hora_int',
              palette='Reds_d')
plt.title('Violência Doméstica por Hora do Dia')
plt.xlabel('Hora do Dia')
plt.ylabel('Número de Ocorrências')
plt.tight_layout()
plt.savefig('vd_por_hora.png')
plt.show()

# Heatmap de Violência Doméstica por Dia da Semana e Hora
vd_heatmap = df[df['violencia_domestica'] == 1].groupby(['dia_semana', 'hora_int']).size().unstack(fill_value=0)
if not vd_heatmap.empty:
    plt.figure(figsize=(14, 8))
    sns.heatmap(vd_heatmap, cmap='Reds', annot=True, fmt='d', linewidths=.5)
    plt.title('Violência Doméstica por Dia da Semana e Hora')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Dia da Semana')
    plt.tight_layout()
    plt.savefig('vd_heatmap_dia_hora.png')
    plt.show()

# Violência Doméstica por Cidade
vd_cidade = df[df['violencia_domestica'] == 1].groupby('cidade').size().sort_values(ascending=False)
plt.figure(figsize=(14, 7))
sns.barplot(x=vd_cidade.index, y=vd_cidade.values, palette='Reds_r')
plt.title('Violência Doméstica por Cidade')
plt.xlabel('Cidade')
plt.ylabel('Número de Ocorrências')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('vd_por_cidade.png')
plt.show()

print("🟣 Análises de estupro concluídas com sucesso.")
print("\n✅ Todas as análises concluídas e gráficos salvos com sucesso!")
