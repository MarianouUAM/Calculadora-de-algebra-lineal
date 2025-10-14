import math

# ==========================================================
#     FUNCIONES AUXILIARES
# ==========================================================
def es_casi_cero(numero, tolerancia=1e-9):
    """Verifica si un número es prácticamente cero"""
    return abs(numero) < tolerancia


def formatea_num(numero, tolerancia=1e-9):
    """Formatea un número para una impresión más limpia"""
    if es_casi_cero(numero, tolerancia):
        return "0"
    entero = int(round(numero))
    if abs(numero - entero) < tolerancia:
        return str(entero)
    return f"{numero:.4f}"


def copia_profunda(matriz):
    """Copia la misma matriz para no tocar la ingresada"""
    return [fila[:] for fila in matriz]


def matriz_a_string(matriz, is_system=False):
    """
    Convertimos la matriz a texto para imprimirla.
    Si is_system es True, formatea una matriz de sistema de ecuaciones.
    """
    if not matriz:
        return "[ ]"
    filas = len(matriz)
    columnas = len(matriz[0])
    salida = []

    for i in range(filas):
        if is_system and columnas > 1:
            izquierda = " ".join(formatea_num(matriz[i][j]) for j in range(columnas - 1))
            derecha = formatea_num(matriz[i][columnas - 1])
            salida.append(f"[ {izquierda} | {derecha} ]")
        else:
            salida.append(f"[ {' '.join(formatea_num(matriz[i][j]) for j in range(columnas))} ]")

    return "\n".join(salida)

# ==========================================================
#     OPERACIONES ENTRE MATRICES (Suma, Multiplicación, Transpuesta)
# ==========================================================
def calcular_operaciones_matrices(matriz_a, matriz_b, operacion):
    """
    Realiza la suma, multiplicación o transpuesta de matrices.
    Incluye pasos explicativos en el caso de la transpuesta.
    """
    # ====== SUMA ======
    if operacion == "suma":
        if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
            return "Error: Las matrices deben tener las mismas dimensiones para la suma."

        filas = len(matriz_a)
        columnas = len(matriz_a[0])
        resultado = [[matriz_a[i][j] + matriz_b[i][j] for j in range(columnas)] for i in range(filas)]
        return resultado

    # ====== MULTIPLICACIÓN ======
    elif operacion == "multiplicacion":
        if len(matriz_a[0]) != len(matriz_b):
            return "Error: El número de columnas de A debe ser igual al número de filas de B."

        filas_a = len(matriz_a)
        columnas_a = len(matriz_a[0])
        columnas_b = len(matriz_b[0])
        resultado = [
            [sum(matriz_a[i][k] * matriz_b[k][j] for k in range(columnas_a)) for j in range(columnas_b)]
            for i in range(filas_a)
        ]
        return resultado

    # ====== TRANSPUESTA ======
    elif operacion == "transpuesta":
        if matriz_a is None or not matriz_a:
            return "Error: Debes proporcionar una matriz válida para calcular la transpuesta."

        filas = len(matriz_a)
        columnas = len(matriz_a[0])

        pasos = []
        pasos.append("Matriz original A:\n" + matriz_a_string(matriz_a))
        pasos.append("Regla: (Las filas de A se convierten en columnas).")

        transpuesta = [[matriz_a[j][i] for j in range(filas)] for i in range(columnas)]

        for i in range(columnas):
            fila_original = [matriz_a[j][i] for j in range(filas)]
            pasos.append(f"Fila {i+1} = Columna {i+1} de A → {fila_original}")

        pasos.append("Resultado final:\n" + matriz_a_string(transpuesta))

        return {"resultado": transpuesta, "pasos": pasos}

    # ====== CASO INVALIDO ======
    else:
        return "Error: Operación no reconocida."


