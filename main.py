import igraph as ig

# ==========================================
# ETAPA 1 - IMPORTAÇÃO E LIMPEZA
# ==========================================


arquivo = "aves-weaver-social.edges"


arestas = []

with open(arquivo, "r") as f:
    for linha in f:
        dados = linha.split()

        if len(dados) >= 2:
            origem = int(dados[0])
            destino = int(dados[1])

            arestas.append((origem, destino))


g = ig.Graph.TupleList(
    arestas,
    directed=False
)

print("=== GRAFO ORIGINAL ===")
print("Nós:", g.vcount())
print("Arestas:", g.ecount())

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


ordem = g.vcount()
tamanho = g.ecount()

densidade = g.density()

diametro = g.diameter()


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


comunidades = g.community_multilevel()

print("\n=== DETECÇÃO DE COMUNIDADES ===")
print("Número de comunidades:", len(comunidades))


for i, comunidade in enumerate(comunidades, start=1):
    print(f"Comunidade {i}: {len(comunidade)} nós")


# ==========================================
# VISUALIZAÇÃO
# ==========================================

layout = g.layout("fr")


degree = g.degree()


tamanhos = [
    5 + (d * 2)
    for d in degree
]


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