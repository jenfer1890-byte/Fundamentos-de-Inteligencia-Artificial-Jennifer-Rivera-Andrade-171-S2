#  IMPORTACION  DE LIBRERIAS
import networkx as nx
import matplotlib.pyplot as plt
from itertools import permutations



# DATOS Y  LA CONFIGURACIÓN INICIAL DEL VIAJE

# Dinero total con el que contamos para realizar el recorrido.
DINERO_INICIAL = 2000

# Mapeo de los nombres cortos por nombres completos.
nombres = {
    "Atlautla": "Atlautla",
    "Ozumba": "Ozumba",
    "Candelaria": "La Candelaria",
    "BellasArtes": "Palacio de Bellas Artes",
    "AcuarioMichin": "Acuario Michin",
    "MuseoAntropologia": "Museo Nacional de Antropologia"
}

# Estado inicial del problema de búsqueda.
estado_inicial = (
    "Atlautla",
    DINERO_INICIAL,
    tuple()
)

# Punto de partida del viaje.
inicio = "Atlautla"

# Lista de lugares que sí o sí debemos visitar en el recorrido.
destinos = [
    "BellasArtes",
    "AcuarioMichin",
    "MuseoAntropologia"
]

#  CREACION DEL GRAFO 

# Inicializacion del grafo dirigido.
# Las aristas representan los caminos con su respectivo costo de transporte.
G = nx.DiGraph()

G.add_nodes_from([
    "Atlautla",
    "Ozumba",
    "Candelaria",
    "BellasArtes",
    "AcuarioMichin",
    "MuseoAntropologia"
])

# ESTABLECER RUTAS Y COSTOS DE TRANSPORTE

# Definimos los tramos y cuánto cuesta moverse entre ellos en pesos.
rutas = [
    ("Atlautla", "Ozumba", 12),
    ("Ozumba", "Candelaria", 50),
    ("Candelaria", "BellasArtes", 5),
    ("BellasArtes", "AcuarioMichin", 15),
    ("AcuarioMichin", "MuseoAntropologia", 5)
]

# Añadimos las conexiones bidireccionales al grafo.
for origen, destino, costo in rutas:
    G.add_edge(origen, destino, peso=costo)
    G.add_edge(destino, origen, peso=costo)

# CONFIGURAR GASTOS EXTRAS (ENTRADAS Y COMIDA)

# Estos gastos son fijos por lugar o consumo, independientes del transporte.
costos_extras = {
    "BellasArtes": 0,
    "AcuarioMichin": 370,
    "MuseoAntropologia": 90,
    "Comida": 300
}

costo_extras_total = sum(costos_extras.values())


# ENCONTRAR LA RUTA ÓPTIMA MEDIANTE FUERZA BRUTA Y DIJKSTRA

# Evaluacion de las posibles combinaciones de visita (3! = 6 órdenes).
# Para cada tramo se usa Dijkstra.
mejor_ruta = None
mejor_costo_transporte = float("inf")

for orden in permutations(destinos):
    
    ruta_candidata = [inicio]
    costo_transporte = 0
    ubicacion_actual = inicio

    # Recorremos cada destino en el orden actual de la permutación.
    for destino in orden:
        camino = nx.dijkstra_path(
            G,
            source=ubicacion_actual,
            target=destino,
            weight="peso"
        )

        # Sumamos los costos de cada paso del camino encontrado.
        for i in range(len(camino) - 1):
            origen_arista = camino[i]
            destino_arista = camino[i + 1]
            costo_transporte += G[origen_arista][destino_arista]["peso"]

        ruta_candidata.extend(camino[1:])
        ubicacion_actual = destino

    # Calculamos el costo y la ruta de regreso al punto de partida (Atlautla).
    camino_regreso = nx.dijkstra_path(
        G,
        source=ubicacion_actual,
        target=inicio,
        weight="peso"
    )

    for i in range(len(camino_regreso) - 1):
        origen_arista = camino_regreso[i]
        destino_arista = camino_regreso[i + 1]
        costo_transporte += G[origen_arista][destino_arista]["peso"]

    ruta_candidata.extend(camino_regreso[1:])

    # Si este recorrido es más económico que el anterior, lo guardamos.
    if costo_transporte < mejor_costo_transporte:
        mejor_costo_transporte = costo_transporte
        mejor_ruta = ruta_candidata