# ==========================================================
#     MÉTODOS DE ELIMINACIÓN Y GAUSS-JORDAN
# ==========================================================
def resolver_eliminacion_filas(matriz_entrada):
    """Resuelve un sistema de ecuaciones por eliminación de filas con todos sus pasos."""
    matriz = copia_profunda(matriz_entrada)
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    pasos = [f"Matriz original:\n{matriz_a_string(matriz, is_system=True)}"]

    fila_pivote = 0
    for indice_columna in range(columnas):
        if fila_pivote >= filas:
            break

        mejor_fila = fila_pivote
        while mejor_fila < filas and es_casi_cero(matriz[mejor_fila][indice_columna]):
            mejor_fila += 1

        if mejor_fila == filas:
            pasos.append(f"Paso: La columna {indice_columna+1} es cero. Se salta.")
            continue

        if mejor_fila != fila_pivote:
            matriz[fila_pivote], matriz[mejor_fila] = matriz[mejor_fila], matriz[fila_pivote]
            pasos.append(f"Paso: F{fila_pivote+1} <-> F{mejor_fila+1}")
            pasos.append(matriz_a_string(matriz, is_system=True))

        pivote = matriz[fila_pivote][indice_columna]
        if not es_casi_cero(pivote) and not es_casi_cero(pivote - 1):
            pasos.append(f"Paso: F{fila_pivote+1} := F{fila_pivote+1} / {formatea_num(pivote)}")
            for j in range(indice_columna, columnas + 1):
                matriz[fila_pivote][j] /= pivote
            pasos.append(matriz_a_string(matriz, is_system=True))

        for indice_fila in range(fila_pivote + 1, filas):
            if es_casi_cero(matriz[indice_fila][indice_columna]):
                continue
            factor = matriz[indice_fila][indice_columna]
            if not es_casi_cero(factor):
                signo = "-" if factor >= 0 else "+"
                factor_absoluto = formatea_num(abs(factor))
                pasos.append(f"Paso: F{indice_fila+1} := F{indice_fila+1} {signo} {factor_absoluto} * F{fila_pivote+1}")
                for indice_j in range(indice_columna, columnas + 1):
                    matriz[indice_fila][indice_j] -= factor * matriz[fila_pivote][indice_j]
                pasos.append(matriz_a_string(matriz, is_system=True))

        fila_pivote += 1

    pasos.append("\nMatriz en forma escalonada (Echelon):\n" + matriz_a_string(matriz, is_system=True))

    inconsistente = False
    for indice_fila in range(filas):
        fila_ceros = all(es_casi_cero(matriz[indice_fila][indice_columna]) for indice_columna in range(columnas))
        if fila_ceros and not es_casi_cero(matriz[indice_fila][columnas]):
            inconsistente = True
            break

    if inconsistente:
        return {"tipo_solucion": "Inconsistente", "solucion": None, "pasos": pasos}

    conteo_pivotes = 0
    for indice_fila in range(filas):
        if any(not es_casi_cero(matriz[indice_fila][indice_columna]) for indice_columna in range(columnas)):
            conteo_pivotes += 1

    if conteo_pivotes < columnas:
        return {"tipo_solucion": "Infinita", "solucion": None, "pasos": pasos}

    solucion = [0.0] * columnas
    for i in range(columnas - 1, -1, -1):
        solucion[i] = matriz[i][columnas]
        for j in range(i + 1, columnas):
            solucion[i] -= matriz[i][j] * solucion[j]
        solucion[i] /= matriz[i][i]

    return {"tipo_solucion": "Única", "solucion": [formatea_num(s) for s in solucion], "pasos": pasos}


