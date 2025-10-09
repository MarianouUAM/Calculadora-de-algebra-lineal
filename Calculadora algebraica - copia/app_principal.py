import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from logica_calculadora import (
    resolver_gauss_jordan,
    resolver_eliminacion_filas,
    matriz_a_string,
    calcular_operaciones_matrices,
    verificar_independencia_lineal
)

# ================================================================
#              CALCULADORA CIENTÍFICA — MODO OSCURO
#                    Estilo WebApp Neumórfico
# ================================================================
class CalculadoraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica — Proyecto Universitario")
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

        # Construcción visual
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

        tk.Label(topbar, text="Calculadora Científica — Proyecto Universitario",
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
        ttk.Label(footer, text="Facultad de Ingeniería — Proyecto Académico", style="Muted.TLabel").pack()

        self._construir_sidebar()

    # ================================================================
    #                      SIDEBAR DE NAVEGACIÓN
    # ================================================================
    def _construir_sidebar(self):
        """Crea los botones de navegación lateral con efecto hover."""
        def nav_button(txt, cmd):
            b = tk.Label(self.sidebar, text=txt, bg="#252525", fg=self.COLOR_TEXT,
                         font=("Segoe UI", 11, "bold"), padx=20, pady=10, anchor="w", cursor="hand2")
            b.pack(fill="x")
            b.bind("<Enter>", lambda e: b.config(bg=self.COLOR_PRIMARY, fg="black"))
            b.bind("<Leave>", lambda e: b.config(bg="#252525", fg=self.COLOR_TEXT))
            b.bind("<Button-1>", lambda e: cmd())

        tk.Label(self.sidebar, text="Menú", bg="#252525", fg=self.COLOR_SUB,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=16, pady=(20, 10))

        nav_button("Inicio", self.vista_menu)
        nav_button("Método Gauss-Jordan", lambda: self.preparar_matriz_unica("Gauss-Jordan"))
        nav_button("Eliminación de Filas", lambda: self.preparar_matriz_unica("Eliminación"))
        nav_button("Suma y Multiplicación", self.preparar_matrices_operaciones)
        nav_button("Independencia Lineal", self.preparar_vectores_independencia)
        nav_button("Transpuesta de Matriz", self.preparar_matriz_transpuesta)

        # Separador y botón salir
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
        """Limpia todo el contenido del área central."""
        for w in self.content.winfo_children():
            w.destroy()

    def card(self, parent=None, pad=20):
        """Crea una tarjeta con sombra tipo neumórfico."""
        parent = parent or self.content
        frame = tk.Frame(parent, bg=self.COLOR_CARD, bd=0, highlightthickness=0)
        frame.pack(padx=20, pady=15, fill="x")
        frame.configure(relief="flat")

        # Sombras sutiles
        frame.config(highlightbackground="#2f2f2f")
        frame.config(highlightcolor="#111111")
        return frame

    def grid_inputs(self, parent, filas, columnas, width=8):
        """Crea una cuadrícula de entradas con estilo oscuro."""
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
    #                         MENÚ PRINCIPAL
    # ================================================================
    def vista_menu(self):
        """Pantalla inicial con estilo neumórfico."""
        self.clear_content()
        ttk.Label(self.content, text="Panel Principal", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 4))
        ttk.Label(self.content, text="Selecciona una opción en la barra lateral o desde las tarjetas inferiores.",
                  style="Muted.TLabel").pack(anchor="w", padx=22, pady=(0, 6))

        # Contenedor de tarjetas
        grid = tk.Frame(self.content, bg=self.COLOR_BG)
        grid.pack(fill="x", padx=12, pady=6)

        cards = [
            ("Método Gauss-Jordan", "Resuelve sistemas y muestra pasos detallados.",
             lambda: self.preparar_matriz_unica("Gauss-Jordan")),
            ("Eliminación de Filas", "Aplica transformaciones elementales a matrices.",
             lambda: self.preparar_matriz_unica("Eliminación")),
            ("Suma y Multiplicación", "Opera entre dos matrices con validación dimensional.",
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
    #                       MÉTODOS DE MATRICES
    # ================================================================
    def preparar_matriz_unica(self, metodo):
        """Pantalla inicial para ingresar dimensiones del sistema."""
        self.metodo_actual = metodo
        self.clear_content()

        ttk.Label(self.content, text=f"{metodo}", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(
            c,
            text="Dimensiones de la matriz aumentada (m × n)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))

        # --- NUEVO diseño centrado y grande ---
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


    def crear_interfaz_matriz_unica(self):
        """Crea la cuadrícula para ingresar un sistema de ecuaciones."""
        try:
            filas = int(self.entrada_filas.get())
            columnas = int(self.entrada_columnas.get())
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para filas y columnas.")
            return

        self.clear_content()
        ttk.Label(self.content, text="Ingrese los valores de la matriz aumentada", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        self.entradas_matriz = self.grid_inputs(c, filas, columnas)

        a = self.card()
        ttk.Button(a, text="Resolver Sistema", style="Primary.TButton", command=self.resolver_sistema).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=lambda: self.preparar_matriz_unica(self.metodo_actual)).pack(side="left")

    def resolver_sistema(self):
        """Llama al método correspondiente (Gauss-Jordan o Eliminación)."""
        try:
            datos = [[float(e.get()) for e in fila] for fila in self.entradas_matriz]
        except ValueError:
            messagebox.showerror("Error", "Solo se permiten números.")
            return

        if self.metodo_actual == "Gauss-Jordan":
            resultados = resolver_gauss_jordan(datos)
            self.mostrar_resultados_gauss_jordan(resultados, datos)
        else:
            resultados = resolver_eliminacion_filas(datos)
            self.mostrar_resultados_eliminacion(resultados)

    # ------------------- Eliminación de Filas -------------------
    def mostrar_resultados_eliminacion(self, resultados):
        self.clear_content()
        ttk.Label(self.content, text="Resultados — Eliminación de Filas", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

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
        ttk.Label(resumen_card, text="Resumen y Solución", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        info = f"Tipo de Solución: {resultados['tipo_solucion']}\n\n"
        if resultados['solucion'] is not None:
            info += "Solución:\n" + "\n".join(f"x{i+1} = {v}" for i, v in enumerate(resultados['solucion']))
        elif resultados['tipo_solucion'] == "Infinita":
            info += "El sistema tiene infinitas soluciones."
        else:
            info += "El sistema no tiene solución."
        tk.Label(resumen_card, text=info, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # Botón volver sin fondo de card
        ttk.Button(
            self.content,
            text="Volver al Menú Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Gauss-Jordan -------------------
    def mostrar_resultados_gauss_jordan(self, resultados, matriz_original):
        self.clear_content()
        ttk.Label(self.content, text="Resultados — Gauss-Jordan", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # Cuadro de pasos
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos de la resolución", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#333333", fg=self.COLOR_TEXT, bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        for p in resultados["pasos"]:
            box.insert(tk.END, p + "\n")
        box.config(state="disabled")

        # Cuadro resumen
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Resumen y Solución", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        info = (
            f"Matriz Original:\n{matriz_a_string(matriz_original)}\n\n"
            f"RREF:\n{matriz_a_string(resultados['matriz_rref'])}\n\n"
            f"Tipo de Solución: {resultados['tipo_solucion']}\n"
            f"Columnas Pivote: {', '.join(map(str, resultados['columnas_pivote']))}\n"
            f"Variables Libres: {', '.join(resultados['variables_libres']) if resultados['variables_libres'] else 'No hay.'}\n"
        )
        if resultados['solucion'] is not None:
            info += "\nSolución:\n" + "\n".join(f"x{i+1} = {v}" for i, v in enumerate(resultados['solucion']))
        tk.Label(resumen_card, text=info, bg="#333333", fg=self.COLOR_TEXT,
                 font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(
            self.content,
            text="Volver al Menú Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Transpuesta -------------------
    def preparar_matriz_transpuesta(self):
        self.clear_content()
        ttk.Label(self.content, text="Transpuesta de una Matriz", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(c, text="Dimensiones de la matriz (m × n)", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(f, text="Filas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=0, padx=10)
        self.entrada_filas_t = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_filas_t.grid(row=0, column=1, padx=10)

        tk.Label(f, text="Columnas:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=2, padx=10)
        self.entrada_columnas_t = tk.Entry(f, width=10, font=("Segoe UI", 13), justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_columnas_t.grid(row=0, column=3, padx=10)

        ttk.Button(c, text="Crear Matriz", style="Primary.TButton", command=self.crear_interfaz_matriz_transpuesta).pack(anchor="center", pady=(20, 10))


    def crear_interfaz_matriz_transpuesta(self):
        try:
            filas = int(self.entrada_filas_t.get())
            cols = int(self.entrada_columnas_t.get())
            if filas <= 0 or cols <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese números enteros positivos.")
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
            messagebox.showerror("Error", "Solo se permiten números.")
            return
        resultado = calcular_operaciones_matrices(matriz, None, "transpuesta")
        self.mostrar_resultado_transpuesta(matriz, resultado)

    def mostrar_resultado_transpuesta(self, matriz, resultado):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Transpuesta", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        if isinstance(resultado, str):
            c = self.card()
            ttk.Label(c, text=resultado, style="CardTitle.TLabel").pack(anchor="w", padx=15)
            ttk.Button(c, text="Volver al Menú Principal", style="Primary.TButton", command=self.vista_menu).pack(anchor="e", pady=8)
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
            text="Volver al Menú Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)()

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
            messagebox.showerror("Error", "Ingrese valores válidos para dimensiones.")
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
            messagebox.showerror("Error", "Solo se permiten números.")
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
        ttk.Label(self.content, text=f"Resultado — {'Suma' if tipo == 'suma' else 'Multiplicación'}", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        c = self.card()
        box = scrolledtext.ScrolledText(c, height=20, font=("Consolas", 12), bg="#333333", fg=self.COLOR_TEXT, bd=0)
        box.pack(fill="both", expand=True, padx=10, pady=6)
        txt = f"Matriz A:\n{matriz_a_string(a)}\n\nMatriz B:\n{matriz_a_string(b)}\n\nResultado:\n{matriz_a_string(resultado)}"
        box.insert(tk.END, txt)
        box.config(state="disabled")
        ttk.Button(
            self.content,
            text="Volver al Menú Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

    # ------------------- Independencia Lineal -------------------
    def preparar_vectores_independencia(self):
        self.vectores = []
        self.clear_content()
        ttk.Label(self.content, text="Independencia Lineal", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(c, text="Ingresa los vectores separados por comas (ej: 1, 2, 3)", style="CardText.TLabel").pack(anchor="w", padx=15)
        f = tk.Frame(c, bg=self.COLOR_CARD); f.pack(pady=8)
        self.entrada_vector = tk.Entry(f, width=45, bg="#3a3a3a", fg=self.COLOR_TEXT, insertbackground=self.COLOR_PRIMARY)
        self.entrada_vector.pack(side="left", padx=(0, 8))
        ttk.Button(f, text="Agregar", style="Accent.TButton", command=self.agregar_vector).pack(side="left")
        self.texto_vectores = tk.StringVar(value="Ningún vector agregado aún.")
        ttk.Label(c, textvariable=self.texto_vectores, style="CardText.TLabel").pack(anchor="w", padx=15, pady=(5, 0))

        a = self.card()
        ttk.Button(a, text="Verificar Independencia", style="Primary.TButton", command=self.mostrar_resultado_independencia).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=self.vista_menu).pack(side="left")

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
            messagebox.showerror("Error", "Solo se permiten números separados por comas.")

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
            text="Volver al Menú Principal",
            style="Primary.TButton",
            command=self.vista_menu
        ).pack(anchor="center", pady=20)

# ================================================================
#                        EJECUCIÓN PRINCIPAL
# ================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()

