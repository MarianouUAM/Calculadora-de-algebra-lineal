import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
from fractions import Fraction
from logica_calculadora import (
    resolver_gauss_jordan,
    resolver_eliminacion_filas,
    matriz_a_string,
    calcular_operaciones_matrices,
    verificar_independencia_lineal,
    resolver_sistema_homogeneo,
    calcular_inversa,
    calcular_determinante_auto,
    resolver_cramer,
    formatea_num,
    es_casi_cero
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
        """Crea los botones de navegación lateral con diseño mejorado."""
        def nav_button(txt, cmd, icon="•"):
            btn_frame = tk.Frame(self.sidebar, bg="#252525", height=44)
            btn_frame.pack(fill="x", pady=1)
            btn_frame.pack_propagate(False)
            
            btn_content = tk.Frame(btn_frame, bg="#252525")
            btn_content.pack(fill="both", expand=True, padx=15)
            
            # Icono
            icon_label = tk.Label(btn_content, text=icon, bg="#252525", fg=self.COLOR_PRIMARY,
                                font=("Segoe UI", 12), width=3, anchor="w")
            icon_label.pack(side="left")
            
            # Texto
            text_label = tk.Label(btn_content, text=txt, bg="#252525", fg=self.COLOR_TEXT,
                                font=("Segoe UI", 11), anchor="w", cursor="hand2")
            text_label.pack(side="left", fill="x", expand=True)
            
            def on_enter(e):
                btn_content.config(bg=self.COLOR_PRIMARY)
                icon_label.config(bg=self.COLOR_PRIMARY, fg="black")
                text_label.config(bg=self.COLOR_PRIMARY, fg="black")
            
            def on_leave(e):
                btn_content.config(bg="#252525")
                icon_label.config(bg="#252525", fg=self.COLOR_PRIMARY)
                text_label.config(bg="#252525", fg=self.COLOR_TEXT)
            
            def on_click(e):
                cmd()
            
            btn_content.bind("<Enter>", on_enter)
            btn_content.bind("<Leave>", on_leave)
            btn_content.bind("<Button-1>", on_click)
            icon_label.bind("<Enter>", on_enter)
            icon_label.bind("<Leave>", on_leave)
            icon_label.bind("<Button-1>", on_click)
            text_label.bind("<Enter>", on_enter)
            text_label.bind("<Leave>", on_leave)
            text_label.bind("<Button-1>", on_click)
            
            return btn_frame

        # Header del sidebar
        sidebar_header = tk.Frame(self.sidebar, bg="#1a1a1a", height=80)
        sidebar_header.pack(fill="x", pady=(0, 5))
        sidebar_header.pack_propagate(False)
        
        header_content = tk.Frame(sidebar_header, bg="#1a1a1a")
        header_content.pack(expand=True, fill="both", padx=20)
        
        ttk.Label(header_content, text="HERRAMIENTAS", 
                style="Muted.TLabel", 
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(15, 5))
        
        ttk.Label(header_content, text="Álgebra Lineal", 
                style="H2.TLabel", 
                font=("Segoe UI", 14, "bold")).pack(anchor="w")
        
        # Separador
        tk.Frame(self.sidebar, bg="#303030", height=2).pack(fill="x", pady=(0, 5))
        
        # boton de inicio
        nav_button("Inicio", self.vista_menu, "🏠")

        # Grupo: Sistemas de Ecuaciones
        group_label = tk.Label(self.sidebar, text="  SISTEMAS LINEALES", bg="#252525", 
                            fg=self.COLOR_SUB, font=("Segoe UI", 9, "bold"), 
                            anchor="w", pady=8)
        group_label.pack(fill="x", pady=(5, 0))
        
        # Botones del grupo
        nav_button("Gauss-Jordan", lambda: self.preparar_matriz_unica("Gauss-Jordan"), "⚡")
        nav_button("Eliminación de Filas", lambda: self.preparar_matriz_unica("Eliminacion"), "🔍")
        nav_button("Método de Cramer", self.preparar_cramer, "🧮")
        nav_button("Sistema Homogéneo", self.preparar_matriz_homogeneo, "⚖️")

        # Separador entre grupos
        tk.Frame(self.sidebar, bg="#303030", height=1).pack(fill="x", pady=10)

        # Grupo: Operaciones Matriciales
        group_label2 = tk.Label(self.sidebar, text="  OPERACIONES MATRICIALES", bg="#252525", 
                            fg=self.COLOR_SUB, font=("Segoe UI", 9, "bold"), 
                            anchor="w", pady=8)
        group_label2.pack(fill="x", pady=(5, 0))
        
        nav_button("Suma y Multiplicación", self.preparar_matrices_operaciones, "➕")
        nav_button("Transpuesta", self.preparar_matriz_transpuesta, "🔄")
        nav_button("Inversa", self.preparar_inversa_matriz, "🔺")
        nav_button("Determinantes", self.preparar_determinante, "📐")

        # Separador entre grupos
        tk.Frame(self.sidebar, bg="#303030", height=1).pack(fill="x", pady=10)

        # Grupo: Transformaciones y Vectores
        group_label3 = tk.Label(self.sidebar, text="  VECTORES Y TRANSFORMACIONES", bg="#252525", 
                            fg=self.COLOR_SUB, font=("Segoe UI", 9, "bold"), 
                            anchor="w", pady=8)
        group_label3.pack(fill="x", pady=(5, 0))
        
        nav_button("Independencia Lineal", self.preparar_vectores_independencia, "📊")
        #nav_button("Construir T(x)=A·x", self.preparar_construir_transformacion, "🛠️")
        nav_button("Probar Linealidad", self.preparar_linealidad, "📈")

        # Espacio flexible
        tk.Frame(self.sidebar, bg="#252525").pack(fill="both", expand=True)

        # Botón salir en la parte inferior
        bottom_frame = tk.Frame(self.sidebar, bg="#252525")
        bottom_frame.pack(fill="x", side="bottom", pady=(0, 10))
        
        tk.Frame(bottom_frame, bg="#303030", height=2).pack(fill="x", pady=(0, 15))
        
        exit_btn = nav_button("Cerrar Aplicación", lambda: self.root.destroy(), "🚪")
        
        # Info de versión
        version_frame = tk.Frame(bottom_frame, bg="#252525")
        version_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        ttk.Label(version_frame, text="v1.0 • Proyecto Académico", 
                style="Muted.TLabel", 
                font=("Segoe UI", 8)).pack(anchor="center")

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
        """Pantalla inicial con estilo neumorfico mejorado."""
        self.clear_content()
        
        # Header principal con gradiente sutil
        header_frame = tk.Frame(self.content, bg=self.COLOR_BG)
        header_frame.pack(fill="x", padx=22, pady=(25, 15))
        
        ttk.Label(header_frame, text="Panel Principal", style="H1.TLabel").pack(anchor="w", pady=(0, 4))
        
        # Subtítulo con icono conceptual
        sub_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        sub_frame.pack(anchor="w", fill="x")
        
        ttk.Label(sub_frame, 
                text="Selecciona una opción en la barra lateral o desde las tarjetas inferiores",
                style="Muted.TLabel").pack(side="left")
        
        # Indicador de estado del sistema
        status_frame = tk.Frame(header_frame, bg=self.COLOR_BG)
        status_frame.pack(anchor="w", pady=(8, 0))
        
        status_dot = tk.Frame(status_frame, width=8, height=8, bg=self.COLOR_PRIMARY, relief="flat")
        status_dot.pack(side="left", padx=(0, 8))
        status_dot.pack_propagate(False)
        
        ttk.Label(status_frame, text="Sistema operativo • Todos los módulos disponibles", 
                style="Muted.TLabel", font=("Segoe UI", 9)).pack(side="left")

        # Contenedor principal para tarjetas (usando pack)
        cards_container = tk.Frame(self.content, bg=self.COLOR_BG)
        cards_container.pack(fill="both", expand=True, padx=12, pady=10)

        cards = [
            ("Método Gauss-Jordan", "Resuelve sistemas y muestra pasos detallados", "⚡",
            lambda: self.preparar_matriz_unica("Gauss-Jordan")),
            ("Eliminación de Filas", "Aplica transformaciones elementales a matrices", "🔍",
            lambda: self.preparar_matriz_unica("Eliminacion")),
            ("Suma y Multiplicación", "Opera entre dos matrices con validación dimensional", "➕",
            self.preparar_matrices_operaciones),
            ("Independencia Lineal", "Analiza vectores y determina su independencia", "📊",
            self.preparar_vectores_independencia),
            ("Transpuesta de Matriz", "Calcula la transpuesta y muestra el proceso", "🔄",
            self.preparar_matriz_transpuesta),
            ("Sistema Homogéneo", "Resuelve sistemas Ax=0 con solución paramétrica", "⚖️",
            self.preparar_matriz_homogeneo),
        ]

        # Crear dos columnas usando frames
        columns_frame = tk.Frame(cards_container, bg=self.COLOR_BG)
        columns_frame.pack(fill="both", expand=True)
        
        left_column = tk.Frame(columns_frame, bg=self.COLOR_BG)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 6))
        
        right_column = tk.Frame(columns_frame, bg=self.COLOR_BG)
        right_column.pack(side="right", fill="both", expand=True, padx=(6, 0))

        for i, (titulo, desc, icono, comando) in enumerate(cards):
            # Alternar entre columnas izquierda y derecha
            if i % 2 == 0:
                parent_column = left_column
            else:
                parent_column = right_column
            
            c = self.card(parent_column)
            c.pack(fill="x", padx=8, pady=8)
            
            # Header de tarjeta con icono
            card_header = tk.Frame(c, bg=self.COLOR_CARD)
            card_header.pack(fill="x", padx=15, pady=(12, 8))
            
            # Icono
            icon_label = tk.Label(card_header, text=icono, bg=self.COLOR_CARD, fg=self.COLOR_PRIMARY,
                                font=("Segoe UI", 16))
            icon_label.pack(side="left", padx=(0, 10))
            
            # Título
            title_frame = tk.Frame(card_header, bg=self.COLOR_CARD)
            title_frame.pack(side="left", fill="x", expand=True)
            
            ttk.Label(title_frame, text=titulo, style="CardTitle.TLabel").pack(anchor="w")
            ttk.Label(title_frame, text=desc, style="CardText.TLabel", 
                    font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 0))
            
            # Botón de acción
            btn_frame = tk.Frame(c, bg=self.COLOR_CARD)
            btn_frame.pack(fill="x", padx=15, pady=(8, 12))
            
            ttk.Button(btn_frame, text="Abrir herramienta", style="Primary.TButton", 
                    command=comando).pack(side="right")
            
            # Efecto hover para la tarjeta completa
            def make_hover_effect(card=c, original_bg=self.COLOR_CARD):
                def on_enter(e):
                    card.config(bg=self.COLOR_LIGHT)
                    for child in card.winfo_children():
                        if isinstance(child, tk.Frame):
                            child.config(bg=self.COLOR_LIGHT)
                
                def on_leave(e):
                    card.config(bg=original_bg)
                    for child in card.winfo_children():
                        if isinstance(child, tk.Frame):
                            child.config(bg=original_bg)
                
                card.bind("<Enter>", on_enter)
                card.bind("<Leave>", on_leave)
                card_header.bind("<Enter>", on_enter)
                card_header.bind("<Leave>", on_leave)
                title_frame.bind("<Enter>", on_enter)
                title_frame.bind("<Leave>", on_leave)
                btn_frame.bind("<Enter>", on_enter)
                btn_frame.bind("<Leave>", on_leave)
            
            make_hover_effect()

        # Footer del dashboard
        footer_card = self.card(self.content)
        footer_frame = tk.Frame(footer_card, bg=self.COLOR_CARD)
        footer_frame.pack(fill="x", padx=20, pady=15)
        
        ttk.Label(footer_frame, 
                text="💡 Tip: Usa el menú lateral para acceder a todas las herramientas disponibles",
                style="CardText.TLabel", 
                font=("Segoe UI", 10, "italic")).pack(side="left")
        
        ttk.Label(footer_frame, 
                text=f"{len(cards)} herramientas disponibles", 
                style="CardText.TLabel",
                font=("Segoe UI", 10)).pack(side="right")

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
        ttk.Label(self.content, text="Resultado — Eliminación de Filas", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # ======== PROCESO ========
        pasos_card = self.card()
        ttk.Label(pasos_card, text="🔄 Proceso de eliminación:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 11),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for paso in resultados["pasos"]:
            if "Paso:" in paso:
                box.insert(tk.END, f"🎯 {paso}\n", "paso")
            elif "Matriz en forma escalonada" in paso:
                box.insert(tk.END, f"📊 {paso}\n", "importante")
            else:
                box.insert(tk.END, paso + "\n")
        
        box.tag_configure("paso", foreground="#FF9800")
        box.tag_configure("importante", foreground="#4FC3F7")
        box.config(state="disabled")

        # ======== CONCLUSIÓN ========
        resumen_card = self.card()
        ttk.Label(resumen_card, text="📈 Conclusión:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        tipo = resultados['tipo_solucion']
        if tipo == "Única":
            color = "#4CAF50"
            icon = "✅"
            info = f"{icon} SOLUCIÓN ÚNICA\n\n"
            info += "Solución del sistema:\n" + "\n".join(f"• x{i+1} = {v}" for i, v in enumerate(resultados['solucion']))
        elif tipo == "Infinita":
            color = "#FF9800"
            icon = "🔶"
            info = f"{icon} INFINITAS SOLUCIONES\n\nEl sistema tiene infinitas soluciones"
        else:
            color = "#F44336"
            icon = "❌"
            info = f"{icon} SISTEMA INCONSISTENTE\n\nEl sistema no tiene solución"
        
        tk.Label(resumen_card, text=info, bg="#333333", fg=color,
                font=("Consolas", 12, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

    # ------------------- Gauss-Jordan -------------------
    def mostrar_resultados_gauss_jordan(self, resultados, matriz_original):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Método Gauss-Jordan", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # MATRIZ ORIGINAL
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz original del sistema:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_str = matriz_a_string(matriz_original, is_system=True)
        tk.Label(matriz_card, text=matriz_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # PROCESO
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Proceso de resolución:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 11),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for p in resultados["pasos"]:
            if "Paso:" in p:
                box.insert(tk.END, f"{p}\n", "paso")
            elif "Columna" in p and "Variable libre" in p:
                box.insert(tk.END, f"{p}\n", "libre")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("paso", foreground="#FF9800")
        box.tag_configure("libre", foreground="#4CAF50")
        box.config(state="disabled")

        # CONCLUSIÓN
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Conclusión:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        info = f"Tipo de Solución: {resultados['tipo_solucion']}\n"
        info += f"Columnas Pivote: {', '.join(map(str, resultados['columnas_pivote']))}\n"
        info += f"Variables Libres: {', '.join(resultados['variables_libres']) if resultados['variables_libres'] else 'No hay'}\n\n"
        
        if resultados['solucion'] is not None:
            info += "Solución del sistema:\n" + "\n".join(f"x{i+1} = {v}" for i, v in enumerate(resultados['solucion']))
        elif resultados['tipo_solucion'] == "Infinita":
            info += "El sistema tiene infinitas soluciones (variables libres presentes)"
        else:
            info += "El sistema no tiene solución única"
        
        color = "#4CAF50" if resultados['tipo_solucion'] == "Única" else "#FF9800" if resultados['tipo_solucion'] == "Infinita" else "#F44336"
        
        tk.Label(resumen_card, text=info, bg="#333333", fg=color,
                font=("Consolas", 12, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # BOTONES
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)
        
        ttk.Button(self.content, text="Resolver otro sistema", style="Primary.TButton",
                command=lambda: self.preparar_matriz_unica("Gauss-Jordan")).pack(side="left", padx=8, pady=20)
        ttk.Button(self.content, text="Volver al Inicio", style="Danger.TButton",
                command=self.vista_menu).pack(side="left", padx=8, pady=20)
            
        
    def mostrar_resultados_homogeneo(self, resultados, matriz_original):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Sistema Homogéneo (Ax = 0)", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # MATRIZ ORIGINAL
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz original de coeficientes:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_str = matriz_a_string(matriz_original)
        tk.Label(matriz_card, text=matriz_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # PROCESO
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Proceso de resolución:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 11),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for p in resultados["pasos"]:
            if "Paso:" in p:
                box.insert(tk.END, f"{p}\n", "paso")
            elif "Variable libre" in p:
                box.insert(tk.END, f"{p}\n", "libre")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("paso", foreground="#FF9800")
        box.tag_configure("libre", foreground="#4CAF50")
        box.config(state="disabled")

        # CONCLUSIÓN
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Conclusión:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        if resultados["tipo_solucion"] == "Única (trivial)":
            color = "#4CAF50"
            texto = "SOLUCIÓN ÚNICA (TRIVIAL)\n\n"
            texto += "x = 0 (solución trivial)\n"
            texto += f"Variables pivote: {', '.join(map(str, resultados['pivotes']))}"
        else:
            color = "#FF9800"
            texto = "INFINITAS SOLUCIONES\n\n"
            texto += f"Variables libres: {', '.join(resultados['variables_libres'])}\n"
            texto += f"Variables pivote: {', '.join(map(str, resultados['pivotes']))}\n\n"
            texto += "Solución general paramétrica:\n"
            
            for i in range(len(resultados["solucion_parametrica"])):
                vec = resultados["solucion_parametrica"][i]
                t = resultados["parametros"][i]
                texto += f"\nPara {t}:\n"
                for idx, coef in enumerate(vec):
                    if not es_casi_cero(coef):
                        texto += f"   x{idx+1} = {formatea_num(coef)} * {t}\n"

        tk.Label(resumen_card, text=texto, bg="#333333", fg=color,
                font=("Consolas", 12, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # BOTONES
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)
        
        ttk.Button(self.content, text="Resolver otro sistema", style="Primary.TButton",
                command=self.preparar_matriz_homogeneo).pack(side="left", padx=8, pady=20)
        ttk.Button(self.content, text="Volver al Inicio", style="Danger.TButton",
                command=self.vista_menu).pack(side="left", padx=8, pady=20)
        
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

    '''def preparar_construir_transformacion(self):
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
                   command=self.vista_menu).pack(side="left", padx=8)'''
        
        
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
        
    def preparar_cramer(self):
        """Pantalla inicial para ingresar un sistema Ax=b (Regla de Cramer)."""
        self.metodo_actual = "Cramer"
        self.clear_content()

        ttk.Label(self.content, text="Método de Cramer", style="H1.TLabel").pack(
            anchor="w", padx=22, pady=(18, 8)
        )

        c = self.card()
        ttk.Label(c, text="Dimensión de la matriz A (n × n)", style="CardTitle.TLabel").pack(
            anchor="center", pady=(10, 15)
        )

        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(f, text="n:", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, font=("Segoe UI", 13)).grid(row=0, column=0, padx=10)
        self.entrada_n_cramer = tk.Entry(f, width=10, font=("Segoe UI", 13),
                                         justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
                                         insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_n_cramer.grid(row=0, column=1, padx=10)

        ttk.Button(c, text="Crear Matrices A y b", style="Primary.TButton",
                   command=self.crear_interfaz_cramer).pack(anchor="center", pady=(20, 10))

    def crear_interfaz_cramer(self):
        """Permite ingresar la matriz A y el vector b."""
        try:
            n = int(self.entrada_n_cramer.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para n.")
            return

        self.clear_content()
        ttk.Label(self.content, text=f"Ingrese los valores de A ({n}×{n}) y el vector b", style="H1.TLabel").pack(
            anchor="w", padx=22, pady=(18, 8)
        )

        c1 = self.card()
        ttk.Label(c1, text="Matriz A:", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        self.matriz_A = self.grid_inputs(c1, n, n)

        c2 = self.card()
        ttk.Label(c2, text="Vector b:", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        self.vector_b = self.grid_inputs(c2, n, 1)

        a = self.card()
        ttk.Button(a, text="Resolver por Cramer", style="Primary.TButton", command=self.resolver_cramer_visual).pack(side="left", padx=8)
        ttk.Button(a, text="Volver", style="Danger.TButton", command=self.preparar_cramer).pack(side="left", padx=8)

    def resolver_cramer_visual(self):
        """Lee las entradas (incluye fracciones) y llama a la lógica de Cramer."""
        
        def convertir_valor(texto):
            texto = texto.strip()

            # Si es fracción tipo a/b
            if "/" in texto:
                try:
                    numerador, denominador = texto.split("/")
                    return float(numerador) / float(denominador)
                except:
                    raise ValueError("Fracción inválida")

            # Si es número normal
            try:
                return float(texto)
            except:
                raise ValueError("Valor inválido")

        try:
            # Leer matriz A
            A = []
            for fila in self.matriz_A:
                A.append([convertir_valor(e.get()) for e in fila])

            # Leer vector b
            b = [convertir_valor(self.vector_b[i][0].get()) for i in range(len(self.vector_b))]

        except Exception as e:
            messagebox.showerror("Error", f"Error en los datos ingresados: {str(e)}\n\nUse números o fracciones válidas (Ej: 1/2, -3/4)")
            return

        # Lógica del método de Cramer
        from logica_calculadora import resolver_cramer
        resultado = resolver_cramer(A, b)  # ESTA LÍNEA FALTABA

        # Interfaz de resultados
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Regla de Cramer", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del método", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=20, font=("Consolas", 12),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # VERIFICAR SI resultado TIENE PASOS
        if "pasos" in resultado and resultado["pasos"]:
            for p in resultado["pasos"]:
                if "det(A)" in p:
                    box.insert(tk.END, f"{p}\n", "detA")
                elif "x" in p and "=" in p:
                    box.insert(tk.END, f"{p}\n", "solucion")
                elif "SOLUCIÓN FINAL" in p:
                    box.insert(tk.END, f"{p}\n", "final")
                else:
                    box.insert(tk.END, p + "\n")
            
            box.tag_configure("detA", foreground="#FF9800")
            box.tag_configure("solucion", foreground="#4CAF50")
            box.tag_configure("final", foreground="#4FC3F7")
        else:
            box.insert(tk.END, "No hay pasos disponibles para mostrar.\n")
        
        box.config(state="disabled")

        if resultado.get("solucion"):
            sol_card = self.card()
            ttk.Label(sol_card, text="Solución", 
                    style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
            
            # Mostrar en fracción y decimal
            for i in range(len(resultado["solucion"])):
                decimal = resultado["solucion"][i]
                fraccion = resultado.get("solucion_fraccion", [])[i] if resultado.get("solucion_fraccion") else decimal
                texto_sol = f"x{i+1} = {fraccion} = {decimal}"
                ttk.Label(sol_card, text=texto_sol, 
                        style="CardText.TLabel", foreground="#4CAF50", 
                        font=("Consolas", 12)).pack(anchor="w", padx=20, pady=2)
        else:
            error_card = self.card()
            ttk.Label(error_card, text="El sistema no tiene solución única.", 
                    style="CardText.TLabel", foreground="#F44336").pack(anchor="w", padx=22, pady=10)

        ttk.Button(self.content, text="Volver al Menú Principal", style="Primary.TButton",
                command=self.vista_menu).pack(anchor="center", pady=20)

    def crear_interfaz_determinante(self):
            try:
                n = int(self.entrada_n_det.get())
                if n <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor válido para n.")
                return

            self.clear_content()
            ttk.Label(
                self.content,
                text=f"Ingrese los valores de la matriz A ({n}×{n})",
                style="H1.TLabel"
            ).pack(anchor="w", padx=22, pady=(18, 8))

            c = self.card()
            self.matriz_det = self.grid_inputs(c, n, n)

            a = self.card()
            ttk.Button(
                a, text="Calcular Determinante", style="Primary.TButton",
                command=self.resolver_determinante_auto
            ).pack(side="left", padx=8)
            ttk.Button(
                a, text="Volver", style="Danger.TButton",
                command=self.preparar_determinante
            ).pack(side="left", padx=8)
        
    def resolver_determinante_auto(self):
        from logica_calculadora import calcular_determinante_auto

        def convertir_valor(texto):
            texto = texto.strip()
            
            if "/" in texto:
                try:
                    numerador, denominador = texto.split("/")
                    return float(numerador) / float(denominador)
                except:
                    raise ValueError("Fracción inválida")
            
            try:
                return float(texto)
            except:
                raise ValueError("Valor inválido")

        try:
            matriz = []
            for fila in self.matriz_det:
                nueva_fila = []
                for e in fila:
                    valor = convertir_valor(e.get())
                    nueva_fila.append(valor)
                matriz.append(nueva_fila)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en los datos ingresados: {str(e)}\n\nUse números o fracciones como: 1/2, -3/4, 2.5")
            return

        resultado = calcular_determinante_auto(matriz)

        self.clear_content()
        ttk.Label(self.content, text="Resultado — Determinante de una Matriz",
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # MÉTODO APLICADO
        info_card = self.card()
        metodo = resultado.get('metodo', 'Método automático')
        ttk.Label(info_card, text=f"Método aplicado: {metodo}", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        if 'razon' in resultado:
            ttk.Label(info_card, text=resultado["razon"], style="CardText.TLabel").pack(anchor="w", padx=15, pady=(0, 8))

        # PROCESO
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del cálculo:", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        pasos = resultado.get("pasos", [])
        for p in pasos:
            if "det(A)" in p or "Determinante" in p:
                box.insert(tk.END, f"{p}\n", "importante")
            elif "=" in p and any(op in p for op in ["+", "-", "*"]):
                box.insert(tk.END, f"{p}\n", "calculo")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("importante", foreground="#4CAF50")
        box.tag_configure("calculo", foreground="#FF9800")
        box.config(state="disabled")

        # RESULTADO FINAL
        res_card = self.card()
        ttk.Label(res_card, text="Resultado final:", style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        det_value = resultado.get('determinante') or resultado.get('resultado', 0)
        resultado_text = f"det(A) = {formatea_num(det_value)}"
        
        if abs(det_value) < 1e-9:
            resultado_text += "\n\nLa matriz es SINGULAR (no invertible)"
            color = "#F44336"
        else:
            resultado_text += "\n\nLa matriz es NO SINGULAR (invertible)"
            color = "#4CAF50"
        
        tk.Label(res_card, text=resultado_text, bg="#333333", fg=color,
                font=("Consolas", 14, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=10)

        ttk.Button(self.content, text="Volver al menú principal",
            style="Primary.TButton", command=self.vista_menu
        ).pack(anchor="center", pady=20)

    def resolver_determinante_visual(self):
            from logica_calculadora import calcular_determinante_auto

            try:
                matriz = []
                for fila in self.entradas_matriz:
                    nueva_fila = []
                    for e in fila:
                        txt = e.get().strip()
                        if "/" in txt:
                            num, den = txt.split("/")
                            nueva_fila.append(int(num) / int(den))
                        else:
                            nueva_fila.append(float(txt))
                    matriz.append(nueva_fila)
            except:
                messagebox.showerror("Error", "Solo números y fracciones como 1/2")
                return

            resultado = calcular_determinante_auto(matriz)

            self.clear_content()
            ttk.Label(self.content, text="Determinante — Paso a Paso", style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

            card = self.card()
            box = scrolledtext.ScrolledText(
                card, height=20, font=("Consolas", 11),
                bg="#2a2a2a", fg="white", bd=0, relief="flat"
            )
            box.pack(fill="both", expand=True, padx=10, pady=10)

            for p in resultado["pasos"]:
                box.insert("end", p + "\n")

            box.insert("end", f"\nRESULTADO FINAL: det(A) = {resultado['determinante']}\n")
            box.config(state="disabled")

    def mostrar_resultados_determinante(self, resultados, matriz_original):
        self.clear_content()
        ttk.Label(self.content, text=f"Resultado — {resultados['metodo']}", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # ======== MATRIZ ORIGINAL ========
        matriz_card = self.card()
        ttk.Label(matriz_card, text="📊 Matriz original:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_str = matriz_a_string(matriz_original)
        tk.Label(matriz_card, text=matriz_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # ======== MÉTODO USADO ========
        metodo_card = self.card()
        ttk.Label(metodo_card, text="🎯 Método aplicado:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        tk.Label(metodo_card, text=resultados["metodo"], bg="#333333", fg="#FF9800",
                font=("Consolas", 11, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # ======== PROCESO ========
        pasos_card = self.card()
        ttk.Label(pasos_card, text="🔄 Proceso de cálculo:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 11),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for p in resultados["pasos"]:
            if "det(A)" in p or "Determinante" in p:
                box.insert(tk.END, f"🎯 {p}\n", "importante")
            elif "=" in p and any(op in p for op in ["+", "-", "*"]):
                box.insert(tk.END, f"🧮 {p}\n", "calculo")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("importante", foreground="#4CAF50")
        box.tag_configure("calculo", foreground="#FF9800")
        box.config(state="disabled")

        # ======== RESULTADO FINAL ========
        res_card = self.card()
        ttk.Label(res_card, text="🏁 Resultado final:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        resultado_text = f"det(A) = {formatea_num(resultados['resultado'])}"
        if abs(resultados['resultado']) < 1e-9:
            resultado_text += "\n\n❌ La matriz es SINGULAR (no invertible)"
            color = "#F44336"
        else:
            resultado_text += "\n\n✅ La matriz es NO SINGULAR (invertible)"
            color = "#4CAF50"
        
        tk.Label(res_card, text=resultado_text, bg="#333333", fg=color,
                font=("Consolas", 14, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=10)
    
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
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Inversa de Matriz", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # MATRIZ ORIGINAL
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz original:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_str = matriz_a_string(matriz_original)
        tk.Label(matriz_card, text=matriz_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # PROCESO
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 11),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for p in resultado.get("pasos", []):
            if "Pivotes encontrados" in p:
                box.insert(tk.END, f"{p}\n", "importante")
            elif "NO es invertible" in p:
                box.insert(tk.END, f"{p}\n", "error")
            elif "SÍ tiene n pivotes" in p:
                box.insert(tk.END, f"{p}\n", "exito")
            elif "Matriz 2x2:" in p or "Determinante =" in p or "Se aplica" in p:
                box.insert(tk.END, f"{p}\n", "naranja")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("importante", foreground="#FF9800")
        box.tag_configure("error", foreground="#F44336")
        box.tag_configure("exito", foreground="#4CAF50")
        box.tag_configure("naranja", foreground="#FF9800")  # Color naranja para fórmulas
        box.config(state="disabled")

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # CONCLUSIÓN
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Conclusión", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        if not resultado["es_invertible"]:
            mensaje = "La matriz NO es invertible\n\n"
            mensaje += "Motivo:\n" + resultado.get("motivo", "No tiene n pivotes.")
            color = "#F44336"
        else:
            inversa = resultado.get("inversa", [])
            mensaje = "La matriz SÍ es invertible\n\n"
            mensaje += f"Matriz Original:\n{matriz_a_string(matriz_original)}\n\n"
            mensaje += f"Inversa A⁻¹:\n{matriz_a_string(inversa)}"
            color = "#4CAF50"

        tk.Label(resumen_card, text=mensaje, bg="#333333", fg=color,
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # BOTONES
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)
        
        ttk.Button(self.content, text="Calcular otra inversa", style="Primary.TButton",
                command=self.preparar_inversa_matriz).pack(side="left", padx=8, pady=20)
        ttk.Button(self.content, text="Volver al Inicio", style="Danger.TButton",
                command=self.vista_menu).pack(side="left", padx=8, pady=20)


    def mostrar_resultado_transformacion(self, pasos, matriz_A):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Matriz de Transformación T(x)=A·x",
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # PASOS
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for p in pasos:
            if "Analizando" in p:
                box.insert(tk.END, f"{p}\n", "analisis")
            elif "Coeficientes finales" in p:
                box.insert(tk.END, f"{p}\n", "resultado")
            elif "Matriz A resultante" in p:
                box.insert(tk.END, f"{p}\n", "final")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("analisis", foreground="#FF9800")
        box.tag_configure("resultado", foreground="#4CAF50")
        box.tag_configure("final", foreground="#4FC3F7")
        box.config(state="disabled")

        # MATRIZ FINAL
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz A resultante", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        texto_matriz = matriz_a_string(matriz_A)
        tk.Label(matriz_card, text=texto_matriz, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(self.content, text="Volver al Menu Principal",
            style="Primary.TButton", command=self.vista_menu
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
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Linealidad de T(x) = A·x + b",
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # PASOS
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Pasos del proceso",
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        box = scrolledtext.ScrolledText(pasos_card, height=18, font=("Consolas", 12),
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        for p in pasos:
            if "T(0)" in p and "=" in p:
                box.insert(tk.END, f"{p}\n", "importante")
            elif "ES transformación lineal" in p:
                box.insert(tk.END, f"{p}\n", "exito")
            elif "NO es transformación lineal" in p:
                box.insert(tk.END, f"{p}\n", "error")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("importante", foreground="#FF9800")
        box.tag_configure("exito", foreground="#4CAF50")
        box.tag_configure("error", foreground="#F44336")
        box.config(state="disabled")

        # CONCLUSIÓN
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Conclusión",
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        if es_lineal:
            conclusion = "T ES transformación lineal (b = 0)"
            color = "#4CAF50"
        else:
            conclusion = "T NO es transformación lineal (b ≠ 0)"
            color = "#F44336"

        tk.Label(resumen_card, text=conclusion, bg="#333333", fg=color,
                font=("Consolas", 13, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        ttk.Button(self.content, text="Volver al Menú Principal",
            style="Primary.TButton", command=self.vista_menu
        ).pack(anchor="center", pady=20)
        
    # ------------------- Matriz Transpuesta -------------------
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
            messagebox.showerror("Error", "Solo se permiten números.")
            return
            
        resultado = calcular_operaciones_matrices(matriz, None, "transpuesta")
        self.mostrar_resultado_transpuesta(matriz, resultado)

    def mostrar_resultado_transpuesta(self, matriz, resultado):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Transpuesta", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        
        if isinstance(resultado, str):
            # Si hay error
            c = self.card()
            ttk.Label(c, text=resultado, style="CardTitle.TLabel", foreground="#F44336").pack(anchor="w", padx=15)
            ttk.Button(c, text="Volver al Menu Principal", style="Primary.TButton", 
                    command=self.vista_menu).pack(anchor="e", pady=8)
            return

        pasos = resultado.get("pasos", [])
        transpuesta = resultado.get("resultado", [])

        # MATRIZ ORIGINAL
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz original:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_str = matriz_a_string(matriz)
        tk.Label(matriz_card, text=matriz_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # PROCESO
        pasos_card = self.card()
        ttk.Label(pasos_card, text="Proceso de cálculo:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        box = scrolledtext.ScrolledText(pasos_card, height=14, font=("Consolas", 12), 
                                        bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
        box.pack(fill="both", expand=True, padx=10, pady=6)
        
        for p in pasos:
            if "Fila" in p and "Columna" in p:
                box.insert(tk.END, f"{p}\n", "conversion")
            elif "Resultado final" in p:
                box.insert(tk.END, f"{p}\n", "final")
            else:
                box.insert(tk.END, p + "\n")
        
        box.tag_configure("conversion", foreground="#FF9800")
        box.tag_configure("final", foreground="#4CAF50")
        box.config(state="disabled")

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # RESULTADO
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Matriz transpuesta:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        texto = f"Matriz Original ({len(matriz)}×{len(matriz[0])}):\n{matriz_a_string(matriz)}\n\n"
        texto += f"Matriz Transpuesta ({len(transpuesta)}×{len(transpuesta[0])}):\n{matriz_a_string(transpuesta)}"
        
        tk.Label(resumen_card, text=texto, bg="#333333", fg="#4CAF50",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # BOTONES
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)
        
        ttk.Button(self.content, text="Calcular otra transpuesta", style="Primary.TButton",
                command=self.preparar_matriz_transpuesta).pack(side="left", padx=8, pady=20)
        ttk.Button(self.content, text="Volver al Inicio", style="Danger.TButton",
                command=self.vista_menu).pack(side="left", padx=8, pady=20)

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
            messagebox.showerror("Error", "Solo se permiten números.")
            return
        
        # Validaciones dimensionales
        if tipo == "suma" and (len(a) != len(b) or len(a[0]) != len(b[0])):
            error_msg = "Error: Para A+B, A y B deben tener mismas dimensiones.\n"
            error_msg += f"A: {len(a)}×{len(a[0])}, B: {len(b)}×{len(b[0])}"
            self.mostrar_resultado_operaciones(a, b, error_msg, tipo)
            return
            
        if tipo == "multiplicacion" and len(a[0]) != len(b):
            error_msg = "Error: Para A·B, columnas(A) debe ser igual a filas(B).\n"
            error_msg += f"Columnas de A: {len(a[0])}, Filas de B: {len(b)}"
            self.mostrar_resultado_operaciones(a, b, error_msg, tipo)
            return
        
        res = calcular_operaciones_matrices(a, b, tipo)
        self.mostrar_resultado_operaciones(a, b, res, tipo)

    def mostrar_resultado_operaciones(self, a, b, resultado, tipo):
        self.clear_content()
        ttk.Label(self.content, text=f"Resultado — {'Suma' if tipo == 'suma' else 'Multiplicación'}", 
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))
        
        # MATRIZ A
        matriz_a_card = self.card()
        ttk.Label(matriz_a_card, text="Matriz A:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_a_str = matriz_a_string(a)
        tk.Label(matriz_a_card, text=matriz_a_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # MATRIZ B
        matriz_b_card = self.card()
        ttk.Label(matriz_b_card, text="Matriz B:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        matriz_b_str = matriz_a_string(b)
        tk.Label(matriz_b_card, text=matriz_b_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # RESULTADO
        resultado_card = self.card()
        ttk.Label(resultado_card, text=f"Resultado {'A + B' if tipo == 'suma' else 'A × B'}:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        if isinstance(resultado, str):
            # Si hay error
            tk.Label(resultado_card, text=resultado, bg="#333333", fg="#F44336",
                    font=("Consolas", 12, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)
        else:
            # Si es resultado válido
            resultado_str = matriz_a_string(resultado)
            tk.Label(resultado_card, text=resultado_str, bg="#333333", fg="#4CAF50",
                    font=("Consolas", 12, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # BOTONES
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)
        
        ttk.Button(self.content, text="Realizar otra operación", style="Primary.TButton",
                command=self.preparar_matrices_operaciones).pack(side="left", padx=8, pady=20)
        ttk.Button(self.content, text="Volver al Inicio", style="Danger.TButton",
                command=self.vista_menu).pack(side="left", padx=8, pady=20)

    # ------------------- Independencia Lineal -------------------
    def preparar_vectores_independencia(self):
        """Interfaz para verificar independencia lineal con entrada matricial."""
        self.clear_content()

        ttk.Label(
            self.content,
            text="Independencia Lineal",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(
            c,
            text="Dimensiones de la matriz de vectores (m x n)",
            style="CardTitle.TLabel"
        ).pack(anchor="center", pady=(10, 15))

        f = tk.Frame(c, bg=self.COLOR_CARD)
        f.pack(pady=15)

        tk.Label(f, text="Número de vectores (m):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT, 
                font=("Segoe UI", 13)).grid(row=0, column=0, padx=10)
        self.entrada_filas_indep = tk.Entry(f, width=10, font=("Segoe UI", 13),
                                        justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
                                        insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_filas_indep.grid(row=0, column=1, padx=10)

        tk.Label(f, text="Dimensión de vectores (n):", bg=self.COLOR_CARD, fg=self.COLOR_TEXT,
                font=("Segoe UI", 13)).grid(row=0, column=2, padx=10)
        self.entrada_columnas_indep = tk.Entry(f, width=10, font=("Segoe UI", 13),
                                            justify="center", bg="#3a3a3a", fg=self.COLOR_TEXT,
                                            insertbackground=self.COLOR_PRIMARY, relief="flat")
        self.entrada_columnas_indep.grid(row=0, column=3, padx=10)

        ttk.Button(
            c, text="Crear Matriz de Vectores", style="Primary.TButton",
            command=self.crear_interfaz_independencia
        ).pack(anchor="center", pady=(20, 10))
        
        
    def crear_interfaz_independencia(self):
        """Crea la interfaz para ingresar la matriz de vectores."""
        try:
            filas = int(self.entrada_filas_indep.get())  # Número de vectores
            columnas = int(self.entrada_columnas_indep.get())  # Dimensión de cada vector
            if filas <= 0 or columnas <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para filas y columnas.")
            return

        self.clear_content()
        ttk.Label(
            self.content,
            text=f"Ingrese los vectores (cada fila es un vector en R^{columnas})",
            style="H1.TLabel"
        ).pack(anchor="w", padx=22, pady=(18, 8))

        c = self.card()
        ttk.Label(c, text="Matriz de vectores (cada fila = un vector):", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 10))
        
        self.entradas_matriz_indep = self.grid_inputs(c, filas, columnas)

        a = self.card()
        ttk.Button(
            a, text="Verificar Independencia", style="Primary.TButton",
            command=self.resolver_independencia
        ).pack(side="left", padx=8)
        ttk.Button(
            a, text="Volver al Inicio", style="Danger.TButton",
            command=self.vista_menu
        ).pack(side="left", padx=8)
        
    def resolver_independencia(self):
        """Resuelve la independencia lineal con la matriz ingresada."""
        try:
            # Leer la matriz de vectores
            vectores = []
            for fila in self.entradas_matriz_indep:
                vector_fila = []
                for entrada in fila:
                    valor = entrada.get().strip()
                    if not valor:
                        messagebox.showerror("Error", "Todos los campos deben estar llenos.")
                        return
                    # Permitir fracciones
                    if "/" in valor:
                        try:
                            num, den = valor.split("/")
                            vector_fila.append(float(num) / float(den))
                        except:
                            raise ValueError(f"Fracción inválida: {valor}")
                    else:
                        vector_fila.append(float(valor))
                vectores.append(vector_fila)
        except ValueError as e:
            messagebox.showerror("Error", f"Dato inválido: {str(e)}\n\nUse números o fracciones como: 1, 2.5, 1/2, -3/4")
            return

        # Llamar a la lógica de independencia lineal
        resultado = verificar_independencia_lineal(vectores)

        # Mostrar resultados
        self.mostrar_resultado_independencia(vectores, resultado)
        
    def mostrar_resultado_independencia(self, vectores_originales, resultado):
        self.clear_content()
        ttk.Label(self.content, text="Resultado — Independencia Lineal",
                style="H1.TLabel").pack(anchor="w", padx=22, pady=(18, 8))

        # MATRIZ ORIGINAL
        matriz_card = self.card()
        ttk.Label(matriz_card, text="Matriz original de vectores:", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
        
        matriz_str = matriz_a_string(vectores_originales)
        tk.Label(matriz_card, text=matriz_str, bg="#333333", fg="#4FC3F7",
                font=("Consolas", 12), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # PROCESO
        if "pasos" in resultado and resultado["pasos"]:
            pasos_card = self.card()
            ttk.Label(pasos_card, text="Proceso de verificación:", 
                    style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))
            
            box = scrolledtext.ScrolledText(pasos_card, height=12, font=("Consolas", 11),
                                            bg="#2a2a2a", fg="#E0E0E0", bd=0, relief="flat")
            box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            for paso in resultado["pasos"]:
                if "Verificando independencia lineal" in paso:
                    box.insert(tk.END, f"{paso}\n", "naranja")
                elif "Matriz inicial" in paso:
                    box.insert(tk.END, f"{paso}\n", "importante")
                elif "Matriz en RREF" in paso:
                    box.insert(tk.END, f"{paso}\n", "importante")
                elif "Cantidad de pivotes" in paso:
                    box.insert(tk.END, f"{paso}\n", "naranja")
                elif "linealmente independientes" in paso.lower() or "linealmente dependientes" in paso.lower():
                    box.insert(tk.END, f"{paso}\n", "conclusion")
                else:
                    box.insert(tk.END, paso + "\n")
            
            box.tag_configure("naranja", foreground="#FF9800")
            box.tag_configure("importante", foreground="#4FC3F7")
            box.tag_configure("conclusion", foreground="#4CAF50")
            box.config(state="disabled")

        # SEPARADOR
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)

        # CONCLUSIÓN
        resumen_card = self.card()
        ttk.Label(resumen_card, text="Conclusión", 
                style="CardTitle.TLabel").pack(anchor="w", padx=15, pady=(5, 3))

        if resultado.get("independientes", False):
            mensaje = "Los vectores son LINEALMENTE INDEPENDIENTES\n\n"
            mensaje += f"Se encontraron {len(resultado.get('pivotes', []))} pivotes\n"
            mensaje += "Todos los vectores son base del espacio generado"
            color = "#4CAF50"
        else:
            mensaje = "Los vectores son LINEALMENTE DEPENDIENTES\n\n"
            mensaje += f"Se encontraron {len(resultado.get('pivotes', []))} pivotes\n"
            mensaje += f"Vectores dependientes: {resultado.get('dependientes', [])}\n"
            mensaje += f"Vectores pivote (independientes): {resultado.get('pivotes', [])}"
            color = "#F44336"
        
        tk.Label(resumen_card, text=mensaje, bg="#333333", fg=color,
                font=("Consolas", 12, "bold"), justify="left", anchor="w").pack(fill="x", padx=10, pady=5)

        # BOTONES
        tk.Frame(self.content, bg="#303030", height=1).pack(fill="x", padx=20, pady=10)
        
        ttk.Button(self.content, text="Analizar otros vectores", style="Primary.TButton",
            command=self.preparar_vectores_independencia
        ).pack(side="left", padx=8, pady=20)
        
        ttk.Button(self.content, text="Volver al Inicio", style="Danger.TButton",
            command=self.vista_menu
        ).pack(side="left", padx=8, pady=20)

# ================================================================
#                        EJECUCION PRINCIPAL
# ================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraApp(root)
    root.mainloop()