# BALANCE FINANCIERO DEL VIAJE


costo_total = mejor_costo_transporte + costo_extras_total
dinero_restante = DINERO_INICIAL - costo_total


# IMPRIMIR RESULTADOS EN CONSOLA


ruta_texto = " -> ".join(nombres[lugar] for lugar in mejor_ruta)

print(f"Ruta óptima: {ruta_texto}")
print(f"Costo total: ${costo_total}")
print(f"Dinero restante: ${dinero_restante}")
print("Complejidad Big O: O(E log V)")

## DISEÑO VISUAL Y PALETA DE COLORES


FONDO = "#FCFAF7"
AZUL_TEXTO = "#23466B"
AZUL_ARISTA = "#91A9C5"
MORADO_RUTA = "#9654D8"

# Tonos pastel para distinguir visualmente cada nodo en el mapa.
colores_nodos = {
    "Atlautla": "#BFE3F5",
    "Ozumba": "#C8E9DF",
    "Candelaria": "#FFF0BF",
    "BellasArtes": "#F8D0CE",
    "AcuarioMichin": "#DDCCF4",
    "MuseoAntropologia": "#D2E8C8"
}

# Coordenadas manuales para acomodar los nodos de forma limpia.
posiciones = {
    "Atlautla": (-2.00, 0.00),
    "Ozumba": (-1.15, 0.80),
    "Candelaria": (0.00, 0.80),
    "BellasArtes": (1.15, 0.80),
    "AcuarioMichin": (1.00, -0.60),
    "MuseoAntropologia": (2.25, -0.60)
}

# Textos ajustados para que quepan bien dentro de los círculos.
etiquetas_cortas = {
    "Atlautla": "Atlautla",
    "Ozumba": "Ozumba",
    "Candelaria": "La Candelaria",
    "BellasArtes": "Palacio de\nBellas Artes",
    "AcuarioMichin": "Acuario Michin",
    "MuseoAntropologia": "Museo Nacional\nde Antropologia"
}

# 10. SELECCIONAR ARISTAS DE LA RUTA ÓPTIMA

aristas_optimas = set()

for i in range(len(mejor_ruta) - 1):
    aristas_optimas.add((mejor_ruta[i], mejor_ruta[i + 1]))



#  CALCULAR CURVATURAS PARA LAS LÍNEAS BIDIRECCIONALES

curvaturas = {}

for origen, destino in G.edges():
    if (destino, origen) in G.edges:
        if origen < destino:
            curvaturas[(origen, destino)] = 0.16
        else:
            curvaturas[(origen, destino)] = -0.16
    else:
        curvaturas[(origen, destino)] = 0.0


#  INICIALIZAR LA VENTANA GRÁFICA EN PANTALLA COMPLETA


fig, ax = plt.subplots(figsize=(16, 9))

fig.patch.set_facecolor(FONDO)
ax.set_facecolor(FONDO)

# Forzamos la ventana a abrirse maximizada de inicio.
try:
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
except Exception:
    try:
        manager.full_screen_toggle()
    except Exception:
        pass


#  CONEXIONES SECUNDARIAS


for origen, destino in G.edges():
    if (origen, destino) in aristas_optimas:
        continue

    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=[(origen, destino)],
        edge_color=AZUL_ARISTA,
        width=2.0,
        arrows=True,
        arrowsize=21,
        connectionstyle=f"arc3,rad={curvaturas[(origen, destino)]}",
        min_source_margin=32,
        min_target_margin=32,
        ax=ax
    )

#  RESALTAR LA RUTA ÓPTIMA EN EL GRAFO


