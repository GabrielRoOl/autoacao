import numpy as np


def criar_populacao_inicial(n_cavalos, limites_caracteristicas):
    """
    n_cavalos: Quantidade de cavalos na nossa população.
    limites_caracteristicas: Lista com (mín, máx) para Velocidade, Resistência e Peso.
    """
    n_genes = len(limites_caracteristicas)
    # Cria a matriz: cada linha é um cavalo, cada coluna é um gene
    populacao_cavalos = np.zeros((n_cavalos, n_genes))

    for i in range(n_cavalos):
        for j in range(n_genes):
            inf, sup = limites_caracteristicas[j]
            # Gerando a característica aleatória dentro do limite da espécie
            populacao_cavalos[i, j] = np.random.uniform(inf, sup)

    return populacao_cavalos


# --- TESTE ---

# Definindo os limites biológicos:
# Gene 0: Velocidade (40 a 70 km/h)
# Gene 1: Resistência (10 a 60 minutos)
# Gene 2: Peso (300 a 600 kg)
limites_biologicos = [(40, 70), (10, 60), (300, 600)]

# Criando um haras com 10 cavalos aleatórios
meu_haras = criar_populacao_inicial(10, limites_biologicos)

print("ID | Velocidade | Resistência | Peso")
print("-" * 40)
for idx, cavalo in enumerate(meu_haras):
    print(f"{idx:02d} | {cavalo[0]:.2f} km/h | {cavalo[1]:.2f} min | {cavalo[2]:.2f} kg")