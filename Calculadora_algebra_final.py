# logica_calculadora.py
import math

def es_casi_cero(numero, tolerancia=1e-4):
    """Verifica si un número es prácticamente cero"""
    return -tolerancia < numero < tolerancia

def formatea_num(numero, tolerancia=1e-4):
    """Formatea un número para una impresión más limpia"""
    if es_casi_cero(numero, tolerancia):
        return "0"
    entero = int(round(numero))
    if abs(numero - entero) < 1e-4:
        return str(entero)
    string_formateado = f"{numero:.10f}".rstrip("0").rstrip(".")
    return string_formateado if string_formateado else "0"

def copia_profunda(matriz):
    """Copia la misma matriz para no tocar la ingresada"""
    return [fila[:] for fila in matriz]

def matriz_a_string(matriz, titulo=None):
    """Convertimos la matriz a texto para imprimirla{}"""
    if not matriz:
        return "[ ]"
    filas = len(matriz)
    columnas = len(matriz[0])
    ultima_columna = columnas - 1
    salida = []
    if titulo:
        salida.append(titulo)
    for indice_fila in range(filas):
        izquierda = " ".join(formatea_num(matriz[indice_fila][indice_columna]) for indice_columna in range(ultima_columna))
        derecha = formatea_num(matriz[indice_fila][ultima_columna])
        salida.append(f"[ {izquierda} | {derecha} ]")
    return "\n".join(salida)

def resolver_eliminacion_filas(matriz_entrada):
    """
    Resuelve un sistema de ecuaciones por eliminación de filas con todos sus pasos
    """
    matriz = copia_profunda(matriz_entrada)
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    pasos = [matriz_a_string(matriz, "Matriz original:")]
    
    "Elimacion"
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
            pasos.append(matriz_a_string(matriz))

        for indice_fila in range(fila_pivote + 1, filas):
            if es_casi_cero(matriz[fila_pivote][indice_columna]): continue
            factor = matriz[indice_fila][indice_columna] / matriz[fila_pivote][indice_columna]
            if not es_casi_cero(factor):
                signo = "-" if factor >= 0 else "+"
                factor_absoluto = formatea_num(abs(factor))
                pasos.append(f"Paso: F{indice_fila+1} := F{indice_fila+1} {signo} {factor_absoluto} * F{fila_pivote+1}")
                for indice_j in range(indice_columna, columnas + 1):
                    matriz[indice_fila][indice_j] -= factor * matriz[fila_pivote][indice_j]
                pasos.append(matriz_a_string(matriz))

        fila_pivote += 1

    for indice_fila in range(filas):
        for indice_columna in range(columnas + 1):
            if es_casi_cero(matriz[indice_fila][indice_columna]):
                matriz[indice_fila][indice_columna] = 0.0

    pasos.append("\nMatriz en forma escalonada (Echelon):")
    pasos.append(matriz_a_string(matriz))

    inconsistente = False
    for indice_fila in range(filas):
        fila_ceros = all(es_casi_cero(matriz[indice_fila][indice_columna]) for indice_columna in range(columnas))
        if fila_ceros and not es_casi_cero(matriz[indice_fila][columnas]):
            inconsistente = True
            break
            
    if inconsistente:
        return {"tipo_solucion": "Inconsistente", "solucion": None, "pasos": pasos}

    solucion = [0.0] * columnas
    conteo_pivotes = 0
    for indice_fila in range(filas):
        if any(not es_casi_cero(matriz[indice_fila][indice_columna]) for indice_columna in range(columnas)):
            conteo_pivotes += 1
    
    if conteo_pivotes < columnas:
        return {"tipo_solucion": "Infinita", "solucion": None, "pasos": pasos}
        
    for indice_fila in range(columnas - 1, -1, -1):
        solucion[indice_fila] = matriz[indice_fila][columnas]
        for indice_j in range(indice_fila + 1, columnas):
            solucion[indice_fila] -= matriz[indice_fila][indice_j] * solucion[indice_j]
        solucion[indice_fila] /= matriz[indice_fila][indice_fila]
        
    return {"tipo_solucion": "Única", "solucion": [formatea_num(s) for s in solucion], "pasos": pasos}

def resolver_gauss_jordan(matriz_entrada):
    """
    Resuelve un sistema por Gauss-Jordan enseñando sus pasos.
    """
    matriz = copia_profunda(matriz_entrada)
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    pasos = [matriz_a_string(matriz, "Matriz original:")]
    columnas_pivote = []

    "Elimacion"
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
            pasos.append(matriz_a_string(matriz))

        pivote = matriz[fila_pivote][indice_columna]
        if not es_casi_cero(pivote - 1):
            pasos.append(f"\nPaso: F{fila_pivote+1} := (1/{formatea_num(pivote)}) * F{fila_pivote+1}")
            for indice_j in range(indice_columna, columnas + 1):
                matriz[fila_pivote][indice_j] /= pivote
            pasos.append(matriz_a_string(matriz))

        pasos.append(f"\nPaso: Anulando otras entradas en la columna {indice_columna+1}.")
        for indice_fila in range(filas):
            if indice_fila == fila_pivote:
                continue
            factor = matriz[indice_fila][indice_columna]
            if not es_casi_cero(factor):
                signo = "-" if factor >= 0 else "+"
                factor_absoluto = formatea_num(abs(factor))
                pasos.append(f"   F{indice_fila+1} := F{indice_fila+1} {signo} {factor_absoluto} * F{fila_pivote+1}")
                for indice_j in range(indice_columna, columnas + 1):
                    matriz[indice_fila][indice_j] -= factor * matriz[fila_pivote][indice_j]
        pasos.append(matriz_a_string(matriz))

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
        "solucion": solucion
    }
