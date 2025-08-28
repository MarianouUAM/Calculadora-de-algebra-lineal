#
# Función para resolver un sistema de ecuaciones lineales 2x2
# del tipo:
#   a*x + b*y = c
#   d*x + e*y = f
# Usando la fórmula de determinantes (Regla de Cramer)

def ecuacion_lineal(a, b, c, d, e, f):
    # Calculamos el determinante principal: |A| = a*e - b*d
    determinante = (a * e) - (b * d)

    # Verificamos si el determinante es distinto de 0
    # Si es 0, el sistema no tiene solución única (puede ser incompatible o tener infinitas soluciones)
    if determinante != 0:
        # Fórmulas de Cramer:
        # x = (c*e - b*f) / determinante
        # y = (a*f - d*c) / determinante
        # Se agregan paréntesis para evitar errores de precedencia en las operaciones
        x = ((c * e) - (b * f)) / determinante
        y = ((a * f) - (d * c)) / determinante

        # Retornamos el resultado como texto formateado
        return f"X = {x}, Y = {y}"
    else:
        return "El determinante es igual a 0, el sistema no tiene solución única."

# Solicitar al usuario los valores separados por coma
# Ejemplo de entrada: 2,3,6,1,-1,1   (sin espacios)
a, b, c, d, e, f = map(float, input("Ingrese los valores a,b,c,d,e,f separados por coma: ").split(','))

# Llamamos a la función y mostramos el resultado
print(ecuacion_lineal(a, b, c, d, e, f))
