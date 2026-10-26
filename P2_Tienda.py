
"""
ACTIVIDAD 2.4 - RUTA DE COMPRAS TIENDA "EL ZORRO"
Buscamos la ruta más corta para comprar en 4 secciones y salir por cajas.
Usamos Fuerza Bruta + Algoritmo de Dijkstra
"""

import networkx as nx                  
import matplotlib.pyplot as plt        
from itertools import permutations     

# 1. DATOS INICIALES
# Aquí ponemos con cuánto dinero entramos y qué lugares tenemos que visitar sí o sí
PRESUPUESTO_INICIAL = 2000             

nombres = {                            
    "Entrada": "Entrada principal",
    "LacteosEmbutidos": "Área de Lácteos y Embutidos",
    "Limpieza": "Pasillo de Artículos de Limpieza",
    "Dulceria": "Pasillo de Dulcería",
    "Mascotas": "Pasillo de Mascotas",
    "CajasSalida": "Área de Cajas y Salida"
}

inicio = "Entrada"                     # Aquí empezamos

destinos = [                           # Estas 4 áreas tenemos que visitar a fuerza
    "LacteosEmbutidos",
    "Limpieza",
    "Dulceria",
    "Mascotas"
]

# 2. CREAMOS EL MAPA DE LA TIENDA
# Cada sección es un nodo y cada pasillo es una línea que los conecta
G = nx.DiGraph()                       

G.add_nodes_from([
    "Entrada",
    "LacteosEmbutidos",
    "Limpieza",
    "Dulceria",
    "Mascotas",
    "CajasSalida"
])

# 3. PONEMOS LOS PASILLOS Y CUÁNTO MIDEN
# Le puse distancia de ida y de regreso porque puedes ir y volver por el mismo pasillo
rutas = [                              
    ("Entrada", "LacteosEmbutidos", 12),
    ("LacteosEmbutidos", "Limpieza", 8),
    ("Limpieza", "Dulceria", 6),
    ("Dulceria", "Mascotas", 10),
    ("Mascotas", "CajasSalida", 15)
]

for origen, destino, distancia in rutas: 
    G.add_edge(origen, destino, peso=distancia) 
    G.add_edge(destino, origen, peso=distancia) 

# 4. CUÁNTO VAMOS A GASTAR APROX
# Esto es lo que estimamos que vamos a comprar en cada área
costos_extras = {                      
    "LacteosEmbutidos": 450,           
    "Limpieza": 250,                   
    "Dulceria": 200,                   
    "Mascotas": 350                    
}

costo_extras_total = sum(costos_extras.values()) 

# 5. BUSCAMOS LA MEJOR RUTA
# La idea es probar todas las combinaciones posibles de las 4 áreas
# Para cada combinación usamos Dijkstra para ver el camino más corto entre punto y punto
mejor_ruta = None                      
minima_distancia = float("inf")        

for orden in permutations(destinos):   # Aquí prueba las 24 combinaciones posibles 4!
    
    ruta_candidata = [inicio]          
    distancia_total_recorrido = 0      
    ubicacion_actual = inicio          

    for destino in orden:              
        # Con Dijkstra encontramos el camino más corto de donde estoy al siguiente destino
        camino = nx.dijkstra_path(     
            G,
            source=ubicacion_actual,
            target=destino,
            weight="peso"
        )

        # Sumamos los metros de cada pedacito del camino
        for i in range(len(camino) - 1): 
            origen_arista = camino[i]  
            destino_arista = camino[i + 1] 
            distancia_total_recorrido += G[origen_arista][destino_arista]["peso"] 

        ruta_candidata.extend(camino[1:]) 
        ubicacion_actual = destino     

    # Al final nos tenemos que ir a cajas
    camino_regreso = nx.dijkstra_path( 
        G,
        source=ubicacion_actual,
        target="CajasSalida",
        weight="peso"
    )

    for i in range(len(camino_regreso) - 1): 
        origen_arista = camino_regreso[i]
        destino_arista = camino_regreso[i + 1]
        distancia_total_recorrido += G[origen_arista][destino_arista]["peso"]

    ruta_candidata.extend(camino_regreso[1:]) 

    # Si esta ruta es más corta que la mejor que teníamos, la guardamos
    if distancia_total_recorrido < minima_distancia: 
        minima_distancia = distancia_total_recorrido 
        mejor_ruta = ruta_candidata    

# 6. CUENTAS DE DINERO
dinero_restante = PRESUPUESTO_INICIAL - costo_extras_total 

# 7. IMPRIMIR TODO EN PANTALLA
ruta_texto = " -> ".join(nombres[lugar] for lugar in mejor_ruta) 

print(f"Ruta óptima en El Zorro: {ruta_texto}")          
print(f"Distancia total recorrida: {minima_distancia} m") 
print(f"Costo de productos: ${costo_extras_total}")        
print(f"Dinero restante: ${dinero_restante}")             
print("Complejidad Big O: O(E log V)")                    

# 8. AHORA VAMOS A DIBUJAR EL MAPA BONITO
FONDO = "#FFFDFD"                      
ROJO_TEXTO = "#6B2323"                 
ROJO_ARISTA = "#D49B9B"                
ROJO_RUTA = "#D93838"                  

colores_nodos = {                      
    "Entrada": "#FADBD8",
    "LacteosEmbutidos": "#F5B7B1",     
    "Limpieza": "#FAD7A0",
    "Dulceria": "#F9EBEA",
    "Mascotas": "#EBEDEF",
    "CajasSalida": "#F2D7D5"
}