def resolver_gauss_jordan(matriz_entrada):
    """Resuelve un sistema por Gauss-Jordan enseñando sus pasos."""
    matriz = copia_profunda(matriz_entrada)
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    pasos = [f"Matriz original:\n{matriz_a_string(matriz, is_system=True)}"]
    columnas_pivote = []

    fila_pivote = 0
    for indice_columna in range(columnas):
        if fila_pivote >= filas:
            break

        mejor_fila = fila_pivote
        maximo_absoluto = abs(matriz[mejor_fila][indice_columna])
        for indice_fila in range(fila_pivote + 1, filas):
            if abs(matriz[indice_fila][indice_columna]) > maximo_absoluto:
                maximo_absoluto = abs(matriz[indice_fila][indice_columna])
                mejor_fila = indice_fila

        if es_casi_cero(maximo_absoluto):
            pasos.append(f"\nColumna {indice_columna+1}: No hay pivote (todos ceros). Variable libre: x{indice_columna+1}.")
            continue

        if mejor_fila != fila_pivote:
            pasos.append(f"\nPaso: F{fila_pivote+1} <-> F{mejor_fila+1}")
            matriz[fila_pivote], matriz[mejor_fila] = matriz[mejor_fila], matriz[fila_pivote]
            pasos.append(matriz_a_string(matriz, is_system=True))

        pivote = matriz[fila_pivote][indice_columna]
        if not es_casi_cero(pivote - 1):
            pasos.append(f"\nPaso: F{fila_pivote+1} := (1/{formatea_num(pivote)}) * F{fila_pivote+1}")
            for j in range(indice_columna, columnas + 1):
                matriz[fila_pivote][j] /= pivote
            pasos.append(matriz_a_string(matriz, is_system=True))

        pasos.append(f"\nPaso: Anulando otras entradas en la columna {indice_columna+1}.")
        for indice_fila in range(filas):
            if indice_fila == fila_pivote:
                continue
            factor = matriz[indice_fila][indice_columna]
            if not es_casi_cero(factor):
                signo = "-" if factor >= 0 else "+"
                factor_absoluto = formatea_num(abs(factor))
                pasos.append(f"  F{indice_fila+1} := F{indice_fila+1} {signo} {factor_absoluto} * F{fila_pivote+1}")
                for indice_j in range(indice_columna, columnas + 1):
                    matriz[indice_fila][indice_j] -= factor * matriz[fila_pivote][indice_j]
        pasos.append(matriz_a_string(matriz, is_system=True))

        columnas_pivote.append(indice_columna)
        fila_pivote += 1

    for indice_fila in range(filas):
        for indice_columna in range(columnas + 1):
            if es_casi_cero(matriz[indice_fila][indice_columna]):
                matriz[indice_fila][indice_columna] = 0.0

    inconsistente = any(
        all(es_casi_cero(matriz[indice_fila][indice_columna]) for indice_columna in range(columnas)) and not es_casi_cero(matriz[indice_fila][columnas])
        for indice_fila in range(filas)
    )

    if inconsistente:
        tipo = "Inconsistente"
        solucion = None
    elif len(columnas_pivote) == columnas:
        tipo = "Única"
        solucion = [formatea_num(matriz[indice_fila][columnas]) for indice_fila in range(columnas)]
    else:
        tipo = "Infinita"
        solucion = None

    return {
        "matriz_rref": matriz,
        "pasos": pasos,
        "columnas_pivote": [c + 1 for c in columnas_pivote],
        "variables_libres": [f"x{c+1}" for c in range(columnas) if c not in columnas_pivote],
        "tipo_solucion": tipo,
        "solucion": solucion,
    }