for origen, destino in G.edges():
    if (origen, destino) not in aristas_optimas:
        continue

    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=[(origen, destino)],
        edge_color=MORADO_RUTA,
        width=3.0,
        arrows=True,
        arrowsize=23,
        connectionstyle=f"arc3,rad={curvaturas[(origen, destino)]}",
        min_source_margin=32,
        min_target_margin=32,
        ax=ax
    )



# UBICACIONES DE LOS NODOS


nx.draw_networkx_nodes(
    G,
    posiciones,
    node_size=3900,
    node_color=[colores_nodos[nodo] for nodo in G.nodes()],
    edgecolors="#8197AE",
    linewidths=2.0,
    ax=ax
)

#  ETIQUETAS DE TEXTO A LOS NODOS

nx.draw_networkx_labels(
    G,
    posiciones,
    labels=etiquetas_cortas,
    font_size=10,
    font_weight="bold",
    font_color=AZUL_TEXTO,
    ax=ax
)

# COLOCACION DE COSTOS SOBRE LOS ARISTAS

for origen, destino, datos in G.edges(data=True):
    costo = datos["peso"]

    x1, y1 = posiciones[origen]
    x2, y2 = posiciones[destino]

    dx = x2 - x1
    dy = y2 - y1

    longitud = max((dx**2 + dy**2) ** 0.5, 0.001)

    perpendicular_x = -dy / longitud
    perpendicular_y = dx / longitud

    signo = 1 if curvaturas[(origen, destino)] > 0 else -1

    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2

    xm += perpendicular_x * 0.12 * signo
    ym += perpendicular_y * 0.12 * signo

    es_optima = (origen, destino) in aristas_optimas
    color_texto = MORADO_RUTA if es_optima else AZUL_TEXTO
    color_fondo = "#F0E4FF" if es_optima else "#EAF1F8"

    ax.text(
        xm,
        ym,
        f"${costo}",
        fontsize=9,
        fontweight="bold",
        color=color_texto,
        ha="center",
        va="center",
        clip_on=False,
        bbox={
            "boxstyle": "round,pad=0.30",
            "facecolor": color_fondo,
            "edgecolor": "none",
            "alpha": 0.98
        },
        zorder=10
    )

# CONFIGURAR EL TÍTULO PRINCIPAL (CENTRADO Y SIN SUBTÍTULO)

fig.suptitle(
    "VIAJE TURISTICO: ATLAUTLA - CIUDAD DE MEXICO",
    fontsize=20,
    fontweight="bold",
    color=AZUL_TEXTO,
    x=0.5,          # Centrado horizontal exacto
    y=0.92          # Altura adecuada en la ventana
)

# CREACION DEL PANEL INFORMATIVO DE PRESUPUESTO

resumen = (
    f"Presupuesto inicial: ${DINERO_INICIAL}\n"
    f"Costo de transporte: ${mejor_costo_transporte}\n"
    f"Entradas y comida: ${costo_extras_total}\n"
    f"Costo total: ${costo_total}\n"
    f"Dinero restante: ${dinero_restante}"
)

ax.text(
    0.025,
    0.035,
    resumen,
    transform=ax.transAxes,
    fontsize=10,
    color=AZUL_TEXTO,
    verticalalignment="bottom",
    bbox={
        "boxstyle": "round,pad=0.75",
        "facecolor": "#E5F3FC",
        "edgecolor": "#B8DDF5",
        "linewidth": 1.5
    }
)

#  AÑADIR LA TEXTO  AL MAPA

ax.plot([], [], color=MORADO_RUTA, linewidth=3, label="Ruta óptima")
ax.plot([], [], color=AZUL_ARISTA, linewidth=2, label="Otras conexiones")

ax.legend(
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#D6E1EA",
    fontsize=10
)

#  AJUSTES  DE VISUALIZACIÓN

ax.set_xlim(-2.85, 2.95)
ax.set_ylim(-1.35, 1.40)

ax.axis("off")

fig.subplots_adjust(
    left=0.07,
    right=0.93,
    bottom=0.12,
    top=0.85
)

for texto in ax.texts:
    texto.set_clip_on(False)

plt.show()