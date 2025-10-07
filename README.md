# Sistema de Previsão de Crimes

Este projeto consiste em uma aplicação web interativa para prever a probabilidade de ocorrência de crimes em diferentes localidades da Região Metropolitana do Recife, utilizando um modelo de Machine Learning (XGBoost Classifier).

## Estrutura do Projeto

```
seu_projeto/
├── api/                     # Backend da aplicação (API Flask)
│   ├── app.py               # Lógica da API e carregamento do modelo
│   ├── model.pkl            # Modelo XGBoost Classifier treinado
│   ├── bairros_map.pkl      # Mapeamento de bairros para IDs numéricos
│   ├── cidades_map.pkl      # Mapeamento de cidades para IDs numéricos
│   ├── tipos_crime_map.pkl  # Mapeamento de tipos de crime para IDs numéricos
│   ├── status_investigacao_map.pkl # Mapeamento de status de investigação (não usado na API, mas gerado)
│   └── requirements.txt     # Dependências Python para o backend
├── notebooks/               # Notebooks e scripts de análise e treinamento do modelo
│   └── analise_e_treinamento.py # Script para pré-processamento, treinamento e salvamento do modelo
├── static/                  # Arquivos estáticos do frontend (CSS, JS)
│   ├── css/
│   │   └── style.css        # Estilos da aplicação
│   └── js/
│       └── script.js        # Lógica JavaScript do frontend e interação com o mapa
├── templates/               # Arquivos HTML do frontend
│   └── index.html           # Página principal da aplicação
├── ocorrencias.csv          # Conjunto de dados brutos de ocorrências
└── requirements.txt         # Dependências Python para o ambiente geral
```

## Como Configurar e Rodar o Projeto

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### Pré-requisitos

Certifique-se de ter o Python 3.8+ e `pip` instalados em sua máquina.

### 1. Clonar o Repositório (se aplicável) ou Navegar até a Pasta do Projeto

Se você recebeu o projeto como um arquivo ZIP, descompacte-o. Se for um repositório Git, clone-o:

```bash
git clone <URL_DO_REPOSITORIO>
cd seu_projeto
```

### 2. Configurar o Ambiente Python

É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

```bash
python3 -m venv venv
source venv/bin/activate  # No Linux/macOS
# venv\Scripts\activate   # No Windows
```

### 3. Instalar as Dependências

Instale todas as bibliotecas Python necessárias usando o arquivo `requirements.txt` fornecido:

```bash
pip install -r requirements.txt
```

### 4. Treinar e Salvar o Modelo (se ainda não o fez)

O modelo de Machine Learning e os mapeamentos de variáveis categóricas são gerados pelo script `analise_e_treinamento.py`. Se os arquivos `.pkl` não estiverem presentes na pasta `api/`, você precisará executá-lo:

```bash
python3 notebooks/analise_e_treinamento.py
```

Este script irá gerar:
- `api/model.pkl`: O modelo XGBoost Classifier treinado.
- `api/bairros_map.pkl`
- `api/cidades_map.pkl`
- `api/tipos_crime_map.pkl`
- `api/status_investigacao_map.pkl`

### 5. Iniciar a API Backend

Navegue até a pasta `api` e inicie o servidor Flask:

```bash
cd api
python3 app.py
```

O servidor da API estará rodando em `http://0.0.0.0:5000` (ou `http://127.0.0.1:5000`). Mantenha este terminal aberto.

### 6. Acessar o Frontend

Com a API rodando, abra o arquivo `seu_projeto/templates/index.html` em seu navegador web. Você pode fazer isso diretamente pelo explorador de arquivos ou usando um servidor web local simples (como o `http.server` do Python, se necessário para alguns recursos do navegador).

```bash
# Em um novo terminal, na raiz do projeto (seu_projeto/)
python3 -m http.server 8000
# Então, abra seu navegador e vá para http://localhost:8000/templates/index.html
```

Você poderá interagir com os filtros, visualizar o mapa e obter as previsões de probabilidade de crime.

## Uso da Aplicação

1.  **Filtros de Consulta:** Selecione a cidade, bairro, tipo de crime, data e, opcionalmente, a hora nos campos fornecidos.
2.  **Analisar Probabilidade:** Clique no botão "Analisar Probabilidade" para enviar os dados para a API e receber a previsão.
3.  **Resultado da Análise:** A probabilidade de ocorrência de crime será exibida em percentual, juntamente com uma barra visual.
4.  **Mapa de Histórico:** O mapa exibirá um marcador na localização do bairro consultado, com a probabilidade de crime no popup.

## Sugestões de Melhoria

*   **Dados de Localização:** Atualmente, as coordenadas dos bairros são estáticas no `script.js`. Para uma solução mais robusta, considere integrar uma API de geocodificação (ex: Google Maps API, OpenStreetMap Nominatim) para obter coordenadas dinamicamente.
*   **Dados de Não-Ocorrências:** A geração de contextos negativos no script de treinamento é uma simplificação. A precisão do modelo pode ser melhorada com dados reais de locais e horários onde *não* houve ocorrências de crime.
*   **Interface do Usuário:** Melhorar a experiência do usuário com feedback visual mais rico, validação de formulário em tempo real e talvez um histórico de consultas.
*   **Escalabilidade:** Para um ambiente de produção, considere usar um servidor WSGI (como Gunicorn ou uWSGI) para a aplicação Flask e um servidor web (como Nginx ou Apache) para servir os arquivos estáticos e atuar como proxy reverso.

---

**Autor:** Manus AI
**Data:** Outubro de 2025

