import heapq
from collections import deque, defaultdict

TRAMOS = [("Morelia","Toluca",245),("Morelia","Querétaro",195),("Querétaro","Toluca",190),
          ("Querétaro","CDMX",213),("Querétaro","Pachuca",240),("Toluca","CDMX",66),
          ("Toluca","Cuernavaca",110),("CDMX","Cuernavaca",89),("CDMX","Pachuca",95),
          ("CDMX","Puebla",130),("Pachuca","Tlaxcala",150),("Tlaxcala","Puebla",35),
          ("Cuernavaca","Puebla",160)]
GRAFO = defaultdict(dict)
for a, b, km in TRAMOS:          # cada tramo = 2 arcos dirigidos
    GRAFO[a][b] = km; GRAFO[b][a] = km
def vecinos(s): return sorted(GRAFO[s].items())      # orden alfabético
INICIO, META = "Morelia", "Puebla"
def costo(ruta): return sum(GRAFO[a][b] for a, b in zip(ruta, ruta[1:]))
def camino(padre, s):
    r = []
    while s is not None: r.append(s); s = padre[s]
    return r[::-1]

def bfs():
    padre = {INICIO: None}; frontera = deque([INICIO]); expandidos = 0
    while frontera:
        n = frontera.popleft(); expandidos += 1
        if n == META: return camino(padre, n), expandidos
        for v, _ in vecinos(n):
            if v not in padre: padre[v] = n; frontera.append(v)

def dfs():
    padre = {}; frontera = [(INICIO, None)]; explorado = set(); expandidos = 0
    while frontera:
        n, p = frontera.pop()
        if n in explorado: continue
        explorado.add(n); padre[n] = p; expandidos += 1
        if n == META: return camino(padre, n), expandidos
        for v, _ in reversed(vecinos(n)):            # así se explora primero el alfabético
            if v not in explorado: frontera.append((v, n))

def dls(n, limite, ruta, cont):
    cont[0] += 1
    if n == META: return ruta
    if limite == 0: return None
    for v, _ in vecinos(n):
        if v not in ruta:                             # evita ciclos en la rama actual
            r = dls(v, limite-1, ruta+[v], cont)
            if r: return r

def ids():
    total = [0]
    for l in range(0, 20):
        r = dls(INICIO, l, [INICIO], total)
        if r: return r, total[0], l

def ucs():
    frontera = [(0, INICIO)]; g = {INICIO: 0}; padre = {INICIO: None}
    hechos = set(); expandidos = 0
    while frontera:
        c, n = heapq.heappop(frontera)
        if n in hechos: continue
        hechos.add(n); expandidos += 1
        if n == META: return camino(padre, n), expandidos
        for v, km in vecinos(n):
            if c + km < g.get(v, float("inf")):
                g[v] = c + km; padre[v] = n; heapq.heappush(frontera, (g[v], v))

if __name__ == "__main__":
    print(f"{'Algoritmo':6} {'Tramos':>6} {'Km':>5} {'Expandidos':>10}  Ruta")
    for nombre, f in [("BFS", bfs), ("DFS", dfs), ("IDS", ids), ("UCS", ucs)]:
        r = f(); ruta, exp = r[0], r[1]
        extra = f"  (límite = {r[2]})" if nombre == "IDS" else ""
        print(f"{nombre:6} {len(ruta)-1:>6} {costo(ruta):>5} {exp:>10}  {' -> '.join(ruta)}{extra}")
