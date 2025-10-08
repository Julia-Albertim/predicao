# formatar_bairros.py

# Abrir o arquivo com a lista de bairros (1 por linha)
with open("bairros_unicos.csv", "r", encoding="utf-8") as f:
    bairros = [linha.strip() for linha in f if linha.strip()]  # Remove linhas vazias e espaços

# Gera a lista formatada para uso em Python
bairros_formatados = [f'"{bairro}"' for bairro in bairros]

# Junta com vírgulas e quebras de linha para melhor visualização
resultado = ",\n".join(bairros_formatados)

print("bairros = [\n" + resultado + "\n]")
