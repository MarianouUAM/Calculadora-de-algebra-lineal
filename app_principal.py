# app_principal.py

import tkinter as tk
from tkinter import messagebox, scrolledtext, font
from logica_calculadora import resolver_gauss_jordan, resolver_eliminacion_filas, matriz_a_string, formatea_num

class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica ⚛️")
        self.root.geometry("800x650")
        self.root.configure(bg="#F0F0F0")
        
        self.filas = 0
        self.columnas = 0
        self.entradas_matriz = []
        self.metodo_actual = ""
        
        self.crear_widgets_menu_principal()

    def limpiar_pantalla(self):
        """Elimina todos los widgets de la ventana actual."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_widgets_menu_principal(self):
        """Crea la interfaz del menú de bienvenida."""
        self.limpiar_pantalla()
        self.root.geometry("800x600")
        
        marco = tk.Frame(self.root, padx=20, pady=20, bg="#F0F0F0")
        marco.pack(expand=True, fill="both")

        titulo = tk.Label(marco, text="CALCULADORA CIENTÍFICA", font=("Helvetica", 24, "bold"), fg="#1E88E5", bg="#F0F0F0")
        titulo.pack(pady=10)
        
        bienvenida = tk.Label(marco, text="Bienvenido!", font=("Helvetica", 18), fg="#4CAF50", bg="#F0F0F0")
        bienvenida.pack(pady=5)
        
        informacion = tk.Label(marco, text="Selecciona un método para resolver sistemas de ecuaciones lineales:", font=("Helvetica", 12), bg="#F0F0F0")
        informacion.pack(pady=20)

        estilo_btn = {"font": ("Helvetica", 14), "bg": "#E3F2FD", "fg": "#333", "relief": tk.RAISED, "bd": 2}
        
        btn_gauss_jordan = tk.Button(marco, text="Método de Gauss-Jordan (Paso a Paso)", command=lambda: self.preparar_matriz("Gauss-Jordan"), **estilo_btn)
        btn_gauss_jordan.pack(pady=10, ipadx=20, ipady=10)
        
        btn_eliminacion = tk.Button(marco, text="Método de Eliminación de Filas (con Pasos)", command=lambda: self.preparar_matriz("Eliminación"), **estilo_btn)
        btn_eliminacion.pack(pady=10, ipadx=20, ipady=10)
        
        btn_salir = tk.Button(marco, text="Salir", font=("Helvetica", 12), command=self.root.destroy, bg="#FFCDD2", fg="#333", relief=tk.RAISED, bd=2)
        btn_salir.pack(pady=20)

    def preparar_matriz(self, metodo):
        """Prepara la interfaz para ingresar las dimensiones de la matriz."""
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
        
        btn_crear = tk.Button(marco, text="Crear Matriz", font=("Helvetica", 12, "bold"), command=self.crear_interfaz_matriz)
        btn_crear.pack(pady=10)
        
        btn_volver = tk.Button(marco, text="Volver", command=lambda: self.crear_widgets_menu_principal(), bg="#FFCDD2")
        btn_volver.pack(pady=10)
        
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(self.root.attributes, '-topmost', False)

    def crear_interfaz_matriz(self):
        """Crea la cuadrícula para el ingreso de datos de la matriz."""
        try:
            self.filas = int(self.entrada_filas.get())
            self.columnas = int(self.entrada_columnas.get())
            if self.filas <= 0 or self.columnas <= 0:
                raise ValueError
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
            fila_entradas = []
            for indice_columna in range(self.columnas + 1):
                color_fondo = "#E0E0E0" if indice_columna == self.columnas else "#FFFFFF"
                entrada = tk.Entry(marco_matriz, width=5, font=("Helvetica", 12), justify='center', bg=color_fondo)
                entrada.grid(row=indice_fila, column=indice_columna, padx=2, pady=2)
                fila_entradas.append(entrada)
            self.entradas_matriz.append(fila_entradas)

        btn_resolver = tk.Button(marco, text="Resolver Sistema", font=("Helvetica", 12, "bold"), command=self.resolver_sistema)
        btn_resolver.pack(pady=20)
        
        btn_volver = tk.Button(marco, text="Volver", command=lambda: self.preparar_matriz(self.metodo_actual), bg="#FFCDD2")
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
        
        # 1. Pasos de la resolución (historial de operaciones)
        tk.Label(marco, text="Pasos de la Resolución:", font=("Helvetica", 12), bg="#F0F0F0").pack(anchor="w", pady=(10, 0))
        texto_pasos = scrolledtext.ScrolledText(marco, height=15, font=("Courier", 12))
        for paso in resultados["pasos"]:
            texto_pasos.insert(tk.END, paso + "\n")
        texto_pasos.config(state=tk.DISABLED)
        texto_pasos.pack(pady=5, fill="both", expand=True)

        # 2. Resumen final y solución
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