posiciones = {                         # Aquí le digo donde va cada nodo para que se vea como tienda
    "Entrada": (-2.00, 0.00),
    "LacteosEmbutidos": (-1.15, 0.80),
    "Limpieza": (0.00, 0.80),
    "Dulceria": (1.15, 0.80),
    "Mascotas": (1.00, -0.60),
    "CajasSalida": (2.25, -0.60)
}

etiquetas_cortas = {                   
    "Entrada": "Entrada",
    "LacteosEmbutidos": "Área de Lácteos\ny Embutidos",
    "Limpieza": "Pasillo de Artículos\nde Limpieza",
    "Dulceria": "Pasillo de\nDulcería",
    "Mascotas": "Pasillo de\nMascotas",
    "CajasSalida": "Área de Cajas\ny Salida"
}

# Guardamos qué líneas son parte de la ruta ganadora para pintarlas diferente
aristas_optimas = set()                

for i in range(len(mejor_ruta) - 1):   
    aristas_optimas.add((mejor_ruta[i], mejor_ruta[i + 1])) 

# Para que las flechas de ida y vuelta no se encimen, las curvamos un poco
curvaturas = {}                        

for origen, destino in G.edges():      
    if (destino, origen) in G.edges:   
        if origen < destino:           
            curvaturas[(origen, destino)] = 0.16 
        else:
            curvaturas[(origen, destino)] = -0.16 
    else:
            curvaturas[(origen, destino)] = 0.0 

# Creamos la ventana y la ponemos en pantalla completa
fig, ax = plt.subplots(figsize=(16, 9)) 

fig.patch.set_facecolor(FONDO)         
ax.set_facecolor(FONDO)                

try:                                   
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')
except Exception:
    try:
        manager.full_screen_toggle()
    except Exception:
        pass

# Primero dibujamos todos los pasillos normales en color bajito
for origen, destino in G.edges():      
    if (origen, destino) in aristas_optimas:
        continue

    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=[(origen, destino)],
        edge_color=ROJO_ARISTA,
        width=2.0,
        arrows=True,
        arrowsize=21,
        connectionstyle=f"arc3,rad={curvaturas[(origen, destino)]}",
        min_source_margin=32,
        min_target_margin=32,
        ax=ax
    )

# Después dibujamos encima la ruta óptima en rojo fuerte para que resalte
for origen, destino in G.edges():      
    if (origen, destino) not in aristas_optimas:
        continue

    nx.draw_networkx_edges(
        G,
        posiciones,
        edgelist=[(origen, destino)],
        edge_color=ROJO_RUTA,
        width=3.0,
        arrows=True,
        arrowsize=23,
        connectionstyle=f"arc3,rad={curvaturas[(origen, destino)]}",
        min_source_margin=32,
        min_target_margin=32,
        ax=ax
    )

# Dibujamos los círculos de cada área
nx.draw_networkx_nodes(                
    G,
    posiciones,
    node_size=3900,
    node_color=[colores_nodos[nodo] for nodo in G.nodes()],
    edgecolors="#C0392B",
    linewidths=2.0,
    ax=ax
)

# Ponemos el nombre a cada área
nx.draw_networkx_labels(               
    G,
    posiciones,
    labels=etiquetas_cortas,
    font_size=10,
    font_weight="bold",
    font_color=ROJO_TEXTO,
    ax=ax
)

# Y ponemos cuántos metros hay en cada pasillo
for origen, destino, datos in G.edges(data=True): 
    distancia = datos["peso"]

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
    color_texto = ROJO_RUTA if es_optima else ROJO_TEXTO
    color_fondo = "#FADBD8" if es_optima else "#FFFFFF"

    ax.text(
        xm,
        ym,
        f"{distancia} m",
        fontsize=9,
        fontweight="bold",
        color=color_texto,
        ha="center",
        va="center",
        clip_on=False,
        bbox={
            "boxstyle": "round,pad=0.30",
            "facecolor": color_fondo,
            "edgecolor": "#F5B7B1",
            "alpha": 0.98
        },
        zorder=10
    )

# Título del mapa
fig.suptitle(                          
    "TIENDA EL ZORRO: RUTA DE COMPRAS Y RECORRIDO",
    fontsize=20,
    fontweight="bold",
    color=ROJO_TEXTO,
    x=0.5,          
    y=0.92          
)

# Cuadro con el resumen de gastos y distancia
resumen = (                            
    f"Presupuesto inicial: ${PRESUPUESTO_INICIAL}\n"
    f"Costo de productos: ${costo_extras_total}\n"
    f"Dinero restante: ${dinero_restante}\n"
    f"Distancia total: {minima_distancia} m"
)

ax.text(                               
    0.025,
    0.035,
    resumen,
    transform=ax.transAxes,
    fontsize=10,
    color=ROJO_TEXTO,
    verticalalignment="bottom",
    bbox={
        "boxstyle": "round,pad=0.75",
        "facecolor": "#FDEDEC",
        "edgecolor": "#F5B7B1",
        "linewidth": 1.5
    }
)

# Leyenda para saber qué es cada color
ax.plot([], [], color=ROJO_RUTA, linewidth=3, label="Ruta óptima de compra")     
ax.plot([], [], color=ROJO_ARISTA, linewidth=2, label="Pasillos alternos")      

ax.legend(                             
    loc="upper right",
    frameon=True,
    facecolor="white",
    edgecolor="#F5B7B1",
    fontsize=10
)

# Ajustes finales para que se vea bien
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

plt.show()  # Aquí ya muestra el mapa y espera a que lo cierres