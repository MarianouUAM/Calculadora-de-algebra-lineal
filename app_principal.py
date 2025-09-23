import tkinter as tk
from tkinter import messagebox, scrolledtext, font, ttk
import math
from logica_calculadora import resolver_gauss_jordan, resolver_eliminacion_filas, matriz_a_string, formatea_num, calcular_operaciones_matrices

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica ⚛️")
        self.root.geometry("800x650")
        self.root.configure(bg="#363636")
        
        self.entradas_matriz_a = []
        self.entradas_matriz_b = []
        self.filas_a = 0
        self.columnas_a = 0
        self.filas_b = 0
        self.columnas_b = 0
        self.metodo_actual = ""
        
        self.crear_widgets_menu_principal()

    def limpiar_pantalla(self):
        """Elimina todos los widgets de la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_widgets_menu_principal(self):
        """Crea la interfaz del menú de bienvenida."""
        self.limpiar_pantalla()
        self.root.geometry("800x650")
        
        main_frame = tk.Frame(self.root, bg="#363636", padx=30, pady=30, relief=tk.FLAT, bd=0)
        main_frame.pack(expand=True, fill="both")

        title_label = tk.Label(main_frame, text="CALCULADORA CIENTÍFICA", font=("Arial", 28, "bold"), fg="#FFD700", bg="#363636")
        title_label.pack(pady=(20, 5))
        
        welcome_label = tk.Label(main_frame, text="BIENVENIDOS", font=("Arial", 16, "bold"), fg="#D3D3D3", bg="#363636")
        welcome_label.pack(pady=(0, 30))

        button_frame = tk.Frame(main_frame, bg="#4F4F4F", padx=20, pady=20, relief=tk.RIDGE, bd=2)
        button_frame.pack(pady=20)
        
        style_button = {"font": ("Arial", 12), "fg": "#000", "bg": "#D3D3D3", "width": 30, "height": 2, "bd": 3, "relief": tk.RAISED}
        
        btn_gauss_jordan = tk.Button(button_frame, text="Método de Gauss-Jordan", command=lambda: self.preparar_matriz_unica("Gauss-Jordan"), **style_button)
        btn_gauss_jordan.pack(pady=10)
        
        btn_eliminacion = tk.Button(button_frame, text="Método de Eliminación de Filas", command=lambda: self.preparar_matriz_unica("Eliminación"), **style_button)
        btn_eliminacion.pack(pady=10)

        new_button_frame = tk.Frame(main_frame, bg="#363636")
        new_button_frame.pack(pady=(10, 20))

        new_label = tk.Label(new_button_frame, text="¡NUEVO!", font=("Arial", 12, "bold"), fg="#FF0000", bg="#363636")
        new_label.pack(side=tk.TOP)
        
        btn_operaciones = tk.Button(new_button_frame, text="Método de Suma y Multiplicación", command=self.preparar_matrices_operaciones, **style_button)
        btn_operaciones.pack()

        btn_salir = tk.Button(main_frame, text="SALIR", font=("Arial", 14, "bold"), bg="#FF4500", fg="#000", relief=tk.RAISED, bd=3, width=10, command=self.root.destroy)
        btn_salir.pack(pady=20)
        
    def preparar_matrices_operaciones(self):
        """Pide las dimensiones para dos matrices."""
        self.limpiar_pantalla()
        self.root.geometry("800x600")
        
        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")
        
        titulo = tk.Label(marco, text="Ingresa las Dimensiones de las Matrices", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
        titulo.pack(pady=10)

        # Marco para la Matriz A
        frame_a = tk.LabelFrame(marco, text="Matriz A", padx=10, pady=10)
        frame_a.pack(pady=10)
        
        tk.Label(frame_a, text="Filas (m):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.entrada_filas_a = tk.Entry(frame_a, width=5, font=("Helvetica", 12))
        self.entrada_filas_a.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_a, text="Columnas (n):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.entrada_columnas_a = tk.Entry(frame_a, width=5, font=("Helvetica", 12))
        self.entrada_columnas_a.pack(side=tk.LEFT, padx=5)

        # Marco para la Matriz B
        frame_b = tk.LabelFrame(marco, text="Matriz B", padx=10, pady=10)
        frame_b.pack(pady=10)
        
        tk.Label(frame_b, text="Filas (m):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.entrada_filas_b = tk.Entry(frame_b, width=5, font=("Helvetica", 12))
        self.entrada_filas_b.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_b, text="Columnas (n):", font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        self.entrada_columnas_b = tk.Entry(frame_b, width=5, font=("Helvetica", 12))
        self.entrada_columnas_b.pack(side=tk.LEFT, padx=5)
        
        btn_crear = tk.Button(marco, text="Crear Matrices", font=("Helvetica", 12, "bold"), command=self.crear_interfaz_operaciones_matrices)
        btn_crear.pack(pady=10)
        
        btn_volver = tk.Button(marco, text="Volver", command=self.crear_widgets_menu_principal, bg="#FFCDD2")
        btn_volver.pack(pady=10)

    def crear_interfaz_operaciones_matrices(self):
        """Crea la interfaz para ingresar dos matrices con sus dimensiones."""
        try:
            self.filas_a = int(self.entrada_filas_a.get())
            self.columnas_a = int(self.entrada_columnas_a.get())
            self.filas_b = int(self.entrada_filas_b.get())
            self.columnas_b = int(self.entrada_columnas_b.get())
            
            if self.filas_a <= 0 or self.columnas_a <= 0 or self.filas_b <= 0 or self.columnas_b <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingresa números enteros positivos para las dimensiones.")
            return

        self.limpiar_pantalla()
        
        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")
        
        titulo = tk.Label(marco, text="Ingresa los valores de las matrices:", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
        titulo.pack(pady=10)

        # Frame para las dos matrices
        matrices_frame = tk.Frame(marco, bg="#F0F0F0")
        matrices_frame.pack(pady=10)

        # Marco para la Matriz A
        marco_matriz_a = tk.Frame(matrices_frame, bg="#F0F0F0")
        marco_matriz_a.pack(side=tk.LEFT, padx=20, anchor=tk.N)
        tk.Label(marco_matriz_a, text="Matriz A", font=("Helvetica", 14), bg="#F0F0F0").pack()
        self.entradas_matriz_a = self.crear_cuadricula_matriz(marco_matriz_a, self.filas_a, self.columnas_a)

        # Marco para la Matriz B
        marco_matriz_b = tk.Frame(matrices_frame, bg="#F0F0F0")
        marco_matriz_b.pack(side=tk.LEFT, padx=20, anchor=tk.N)
        tk.Label(marco_matriz_b, text="Matriz B", font=("Helvetica", 14), bg="#F0F0F0").pack()
        self.entradas_matriz_b = self.crear_cuadricula_matriz(marco_matriz_b, self.filas_b, self.columnas_b)
        
        op_frame = tk.Frame(marco, bg="#F0F0F0")
        op_frame.pack(pady=20)

        btn_sumar = tk.Button(op_frame, text="Sumar Matrices", font=("Helvetica", 12, "bold"), command=lambda: self.resolver_operaciones("suma"))
        btn_sumar.pack(side=tk.LEFT, padx=10)

        btn_multiplicar = tk.Button(op_frame, text="Multiplicar Matrices", font=("Helvetica", 12, "bold"), command=lambda: self.resolver_operaciones("multiplicacion"))
        btn_multiplicar.pack(side=tk.LEFT, padx=10)
        
        btn_volver = tk.Button(marco, text="Volver", command=self.preparar_matrices_operaciones, bg="#FFCDD2")
        btn_volver.pack(pady=10)

    def crear_cuadricula_matriz(self, parent_frame, filas, columnas):
        """Función auxiliar para crear la cuadrícula de entrada."""
        entradas = []
        for i in range(filas):
            fila_frame = tk.Frame(parent_frame, bg="#F0F0F0")
            fila_frame.pack()
            fila_entradas = []
            for j in range(columnas):
                entrada = tk.Entry(fila_frame, width=5, font=("Helvetica", 12), justify='center', bg="#FFFFFF")
                entrada.pack(padx=2, pady=2, side=tk.LEFT)
                fila_entradas.append(entrada)
            entradas.append(fila_entradas)
        return entradas

    def resolver_operaciones(self, operacion):
        """Lee las matrices y llama a la función de operaciones."""
        try:
            matriz_a = [[float(entrada.get()) for entrada in fila] for fila in self.entradas_matriz_a]
            matriz_b = [[float(entrada.get()) for entrada in fila] for fila in self.entradas_matriz_b]
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingresa solo números en las matrices.")
            return

        if operacion == "suma":
            if len(matriz_a) != len(matriz_b) or len(matriz_a[0]) != len(matriz_b[0]):
                messagebox.showerror("Error de Dimensiones", "Para la suma, las matrices deben tener las mismas dimensiones.")
                return
        elif operacion == "multiplicacion":
            if len(matriz_a[0]) != len(matriz_b):
                messagebox.showerror("Error de Dimensiones", "Para la multiplicación, el número de columnas de la primera matriz debe ser igual al número de filas de la segunda.")
                return

        resultado_op = calcular_operaciones_matrices(matriz_a, matriz_b, operacion)
        self.mostrar_resultado_operaciones(matriz_a, matriz_b, resultado_op, operacion)

    def mostrar_resultado_operaciones(self, matriz1, matriz2, resultado, operacion):
        """Muestra el resultado de la suma o multiplicación de matrices."""
        self.limpiar_pantalla()
        self.root.geometry("800x600")

        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")

        titulo = tk.Label(marco, text=f"Resultado de la {'Suma' if operacion == 'suma' else 'Multiplicación'}", font=("Helvetica", 16, "bold"), fg="#1E88E5", bg="#F0F0F0")
        titulo.pack(pady=10)

        # La función matriz_a_string no requiere el argumento is_system
        texto_matrices = f"Matriz A:\n{matriz_a_string(matriz1)}\n\n"
        texto_matrices += f"Matriz B:\n{matriz_a_string(matriz2)}\n\n"

        if isinstance(resultado, str):
            texto_matrices += resultado
        else:
            texto_matrices += "Resultado:\n" + matriz_a_string(resultado)

        texto_resultado = scrolledtext.ScrolledText(marco, height=20, font=("Courier", 12))
        texto_resultado.insert(tk.END, texto_matrices)
        texto_resultado.config(state=tk.DISABLED)
        texto_resultado.pack(pady=10, fill="both", expand=True)

        btn_volver = tk.Button(marco, text="Volver al Menú Principal", command=self.crear_widgets_menu_principal)
        btn_volver.pack(pady=20)
        
    def preparar_matriz_unica(self, metodo):
        """Prepara la interfaz para ingresar las dimensiones de la matriz única."""
        self.metodo_actual = metodo
        self.limpiar_pantalla()
        self.root.geometry("600x400")
        
        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")
        
        titulo = tk.Label(marco, text="Ingresar Dimensiones de la Matriz", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
        titulo.pack(pady=10)
        
        marco_dimensiones = tk.Frame(marco, bg="#F0F0F0")
        marco_dimensiones.pack(pady=20)
        
        tk.Label(marco_dimensiones, text="Filas (m):", font=("Helvetica", 12), bg="#F0F0F0").pack(side=tk.LEFT, padx=5)
        self.entrada_filas = tk.Entry(marco_dimensiones, width=5, font=("Helvetica", 12))
        self.entrada_filas.pack(side=tk.LEFT, padx=5)
        
        tk.Label(marco_dimensiones, text="Columnas (n):", font=("Helvetica", 12), bg="#F0F0F0").pack(side=tk.LEFT, padx=5)
        self.entrada_columnas = tk.Entry(marco_dimensiones, width=5, font=("Helvetica", 12))
        self.entrada_columnas.pack(side=tk.LEFT, padx=5)
        
        btn_crear = tk.Button(marco, text="Crear Matriz", font=("Helvetica", 12, "bold"), command=self.crear_interfaz_matriz_unica)
        btn_crear.pack(pady=10)
        
        btn_volver = tk.Button(marco, text="Volver", command=lambda: self.crear_widgets_menu_principal(), bg="#FFCDD2")
        btn_volver.pack(pady=10)
        
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

    def crear_interfaz_matriz_unica(self):
        """Crea la cuadrícula para el ingreso de datos de una sola matriz."""
        try:
            filas = int(self.entrada_filas.get())
            columnas = int(self.entrada_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
            self.filas = filas
            self.columnas = columnas
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingresa números enteros positivos para las dimensiones.")
            return

        self.limpiar_pantalla()
        self.root.geometry(f"{max(600, (self.columnas + 1) * 70)}x{max(400, (self.filas + 1) * 40 + 200)}")
        
        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")
        
        titulo = tk.Label(marco, text="Ingresa los valores de la matriz:", font=("Helvetica", 16, "bold"), bg="#F0F0F0")
        titulo.pack(pady=10)
        
        marco_matriz = tk.Frame(marco, bg="#F0F0F0")
        marco_matriz.pack(pady=10)
        
        self.entradas_matriz = []
        for indice_fila in range(self.filas):
            fila_frame = tk.Frame(marco_matriz, bg="#F0F0F0")
            fila_frame.pack()
            fila_entradas = []
            for indice_columna in range(self.columnas + 1):
                color_fondo = "#E0E0E0" if indice_columna == self.columnas else "#FFFFFF"
                entrada = tk.Entry(fila_frame, width=5, font=("Helvetica", 12), justify='center', bg=color_fondo)
                entrada.pack(side=tk.LEFT, padx=2, pady=2)
                fila_entradas.append(entrada)
            self.entradas_matriz.append(fila_entradas)

        btn_resolver = tk.Button(marco, text="Resolver Sistema", font=("Helvetica", 12, "bold"), command=self.resolver_sistema)
        btn_resolver.pack(pady=20)
        
        btn_volver = tk.Button(marco, text="Volver", command=lambda: self.preparar_matriz_unica(self.metodo_actual), bg="#FFCDD2")
        btn_volver.pack(pady=10)

    def resolver_sistema(self):
        """Lee la matriz y llama a la función de resolución adecuada."""
        datos_matriz = []
        try:
            for indice_fila in range(self.filas):
                valores_fila = [float(entrada.get()) for entrada in self.entradas_matriz[indice_fila]]
                datos_matriz.append(valores_fila)
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingresa solo números en la matriz.")
            return

        if self.metodo_actual == "Gauss-Jordan":
            resultados = resolver_gauss_jordan(datos_matriz)
            self.mostrar_resultados_gauss_jordan(resultados, datos_matriz)
        else:
            resultados = resolver_eliminacion_filas(datos_matriz)
            self.mostrar_resultados_eliminacion(resultados)

    def mostrar_resultados_eliminacion(self, resultados):
        """Muestra los resultados del método de eliminación."""
        self.limpiar_pantalla()
        self.root.geometry("800x650")

        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")
        
        titulo = tk.Label(marco, text="Resultados de Eliminación de Filas", font=("Helvetica", 16, "bold"), fg="#1E88E5", bg="#F0F0F0")
        titulo.pack(pady=10)
        
        tk.Label(marco, text="Pasos del proceso:", font=("Helvetica", 12), bg="#F0F0F0").pack(anchor="w", pady=(10,0))
        texto_pasos = scrolledtext.ScrolledText(marco, height=15, font=("Courier", 12))
        texto_pasos.insert(tk.END, "\n".join(resultados["pasos"]))
        texto_pasos.config(state=tk.DISABLED)
        texto_pasos.pack(pady=5, fill="both", expand=True)

        marco_resumen = tk.Frame(marco, bg="#F0F0F0")
        marco_resumen.pack(pady=10)

        lista_informacion = [
            f"Tipo de Solución: {resultados['tipo_solucion']}"
        ]

        if resultados['solucion'] is not None:
            string_solucion = "Solución:\n" + "\n".join(f"x{indice+1} = {valor}" for indice, valor in enumerate(resultados['solucion']))
            lista_informacion.append(string_solucion)
        elif resultados['tipo_solucion'] == 'Infinita':
            lista_informacion.append("El sistema tiene INFINITAS soluciones.")
        
        for informacion in lista_informacion:
            tk.Label(marco_resumen, text=informacion, font=("Helvetica", 14), fg="#333", bg="#F0F0F0", justify="left").pack(anchor="w", pady=(5,0))
        
        btn_volver = tk.Button(marco, text="Volver al Menú Principal", command=self.crear_widgets_menu_principal)
        btn_volver.pack(pady=20)

    def mostrar_resultados_gauss_jordan(self, resultados, matriz_original):
        """Muestra los resultados del método de Gauss-Jordan."""
        self.limpiar_pantalla()
        self.root.geometry("900x750")
        
        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")
        
        titulo = tk.Label(marco, text="Resultados del Método de Gauss-Jordan", font=("Helvetica", 18, "bold"), fg="#1E88E5", bg="#F0F0F0")
        titulo.pack(pady=10)
        
        tk.Label(marco, text="Pasos de la Resolución:", font=("Helvetica", 12), bg="#F0F0F0").pack(anchor="w", pady=(10, 0))
        texto_pasos = scrolledtext.ScrolledText(marco, height=15, font=("Courier", 12))
        for paso in resultados["pasos"]:
            texto_pasos.insert(tk.END, paso + "\n")
        texto_pasos.config(state=tk.DISABLED)
        texto_pasos.pack(pady=5, fill="both", expand=True)

        marco_resumen = tk.Frame(marco, bg="#E0E0E0", padx=15, pady=15, relief=tk.GROOVE, bd=2)
        marco_resumen.pack(pady=10)
        
        tk.Label(marco_resumen, text="Resumen y Solución", font=("Helvetica", 14, "bold"), bg="#E0E0E0").pack(pady=(0, 5))
        
        lista_informacion = [
            f"Matriz Original:\n{matriz_a_string(matriz_original)}\n",
            f"Matriz en forma escalonada reducida (RREF):\n{matriz_a_string(resultados['matriz_rref'])}\n",
            f"Tipo de Solución: {resultados['tipo_solucion']}",
            f"Columnas Pivote: {', '.join(map(str, resultados['columnas_pivote']))}",
            f"Variables Libres: {', '.join(resultados['variables_libres']) if resultados['variables_libres'] else 'No hay.'}"
        ]
        
        if resultados['solucion'] is not None:
            string_solucion = "Solución:\n" + "\n".join(f"x{indice+1} = {valor}" for indice, valor in enumerate(resultados['solucion']))
            lista_informacion.append(string_solucion)
        
        for informacion in lista_informacion:
            tk.Label(marco_resumen, text=informacion, font=("Helvetica", 12), fg="#333", bg="#E0E0E0", justify="left").pack(anchor="w", pady=(5, 0))
            
        btn_volver = tk.Button(marco, text="Volver al Menú Principal", command=self.crear_widgets_menu_principal)
        btn_volver.pack(pady=20)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()
