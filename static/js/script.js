// Inicializar o mapa
const map = L.map('map').setView([-8.0476, -34.8770], 11); // Coordenadas de Recife

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 18,
}).addTo(map);

// Coordenadas aproximadas dos bairros (exemplo simplificado)
const bairrosCoordenadas = {
    'Recife': {
        'Boa Viagem': [-8.1278, -34.8975],
        'Pina': [-8.0892, -34.8811],
        'Boa Vista': [-8.0554, -34.8867],
        'Recife': [-8.0631, -34.8711],
        'Santo Amaro': [-8.0478, -34.8811],
        'São José': [-8.0597, -34.8769],
        'Ilha do Leite': [-8.0542, -34.8903],
        'Paissandu': [-8.0447, -34.8825],
        'Espinheiro': [-8.0392, -34.8903],
        'Graças': [-8.0397, -34.8975],
        'Aflitos': [-8.0364, -34.9003],
        'Jaqueira': [-8.0428, -34.9031],
        'Parnamirim': [-8.0378, -34.9089],
        'Santana': [-8.0342, -34.8903],
        'Casa Amarela': [-8.0197, -34.9089],
        'Apipucos': [-8.0108, -34.9361],
        'Poço da Panela': [-8.0142, -34.9233],
        'Monteiro': [-8.0192, -34.9189],
        'Dois Irmãos': [-8.0044, -34.9489],
        'Várzea': [-8.0378, -34.9553],
        'Cidade Universitária': [-8.0508, -34.9511],
        'Engenho do Meio': [-8.0347, -34.9233],
        'Torrões': [-8.0289, -34.9297],
        'Cordeiro': [-8.0544, -34.9089],
        'Ilha do Retiro': [-8.0522, -34.9003],
        'Madalena': [-8.0564, -34.9089],
        'Torre': [-8.0508, -34.8975],
        'Zumbi': [-8.0564, -34.8903],
        'Encruzilhada': [-8.0625, -34.9003],
        'Prado': [-8.0681, -34.8903],
        'Hipódromo': [-8.0747, -34.8903],
        'San Martin': [-8.0803, -34.8903],
        'Afogados': [-8.0858, -34.9089],
        'Bongi': [-8.0914, -34.9189],
        'Mustardinha': [-8.0969, -34.9189],
        'Curado': [-8.1025, -34.9361],
        'Jardim São Paulo': [-8.1081, -34.9361],
        'Sancho': [-8.1136, -34.9361],
        'Barro': [-8.0803, -34.9003],
        'Coelhos': [-8.0625, -34.8711],
        'Cabanga': [-8.0681, -34.8811],
        'Imbiribeira': [-8.1192, -34.9089],
        'Ipsep': [-8.1247, -34.9189],
        'Cohab': [-8.1303, -34.9233],
        'Ibura': [-8.1358, -34.9297],
        'Jordão': [-8.1414, -34.9361],
        'Areias': [-8.1469, -34.9425],
        'Nova Descoberta': [-8.0289, -34.8903],
        'Alto Santa Terezinha': [-8.0233, -34.8903],
        'Brejo da Guabiraba': [-8.0044, -34.9233],
        'Brejo de Beberibe': [-7.9989, -34.9189],
        'Alto do Mandu': [-8.0100, -34.8975],
        'Linha do Tiro': [-8.0156, -34.9003],
        'Água Fria': [-8.0211, -34.9089],
        'Fundão': [-8.0267, -34.9089],
        'Beberibe': [-8.0322, -34.8711],
        'Cajueiro': [-8.0378, -34.8711],
        'Porto da Madeira': [-8.0433, -34.8711],
        'Arruda': [-8.0489, -34.8711],
        'Campina do Barreto': [-8.0544, -34.8711],
        'Campo Grande': [-8.0600, -34.8711],
        'Alto José do Pinho': [-8.0656, -34.8711],
        'Alto José Bonifácio': [-8.0711, -34.8711],
        'Bomba do Hemetério': [-8.0767, -34.8711],
        'Ponto de Parada': [-8.0822, -34.8711],
        'Macaxeira': [-8.0878, -34.8711],
        'Passarinho': [-8.0933, -34.8711],
        'Dois Unidos': [-8.0989, -34.8711],
        'Vasco da Gama': [-8.1044, -34.8711],
        'Guabiraba': [-8.0100, -34.9089],
        'Pau Ferro': [-8.0156, -34.9089],
        'Morro da Conceição': [-8.0211, -34.9089],
        'Alto do Céu': [-8.0267, -34.9089],
        'Sítio dos Pintos': [-8.0322, -34.9089],
        'Caxangá': [-8.0378, -34.9361],
        'Iputinga': [-8.0433, -34.9361],
        'Cidade Universitária': [-8.0489, -34.9361],
        'Tamarineira': [-8.0544, -34.9361],
        'Casa Forte': [-8.0600, -34.9361],
        'Poço': [-8.0656, -34.9361],
        'Derby': [-8.0711, -34.9361],
        'Soledade': [-8.0767, -34.9361],
        'Boa Vista': [-8.0822, -34.9361],
        'Cabanga': [-8.0878, -34.9361],
        'Ilha Joana Bezerra': [-8.0933, -34.9361],
        'Coqueiral': [-8.0989, -34.9361],
        'Brasília Teimosa': [-8.1044, -34.8711],
        'Pina': [-8.1100, -34.8811],
        'Boa Viagem': [-8.1156, -34.8975],
        'Setúbal': [-8.1211, -34.9089],
        'Imbiribeira': [-8.1267, -34.9189],
        'Ipsep': [-8.1322, -34.9233],
        'Torreão': [-8.1378, -34.9297],
        'Curado': [-8.1433, -34.9361],
        'Barro': [-8.1489, -34.9425],
        'Jardim São Paulo': [-8.1544, -34.9489],
        'Sancho': [-8.1600, -34.9553],
        'Mustardinha': [-8.1656, -34.9617],
        'Bongi': [-8.1711, -34.9681],
        'Afogados': [-8.1767, -34.9745],
        'San Martin': [-8.1822, -34.9809],
        'Mangueira': [-8.1878, -34.9873],
        'Cordeiro': [-8.1933, -34.9937],
        'Engenho do Meio': [-8.1989, -35.0001],
        'Torrões': [-8.2044, -35.0065],
        'Várzea': [-8.2100, -35.0129],
        'Cidade Universitária': [-8.2156, -35.0193],
        'Jardim São Paulo': [-8.2211, -35.0257],
        'Sancho': [-8.2267, -35.0321],
        'Curado': [-8.2322, -35.0385],
        'Barro': [-8.2378, -35.0449],
        'Jardim São Paulo': [-8.2433, -35.0513],
        'Sancho': [-8.2489, -35.0577],
        'Curado': [-8.2544, -35.0641],
        'Barro': [-8.2600, -35.0705],
        'Jardim São Paulo': [-8.2656, -35.0769],
        'Sancho': [-8.2711, -35.0833],
        'Curado': [-8.2767, -35.0897],
        'Barro': [-8.2822, -35.0961],
        'Nova Olinda': [-8.0489, -34.8711],
        'Cajueiro': [-8.0544, -34.8711],
        'Ponto de Parada': [-8.0600, -34.8711]
    },
    'Olinda': {
        'Carmo': [-7.9989, -34.8447],
        'Varadouro': [-8.0044, -34.8511],
        'Ribeira': [-8.0100, -34.8575],
        'Sé': [-8.0156, -34.8639],
        'Guadalupe': [-8.0211, -34.8703],
        'Bairro Novo': [-8.0267, -34.8767],
        'Peixinhos': [-8.0322, -34.8831],
        'Santa Tereza': [-8.0378, -34.8895],
        'Jardim Atlântico': [-8.0433, -34.8959],
        'Casa Caiada': [-8.0489, -34.9023],
        'Rio Doce': [-8.0544, -34.9087],
        'Bairro Novo': [-8.0600, -34.9151],
        'Fragoso': [-8.0656, -34.9215],
        'Ouro Preto': [-8.0711, -34.9279],
        'Jardim Brasil': [-8.0767, -34.9343],
        'Bultrins': [-8.0822, -34.9407],
        'Salgadinho': [-8.0878, -34.9471],
        'Tabajara': [-8.0933, -34.9535],
        'Jardim Brasil II': [-8.0989, -34.9599],
        'Aguazinha': [-8.1044, -34.9663],
        'Passarinho': [-8.1100, -34.9727],
        'Jardim Atlântico': [-8.1156, -34.9791],
        'Casa Caiada': [-8.1211, -34.9855],
        'Rio Doce': [-8.1267, -34.9919],
        'Bairro Novo': [-8.1322, -34.9983],
        'Fragoso': [-8.1378, -35.0047],
        'Ouro Preto': [-8.1433, -35.0111],
        'Jardim Brasil': [-8.1489, -35.0175],
        'Bultrins': [-8.1544, -35.0239],
        'Salgadinho': [-8.1600, -35.0303],
        'Tabajara': [-8.1656, -35.0367],
        'Jardim Brasil II': [-8.1711, -35.0431],
        'Aguazinha': [-8.1767, -35.0495],
        'Passarinho': [-8.1822, -35.0559]
    },
    'Jaboatão dos Guararapes': {
        'Piedade': [-8.1878, -35.0623],
        'Candeias': [-8.1933, -35.0687],
        'Barra de Jangada': [-8.1989, -35.0751],
        'Cajueiro Seco': [-8.2044, -35.0815],
        'Muribeca': [-8.2100, -35.0879],
        'Prazeres': [-8.2156, -35.0943],
        'Socorro': [-8.2211, -35.1007],
        'Jardim Jordão': [-8.2267, -35.1071],
        'Guararapes': [-8.2322, -35.1135],
        'Comportas': [-8.2378, -35.1199],
        'Cavaleiro': [-8.2433, -35.1263],
        'Sucupira': [-8.2489, -35.1327],
        'Zumbi': [-8.2544, -35.1391],
        'Jardim Piedade': [-8.2600, -35.1455],
        'Barra de Jangada': [-8.2656, -35.1519],
        'Candeias': [-8.2711, -35.1583],
        'Piedade': [-8.2767, -35.1647],
        'Cajueiro Seco': [-8.2822, -35.1711],
        'Muribeca': [-8.2878, -35.1775],
        'Prazeres': [-8.2933, -35.1839],
        'Socorro': [-8.2989, -35.1903],
        'Jardim Jordão': [-8.3044, -35.1967],
        'Guararapes': [-8.3100, -35.2031],
        'Comportas': [-8.3156, -35.2095],
        'Cavaleiro': [-8.3211, -35.2159],
        'Sucupira': [-8.3267, -35.2223],
        'Zumbi': [-8.3322, -35.2287],
        'Jardim Piedade': [-8.3378, -35.2351],
        'Barra de Jangada': [-8.3433, -35.2415],
        'Candeias': [-8.3489, -35.2479],
        'Piedade': [-8.3544, -35.2543],
        'Cajueiro Seco': [-8.3600, -35.2607],
        'Muribeca': [-8.3656, -35.2671],
        'Prazeres': [-8.3711, -35.2735],
        'Socorro': [-8.3767, -35.2799],
        'Jardim Jordão': [-8.3822, -35.2863],
        'Guararapes': [-8.3878, -35.2927],
        'Comportas': [-8.3933, -35.2991],
        'Cavaleiro': [-8.3989, -35.3055],
        'Sucupira': [-8.4044, -35.3119],
        'Zumbi': [-8.4100, -35.3183],
        'Jardim Piedade': [-8.4156, -35.3247],
        'Barra de Jangada': [-8.4211, -35.3311],
        'Candeias': [-8.4267, -35.3375],
        'Piedade': [-8.4322, -35.3439],
        'Cajueiro Seco': [-8.4378, -35.3503],
        'Muribeca': [-8.4433, -35.3567],
        'Prazeres': [-8.4489, -35.3631],
        'Socorro': [-8.4544, -35.3695],
        'Jardim Jordão': [-8.4600, -35.3759],
        'Guararapes': [-8.4656, -35.3823],
        'Comportas': [-8.4711, -35.3887],
        'Cavaleiro': [-8.4767, -35.3951],
        'Sucupira': [-8.4822, -35.4015],
        'Zumbi': [-8.4878, -35.4079],
        'Jardim Piedade': [-8.4933, -35.4143],
        'Barra de Jangada': [-8.4989, -35.4207],
        'Candeias': [-8.5044, -35.4271],
        'Piedade': [-8.5100, -35.4335],
        'Cajueiro Seco': [-8.5156, -35.4399],
        'Muribeca': [-8.5211, -35.4463],
        'Prazeres': [-8.5267, -35.4527],
        'Socorro': [-8.5322, -35.4591],
        'Jardim Jordão': [-8.5378, -35.4655],
        'Guararapes': [-8.5433, -35.4719],
        'Comportas': [-8.5489, -35.4783],
        'Cavaleiro': [-8.5544, -35.4847],
        'Sucupira': [-8.5600, -35.4911],
        'Zumbi': [-8.5656, -35.4975],
        'Jardim Piedade': [-8.5711, -35.5039],
        'Curado II': [-8.1025, -34.9361]
    }
};

