
def es_casi_cero(x, tol=1e-10):
    return -tol < x < tol

def formatea_num(x, tol=1e-10):
    """
    Convierte un número a cadena agradable:
    - Si está muy cerca de un entero, imprime entero.
    - Si no, imprime con 10 cifras decimales recortando ceros finales.
    """
    if es_casi_cero(x, tol):
        x = 0.0
    # ¿Cerca de un entero?
    entero = int(round(x))
    if abs(x - entero) < 1e-12:
        return str(entero)
    s = f"{x:.10f}".rstrip("0").rstrip(".")
    return s if s else "0"

def imprime_matriz(M, titulo=None):
    """
    Imprime una matriz (lista de listas) con estilo tipo corchetes.
    Ejemplo:
    [ 1 0 2 | 3 ]
    """
    if titulo:
        print(titulo)
    if not M:
        print("[ ]")
        return
    filas = len(M)
    cols  = len(M[0])
    # Se asume que la matriz recibida es aumentada [A|b], última columna es b
    ult = cols - 1
    for i in range(filas):
        izq = " ".join(formatea_num(M[i][j]) for j in range(ult))
        der = formatea_num(M[i][ult])
        print(f"[ {izq} | {der} ]")

def copia_profunda(M):
    """Copia una matriz (lista de listas) para no modificar el original."""
    return [fila[:] for fila in M]

# ---------- Lectura de datos ----------

def leer_matriz_aumentada():
   
    # Leer m y n
    m = int(input("Número de ecuaciones m = "))
    n = int(input("Número de incógnitas n = "))
    print("Ingrese cada fila con", n, "coeficientes de A y el término independiente b.")
    print("Formato: a1 a2 ... y b   (separados por espacios)")
    aug = []
    for i in range(m):
        while True:
            texto = input(f"Fila {i+1}: ")
            partes = texto.strip().split()
            if len(partes) != n + 1:
                print(f"  -> Debe ingresar exactamente {n+1} valores. Intente de nuevo.")
                continue
            try:
                fila = [float(x) for x in partes]
                aug.append(fila)
                break
            except ValueError:
                print("  -> Solo se permiten números. Intente de nuevo.")
    return aug

def intercambia_filas(M, i, j, pasos, mostrar=True):
    """R_i <-> R_j"""
    if i == j:
        return
    M[i], M[j] = M[j], M[i]
    msg = f"R{i+1} <-> R{j+1}"
    pasos.append(msg)
    if mostrar:
        print(msg)
        imprime_matriz(M)

def escala_fila(M, i, esc, pasos, mostrar=True, tol=1e-10):
    """R_i := (1/esc) * R_i, pensado para normalizar pivote (si esc != 1)."""
    if es_casi_cero(esc, tol) or abs(esc - 1.0) < 1e-15:
        return
    for j in range(len(M[0])):
        M[i][j] /= esc
    msg = f"R{i+1} := (1/{formatea_num(esc)}) * R{i+1}"
    pasos.append(msg)
    if mostrar:
        print(msg)
        imprime_matriz(M)

def combina_fila(M, destino, fuente, factor, pasos, mostrar=True, tol=1e-10):
    """R_destino := R_destino - factor * R_fuente (para anular entradas)."""
    if es_casi_cero(factor, tol):
        return
    for j in range(len(M[0])):
        M[destino][j] -= factor * M[fuente][j]
    signo = "-" if factor >= 0 else "+"
    fac_abs = formatea_num(abs(factor))
    msg = f"R{destino+1} := R{destino+1} {signo} {fac_abs} * R{fuente+1}"
    pasos.append(msg)
    if mostrar:
        print(msg)
        imprime_matriz(M)

# ---------- Gauss-Jordan con pivoteo parcial ----------

