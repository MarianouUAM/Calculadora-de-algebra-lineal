import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from logica_calculadora import (
    resolver_gauss_jordan,
    resolver_eliminacion_filas,
    matriz_a_string,
    calcular_operaciones_matrices,
    verificar_independencia_lineal,
    resolver_sistema_homogeneo,
    calcular_inversa,
    formatea_num
)

# ================================================================
#              CALCULADORA CIENTIFICA — MODO OSCURO
#                    Estilo WebApp Neumorfico
# ================================================================
class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Cientifica — Proyecto Universitario")
        self.root.geometry("1080x720")
        self.root.minsize(980, 620)
        self._colores_estilo()
        

        # Variables globales
        self.metodo_actual = ""
        self.entradas_matriz = []
        self.entradas_matriz_a = []
        self.entradas_matriz_b = []
        self.entradas_matriz_t = []
        self.filas_a = self.columnas_a = self.filas_b = self.columnas_b = 0

        # Construccion visual
        self._construir_shell()
        self.vista_menu()

    # ================================================================
    #                        ESTILOS GENERALES
    # ================================================================
    def _colores_estilo(self):
        self.COLOR_BG = "#1e1e1e"          # Fondo general
        self.COLOR_CARD = "#2b2b2b"        # Tarjetas
        self.COLOR_LIGHT = "#3a3a3a"       # Relieve claro
        self.COLOR_DARK = "#141414"        # Sombra
        self.COLOR_TEXT = "#f2f2f2"        # Texto principal
        self.COLOR_SUB = "#bfbfbf"         # Texto secundario
        self.COLOR_PRIMARY = "#00C8FF"     # Cyan
        self.COLOR_ACCENT = "#FF8C42"      # Naranja
        self.COLOR_DANGER = "#D9534F"      # Rojo tenue

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background=self.COLOR_BG)
        style.configure("Card.TFrame", background=self.COLOR_CARD, relief="flat")

        # Botones
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"),
                        padding=10, background=self.COLOR_PRIMARY, foreground="black", borderwidth=0)
        style.map("Primary.TButton",
                  background=[("active", "#33D1FF")])

        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"),
                        padding=10, background=self.COLOR_ACCENT, foreground="black", borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", "#FF9F5E")])

        style.configure("Danger.TButton", font=("Segoe UI", 11, "bold"),
                        padding=10, background=self.COLOR_DANGER, foreground="white", borderwidth=0)
        style.map("Danger.TButton",
                  background=[("active", "#E46A6A")])

        style.configure("Ghost.TButton", font=("Segoe UI", 11),
                        padding=8, background=self.COLOR_BG, foreground=self.COLOR_TEXT, borderwidth=0)
        style.map("Ghost.TButton",
                  background=[("active", "#2a2a2a")])

        # Etiquetas
        style.configure("H1.TLabel", background=self.COLOR_BG, foreground=self.COLOR_PRIMARY, font=("Segoe UI", 22, "bold"))
        style.configure("H2.TLabel", background=self.COLOR_BG, foreground=self.COLOR_TEXT, font=("Segoe UI", 14, "bold"))
        style.configure("Muted.TLabel", background=self.COLOR_BG, foreground=self.COLOR_SUB, font=("Segoe UI", 11))
        style.configure("CardTitle.TLabel", background=self.COLOR_CARD, foreground=self.COLOR_TEXT, font=("Segoe UI", 14, "bold"))
        style.configure("CardText.TLabel", background=self.COLOR_CARD, foreground=self.COLOR_SUB, font=("Segoe UI", 11))

    # ================================================================
    #                  ESTRUCTURA PRINCIPAL (SHELL)
    # ================================================================
    def _construir_shell(self):
        """Crea la estructura general: barra superior + sidebar + contenido."""
        self.root.configure(bg=self.COLOR_BG)

        # Barra superior
        topbar = tk.Frame(self.root, bg="#242424", height=60)
        topbar.pack(side="top", fill="x")

        tk.Label(topbar, text="Calculadora Cientifica — Proyecto Universitario",
                 bg="#242424", fg=self.COLOR_PRIMARY,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=20, pady=12)

        # Contenedor principal
        main_frame = tk.Frame(self.root, bg=self.COLOR_BG)
        main_frame.pack(fill="both", expand=True)

        # Sidebar lateral
        self.sidebar = tk.Frame(main_frame, bg="#252525", width=240)
        self.sidebar.pack(side="left", fill="y")

        # Contenido central
        self.content = tk.Frame(main_frame, bg=self.COLOR_BG)
        self.content.pack(side="left", fill="both", expand=True)

        # Footer
        footer = tk.Frame(self.root, bg=self.COLOR_BG)
        footer.pack(side="bottom", fill="x", pady=10)
        ttk.Label(footer, text="Facultad de Ingenieria — Proyecto Academico", style="Muted.TLabel").pack()

        self._construir_sidebar()

    # ================================================================
    #                      SIDEBAR DE NAVEGACION
    # ================================================================
    def _construir_sidebar(self):
        """Crea los botones de navegacion lateral con efecto hover."""
        def nav_button(txt, cmd):
            b = tk.Label(self.sidebar, text=txt, bg="#252525", fg=self.COLOR_TEXT,
                         font=("Segoe UI", 11, "bold"), padx=20, pady=10, anchor="w", cursor="hand2")
            b.pack(fill="x")
            b.bind("<Enter>", lambda e: b.config(bg=self.COLOR_PRIMARY, fg="black"))
            b.bind("<Leave>", lambda e: b.config(bg="#252525", fg=self.COLOR_TEXT))
            b.bind("<Button-1>", lambda e: cmd())

        tk.Label(self.sidebar, text="Menu", bg="#252525", fg=self.COLOR_SUB,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=16, pady=(20, 10))

        nav_button("Inicio", self.vista_menu)
        nav_button("Metodo Gauss-Jordan", lambda: self.preparar_matriz_unica("Gauss-Jordan"))
        nav_button("Eliminacion de Filas", lambda: self.preparar_matriz_unica("Eliminacion"))
        nav_button("Sistema Homogeneo", self.preparar_matriz_homogeneo)
        nav_button("Suma y Multiplicacion", self.preparar_matrices_operaciones)
        nav_button("Independencia Lineal", self.preparar_vectores_independencia)
        nav_button("Transpuesta de Matriz", self.preparar_matriz_transpuesta)
        nav_button("Probar Linealidad T(x)=Ax+b)", self.preparar_linealidad)
        nav_button("Construir T(x)=A·x", self.preparar_construir_transformacion)
        nav_button("Inversa de Matriz", self.preparar_inversa_matriz)
        nav_button("Determinantes", self.preparar_determinante)




        # Separador y boton salir
        tk.Frame(self.sidebar, bg="#303030", height=2).pack(fill="x", pady=10)
        salir = tk.Label(self.sidebar, text="Salir", bg="#252525", fg=self.COLOR_DANGER,
                         font=("Segoe UI", 11, "bold"), padx=20, pady=10, anchor="w", cursor="hand2")
        salir.pack(fill="x")
        salir.bind("<Enter>", lambda e: salir.config(bg="#3c3c3c"))
        salir.bind("<Leave>", lambda e: salir.config(bg="#252525"))
        salir.bind("<Button-1>", lambda e: self.root.destroy())

    # ================================================================
    #                        UTILIDADES VISUALES
    # ================================================================
    def clear_content(self):
        """Limpia todo el contenido del area central."""
        for w in self.content.winfo_children():
            w.destroy()

    def card(self, parent=None, pad=20):
        """Crea una tarjeta con sombra tipo neumorfico."""
        parent = parent or self.content
        frame = tk.Frame(parent, bg=self.COLOR_CARD, bd=0, highlightthickness=0)
        frame.pack(padx=20, pady=15, fill="x")
        frame.configure(relief="flat")

        # Sombras sutiles
        frame.config(highlightbackground="#2f2f2f")
        frame.config(highlightcolor="#111111")
        return frame

    def grid_inputs(self, parent, filas, columnas, width=8):
        """Crea una cuadricula de entradas con estilo oscuro."""
        entradas = []
        g = tk.Frame(parent, bg=self.COLOR_CARD)
        g.pack()
        for i in range(filas):
            row = []
            for j in range(columnas):
                e = tk.Entry(g, width=width, justify="center", bd=0,
                             font=("Segoe UI", 12),
                             bg="#3a3a3a", fg=self.COLOR_TEXT,
                             insertbackground=self.COLOR_PRIMARY)
                e.grid(row=i, column=j, padx=4, pady=4, ipadx=4, ipady=6)
                row.append(e)
            entradas.append(row)
        return entradas

    # ================================================================
    #                         MENU PRINCIPAL
    # ================================================================
    def vista_menu(self):
        """Pantalla inicial con estilo neumorfico."""
        self.clear_content()
        ttk.Label(self.content, text="Panel Principal", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 4))
        ttk.Label(self.content, text="Selecciona una opcion en la barra lateral o desde las tarjetas inferiores.",
                  style="Muted.TLabel").pack(anchor="w", padx=22, pady=(0, 6))

        # Contenedor de tarjetas
        grid = tk.Frame(self.content, bg=self.COLOR_BG)
        grid.pack(fill="x", padx=12, pady=6)

        cards = [
            ("Metodo Gauss-Jordan", "Resuelve sistemas y muestra pasos detallados.",
             lambda: self.preparar_matriz_unica("Gauss-Jordan")),
            ("Eliminacion de Filas", "Aplica transformaciones elementales a matrices.",
             lambda: self.preparar_matriz_unica("Eliminacion")),
            ("Suma y Multiplicacion", "Opera entre dos matrices con validacion dimensional.",
             self.preparar_matrices_operaciones),
            ("Independencia Lineal", "Analiza vectores y determina su independencia.",
             self.preparar_vectores_independencia),
            ("Transpuesta de Matriz", "Calcula la transpuesta y muestra el proceso.",
             self.preparar_matriz_transpuesta),
        ]

        for titulo, desc, comando in cards:
            c = self.card(grid)
            ttk.Label(c, text=titulo, style="CardTitle.TLabel").pack(anchor="w", pady=(5, 2), padx=15)
            ttk.Label(c, text=desc, style="CardText.TLabel").pack(anchor="w", padx=15)
            ttk.Button(c, text="Abrir", style="Primary.TButton", command=comando).pack(anchor="e", padx=15, pady=10)

    # ================================================================
    #                       METODOS DE MATRICES
    # ================================================================
    def preparar_matriz_unica(self, metodo):
        """Pantalla inicial para ingresar dimensiones del sistema."""
        self.metodo_actual = metodo
        self.clear_content()

        ttk.Label(self.content, text=f"{metodo}", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(
            c,
            text="Dimensiones de la matriz aumentada (m x n)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))

        # --- NUEVO diseno centrado y grande ---
        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(
            f, text="Filas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
            font=("Segoe UI", 13)
        ).grid(row=0, column=0, padx=10)

        self.entrada_filas = tk.Entry(
            f, width=10, font=("Segoe UI", 13),
            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY, relief="flat"
        )

        self.entrada_filas.grid(row=0, column=1, padx=10)

        tk.Label(
            f, text="Columnas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
            font=("Segoe UI", 13)
        ).grid(row=0, column=2, padx=10)

        self.entrada_columnas = tk.Entry(
            f, width=10, font=("Segoe UI", 13),
            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY, relief="flat"
        )

        self.entrada_columnas.grid(row=0, column=3, padx=10)

        ttk.Button(
            c, text="Crear Matriz", style="Primary.TButton",
            command=self.crear_interfaz_matriz_unica
        ).pack(anchor="center", pady=(20, 10))

    def preparar_matriz_homogeneo(self):
        """Pantalla inicial para sistemas homogeneos (solo coeficientes)."""
        self.metodo_actual = "Sistema Homogeneo"
        self.clear_content()

        ttk.Label(self.content, text="Sistema Homogeneo (Ax = 0)", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(
            c,
            text="Dimensiones de la matriz de coeficientes (m x n)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))

        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(f, text="Filas (ecuaciones):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=0, padx=10)
        self.entrada_filas = tk.Entry(f, width=10, font=("Segoe UI", 13),
                                     justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
                                     insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_filas.grid(row=0, column=1, padx=10)

        tk.Label(f, text="Columnas (variables):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=2, padx=10)
        self.entrada_columnas = tk.Entry(f, width=10, font=("Segoe UI", 13),
                                        justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
                                        insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_columnas.grid(row=0, column=3, padx=10)

        ttk.Button(
            c, text="Crear Matriz", style="Primary.TButton",
            command=self.crear_interfaz_matriz_homogeneo
        ).pack(anchor="center", pady=(20, 10))


    def crear_interfaz_matriz_unica(self):
        """Crea la cuadricula para ingresar un sistema de ecuaciones."""
        try:
            filas = int(self.entrada_filas.get())
            columnas = int(self.entrada_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores validos para filas y columnas.")
            return

        self.clear_content()
        ttk.Label(self.content, text="Ingrese los valores de la matriz aumentada", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        self.entradas_matriz = self.grid_inputs(c, filas, columnas)

        a = self.card()
        ttk.Button(a, text="Resolver Sistema", style="Primary.TButton", command=self.resolver_sistema).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=lambda: self.preparar_matriz_unica(self.metodo_actual)).pack(side="left")

    def crear_interfaz_matriz_homogeneo(self):
        """Crea la cuadricula para ingresar solo los coeficientes del sistema homogeneo."""
        try:
            filas = int(self.entrada_filas.get())
            columnas = int(self.entrada_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores validos para filas y columnas.")
            return

        self.clear_content()
        ttk.Label(self.content, text="Ingrese los coeficientes de la matriz (Ax = 0)", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        # Solo coeficientes (sin columna de resultados)
        self.entradas_matriz = self.grid_inputs(c, filas, columnas)

        a = self.card()
        ttk.Button(a, text="Resolver Sistema Homogeneo", style="Primary.TButton", command=self.resolver_sistema_homogeneo_visual).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=self.preparar_matriz_homogeneo).pack(side="left")

    def resolver_sistema(self):
        """Llama al metodo correspondiente (Gauss-Jordan o Eliminacion)."""
        try:
            datos = [[float(e.get()) for e in fila] for fila in self.entradas_matriz]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten numeros.")
            return

        if self.metodo_actual == "Gauss-Jordan":
            resultados = resolver_gauss_jordan(datos)
            self.mostrar_resultados_gauss_jordan(resultados, datos)
        else:
            resultados = resolver_eliminacion_filas(datos)
            self.mostrar_resultados_eliminacion(resultados)

    def resolver_sistema_homogeneo_visual(self):
        """Lee la matriz de coeficientes, agrega columna de ceros y resuelve el sistema homogeneo."""
        try:
            # Leer solo coeficientes
            matriz_coef = [[float(e.get()) for e in fila] for fila in self.entradas_matriz]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten numeros.")
            return

        # Agregar columna de ceros (Ax = 0)
        matriz_aumentada = [fila + [0.0] for fila in matriz_coef]

        # Llamar a la logica
        from logica_calculadora import resolver_sistema_homogeneo
        resultados = resolver_sistema_homogeneo(matriz_aumentada)

        # Mostrar resultados
        self.mostrar_resultados_homogeneo(resultados, matriz_coef)

            

    # ------------------- Eliminacion de Filas -------------------
    def mostrar_resultados_eliminacion(self, resultados):
        self.clear_content()
        ttk.Label(self.content, text="Resultados — Eliminacion de Filas", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # Cuadro de pasos
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#333333", fg=self.COLOR_TEXT, bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        box.insert(tk.END, "\n".join(resultados["pasos"]))
        box.config(state="disabled")

        # Cuadro de resumen
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Resumen y Solucion", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        info = f"Tipo de Solucion: {resultados['tipo_solucion']}\n\n"
        if resultados['solucion'] is not None:
            info += "Solucion:\n" + "\n".join(f"x{i+1} = {v}" for i, v in enumerate(resultados['solucion']))
        elif resultados['tipo_solucion'] == "Infinita":
            info += "El sistema tiene infinitas soluciones."
        else:
            info += "El sistema no tiene solucion."
        tk.Label(resumen_card, text=info, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # Boton volver sin fondo de card
        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Gauss-Jordan -------------------
    def mostrar_resultados_gauss_jordan(self, resultados, matriz_original):
        self.clear_content()
        ttk.Label(self.content, text="Resultados — Gauss-Jordan", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # Cuadro de pasos
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos de la resolucion", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#333333", fg=self.COLOR_TEXT, bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for p in resultados["pasos"]:
            box.insert(tk.END, p + "\n")
        box.config(state="disabled")

        # Cuadro resumen
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Resumen y Solucion", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        info = (
            f"Matriz Original:\n{matriz_a_string(matriz_original)}\n\n"
            f"RREF:\n{matriz_a_string(resultados['matriz_rref'])}\n\n"
            f"Tipo de Solucion: {resultados['tipo_solucion']}\n"
            f"Columnas Pivote: {', '.join(map(str, resultados['columnas_pivote']))}\n"
            f"Variables Libres: {', '.join(resultados['variables_libres']) if resultados['variables_libres'] else 'No hay.'}\n"
        )
        if resultados['solucion'] is not None:
            info += "\nSolucion:\n" + "\n".join(f"x{i+1} = {v}" for i, v in enumerate(resultados['solucion']))
        tk.Label(resumen_card, text=info, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    def mostrar_resultados_homogeneo(self, resultados, matriz_original):
        """Muestra los pasos y la solucion general de un sistema homogeneo."""
        self.clear_content()
        ttk.Label(self.content, text="Resultados — Sistema Homogeneo (Ax = 0)", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # ----- Cuadro de pasos -----
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso (Gauss-Jordan)", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#333333", fg=self.COLOR_TEXT, bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for p in resultados["pasos"]:
            box.insert(tk.END, p + "\n")
        box.config(state="disabled")

        # ----- Cuadro de resumen -----
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Resumen y Solucion", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        texto_resumen = ""
        texto_resumen += f"Matriz Original (solo coeficientes):\n{matriz_a_string(matriz_original)}\n\n"

        if "matriz_rref" in resultados:
            texto_resumen += f"Matriz RREF (con columna de ceros):\n{matriz_a_string(resultados['matriz_rref'], is_system=True)}\n\n"

        texto_resumen += f"Tipo de solucion: {resultados['tipo_solucion']}\n"

        if resultados["tipo_solucion"] == "Unica (trivial)":
            texto_resumen += "\nUnica solucion: x = 0 (solucion trivial)"
        else:
            texto_resumen += "\nVariables libres: "
            texto_resumen += ", ".join(resultados["variables_libres"]) if resultados["variables_libres"] else "Ninguna"
            texto_resumen += "\nVariables pivote: "
            texto_resumen += ", ".join(f"x{p}" for p in resultados["pivotes"])
            texto_resumen += "\n\nSolucion general:\n"

            # Construir la solucion parametrica legible
            for i in range(len(resultados["solucion_parametrica"])):
                vec = resultados["solucion_parametrica"][i]
                t = resultados["parametros"][i]
                texto_resumen += f"Para {t}:\n"
                for idx, coef in enumerate(vec):
                    if coef == 0:
                        texto_resumen += f"  x{idx+1} = 0\n"
                    else:
                        texto_resumen += f"  x{idx+1} = {formatea_num(coef)} * {t}\n"
                texto_resumen += "\n"

        tk.Label(resumen_card, text=texto_resumen, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Transpuesta -------------------
    def preparar_matriz_transpuesta(self):
        self.clear_content()
        ttk.Label(self.content, text="Transpuesta de una Matriz", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(c, text="Dimensiones de la matriz (m x n)", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(f, text="Filas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=0, padx=10)
        self.entrada_filas_t = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_filas_t.grid(row=0, column=1, padx=10)

        tk.Label(f, text="Columnas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=2, padx=10)
        self.entrada_columnas_t = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_columnas_t.grid(row=0, column=3, padx=10)

        ttk.Button(c, text="Crear Matriz", style="Primary.TButton", command=self.crear_interfaz_matriz_transpuesta).pack(anchor="center", pady=(20, 10))

    def preparar_linealidad(self):
        """Pantalla inicial para probar si T(x)=Ax+b es lineal."""
        self.clear_content()
        self.metodo_actual = "Linealidad"

        ttk.Label(
            self.content,
            text="Probar Linealidad de T(x) = A·x + b",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(
            c,
            text="Dimensiones de la matriz A (m × n)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))

        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        # FILAS (m)
        tk.Label(
            f, text="Filas (m):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
            font=("Segoe UI", 13)
        ).grid(row=0, column=0, padx=10)
        self.entrada_filas_lineal = tk.Entry(
            f, width=10, font=("Segoe UI", 13),
            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY, relief="flat"
        )
        self.entrada_filas_lineal.grid(row=0, column=1, padx=10)

        # COLUMNAS (n)
        tk.Label(
            f, text="Columnas (n):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
            font=("Segoe UI", 13)
        ).grid(row=0, column=2, padx=10)
        self.entrada_columnas_lineal = tk.Entry(
            f, width=10, font=("Segoe UI", 13),
            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY, relief="flat"
        )
        self.entrada_columnas_lineal.grid(row=0, column=3, padx=10)

        ttk.Button(
            c, text="Crear Matrices A y b",
            style="Primary.TButton",
            command=self.crear_interfaz_linealidad
        ).pack(anchor="center", pady=(20, 10))

    def preparar_construir_transformacion(self):
        """Pantalla inicial para construir la matriz A de T(x)=Ax."""
        self.clear_content()
    
        ttk.Label(self.content, text="Construir T(x) = A·x", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
    
        c = self.card()
        ttk.Label(
            c,
            text="Ingrese la cantidad de variables (n) y ecuaciones (m)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))
    
        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=10)
    
        # Variables
        tk.Label(f, text="Numero de variables (n):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
                 font=("Segoe UI", 13)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entrada_n_vars = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center",
                                       bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY,
                                       relief="flat")
        self.entrada_n_vars.grid(row=0, column=1, padx=10, pady=5)
    
        # Ecuaciones
        tk.Label(f, text="Numero de ecuaciones (m):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
                 font=("Segoe UI", 13)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entrada_m_ecuaciones = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center",
                                             bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY,
                                             relief="flat")
        self.entrada_m_ecuaciones.grid(row=1, column=1, padx=10, pady=5)
    
        a = self.card()
        ttk.Button(a, text="Continuar", style="Primary.TButton",
                   command=self.crear_interfaz_transformacion).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton",
                   command=self.vista_menu).pack(side="left", padx=8)
        
        
    def preparar_inversa_matriz(self):
        """Pantalla inicial para ingresar dimensión de la matriz (n x n)."""
        self.metodo_actual = "Inversa"
        self.clear_content()

        ttk.Label(self.content, text="Inversa de una Matriz", style="H1.TLabel").pack(
            anchor="w", padx=22, pady=(18, 8)
        )

        c = self.card()
        ttk.Label(c, text="Dimensión de la matriz (n × n)", style="CardTitle.TLabel").pack(
            anchor="center", pady=(10, 15)
        )

        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(
            f, text="n:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
            font=("Segoe UI", 13)
        ).grid(row=0, column=0, padx=10)

        self.entrada_n_inversa = tk.Entry(
            f, width=10, font=("Segoe UI", 13),
            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY, relief="flat"
        )
        self.entrada_n_inversa.grid(row=0, column=1, padx=10)

        ttk.Button(
            c, text="Crear Matriz", style="Primary.TButton",
            command=self.crear_interfaz_inversa
        ).pack(anchor="center", pady=(20, 10))
        
    def preparar_determinante(self):
        """Pantalla inicial para ingresar dimensión de la matriz (n x n)."""
        self.metodo_actual = "Determinante"
        self.clear_content()

        ttk.Label(self.content, text="Determinante de una Matriz", style="H1.TLabel").pack(
            anchor="w", padx=22, pady=(18, 8)
        )

        c = self.card()
        ttk.Label(
            c,
            text="Dimensión de la matriz (n × n)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))

        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(
            f, text="n:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
            font=("Segoe UI", 13)
        ).grid(row=0, column=0, padx=10)

        self.entrada_n_det = tk.Entry(
            f, width=10, font=("Segoe UI", 13),
            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY, relief="flat"
        )
        self.entrada_n_det.grid(row=0, column=1, padx=10)

        ttk.Button(
            c, text="Crear Matriz", style="Primary.TButton",
            command=self.crear_interfaz_determinante
        ).pack(anchor="center", pady=(20, 10))
        
    def crear_interfaz_determinante(self):
   
        try:
            n = int(self.entrada_n_det.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para n.")
            return

        # ✅ Limpiar pantalla
        self.clear_content()

        # ✅ MUY IMPORTANTE:
        # Si ya se había calculado antes y existe una matriz guardada,
        # la eliminamos para NO usar la anterior.
        if hasattr(self, "matriz_det"):
            del self.matriz_det

        ttk.Label(
            self.content,
            text=f"Ingrese los valores de la matriz A ( {n} × {n} )",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()

        # Guardamos n por si lo necesitamos después
        self.n_det = n

        # ✅ Crear la cuadrícula de entradas (n × n)
        self.entradas_matriz_det = self.grid_inputs(c, n, n)

        # ✅ Botones inferiores
        a = self.card()
        ttk.Button(
            a, text="Continuar", style="Primary.TButton",
            command=self.elegir_metodo_determinante
        ).pack(side="left", padx=8)

        ttk.Button(
            a, text="Volver", style="Danger.TButton",
            command=self.preparar_determinante
        ).pack(side="left", padx=8)

        
    def elegir_metodo_determinante(self):
   
        # Si la matriz aún NO ha sido guardada (primera vez):
        if not hasattr(self, "matriz_det"):
            try:
                matriz = [
                    [float(e.get()) for e in fila]
                    for fila in self.entradas_matriz_det
                ]
            except ValueError:
                messagebox.showerror("Error", "Solo se permiten números en la matriz.")
                return
            
            # Guardamos la matriz para reutilizarla después
            self.matriz_det = matriz

        else:
            # Ya fue guardada previamente (al volver desde resultados)
            matriz = self.matriz_det

        n = len(matriz)

        self.clear_content()
        ttk.Label(
            self.content,
            text=f"Seleccione el método para calcular det(A) de {n}×{n}",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        from functools import partial  # Para pasar parámetros al comando

        # === Mostrar métodos disponibles según n ===

        if n == 2:
            ttk.Button(
                c, text="Fórmula 2x2 (ad - bc)", style="Primary.TButton",
                command=partial(self.resolver_determinante_visual, "2x2")
            ).pack(fill="x", padx=10, pady=5)

        if n == 3:
            ttk.Button(
                c, text="Regla de Sarrus (solo 3x3)", style="Primary.TButton",
                command=partial(self.resolver_determinante_visual, "sarrus")
            ).pack(fill="x", padx=10, pady=5)

        # Cofactor (siempre disponible)
        ttk.Button(
            c, text="Desarrollo por Cofactores (general n×n)", style="Primary.TButton",
            command=partial(self.resolver_determinante_visual, "cofactor")
        ).pack(fill="x", padx=10, pady=5)

        # Propiedades / Triangular (siempre)
        ttk.Button(
            c, text="Propiedades / Reducción a triangular", style="Primary.TButton",
            command=partial(self.resolver_determinante_visual, "propiedades")
        ).pack(fill="x", padx=10, pady=5)

        # Botón volver
        ttk.Button(
            c, text="Volver", style="Danger.TButton",
            command=self.crear_interfaz_determinante
        ).pack(fill="x", padx=10, pady=(20, 10))


    def resolver_determinante_visual(self, metodo):
        """
        Llama a la lógica para calcular el determinante
        según el método elegido y luego muestra los resultados.
        """
        from logica_calculadora import calcular_determinante  # Importar la función lógica

        # Usamos la matriz que guardamos previamente
        matriz = self.matriz_det

        # Llamar a la lógica
        resultados = calcular_determinante(matriz, metodo)

        # Mostrar los resultados (pasos + valor)
        self.mostrar_resultados_determinante(resultados, matriz)

        
           
        
    def mostrar_resultados_determinante(self, resultados, matriz_original):
        self.clear_content()

        # Título general
        ttk.Label(
            self.content,
            text=f"Resultado — {resultados['metodo']}",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        # Mostrar la matriz original
        mat_card = self.card()
        ttk.Label(mat_card, text="Matriz Original:", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        tk.Label(
            mat_card,
            text=matriz_a_string(matriz_original),
            bg="#333333", fg=self.COLOR_TEXT,
            font=("Consolas", 12),
            justify="left", anchor="w"
        ).pack(fill="x", padx=10, pady=5)

        # Cuadro de pasos
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del cálculo", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        box = scrolledtext.ScrolledText(
            pasos_card, height=18, font=("Consolas", 12),
            bg="#333333", fg=self.COLOR_TEXT, bd=0, relief="flat"
        )
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for p in resultados["pasos"]:
            box.insert(tk.END, p + "\n")
        box.config(state="disabled")

        # Resultado final
        res_card = self.card()
        ttk.Label(res_card, text="Valor del Determinante:", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        tk.Label(
            res_card,
            text=str(resultados["resultado"]),
            bg="#333333", fg=self.COLOR_TEXT,
            font=("Consolas", 14, "bold"),
            justify="left", anchor="w"
        ).pack(fill="x", padx=10, pady=8)

        # Botones inferiores
        btns = self.card()
        ttk.Button(
            btns, text="Otro método con la misma matriz", style="Primary.TButton",
            command=self.elegir_metodo_determinante
        ).pack(side="left", padx=8)

        ttk.Button(
            btns, text="Volver al Menú Principal", style="Danger.TButton",
            command=self.vista_menu
        ).pack(side="left", padx=8)



    
    def crear_interfaz_inversa(self):
        try:
            n = int(self.entrada_n_inversa.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor valido para n.")
            return
        
        self.clear_content()
        ttk.Label(
            self.content,
            text="Ingrese los valores de la matriz A (n × n)",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        self.entradas_matriz_inversa = self.grid_inputs(c, n, n)

        a = self.card()
        ttk.Button(
            a, text="Calcular Inversa", style="Primary.TButton",
            command=self.resolver_inversa_visual
        ).pack(side="left", padx=8)

        ttk.Button(
            a, text="Volver", style="Danger.TButton",
            command=self.preparar_inversa_matriz
        ).pack(side="left")
   


    def crear_interfaz_transformacion(self):
        """Crea la interfaz para ingresar las expresiones de T(x)."""
        try:
            n = int(self.entrada_n_vars.get())   # Numero de variables
            m = int(self.entrada_m_ecuaciones.get())  # Numero de ecuaciones
            if n <= 0 or m <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores validos para n y m.")
            return
    
        self.num_variables = n
        self.num_ecuaciones = m
    
        self.clear_content()
        ttk.Label(
            self.content,
            text="Ingrese cada componente de T(x) (una por fila):",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))
    
        c = self.card()
        # Lista para guardar las entradas de expresiones
        self.entradas_expresiones = []
    
        for i in range(m):
            frame = tk.Frame(c, bg=self.COLOR_CARD)
            frame.pack(fill="x", pady=5, padx=10)
    
            etiqueta = tk.Label(
                frame,
                text=f"Ecuacion {i+1}:",
                bg=self.COLOR_CARD,
                fg=self.COLOR_TEXT,
                font=("Segoe UI", 12)
            )
            etiqueta.pack(side="left", padx=10)
    
            entrada = tk.Entry(
                frame,
                width=50,
                font=("Segoe UI", 12),
                bg="#3a3a3a",
                fg=self.COLOR_TEXT,
                insertbackground=self.COLOR_PRIMARY,
                justify="left",
                relief="flat"
            )
            entrada.pack(side="left", padx=10, ipady=6, fill="x", expand=True)
    
            self.entradas_expresiones.append(entrada)
    
        # Botones inferiores
        a = self.card()
        ttk.Button(
            a,
            text="Construir Matriz",
            style="Primary.TButton",
            command=self.resolver_transformacion  # ESTE METODO VA EN EL BLOQUE 3
        ).pack(side="left", padx=8)
    
        ttk.Button(
            a,
            text="Volver",
            style="Danger.TButton",
            command=self.preparar_construir_transformacion
        ).pack(side="left", padx=8)

    def resolver_transformacion(self):
        """Lee las expresiones, llama a la logica y muestra el resultado."""
        # Leer expresiones
        expresiones = []
        for entrada in self.entradas_expresiones:
            texto = entrada.get().strip()
            if not texto:
                messagebox.showerror("Error", "Todas las ecuaciones deben tener contenido.")
                return
            expresiones.append(texto)
    
        # Llamar a la logica (la implementaremos en logica_calculadora.py)
        try:
            from logica_calculadora import construir_matriz_transformacion
            pasos, matriz_A = construir_matriz_transformacion(expresiones, self.num_variables)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrio un problema: {str(e)}")
            return
    
        # Mostrar resultado
        self.mostrar_resultado_transformacion(pasos, matriz_A)
        
        
    def resolver_inversa_visual(self):
        try:
            matriz = [[float(e.get()) for e in fila] for fila in self.entradas_matriz_inversa]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten numeros en la matriz.")
            return
        resultado = calcular_inversa(matriz)

        self.mostrar_resultado_inversa(resultado, matriz)
        
        
    def mostrar_resultado_inversa(self, resultado, matriz_original):
        """Muestra los pasos y el resultado de la inversa o la explicación si no es invertible."""
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Inversa de Matriz", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#333333", fg=self.COLOR_TEXT, bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for p in resultado.get("pasos", []):
            box.insert("end", p + "\n")
        box.config(state="disabled")

        resumen_card = self.card()
        ttk.Label(resumen_card, text="Conclusión", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        if not resultado["es_invertible"]:
            mensaje = "La matriz NO es invertible.\n\nMotivo:\n" + resultado.get("motivo", "No tiene n pivotes.")
            tk.Label(resumen_card, text=mensaje, bg="#333333", fg=self.COLOR_TEXT,
                    font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)
        else:
            inversa = resultado.get("inversa", [])
            texto = f"Matriz Original:\n{matriz_a_string(matriz_original)}\n\nInversa A⁻¹:\n{matriz_a_string(inversa)}"
            tk.Label(resumen_card, text=texto, bg="#333333", fg=self.COLOR_TEXT,
                    font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)


    def mostrar_resultado_transformacion(self, pasos, matriz_A):
        """Muestra los pasos y la matriz final A."""
        from logica_calculadora import matriz_a_string
    
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Matriz de Transformacion T(x)=A·x",
                  style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
    
        # ----- Card de pasos -----
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
    
        box = scrolledtext.ScrolledText(
            pasos_card,
            height=18,
            font=("Consolas", 12),
            bg="#333333",
            fg=self.COLOR_TEXT,
            bd=0,
            relief="flat"
        )
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
        for p in pasos:
            box.insert("end", p + "\n")
        box.config(state="disabled")
    
        # ----- Card de matriz final -----
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz A resultante", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
    
        texto_matriz = matriz_a_string(matriz_A)
        tk.Label(matriz_card, text=texto_matriz, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)
    
        # ----- Boton volver -----
        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)    

    def crear_interfaz_linealidad(self):
        """Crea la interfaz para ingresar A y b."""
        try:
            m = int(self.entrada_filas_lineal.get())
            n = int(self.entrada_columnas_lineal.get())
            if m <= 0 or n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para m y n.")
            return

        self.clear_content()
        ttk.Label(
            self.content,
            text="Ingrese los valores de A y b",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        # ---- Card principal ----
        c = self.card()

        # Contenedor de A y b
        cont = tk.Frame(c, bg=self.COLOR_CARD)
        cont.pack(pady=10)

        # ===== MATRIZ A =====
        frameA = tk.Frame(cont, bg=self.COLOR_CARD)
        frameA.pack(side="left", padx=20)
        ttk.Label(frameA, text="Matriz A", style="CardTitle.TLabel").pack(anchor="w")
        self.entradas_matriz_a = self.grid_inputs(frameA, m, n)

        # ===== VECTOR b (columna m×1) =====
        frameB = tk.Frame(cont, bg=self.COLOR_CARD)
        frameB.pack(side="left", padx=20)
        ttk.Label(frameB, text="Vector b (m×1)", style="CardTitle.TLabel").pack(anchor="w")

        self.entradas_vector_b = []
        for i in range(m):
            e = tk.Entry(
                frameB, width=8, justify="center", bd=0,
                font=("Segoe UI", 12),
                bg="#3a3a3a", fg=self.COLOR_TEXT,
                insertbackground=self.COLOR_PRIMARY
            )
            e.pack(padx=4, pady=4, ipady=6)  
            self.entradas_vector_b.append(e)
       

        # ---- Botones inferior ----
        a = self.card()
        ttk.Button(
            a, text="Probar Linealidad",
            style="Primary.TButton",
            command=self.resolver_linealidad
        ).pack(side="left", padx=8)

        ttk.Button(
            a, text="Volver",
            style="Danger.TButton",
            command=self.preparar_linealidad
        ).pack(side="left", padx=8)

    def resolver_linealidad(self):
        """Calcula T(0) = A·0 + b y determina si es lineal."""
        try:
            A = [[float(e.get()) for e in fila] for fila in self.entradas_matriz_a]
            b = [float(e.get()) for e in self.entradas_vector_b]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten números en A y b.")
            return

        m = len(A)      # Filas
        n = len(A[0])   # Columnas

        # Vector cero de tamaño n (x en R^n)
        x0 = [0.0] * n

        # Calcular A·x0 (que debe dar vector cero de tamaño m)
        Ax0 = [sum(A[i][j] * x0[j] for j in range(n)) for i in range(m)]

        # T(0) = A·0 + b = b
        T0 = [Ax0[i] + b[i] for i in range(m)]

        # PASO A PASO
        pasos = []
        pasos.append("Definimos T(x) = A·x + b")
        pasos.append(f"\nVector 0 en R^{n}: {x0}")
        pasos.append(f"\n1) Calculamos A·0:")
        pasos.append(f"A·0 = {Ax0}")
        pasos.append(f"\n2) Ahora T(0) = A·0 + b:")
        pasos.append(f"T(0) = {Ax0} + {b} = {T0}")

        # Verificar si T(0) = 0
        es_lineal = all(abs(val) < 1e-9 for val in T0)

        if es_lineal:
            pasos.append("\nComo T(0) = 0, T ES transformación lineal ✅")
        else:
            pasos.append("\nComo T(0) ≠ 0, T NO es transformación lineal ❌")

        # Mostrar resultado final
        self.mostrar_resultado_linealidad(pasos, es_lineal)

    def mostrar_resultado_linealidad(self, pasos, es_lineal):
        """Muestra el paso a paso y la conclusión de la linealidad."""
        self.clear_content()
        ttk.Label(
            self.content,
            text="Resultado — Linealidad de T(x) = A·x + b",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        # ----- Card de pasos -----
        pasos_card = self.card()
        ttk.Label(
            pasos_card,
            text="Pasos del proceso",
            style="CardTitle.TLabel"
        ).pack(anchor="w", padx=15, pady=(5, 3))

        box = scrolledtext.ScrolledText(
            pasos_card, height=18,
            font=("Consolas", 12),
            bg="#333333", fg=self.COLOR_TEXT,
            bd=0, relief="flat"
        )
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for p in pasos:
            box.insert("end", p + "\n")
        box.config(state="disabled")

        # ----- Card de conclusión -----
        resumen_card = self.card()
        ttk.Label(
            resumen_card,
            text="Conclusión",
            style="CardTitle.TLabel"
        ).pack(anchor="w", padx=15, pady=(5, 3))

        conclusion = "T ES transformación lineal (b = 0)" if es_lineal else "T NO es transformación lineal (b ≠ 0)"
        tk.Label(
            resumen_card,
            text=conclusion,
            bg="#333333", fg=self.COLOR_TEXT,
            font=("Consolas", 13, "bold"),
            justify="left", anchor="w"
        ).pack(fill="x", padx=10, pady=5)

        # Botón para volver
        ttk.Button(
            self.content,
            text="Volver al Menú Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    def crear_interfaz_matriz_transpuesta(self):
        try:
            filas = int(self.entrada_filas_t.get())
            cols = int(self.entrada_columnas_t.get())
            if filas <= 0 or cols <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese numeros enteros positivos.")
            return
        self.clear_content()
        ttk.Label(self.content, text="Valores de la Matriz", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        c = self.card()
        self.entradas_matriz_t = self.grid_inputs(c, filas, cols)
        a = self.card()
        ttk.Button(a, text="Calcular Transpuesta", style="Accent.TButton", command=self.resolver_transpuesta).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=self.preparar_matriz_transpuesta).pack(side="left")

    def resolver_transpuesta(self):
        try:
            matriz = [[float(e.get()) for e in fila] for fila in self.entradas_matriz_t]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten numeros.")
            return
        resultado = calcular_operaciones_matrices(matriz, None, "transpuesta")
        self.mostrar_resultado_transpuesta(matriz, resultado)

    def mostrar_resultado_transpuesta(self, matriz, resultado):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Transpuesta", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        if isinstance(resultado, str):
            c = self.card()
            ttk.Label(c, text=resultado, style="CardTitle.TLabel").pack(anchor="w", padx=15)
            ttk.Button(c, text="Volver al Menu Principal", style="Primary.TButton", command=self.vista_menu).pack(anchor="e", pady=8)
            return
        pasos = resultado.get("pasos", [])
        transpuesta = resultado.get("resultado", [])

        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=14, font=("Consolas", 12), bg="#333333", fg=self.COLOR_TEXT, bd=0)
        box.pack(fill="both", expand=True, padx=10, pady=6)
        box.insert(tk.END, "\n".join(pasos))
        box.config(state="disabled")

        resumen_card = self.card()
        ttk.Label(resumen_card, text="Resumen", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        text = f"Matriz Original:\n{matriz_a_string(matriz)}\n\nTranspuesta:\n{matriz_a_string(transpuesta)}"
        tk.Label(resumen_card, text=text, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Operaciones entre matrices -------------------
    def preparar_matrices_operaciones(self):
        self.clear_content()
        ttk.Label(self.content, text="Operaciones entre Matrices", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(c, text="Dimensiones de A y B", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=20)

        tk.Label(f, text="A — Filas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=0, padx=10, pady=5)
        self.entrada_filas_a = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY)
        self.entrada_filas_a.grid(row=0, column=1, padx=10)
        tk.Label(f, text="Columnas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=2, padx=10)
        self.entrada_columnas_a = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY)
        self.entrada_columnas_a.grid(row=0, column=3, padx=10)

        tk.Label(f, text="B — Filas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=1, column=0, padx=10, pady=5)
        self.entrada_filas_b = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY)
        self.entrada_filas_b.grid(row=1, column=1, padx=10)
        tk.Label(f, text="Columnas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=1, column=2, padx=10)
        self.entrada_columnas_b = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY)
        self.entrada_columnas_b.grid(row=1, column=3, padx=10)

        ttk.Button(c, text="Crear Matrices", style="Primary.TButton", command=self.crear_interfaz_operaciones_matrices).pack(anchor="center", pady=(20, 10))


    def crear_interfaz_operaciones_matrices(self):
        try:
            self.filas_a = int(self.entrada_filas_a.get())
            self.columnas_a = int(self.entrada_columnas_a.get())
            self.filas_b = int(self.entrada_filas_b.get())
            self.columnas_b = int(self.entrada_columnas_b.get())
            if min(self.filas_a, self.columnas_a, self.filas_b, self.columnas_b) <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores validos para dimensiones.")
            return

        self.clear_content()
        ttk.Label(self.content, text="Valores de A y B", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        c = self.card()
        cols = tk.Frame(c, bg=self.COLOR_CARD); cols.pack()
        colA = tk.Frame(cols, bg=self.COLOR_CARD); colA.pack(side="left", padx=16)
        colB = tk.Frame(cols, bg=self.COLOR_CARD); colB.pack(side="left", padx=16)
        ttk.Label(colA, text="Matriz A", style="CardTitle.TLabel").pack(anchor="w")
        self.entradas_matriz_a = self.grid_inputs(colA, self.filas_a, self.columnas_a)
        ttk.Label(colB, text="Matriz B", style="CardTitle.TLabel").pack(anchor="w")
        self.entradas_matriz_b = self.grid_inputs(colB, self.filas_b, self.columnas_b)

        a = self.card()
        ttk.Button(a, text="Sumar A + B", style="Primary.TButton", command=lambda: self.resolver_operaciones("suma")).pack(side="left", padx=8)
        ttk.Button(a, text="Multiplicar A · B", style="Accent.TButton", command=lambda: self.resolver_operaciones("multiplicacion")).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=self.preparar_matrices_operaciones).pack(side="left")

    def resolver_operaciones(self, tipo):
        try:
            a = [[float(e.get()) for e in fila] for fila in self.entradas_matriz_a]
            b = [[float(e.get()) for e in fila] for fila in self.entradas_matriz_b]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten numeros.")
            return
        if tipo == "suma" and (len(a) != len(b) or len(a[0]) != len(b[0])):
            messagebox.showerror("Error", "Para A+B, A y B deben tener mismas dimensiones.")
            return
        if tipo == "multiplicacion" and len(a[0]) != len(b):
            messagebox.showerror("Error", "Para A·B, columnas(A)=filas(B).")
            return
        res = calcular_operaciones_matrices(a, b, tipo)
        self.mostrar_resultado_operaciones(a, b, res, tipo)

    def mostrar_resultado_operaciones(self, a, b, resultado, tipo):
        self.clear_content()
        ttk.Label(self.content, text=f"Resultado — {'Suma' if tipo == 'suma' else 'Multiplicacion'}", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        c = self.card()
        box = scrolledtext.ScrolledText(c, height=20, font=("Consolas", 12), bg="#333333", fg=self.COLOR_TEXT, bd=0)
        box.pack(fill="both", expand=True, padx=10, pady=6)
        txt = f"Matriz A:\n{matriz_a_string(a)}\n\nMatriz B:\n{matriz_a_string(b)}\n\nResultado:\n{matriz_a_string(resultado)}"
        box.insert(tk.END, txt)
        box.config(state="disabled")
        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Independencia Lineal -------------------
    def preparar_vectores_independencia(self):
        """Interfaz para verificar independencia lineal con diseno ampliado y responsivo."""
        self.vectores = []
        self.clear_content()

        # ======== Titulo ========
        ttk.Label(
            self.content,
            text="Independencia Lineal",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        # ======== Card principal ========
        c = self.card()

        ttk.Label(
            c,
            text="Ingresa los vectores separados por comas (ej: 1, 2, 3)",
            style="CardText.TLabel"
        ).pack(anchor="w", padx=15, pady=(0, 10))

        # ======== Contenedor de entrada ========
        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(fill="x", expand=True, padx=10, pady=10)

        # Entrada ampliada y centrada
        self.entrada_vector = tk.Entry(
            f,
            width=60,
            font=("Segoe UI", 14),
            bg="#3a3a3a",
            fg=self.COLOR_TEXT,
            insertbackground=self.COLOR_PRIMARY,
            justify="center",
            relief="flat"
        )
        self.entrada_vector.pack(side="left", fill="x", expand=True, padx=(10, 15), ipady=8)

        # Boton grande estilo neumorfico
        ttk.Button(
            f,
            text="Agregar",
            style="Accent.TButton",
            command=self.agregar_vector
        ).pack(side="left", ipadx=20, ipady=8, padx=(0, 10))

        # ======== Texto de estado ========
        self.texto_vectores = tk.StringVar(value="Ningun vector agregado aun.")
        ttk.Label(
            c,
            textvariable=self.texto_vectores,
            style="CardText.TLabel"
        ).pack(anchor="w", padx=15, pady=(5, 0))

        # ======== Botones inferiores ========
        a = self.card()
        a.columnconfigure((0, 1), weight=1)

        ttk.Button(
            a,
            text="Verificar Independencia",
            style="Primary.TButton",
            command=self.mostrar_resultado_independencia
        ).grid(row=0, column=0, padx=10, pady=12, sticky="ew")

        ttk.Button(
            a,
            text="Volver",
            style="Danger.TButton",
            command=self.vista_menu
        ).grid(row=0, column=1, padx=10, pady=12, sticky="ew")

    def agregar_vector(self):
        txt = self.entrada_vector.get().strip()
        if not txt:
            messagebox.showerror("Error", "Debe ingresar un vector.")
            return
        try:
            vec = [float(x.strip()) for x in txt.split(",")]
            if self.vectores and len(vec) != len(self.vectores[0]):
                messagebox.showerror("Error", f"El vector debe tener {len(self.vectores[0])} componentes.")
                return
            self.vectores.append(vec)
            self.texto_vectores.set(f"Vectores ingresados: {len(self.vectores)}")
            self.entrada_vector.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten numeros separados por comas.")

    def mostrar_resultado_independencia(self):
        if len(self.vectores) < 2:
            messagebox.showerror("Error", "Ingresa al menos dos vectores.")
            return
        resultado = verificar_independencia_lineal(self.vectores)
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Independencia Lineal", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        c = self.card()
        box = scrolledtext.ScrolledText(c, height=22, font=("Consolas", 12), bg="#333333", fg=self.COLOR_TEXT, bd=0)
        box.pack(fill="both", expand=True, padx=10, pady=6)
        box.insert(tk.END, resultado)
        box.config(state="disabled")
        ttk.Button(
            self.content,
            text="Volver al Menu Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

# ================================================================
#                        EJECUCION PRINCIPAL
# ================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()