// Variáveis globais
let currentMarkers = [];

// Carregar metadados (cidades, bairros, tipos de crime)
async function loadMetadata() {
    try {
        const response = await fetch('http://localhost:5000/metadata');
        const data = await response.json();

        // Preencher dropdown de cidades
        const cidadeSelect = document.getElementById('cidade');
        data.cidades.forEach(cidade => {
            const option = document.createElement('option');
            option.value = cidade;
            option.textContent = cidade;
            cidadeSelect.appendChild(option);
        });

        // Preencher dropdown de bairros
        const bairroSelect = document.getElementById('bairro');
        data.bairros.forEach(bairro => {
            const option = document.createElement('option');
            option.value = bairro;
            option.textContent = bairro;
            bairroSelect.appendChild(option);
        });

        // Preencher dropdown de tipos de crime
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
            alert(`Erro: ${data.error}\n${data.details ? data.details.join('\n') : ''}`);
        }

    } catch (error) {
        console.error('Erro ao fazer previsão:', error);
        alert('Erro ao conectar com a API. Verifique se o servidor está rodando.');
    }
});

// Atualizar mapa com marcador
function updateMap(cidade, bairro, probabilidade) {
    // Limpar marcadores anteriores
    currentMarkers.forEach(marker => map.removeLayer(marker));
    currentMarkers = [];

    // Obter coordenadas do bairro
    const coords = bairrosCoordenadas[cidade]?.[bairro];

    if (coords) {
        const marker = L.marker(coords).addTo(map);
        marker.bindPopup(`
            <b>${bairro}, ${cidade}</b><br>
            Probabilidade de crime: ${probabilidade}%
        `).openPopup();

        currentMarkers.push(marker);

        // Centralizar mapa no marcador
        map.setView(coords, 13);
    } else {
        alert('Coordenadas do bairro não encontradas no mapa.');
    }
}

// Inicializar ao carregar a página
window.addEventListener('DOMContentLoaded', () => {
    loadMetadata();
});