# ==========================================================
#     RESOLVER SISTEMA HOMOGÉNEO    
# ==========================================================
def resolver_sistema_homogeneo(matriz_entrada):
    """
    Resuelve un sistema homogéneo Ax = 0 usando Gauss-Jordan.
    La matriz_entrada debe incluir la columna de ceros al final.
    Siempre retorna un diccionario.
    """
    # Validación inicial
    if not matriz_entrada or not isinstance(matriz_entrada, list):
        return {
            "tipo_solucion": "Error",
            "pasos": ["La matriz está vacía o no es válida."],
            "variables_libres": [],
            "pivotes": [],
            "solucion_parametrica": [],
            "parametros": [],
            "matriz_rref": []
        }

    matriz = copia_profunda(matriz_entrada)
    filas = len(matriz)
    columnas_totales = len(matriz[0])
    
    if columnas_totales < 1:
        return {
            "tipo_solucion": "Error",
            "pasos": ["La matriz no tiene columnas."],
            "variables_libres": [],
            "pivotes": [],
            "solucion_parametrica": [],
            "parametros": [],
            "matriz_rref": matriz
        }

    columnas = columnas_totales - 1  # Última columna = 0
    pasos = [f"Matriz original (sistema homogéneo):\n{matriz_a_string(matriz, is_system=True)}"]

    fila_pivote = 0
    columnas_pivote = []

    # ==============================
    #    PROCESO GAUSS-JORDAN
    # ==============================
    for col in range(columnas):
        if fila_pivote >= filas:
            break

        mejor_fila = fila_pivote
        while mejor_fila < filas and es_casi_cero(matriz[mejor_fila][col]):
            mejor_fila += 1

        if mejor_fila == filas:
            pasos.append(f"Columna {col+1}: Sin pivote, variable libre: x{col+1}")
            continue

        if mejor_fila != fila_pivote:
            pasos.append(f"Paso: F{fila_pivote+1} <-> F{mejor_fila+1}")
            matriz[fila_pivote], matriz[mejor_fila] = matriz[mejor_fila], matriz[fila_pivote]
            pasos.append(matriz_a_string(matriz, is_system=True))

        pivote = matriz[fila_pivote][col]
        if not es_casi_cero(pivote - 1):
            pasos.append(f"Paso: F{fila_pivote+1} := F{fila_pivote+1} / {formatea_num(pivote)}")
            for j in range(col, columnas + 1):
                matriz[fila_pivote][j] /= pivote
            pasos.append(matriz_a_string(matriz, is_system=True))

        for f in range(filas):
            if f != fila_pivote and not es_casi_cero(matriz[f][col]):
                factor = matriz[f][col]
                pasos.append(f"Paso: F{f+1} := F{f+1} - {formatea_num(factor)} * F{fila_pivote+1}")
                for j in range(col, columnas + 1):
                    matriz[f][j] -= factor * matriz[fila_pivote][j]
                pasos.append(matriz_a_string(matriz, is_system=True))

        columnas_pivote.append(col)
        fila_pivote += 1

    pasos.append("\nMatriz en RREF:\n" + matriz_a_string(matriz, is_system=True))

    # ==============================
    #    ANÁLISIS DE SOLUCIÓN
    # ==============================
    pivotes = columnas_pivote
    libres = [c for c in range(columnas) if c not in pivotes]

    # Caso trivial (sin variables libres)
    if not libres:
        pasos.append("\nNo hay variables libres → solución única (trivial): x = 0")
        return {
            "tipo_solucion": "Única (trivial)",
            "pasos": pasos,
            "variables_libres": [],
            "pivotes": [p+1 for p in pivotes],
            "solucion_parametrica": [],
            "parametros": [],
            "matriz_rref": matriz
        }

    # ==============================
    #  Construir solución general
    # ==============================
    pasos.append(f"\nVariables pivote: {', '.join('x'+str(p+1) for p in pivotes)}")
    pasos.append(f"Variables libres: {', '.join('x'+str(l+1) for l in libres)}")

    coeficientes = []
    parametros = []

    for idx, col_libre in enumerate(libres):
        t = f"t{idx+1}"
        parametros.append(t)
        vector_param = [0]*columnas
        vector_param[col_libre] = 1

        for i, p in enumerate(pivotes):
            valor = matriz[i][col_libre]
            vector_param[p] = -valor if not es_casi_cero(valor) else 0

        coeficientes.append(vector_param)

    pasos.append("\nSolución general:")
    for idx, vec in enumerate(coeficientes):
        t = parametros[idx]
        for var_index, coef in enumerate(vec):
            if not es_casi_cero(coef):
                pasos.append(f"x{var_index+1} = {formatea_num(coef)} * {t}")

    return {
        "tipo_solucion": "Infinitas",
        "pasos": pasos,
        "variables_libres": [f"x{l+1}" for l in libres],
        "pivotes": [p+1 for p in pivotes],
        "solucion_parametrica": coeficientes,
        "parametros": parametros,
        "matriz_rref": matriz
    }

