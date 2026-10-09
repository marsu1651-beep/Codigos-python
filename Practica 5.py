import heapq, time
from p4_busqueda_no_informada import GRAFO, vecinos, INICIO, META, costo

H = {"Morelia":330,"Toluca":150,"Querétaro":250,"CDMX":100,"Pachuca":110,
     "Cuernavaca":100,"Tlaxcala":30,"Puebla":0}

def verificar_heuristica():
    print("Arco            h(n)  c   h(n')  h(n) <= c + h(n')")
    consistente = True
    for a in sorted(GRAFO):
        for b, c in vecinos(a):
            ok = H[a] <= c + H[b]; consistente &= ok
            if not ok: print(f"{a:>10}->{b:<10} {H[a]:>4} {c:>3} {H[b]:>5}  NO")
    print("Consistente:", consistente, "(consistente implica admisible)")

def mejor_primero(f_eval):
    frontera = [(f_eval(0, INICIO), 0, INICIO)]; padre = {INICIO: None}; g = {INICIO: 0}; hechos = set(); exp = 0
    while frontera:
        _, c, n = heapq.heappop(frontera)
        if n in hechos: continue
        hechos.add(n); exp += 1
        if n == META:
            r = []; s = n
            while s: r.append(s); s = padre[s]
            return r[::-1], exp
        for v, km in vecinos(n):
            if c + km < g.get(v, 1e9):
                g[v] = c + km; padre[v] = n
                heapq.heappush(frontera, (f_eval(c + km, v), c + km, v))

# ---------------- 8-puzzle ----------------
INI = (7,2,4,5,0,6,8,3,1); GOAL = (0,1,2,3,4,5,6,7,8)      # 0 = hueco
POS = {v: divmod(i, 3) for i, v in enumerate(GOAL)}
def h0(e): return 0
def h1(e): return sum(1 for i, v in enumerate(e) if v and v != GOAL[i])
def h2(e): return sum(abs(i//3-POS[v][0]) + abs(i%3-POS[v][1]) for i, v in enumerate(e) if v)
def sucesores(e):
    z = e.index(0); r, c = divmod(z, 3)
    for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            l = list(e); j = nr*3+nc; l[z], l[j] = l[j], l[z]; yield tuple(l)

def resolver(h, voraz=False):
    t0 = time.time(); cnt = 0
    frontera = [(h(INI), 0, cnt, INI)]; g = {INI: 0}; hechos = set(); exp = 0
    while frontera:
        _, c, _, e = heapq.heappop(frontera)
        if e in hechos: continue
        hechos.add(e); exp += 1
        if e == GOAL: return c, exp, time.time()-t0
        for s in sucesores(e):
            if c+1 < g.get(s, 1e9):
                g[s] = c+1; cnt += 1
                heapq.heappush(frontera, ((h(s) if voraz else c+1+h(s)), c+1, cnt, s))

if __name__ == "__main__":
    verificar_heuristica()
    for nombre, f in [("Voraz", lambda c, n: H[n]), ("A*", lambda c, n: c + H[n])]:
        ruta, exp = mejor_primero(f)
        print(f"{nombre:6} {' -> '.join(ruta)}  km={costo(ruta)}  expandidos={exp}")
    print("h1 inicial =", h1(INI), " h2 inicial =", h2(INI))
    print(f"{'Método':14} {'Long.':>5} {'Expandidos':>10} {'Tiempo(s)':>9}")
    for nombre, h, v in [("Costo unif.", h0, False), ("Voraz h2", h2, True), ("A* h1", h1, False), ("A* h2", h2, False)]:
        L, e, t = resolver(h, v); print(f"{nombre:14} {L:>5} {e:>10} {t:>9.2f}")
