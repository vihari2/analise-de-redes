import igraph as ig

# ==========================================
# ETAPA 1 - IMPORTAÇÃO E LIMPEZA
# ==========================================

# Caminho do arquivo
arquivo = "aves-weaver-social.edges"

# Ler apenas as duas primeiras colunas
arestas = []

with open(arquivo, "r") as f:
    for linha in f:
        dados = linha.split()

        if len(dados) >= 2:
            origem = int(dados[0])
            destino = int(dados[1])

            arestas.append((origem, destino))

# Criar grafo não direcionado
g = ig.Graph.TupleList(
    arestas,
    directed=False
)

print("=== GRAFO ORIGINAL ===")
print("Nós:", g.vcount())
print("Arestas:", g.ecount())

# Simplificar a rede
g.simplify(
    loops=True,
    multiple=True
)

print("\n=== GRAFO APÓS SIMPLIFICAÇÃO ===")
print("Nós:", g.vcount())
print("Arestas:", g.ecount())

# ==========================================
# ETAPA 2 - CARACTERIZAÇÃO TOPOLÓGICA
# ==========================================

# Ordem e tamanho
ordem = g.vcount()
tamanho = g.ecount()

# Densidade
densidade = g.density()

# Diâmetro
diametro = g.diameter()

# Transitividade
transitividade = g.transitivity_undirected()

print("\n=== CARACTERIZAÇÃO TOPOLÓGICA ===")

print("Ordem (número de nós):", ordem)
print("Tamanho (número de arestas):", tamanho)
print("Densidade:", densidade)
print("Diâmetro:", diametro)
print("Transitividade:", transitividade)

# ==========================================
# ETAPA 3 - IDENTIFICAÇÃO DOS HUBS
# ==========================================

# -------------------------
# CENTRALIDADE POR DEGREE
# -------------------------

degree = g.degree()

# Ordenar os nós pelo grau, do maior para o menor
top_degree = sorted(
    enumerate(degree),
    key=lambda x: x[1],
    reverse=True
)

print("\n=== TOP 5 - DEGREE ===")

for posicao, (indice, valor) in enumerate(top_degree[:5], start=1):
    print(
        f"{posicao}º - Nó {g.vs[indice]['name']}: "
        f"Degree = {valor}"
    )


# -------------------------
# CENTRALIDADE POR BETWEENNESS
# -------------------------

betweenness = g.betweenness()

# Ordenar os nós pela betweenness
top_betweenness = sorted(
    enumerate(betweenness),
    key=lambda x: x[1],
    reverse=True
)

print("\n=== TOP 5 - BETWEENNESS ===")

for posicao, (indice, valor) in enumerate(
    top_betweenness[:5],
    start=1
):
    print(
        f"{posicao}º - Nó {g.vs[indice]['name']}: "
        f"Betweenness = {valor:.2f}"
    )

# ==========================================
# ETAPA 4 - COMUNIDADES E VISUALIZAÇÃO
# ==========================================

import matplotlib.pyplot as plt

# Detectar comunidades usando Louvain
comunidades = g.community_multilevel()

print("\n=== DETECÇÃO DE COMUNIDADES ===")
print("Número de comunidades:", len(comunidades))

# Mostrar tamanho de cada comunidade
for i, comunidade in enumerate(comunidades, start=1):
    print(f"Comunidade {i}: {len(comunidade)} nós")


# ==========================================
# VISUALIZAÇÃO
# ==========================================

# Layout Fruchterman-Reingold
layout = g.layout("fr")

# Grau de cada nó
degree = g.degree()

# Tamanho dos nós proporcional ao grau
tamanhos = [
    5 + (d * 2)
    for d in degree
]

# Cor de acordo com a comunidade
# Criar uma cor diferente para cada comunidade
paleta = ig.RainbowPalette(len(comunidades))

cores = [
    paleta.get(comunidade)
    for comunidade in comunidades.membership
]

# Criar gráfico
fig, ax = plt.subplots(figsize=(12, 10))

ig.plot(
    g,
    target=ax,
    layout=layout,
    vertex_size=tamanhos,
    vertex_color=cores,
    vertex_label=None,
    edge_width=0.5
)

plt.title("Rede Social das Aves - Comunidades")
plt.show()