def construir_matriz_transformacion(expresiones, num_variables):
    """
    Construye la matriz A de una transformación T(x)=A·x a partir de expresiones tipo '3x1 - 2x2 + 5x3'.
    Devuelve una tupla: (pasos, matriz_A)
    pasos = lista de strings explicando el proceso
    matriz_A = lista de listas con los coeficientes
    """

    pasos = []
    matriz_A = []

    for idx_ec, expr in enumerate(expresiones):
        expr_original = expr  # Guardar la expresión original para mostrarla
        expr = expr.replace(" ", "")  # Quitar espacios

        pasos.append(f"Ecuación {idx_ec + 1}: {expr_original}")
        fila = [0.0] * num_variables

        # Normalizar signos: reemplazar '-' por '+-' para poder dividir términos fácilmente
        expr = expr.replace("-", "+-")
        if expr.startswith("+-"):
            expr = "-" + expr[2:]

        terminos = expr.split("+")

        for term in terminos:
            if term == "":
                continue

            variable_encontrada = False

            for var_idx in range(num_variables):
                var_name = f"x{var_idx + 1}"
                if var_name in term:
                    variable_encontrada = True
                    coef_str = term.replace(var_name, "")
                    if coef_str == "" or coef_str == "+":
                        coef = 1.0
                    elif coef_str == "-":
                        coef = -1.0
                    else:
                        try:
                            coef = float(coef_str)
                        except ValueError:
                            coef = 0.0
                    fila[var_idx] = coef
                    pasos.append(f"  Coeficiente de x{var_idx + 1}: {coef}")
                    break

            if not variable_encontrada:
                try:
                    constante = float(term)
                    if abs(constante) > 1e-9:
                        pasos.append(f"  Advertencia: término '{term}' no contiene variable, se ignora.")
                except ValueError:
                    pasos.append(f"  Advertencia: término '{term}' no se pudo interpretar y se ignora.")

        pasos.append(f"Fila {idx_ec + 1} de la matriz A: {fila}\n")
        matriz_A.append(fila)

    pasos.append("Matriz final A:")
    for fila in matriz_A:
        pasos.append(str(fila))

    return pasos, matriz_A



# ==========================================================
#     VERIFICACIÓN DE INDEPENDENCIA LINEAL
# ==========================================================
def verificar_independencia_lineal(vectores):
    """Determina si un conjunto de vectores es linealmente independiente o dependiente."""
    if not vectores:
        return "Error: No se ingresaron vectores."

    n = len(vectores)
    m = len(vectores[0])

    for v in vectores:
        if len(v) != m:
            return "Error: todos los vectores deben tener la misma dimensión."

    matriz = [fila[:] for fila in vectores]
    matriz = [[matriz[j][i] for j in range(n)] for i in range(m)]
    pasos = [f"Matriz formada por los vectores (cada columna = un vector):\n{matriz_a_string(matriz)}"]

    fila_actual = 0
    for columna in range(n):
        pivote = None
        for f in range(fila_actual, m):
            if not es_casi_cero(matriz[f][columna]):
                pivote = f
                break

        if pivote is None:
            pasos.append(f"Columna {columna+1}: todos ceros → sin pivote.")
            continue

        if pivote != fila_actual:
            matriz[fila_actual], matriz[pivote] = matriz[pivote], matriz[fila_actual]
            pasos.append(f"Intercambio: F{fila_actual+1} <-> F{pivote+1}")
            pasos.append(matriz_a_string(matriz))

        pivote_valor = matriz[fila_actual][columna]
        if not es_casi_cero(pivote_valor - 1):
            pasos.append(f"Normalizar F{fila_actual+1}: dividir entre {formatea_num(pivote_valor)}")
        for c in range(n):
            matriz[fila_actual][c] /= pivote_valor
        pasos.append(matriz_a_string(matriz))

        for f in range(m):
            if f != fila_actual:
                factor = matriz[f][columna]
                if not es_casi_cero(factor):
                    signo = "-" if factor >= 0 else "+"
                    pasos.append(f"F{f+1} := F{f+1} {signo} {formatea_num(abs(factor))} * F{fila_actual+1}")
                    for c in range(n):
                        matriz[f][c] -= factor * matriz[fila_actual][c]
                    pasos.append(matriz_a_string(matriz))
        fila_actual += 1

    rango = sum(any(not es_casi_cero(x) for x in fila) for fila in matriz)
    pasos.append(f"\nRango de la matriz: {rango}")
    pasos.append(f"Número de vectores: {n}")

    if rango == n:
        resultado = "Los vectores son LINEALMENTE INDEPENDIENTES."
    else:
        resultado = "Los vectores son LINEALMENTE DEPENDIENTES."

    pasos.append(resultado)
    return "\n".join(pasos)