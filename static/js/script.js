// Inicializar o mapa
const map = L.map('map').setView([-8.0476, -34.8770], 11); // Coordenadas de Recife

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);


// --- Variáveis Globais ---
// REMOVIDO: A variável gigante 'bairrosCoordenadas' foi apagada.
let bairrosData = []; // Irá guardar os dados dos bairros (com coordenadas) vindos da API.
let currentMarkers = [];


// Carregar metadados (cidades, bairros, tipos de crime)
async function loadMetadata() {
    try {
        const response = await fetch('http://localhost:5000/metadata');
        const data = await response.json();

        // MODIFICADO: Guarda os dados completos dos bairros na nossa variável global
        bairrosData = data.bairros;

        // Preencher dropdown de cidades (sem alteração)
        const cidadeSelect = document.getElementById('cidade');
        data.cidades.forEach(cidade => {
            const option = document.createElement('option');
            option.value = cidade;
            option.textContent = cidade;
            cidadeSelect.appendChild(option);
        });

        // MODIFICADO: Preenche dropdown de bairros usando os dados da API
        const bairroSelect = document.getElementById('bairro');
        bairrosData.forEach(bairroInfo => {
            const option = document.createElement('option');
            option.value = bairroInfo.bairro; // O valor é o nome do bairro
            option.textContent = bairroInfo.bairro; // O texto também
            bairroSelect.appendChild(option);
        });

        // Preencher dropdown de tipos de crime (sem alteração)
        const tipoCrimeSelect = document.getElementById('tipo_crime');
        data.tipos_crime.forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo;
            option.textContent = tipo;
            tipoCrimeSelect.appendChild(option);
        });

    } catch (error) {
        console.error('Erro ao carregar metadados:', error);
        alert('Erro ao carregar dados. Certifique-se de que a API está rodando.');
    }
}

// Enviar formulário e obter previsão
document.getElementById('prediction-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = {
        dia: document.getElementById('dia').value,
        hora: document.getElementById('hora').value || '00:00',
        cidade: document.getElementById('cidade').value,
        bairro: document.getElementById('bairro').value,
        tipo_crime: document.getElementById('tipo_crime').value
    };

    try {
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            // Exibir resultado
            const resultSection = document.getElementById('result-section');
            const probabilityValue = document.getElementById('probability-value');
            const probabilityFill = document.getElementById('probability-fill');

            probabilityValue.textContent = `${data.probabilidade_crime}%`;
            probabilityFill.style.width = `${data.probabilidade_crime}%`;

            resultSection.style.display = 'block';

            // Atualizar mapa com marcador do bairro consultado
            updateMap(formData.cidade, formData.bairro, data.probabilidade_crime);

        } else {
            alert(`Erro: ${data.error}\n${data.details ? data.details : ''}`);
        }

    } catch (error) {
        console.error('Erro ao fazer previsão:', error);
        alert('Erro ao conectar com a API. Verifique se o servidor está rodando.');
    }
});

// MODIFICADO: Atualizar mapa com marcador usando os dados da API
function updateMap(cidade, bairro, probabilidade) {
    // Limpar marcadores anteriores
    currentMarkers.forEach(marker => map.removeLayer(marker));
    currentMarkers = [];

    // Obter coordenadas do bairro a partir da variável global 'bairrosData'
    const bairroInfo = bairrosData.find(b => b.bairro === bairro);

    if (bairroInfo) {
        const coords = [bairroInfo.latitude, bairroInfo.longitude];
        const marker = L.marker(coords).addTo(map);
        marker.bindPopup(`
            <b>${bairro}, ${cidade}</b><br>
            Probabilidade de crime: ${probabilidade}%
        `).openPopup();

        currentMarkers.push(marker);

        // Centralizar mapa no marcador com um zoom mais próximo
        map.setView(coords, 14);
    } else {
        console.error(`Coordenadas para o bairro '${bairro}' não encontradas.`);
        // Opcional: voltar para a visão geral se não encontrar o bairro
        map.setView([-8.0476, -34.8770], 11);
    }
}

// Inicializar ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    loadMetadata();
});