def gauss_jordan_rref(aug, tol=1e-10, mostrar=True):
    A = copia_profunda(aug)          # trabajamos sobre una copia
    m = len(A)                       # filas
    n = len(A[0]) - 1 if m else 0    # columnas de A (sin b)
    pasos = []                       # registro de operaciones
    fila_pivote = 0                  # fila actual donde pondremos el próximo pivote
    if mostrar:
        print("\nMatriz aumentada ingresada:")
        imprime_matriz(A)

    # Recorremos columnas de A
    for col in range(n):
        if fila_pivote >= m:
            break

        # --- Pivoteo parcial: elegir fila con mayor |A[i][col]| desde fila_pivote ---
        mejor = fila_pivote
        maxabs = abs(A[mejor][col])
        for i in range(fila_pivote + 1, m):
            if abs(A[i][col]) > maxabs:
                maxabs = abs(A[i][col])
                mejor = i

        # Si el mejor pivote es ~0, no hay pivote en esta columna; pasamos a la siguiente
        if es_casi_cero(maxabs, tol):
            continue

        # Llevar la fila con mejor pivote a 'fila_pivote'
        intercambia_filas(A, fila_pivote, mejor, pasos, mostrar)

        # Normalizar para que el pivote sea 1
        piv = A[fila_pivote][col]
        escala_fila(A, fila_pivote, piv, pasos, mostrar, tol)

        # Anular todas las demás filas en esta columna
        for i in range(m):
            if i == fila_pivote:
                continue
            factor = A[i][col]
            combina_fila(A, i, fila_pivote, factor, pasos, mostrar, tol)

        # Avanzar a la siguiente fila para el próximo pivote
        fila_pivote += 1

    # --- Limpieza numérica: llevar a 0 valores residuales muy pequeños ---
    for i in range(m):
        for j in range(n + 1):
            if es_casi_cero(A[i][j], tol):
                A[i][j] = 0.0

    # --- Detectar inconsistencia: fila [0...0 | c] con c != 0 ---
    inconsistente = False
    for i in range(m):
        todo_cero = True
        for j in range(n):
            if not es_casi_cero(A[i][j], tol):
                todo_cero = False
                break
        if todo_cero and not es_casi_cero(A[i][n], tol):
            inconsistente = True
            break

    # --- Identificar columnas pivote en A (aquellas con un 1 y el resto 0 en esa columna) ---
    pivotes = []
    for col in range(n):
        fila_1 = -1
        ok = True
        for i in range(m):
            if abs(A[i][col] - 1.0) < 1e-12:
                if fila_1 == -1:
                    fila_1 = i
                else:
                    ok = False  # más de un "1" exacto en la columna
                    break
            elif not es_casi_cero(A[i][col], tol):
                ok = False     # algún valor distinto de 0 en la columna
                break
        if ok and fila_1 != -1:
            pivotes.append(col)

    return A, pivotes, inconsistente

# ---------- Deducción y despliegue de soluciones ----------

def clasifica_y_imprime_solucion(rref, pivotes, inconsistente, tol=1e-10):
   
    m = len(rref)
    n = len(rref[0]) - 1 if m else 0

    if inconsistente:
        print("\nSolución: INCONSISTENTE (no existe solución).")
        return

    if len(pivotes) == n:
        # Solución única: los valores están en la última columna donde hay pivote
        x = [0.0] * n
        for r in range(m):
            # localizar columna pivote de esta fila
            col_piv = -1
            for c in range(n):
                if abs(rref[r][c] - 1.0) < 1e-12:
                    col_piv = c
                    break
            if col_piv != -1:
                x[col_piv] = rref[r][n]
        print("\nSolución: ÚNICA")
        for i, xi in enumerate(x, 1):
            print(f"x{i} = {formatea_num(xi)}")
    else:
        # Infinitas soluciones: variables libres = columnas sin pivote
        libres = [c for c in range(n) if c not in pivotes]
        nombres_libres = [f"x{idx+1}" for idx in libres]
        print("\nSolución: INFINITAS (variables libres:", ", ".join(nombres_libres) + ")")
        print("Puede expresarse en forma paramétrica asignando parámetros a las variables libres.")

# ---------- Programa principal ----------

def main():
    """Orquesta la lectura, el proceso Gauss-Jordan y la impresión de resultados."""
    print("=== Resolución de sistemas por Eliminación de Filas (Gauss-Jordan) ===")
    # 1) Leer la matriz aumentada
    aug = leer_matriz_aumentada()

    # 2) Mostrar matriz ingresada
    imprime_matriz(aug, "\nMatriz aumentada [A|b] capturada:")

    # 3) Preguntar si se desean ver todos los pasos
    ver_pasos = input("\n¿Mostrar pasos de eliminación? (s/n): ").strip().lower() == "s"

    # 4) Ejecutar Gauss-Jordan
    rref, pivotes, inconsistente = gauss_jordan_rref(aug, mostrar=ver_pasos)

    # 5) Imprimir RREF final
    imprime_matriz(rref, "\nRREF([A|b]):")

    # 6) Clasificar e imprimir tipo de solución (y valores si es única)
    clasifica_y_imprime_solucion(rref, pivotes, inconsistente)

    print("\nProceso finalizado.")

# Ejecutar si es script principal
if __name__ == "__main__":
    main()
