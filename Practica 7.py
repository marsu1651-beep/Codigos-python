import random, math, copy

# ---------- Parte A ----------
VEC = {"CDMX": ["Edomex","Morelos"],
       "Edomex": ["CDMX","Morelos","Puebla","Tlaxcala","Hidalgo","Querétaro","Guerrero","Michoacán"],
       "Morelos": ["CDMX","Edomex","Puebla","Guerrero"],
       "Puebla": ["Edomex","Morelos","Tlaxcala","Hidalgo","Guerrero"],
       "Tlaxcala": ["Edomex","Puebla","Hidalgo"],
       "Hidalgo": ["Edomex","Puebla","Tlaxcala","Querétaro"],
       "Querétaro": ["Edomex","Hidalgo","Michoacán"],
       "Guerrero": ["Edomex","Morelos","Puebla","Michoacán"],
       "Michoacán": ["Edomex","Guerrero","Querétaro"]}
for a in VEC:
    for b in VEC[a]: assert a in VEC[b], (a, b)            # simetría de la vecindad
def backtracking(colores):
    dom = {v: list(colores) for v in VEC}; asig = {}; nodos = [0]
    def forward(var, val, dom):
        nuevo = copy.deepcopy(dom)
        for w in VEC[var]:
            if w not in asig and val in nuevo[w]:
                nuevo[w].remove(val)
                if not nuevo[w]: return None                # dominio vacío -> falla
        return nuevo
    def bt(dom):
        nodos[0] += 1
        if len(asig) == len(VEC): return True
        libres = [v for v in VEC if v not in asig]
        var = min(libres, key=lambda v: (len(dom[v]), -sum(w not in asig for w in VEC[v])))   # MRV, desempate: grado
        def lcv(val): return sum(val in dom[w] for w in VEC[var] if w not in asig)           # valor que menos restringe
        for val in sorted(dom[var], key=lcv):
            asig[var] = val; nd = forward(var, val, dom)
            if nd and bt(nd): return True
            del asig[var]
        return False
    ok = bt(dom); return (dict(asig) if ok else None), nodos[0]

# ---------- Parte B ----------
random.seed(42)
CIUDADES = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(15)]
def longitud(r): return sum(math.dist(CIUDADES[r[i]], CIUDADES[r[(i+1) % 15]]) for i in range(15))
def torneo(pob, fit, k=3): return min(random.sample(range(len(pob)), k), key=lambda i: fit[i])
def cruza_ox(p1, p2):
    a, b = sorted(random.sample(range(15), 2)); hijo = [None]*15; hijo[a:b+1] = p1[a:b+1]
    resto = [c for c in p2 if c not in hijo[a:b+1]]; j = 0
    for i in range(15):
        if hijo[i] is None: hijo[i] = resto[j]; j += 1
    return hijo
def mutar(r, pm):
    if random.random() < pm:
        a, b = sorted(random.sample(range(15), 2)); r[a:b+1] = reversed(r[a:b+1])   # inversión
    return r
def ag(tam=100, gens=300, pm=0.2, elite=2):
    pob = [random.sample(range(15), 15) for _ in range(tam)]; hist = []; evals = 0
    for _ in range(gens):
        fit = [longitud(r) for r in pob]; evals += tam
        orden = sorted(range(tam), key=lambda i: fit[i]); hist.append(fit[orden[0]])
        nueva = [pob[i][:] for i in orden[:elite]]
        while len(nueva) < tam:
            nueva.append(mutar(cruza_ox(pob[torneo(pob, fit)], pob[torneo(pob, fit)]), pm))
        pob = nueva
    fit = [longitud(r) for r in pob]; i = min(range(tam), key=lambda i: fit[i])
    return pob[i], fit[i], hist, evals
def aleatoria(n):
    return min((longitud(random.sample(range(15), 15)) for _ in range(n)))

if __name__ == "__main__":
    for k in (3, 4):
        sol, nodos = backtracking(["rojo","verde","azul","amarillo"][:k])
        print(f"{k} colores:", "SIN solución" if sol is None else sol, f"| nodos={nodos}")
    print("\nAG vs búsqueda aleatoria (≈30 000 evaluaciones), 5 corridas por configuración")
    print(f"{'Población':>9} {'P.mut':>6} {'Media AG':>9} {'Desv.':>6} {'Mejor':>7}")
    import statistics as st
    for tam, pm in [(50, 0.1), (50, 0.3), (100, 0.1), (100, 0.3)]:
        res = [ag(tam, 30000 // tam, pm)[1] for _ in range(5)]
        print(f"{tam:>9} {pm:>6} {st.mean(res):>9.1f} {st.pstdev(res):>6.1f} {min(res):>7.1f}")
    al = [aleatoria(30000) for _ in range(5)]
    print(f"Aleatoria (30 000 eval.): media={st.mean(al):.1f} desv={st.pstdev(al):.1f} mejor={min(al):.1f}")
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        ruta, L, hist, _ = ag(100, 300, 0.2)
        fig, ax = plt.subplots(1, 2, figsize=(11, 4))
        ax[0].plot(hist); ax[0].set(title="Convergencia del AG", xlabel="Generación", ylabel="Mejor longitud")
        xs = [CIUDADES[i][0] for i in ruta + [ruta[0]]]; ys = [CIUDADES[i][1] for i in ruta + [ruta[0]]]
        ax[1].plot(xs, ys, "o-"); ax[1].set(title=f"Mejor ruta (L={L:.1f})")
        plt.tight_layout(); plt.savefig("p7_resultados.png", dpi=120); print("Gráficas guardadas en p7_resultados.png")
    except ImportError: print("(instala matplotlib para las gráficas)")
