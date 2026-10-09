from collections import deque

# ---------- Parte A: estado (m, c, b) = misioneros y caníbales en la orilla izquierda, b=1 si la barca está a la izquierda
INI_A, META_A = (3, 3, 1), (0, 0, 0)
MOVS = [(1,0),(2,0),(0,1),(0,2),(1,1)]
def valido(m, c):
    if not (0 <= m <= 3 and 0 <= c <= 3): return False
    return (m == 0 or m >= c) and (3-m == 0 or 3-m >= 3-c)     # nunca más caníbales que misioneros (si hay misioneros)
def sucesores_a(e):
    m, c, b = e; sgn = -1 if b else 1
    for dm, dc in MOVS:
        nm, nc = m + sgn*dm, c + sgn*dc
        if valido(nm, nc): yield (dm, dc), (nm, nc, 1-b)
def bfs_a():
    padre = {INI_A: None}; q = deque([INI_A])
    while q:
        e = q.popleft()
        if e == META_A: break
        for mov, s in sucesores_a(e):
            if s not in padre: padre[s] = (e, mov); q.append(s)
    r = []; s = META_A
    while padre[s]: p, mov = padre[s]; r.append((mov, s)); s = p
    return r[::-1], len(padre)

# ---------- Parte B: gato
LINEAS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def ganador(t):
    for a, b, c in LINEAS:
        if t[a] != " " and t[a] == t[b] == t[c]: return t[a]
def terminal(t): return ganador(t) is not None or " " not in t
def utilidad(t): return {"X": 1, "O": -1, None: 0}[ganador(t)]
def sucesores(t, j):
    for i in range(9):
        if t[i] == " ": yield i, t[:i] + j + t[i+1:]
N = [0]
def minimax(t, max_turno):
    N[0] += 1
    if terminal(t): return utilidad(t)
    vals = [minimax(s, not max_turno) for _, s in sucesores(t, "X" if max_turno else "O")]
    return max(vals) if max_turno else min(vals)
def alfabeta(t, a, b, max_turno):
    N[0] += 1
    if terminal(t): return utilidad(t)
    if max_turno:
        v = -2
        for _, s in sucesores(t, "X"):
            v = max(v, alfabeta(s, a, b, False)); a = max(a, v)
            if a >= b: break
        return v
    v = 2
    for _, s in sucesores(t, "O"):
        v = min(v, alfabeta(s, a, b, True)); b = min(b, v)
        if a >= b: break
    return v
def mejor_jugada(t, jugador):                 # la computadora usa alfa-beta
    mx = jugador == "X"; mejor = None; mv = -2 if mx else 2
    for i, s in sucesores(t, jugador):
        v = alfabeta(s, -2, 2, not mx)
        if (mx and v > mv) or (not mx and v < mv): mv, mejor = v, i
    return mejor
def mostrar(t): print("\n".join(" " + " | ".join(t[r*3:r*3+3]) for r in range(3)).replace("\n", "\n---+---+---\n"))
def jugar():                                   # persona (X) vs computadora (O)
    t = " " * 9; turno = "X"
    while not terminal(t):
        mostrar(t)
        if turno == "X":
            i = int(input("\nTu jugada (0-8): "))
            if t[i] != " ": print("Casilla ocupada"); continue
        else: i = mejor_jugada(t, "O")
        t = t[:i] + turno + t[i+1:]; turno = "O" if turno == "X" else "X"
    mostrar(t); print("Ganador:", ganador(t) or "empate")
def verificar_invencible():
    """La computadora (O) nunca pierde: se prueban TODAS las respuestas posibles de X."""
    def rec(t, turno):
        if terminal(t): return ganador(t) != "X"
        if turno == "O": return rec(t[:(i := mejor_jugada(t, "O"))] + "O" + t[i+1:], "X")
        return all(rec(s, "O") for _, s in sucesores(t, "X"))
    return rec(" " * 9, "X")

if __name__ == "__main__":
    sol, n = bfs_a()
    print(f"Parte A: {len(sol)} cruces ({n} estados alcanzados)")
    for k, (mov, s) in enumerate(sol, 1): print(f" {k:>2}. cruzan {mov} (M,C) -> (m,c,b)={s}")
    N[0] = 0; v1 = minimax(" " * 9, True); n1 = N[0]
    N[0] = 0; v2 = alfabeta(" " * 9, -2, 2, True); n2 = N[0]
    print(f"\nParte B: valor minimax={v1} ({n1} nodos) | alfa-beta={v2} ({n2} nodos) | reducción {100*(1-n2/n1):.1f}%")
    print("La computadora (O) nunca pierde contra ninguna secuencia de X:", verificar_invencible())
    # jugar()   # <- descomenta para jugar persona vs computadora
