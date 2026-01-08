import customtkinter as ctk
from PIL import Image
import os
import threading
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

# =============================================================================
#  🎨 CONFIGURACIÓN Y ESTÉTICA MEJORADA
# =============================================================================
C_FONDO      = "#0A0E1A"  
C_SIDEBAR    = "#151923"  
C_CARD       = "#1A1F2E"  
C_ACENTO     = "#00D9FF"  
C_ACENTO_2   = "#7C3AED"
C_TEXTO      = "#F8FAFC"  
C_TEXTO_GRIS = "#94A3B8"  
C_ROJO_ERROR = "#F87171"
C_VERDE_OK   = "#34D399"
C_NUM        = "#1E293B"
C_VAR        = "#0EA5E9"
C_OP         = "#334155"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# =============================================================================
#  🧠 LÓGICA MATEMÁTICA
# =============================================================================
class CalculadoraIntegrales:
    def __init__(self):
        self.x, self.y, self.z = sp.symbols('x y z')
        self.r, self.theta = sp.symbols('r theta')
        self.rho, self.phi = sp.symbols('rho phi')
        
    def parsear_funcion(self, func_str):
        try:
            s = func_str.replace('^', '**').replace('sen', 'sin')
            transformations = (standard_transformations + (implicit_multiplication_application,))
            return parse_expr(s, transformations=transformations)
        except: return None

    def integral_doble(self, func_str, lim1, lim2, sistema="Cartesianas", pasos=30):
        expr = self.parsear_funcion(func_str)
        if expr is None: return "Error Sintaxis", 0, 0

        try:
            try:
                l1_num = [float(lim1[0]), float(lim1[1])]
                l2_num = [float(lim2[0]), float(lim2[1])]
                es_numerico = True
            except:
                es_numerico = False

            val_exacto = 0
            if sistema == "Cartesianas":
                val_exacto = sp.integrate(sp.integrate(expr, (self.y, lim2[0], lim2[1])), (self.x, lim1[0], lim1[1]))
            elif sistema == "Polares":
                val_exacto = sp.integrate(sp.integrate(expr * self.r, (self.r, lim2[0], lim2[1])), (self.theta, lim1[0], lim1[1]))
            
            try: val_exacto_float = float(val_exacto.evalf())
            except: val_exacto_float = str(val_exacto)

            val_num, err = "---", "---"
            
            if es_numerico and isinstance(val_exacto_float, float):
                if sistema == "Cartesianas":
                    f = sp.lambdify((self.x, self.y), expr, 'numpy')
                    x = np.linspace(l1_num[0], l1_num[1], pasos)
                    y = np.linspace(l2_num[0], l2_num[1], pasos)
                    dx, dy = x[1]-x[0], y[1]-y[0]
                    X, Y = np.meshgrid(x[:-1]+dx/2, y[:-1]+dy/2)
                    val_num = np.sum(f(X, Y)) * dx * dy
                elif sistema == "Polares":
                    f = sp.lambdify((self.r, self.theta), expr, 'numpy')
                    th = np.linspace(l1_num[0], l1_num[1], pasos)
                    r_vals = np.linspace(l2_num[0], l2_num[1], pasos)
                    dth, dr = th[1]-th[0], r_vals[1]-r_vals[0]
                    TH, R = np.meshgrid(th[:-1]+dth/2, r_vals[:-1]+dr/2)
                    val_num = np.sum(f(R, TH) * R) * dr * dth
                
                if abs(val_exacto_float) > 1e-9:
                    err = abs((val_exacto_float - val_num) / val_exacto_float) * 100
                else: err = 0.0

            return val_exacto_float, val_num, err

        except Exception as e: return str(e), 0, 0

    def integral_triple(self, func_str, l1, l2, l3, sistema="Cartesianas", pasos=15):
        expr = self.parsear_funcion(func_str)
        if expr is None: return "Error Sintaxis", 0, 0

        try:
            try:
                l1_n = [float(l1[0]), float(l1[1])]
                l2_n = [float(l2[0]), float(l2[1])]
                l3_n = [float(l3[0]), float(l3[1])]
                es_numerico = True
            except: es_numerico = False

            val_exacto = 0
            if sistema == "Cartesianas":
                v = sp.integrate(expr, (self.z, l3[0], l3[1]))
                v = sp.integrate(v, (self.y, l2[0], l2[1]))
                val_exacto = sp.integrate(v, (self.x, l1[0], l1[1]))
            elif sistema == "Cilíndricas":
                v = sp.integrate(expr * self.r, (self.z, l3[0], l3[1]))
                v = sp.integrate(v, (self.r, l2[0], l2[1]))
                val_exacto = sp.integrate(v, (self.theta, l1[0], l1[1]))
            elif sistema == "Esféricas":
                jacob = (self.rho**2) * sp.sin(self.phi)
                v = sp.integrate(expr * jacob, (self.rho, l3[0], l3[1]))
                v = sp.integrate(v, (self.phi, l2[0], l2[1]))
                val_exacto = sp.integrate(v, (self.theta, l1[0], l1[1]))

            try: val_exacto_float = float(val_exacto.evalf())
            except: val_exacto_float = str(val_exacto)

            val_num, err = "---", "---"

            if es_numerico and isinstance(val_exacto_float, float):
                if sistema == "Cartesianas":
                    f = sp.lambdify((self.x, self.y, self.z), expr, 'numpy')
                    x, y, z = np.linspace(l1_n[0], l1_n[1], pasos), np.linspace(l2_n[0], l2_n[1], pasos), np.linspace(l3_n[0], l3_n[1], pasos)
                    dx, dy, dz = x[1]-x[0], y[1]-y[0], z[1]-z[0]
                    X, Y, Z = np.meshgrid(x[:-1]+dx/2, y[:-1]+dy/2, z[:-1]+dz/2, indexing='ij')
                    val_num = np.sum(f(X, Y, Z)) * dx * dy * dz
                elif sistema == "Cilíndricas":
                    f = sp.lambdify((self.r, self.theta, self.z), expr, 'numpy')
                    th, r, z = np.linspace(l1_n[0], l1_n[1], pasos), np.linspace(l2_n[0], l2_n[1], pasos), np.linspace(l3_n[0], l3_n[1], pasos)
                    dth, dr, dz = th[1]-th[0], r[1]-r[0], z[1]-z[0]
                    TH, R, Z = np.meshgrid(th[:-1]+dth/2, r[:-1]+dr/2, z[:-1]+dz/2, indexing='ij')
                    val_num = np.sum(f(R, TH, Z) * R) * dth * dr * dz
                elif sistema == "Esféricas":
                    f = sp.lambdify((self.rho, self.phi, self.theta), expr, 'numpy')
                    th, phi, rho = np.linspace(l1_n[0], l1_n[1], pasos), np.linspace(l2_n[0], l2_n[1], pasos), np.linspace(l3_n[0], l3_n[1], pasos)
                    dth, dphi, drho = th[1]-th[0], phi[1]-phi[0], rho[1]-rho[0]
                    TH, PHI, RHO = np.meshgrid(th[:-1]+dth/2, phi[:-1]+dphi/2, rho[:-1]+drho/2, indexing='ij')
                    val_num = np.sum(f(RHO, PHI, TH) * (RHO**2) * np.sin(PHI)) * dth * dphi * drho
                
                if abs(val_exacto_float) > 1e-9:
                    err = abs((val_exacto_float - val_num) / val_exacto_float) * 100
                else: err = 0.0

            return val_exacto_float, val_num, err

        except Exception as e: return str(e), 0, 0

# =============================================================================
#  📱 INTERFAZ GRÁFICA (APP)
# =============================================================================
class App(ctk.CTk):
    
    def on_hover(self, btn, texto):
        btn.grid_configure(padx=12)
        if not self.sidebar_open:
            try:
                x = self.sidebar.winfo_width() + 10
                y = btn.winfo_rooty() - self.winfo_rooty() + 10
                self.tooltip.configure(text=texto)
                self.tooltip.place(x=x, y=y); self.tooltip.lift()
            except: pass

    def off_hover(self, btn):
        btn.grid_configure(padx=8); self.tooltip.place_forget()

    def __init__(self):
        super().__init__()
        self.title("VectorCalc Pro 2026 ✨")
        self.geometry("1300x850")
        self.configure(fg_color=C_FONDO)

        self.motor_mate = CalculadoraIntegrales()
        self.entry_foco = None 
        self.sidebar_open = False
        self.sidebar_width = 70
        self.sidebar_max = 220
        self.animando = False 

        self.cargar_recursos()

        self.f_hero = ctk.CTkFont(family="Segoe UI", size=36, weight="bold")
        self.f_title = ctk.CTkFont(family="Segoe UI", size=22, weight="bold")
        self.f_subtitle = ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        self.f_text = ctk.CTkFont(family="Segoe UI", size=14)
        self.f_text2 = ctk.CTkFont(family="Segoe UI", size=13)
        self.f_code = ctk.CTkFont(family="Consolas", size=18)
        
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)

        # SIDEBAR con gradiente simulado
        self.sidebar = ctk.CTkFrame(self, width=self.sidebar_width, corner_radius=0, fg_color=C_SIDEBAR)
        self.sidebar.grid(row=0, column=0, sticky="nsew"); self.sidebar.grid_propagate(False)
        self.sidebar.grid_columnconfigure(0, weight=1); self.sidebar.grid_rowconfigure(1, weight=1)

        self.btn_menu = ctk.CTkButton(self.sidebar, text="", image=self.img_menu, width=45, height=45, 
                                      fg_color="transparent", hover_color="#1E293B", command=self.animar_sidebar, corner_radius=12)
        self.btn_menu.grid(row=0, column=0, pady=(25, 20))

        self.menu_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_container.grid(row=1, column=0, sticky="nsew")
        self.menu_container.grid_columnconfigure(0, weight=1); self.menu_container.grid_rowconfigure(4, weight=1) 

        self.btn_home = self.crear_btn_menu(self.menu_container, "Inicio", self.img_home, self.ir_home)
        self.btn_home.grid(row=0, column=0, sticky="ew", pady=6, padx=8)
        self.btn_calc = self.crear_btn_menu(self.menu_container, "Calculadora", self.img_calc, self.ir_calc)
        self.btn_calc.grid(row=1, column=0, sticky="ew", pady=6, padx=8)
        self.btn_graf = self.crear_btn_menu(self.menu_container, "Graficadora", self.img_graf, self.ir_graf)
        self.btn_graf.grid(row=2, column=0, sticky="ew", pady=6, padx=8)
        self.btn_about = self.crear_btn_menu(self.menu_container, "Nosotros", self.img_about, self.ir_about)
        self.btn_about.grid(row=5, column=0, sticky="ew", pady=(6, 25), padx=8)

        self.botones = [self.btn_home, self.btn_calc, self.btn_graf, self.btn_about]
        self.indicador = ctk.CTkFrame(self.menu_container, width=4, height=48, fg_color=C_ACENTO, corner_radius=2)
        self.tooltip = ctk.CTkLabel(self, text="", fg_color="#0F172A", text_color=C_TEXTO, corner_radius=10, padx=12, pady=8, font=self.f_text2)

        # ÁREA DE CONTENIDO
        self.main_area = ctk.CTkFrame(self, fg_color=C_FONDO, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1); self.main_area.grid_rowconfigure(0, weight=1)

        self.frames = {} 
        for name in ["home", "calc", "graf", "about"]:
            self.frames[name] = ctk.CTkFrame(self.main_area, fg_color=C_FONDO, corner_radius=0)

        self.setup_home(); self.setup_calc(); self.setup_graf(); self.setup_about(); self.ir_home()

    def cargar_recursos(self):
        path = os.path.dirname(os.path.realpath(__file__))
        def get_img(name):
            try: return ctk.CTkImage(Image.open(os.path.join(path, name)), size=(24, 24))
            except: return None
        self.img_menu = get_img("menu_icon.png"); self.img_home = get_img("home_icon.png")
        self.img_calc = get_img("calc_icon.png"); self.img_graf = get_img("graph_icon.png"); self.img_about = get_img("about_icon.png")

    def animar_sidebar(self):
        if self.animando: return
        if self.sidebar_open: self.cerrar_sidebar()
        else: self.abrir_sidebar()
    def abrir_sidebar(self):
        self.animando = True; step = 30
        if self.sidebar_width < self.sidebar_max:
            self.sidebar_width += step; self.sidebar.configure(width=self.sidebar_width); self.after(8, self.abrir_sidebar)
        else: self.sidebar_open = True; self.animando = False; self.mostrar_textos(True)
    def cerrar_sidebar(self):
        if self.sidebar_open: self.mostrar_textos(False); self.sidebar_open = False
        self.animando = True; step = 30
        if self.sidebar_width > 70:
            self.sidebar_width -= step; self.sidebar.configure(width=self.sidebar_width); self.after(8, self.cerrar_sidebar)
        else: self.animando = False
    def mostrar_textos(self, m):
        txts = ["   Inicio", "   Calculadora", "   Graficadora", "   Nosotros"]
        for b, t in zip(self.botones, txts): b.configure(text=t if m else "", anchor="w" if m else "center", compound="left" if m else "none")
    def crear_btn_menu(self, p, t, i, c):
        b = ctk.CTkButton(p, text="", image=i, command=c, fg_color="transparent", text_color=C_TEXTO_GRIS, hover_color="#1E293B", font=self.f_text, height=48, corner_radius=12, anchor="center", compound="left")
        b.bind("<Enter>", lambda e, b=b, t=t: self.on_hover(b, t)); b.bind("<Leave>", lambda e, b=b: self.off_hover(b)); return b
    def activar_boton(self, ba):
        for b in self.botones: b.configure(fg_color="transparent", text_color=C_TEXTO_GRIS)
        if ba: ba.configure(fg_color="#1E293B", text_color=C_ACENTO); self.after(10, lambda: [self.indicador.place(x=0, y=ba.winfo_y()+2), self.indicador.lift()])
    def switch_frame(self, n, b):
        for f in self.frames.values(): f.grid_forget()
        self.frames[n].grid(row=0, column=0, sticky="nsew", padx=0, pady=0); self.activar_boton(b)
    def ir_home(self): self.switch_frame("home", self.btn_home)
    def ir_calc(self): self.switch_frame("calc", self.btn_calc)
    def ir_graf(self): self.switch_frame("graf", self.btn_graf)
    def ir_about(self): self.switch_frame("about", self.btn_about)

    # TECLADO
    def set_foco(self, w): self.entry_foco = w
    def write(self, t): self.agregar_caracter(t)
    def write_z(self):
        try: self.write("rho" if self.seg_modo.get()=="Integral Triple" and self.combo_sis.get()=="Esféricas" else "z")
        except: self.write("z")
    def write_angle(self):
        try: self.write("phi" if self.seg_modo.get()=="Integral Triple" and self.combo_sis.get()=="Esféricas" else "theta")
        except: self.write("theta")
    def agregar_caracter(self, c):
        tgt = self.entry_foco if self.entry_foco else self.entry_funcion
        try: tgt.insert(tgt.index("insert"), c)
        except: pass
        if tgt == self.entry_funcion: self.actualizar_renderizado()
    def borrar_caracter(self):
        tgt = self.entry_foco if self.entry_foco else self.entry_funcion
        try: 
            if (idx:=tgt.index("insert")) > 0: tgt.delete(idx-1, idx)
        except: pass
        if tgt == self.entry_funcion: self.actualizar_renderizado()
    def limpiar_todo(self): self.entry_funcion.delete(0, "end"); self.actualizar_renderizado()
    def crear_btn_teclado(self, p, t, c, cmd, x, y):
        btn = ctk.CTkButton(p, text=t, fg_color=c, hover_color=self.hover_color(c), width=55, height=55, font=ctk.CTkFont(family="Segoe UI", size=17, weight="bold"), command=cmd, corner_radius=12)
        btn.grid(row=y, column=x, padx=5, pady=5, sticky="nsew")
    
    def hover_color(self, base):
        hover_map = {C_NUM: "#2D3748", C_VAR: "#0284C7", C_OP: "#475569"}
        return hover_map.get(base, "#334155")

    # VISOR
    def actualizar_renderizado(self, e=None):
        txt = self.entry_funcion.get()
        self.ax_math.clear(); self.ax_math.axis("off")
        color, latex = "white", ""
        if not txt: latex, color = r"\text{\textbf{Escribe tu función...}}", "#64748B"
        else:
            try:
                cl = txt.replace("^", "**").replace("sen", "sin")
                tr = (standard_transformations + (implicit_multiplication_application,))
                ex = parse_expr(cl, transformations=tr, evaluate=False)
                latex = f"${sp.latex(ex)}$"
            except: latex, color = r"\text{" + txt + "}", C_ROJO_ERROR
        self.ax_math.text(0.5, 0.5, latex, fontsize=26, ha='center', va='center', color=color)
        self.canvas_math.draw()

    # PANTALLA CALCULADORA
    def setup_calc(self):
        f = self.frames["calc"]; f.grid_columnconfigure(0, weight=1)
        
        # Header mejorado
        h = ctk.CTkFrame(f, fg_color="transparent"); h.pack(fill="x", padx=35, pady=(20, 15))
        titulo_frame = ctk.CTkFrame(h, fg_color="transparent")
        titulo_frame.pack(side="left")
        ctk.CTkLabel(titulo_frame, text="⚡ Calculadora Vectorial", font=self.f_hero, text_color=C_ACENTO).pack(anchor="w")
        ctk.CTkLabel(titulo_frame, text="Cálculo de integrales múltiples en tiempo real", font=self.f_text2, text_color=C_TEXTO_GRIS).pack(anchor="w", pady=(2,0))
        
        self.seg_modo = ctk.CTkSegmentedButton(h, values=["Integral Doble", "Integral Triple"], command=self.cambiar_modo, 
                                                font=("Segoe UI",14,"bold"), selected_color=C_ACENTO, selected_hover_color="#00B8D4", 
                                                unselected_color="#1E293B", unselected_hover_color="#334155")
        self.seg_modo.set("Integral Doble"); self.seg_modo.pack(side="right", padx=10)

        # Visor mejorado
        vis = ctk.CTkFrame(f, fg_color=C_CARD, corner_radius=18, border_width=2, border_color="#334155"); vis.pack(fill="x", padx=35, pady=8)
        iv = ctk.CTkFrame(vis, fg_color="transparent"); iv.pack(fill="both", expand=True, padx=15, pady=15)
        self.frame_limites = ctk.CTkFrame(iv, fg_color="transparent"); self.frame_limites.pack(side="left", padx=8)

        self.fig_math = plt.figure(figsize=(5.5, 1.6), dpi=100, facecolor=C_CARD)
        self.ax_math = self.fig_math.add_subplot(111); self.ax_math.axis("off")
        self.canvas_math = FigureCanvasTkAgg(self.fig_math, master=iv)
        self.canvas_math.get_tk_widget().pack(side="left", fill="both", expand=True, padx=12)
        self.canvas_math.get_tk_widget().configure(background=C_CARD)
        self.lbl_diff = ctk.CTkLabel(iv, text="dy dx", font=("Times New Roman", 24, "italic"), text_color=C_ACENTO); self.lbl_diff.pack(side="right", padx=12)

        # Barra de edición mejorada
        bi = ctk.CTkFrame(f, fg_color="transparent"); bi.pack(fill="x", padx=40, pady=8)
        ctk.CTkLabel(bi, text="✏️ Editar función:", font=("Segoe UI", 13, "bold"), text_color=C_TEXTO_GRIS).pack(side="left", padx=(0,8))
        self.entry_funcion = ctk.CTkEntry(bi, placeholder_text="Ejemplo: x^2 + y*sin(x)", font=("Consolas", 18), height=50, 
                                        fg_color=C_CARD, text_color=C_TEXTO, border_width=2, border_color=C_ACENTO, corner_radius=12)
        self.entry_funcion.pack(side="left", fill="x", expand=True, padx=8)
        for ev in ["<KeyRelease>", "<FocusIn>", "<Button-1>"]: self.entry_funcion.bind(ev, lambda e: [self.set_foco(self.entry_funcion), self.actualizar_renderizado()])
        self.entry_foco = self.entry_funcion 

        # Contenedor inferior
        bot = ctk.CTkFrame(f, fg_color="transparent"); bot.pack(fill="both", expand=True, padx=35, pady=12)
        bot.grid_columnconfigure(0, weight=3); bot.grid_columnconfigure(1, weight=1)

        # Teclado mejorado
        tec = ctk.CTkFrame(bot, fg_color=C_CARD, corner_radius=18, border_width=2, border_color="#334155"); 
        tec.grid(row=0, column=0, sticky="nsew", padx=(0, 20), pady=0)
        tec_inner = ctk.CTkFrame(tec, fg_color="transparent")
        tec_inner.pack(fill="both", expand=True, padx=12, pady=12)
        
        for i in range(6): tec_inner.grid_columnconfigure(i, weight=1)
        for i in range(5): tec_inner.grid_rowconfigure(i, weight=1)
        
        btns = [
            ["x", C_VAR, lambda: self.write("x"), 0,0], ["sin", C_OP, lambda: self.write("sin("), 1,0], ["7", C_NUM, lambda: self.write("7"), 2,0], ["8", C_NUM, lambda: self.write("8"), 3,0], ["9", C_NUM, lambda: self.write("9"), 4,0], ["/", C_OP, lambda: self.write("/"), 5,0],
            ["y", C_VAR, lambda: self.write("y"), 0,1], ["cos", C_OP, lambda: self.write("cos("), 1,1], ["4", C_NUM, lambda: self.write("4"), 2,1], ["5", C_NUM, lambda: self.write("5"), 3,1], ["6", C_NUM, lambda: self.write("6"), 4,1], ["*", C_OP, lambda: self.write("*"), 5,1],
            ["z/ρ", C_VAR, lambda: self.write_z(), 0,2], ["tan", C_OP, lambda: self.write("tan("), 1,2], ["1", C_NUM, lambda: self.write("1"), 2,2], ["2", C_NUM, lambda: self.write("2"), 3,2], ["3", C_NUM, lambda: self.write("3"), 4,2], ["-", C_OP, lambda: self.write("-"), 5,2],
            ["θ/φ", C_VAR, lambda: self.write_angle(), 0,3], ["√", C_OP, lambda: self.write("sqrt("), 1,3], ["0", C_NUM, lambda: self.write("0"), 2,3], [".", C_NUM, lambda: self.write("."), 3,3], ["(", C_OP, lambda: self.write("("), 4,3], ["+", C_OP, lambda: self.write("+"), 5,3],
            ["π", C_VAR, lambda: self.write("pi"), 0,4], ["e", C_VAR, lambda: self.write("E"), 1,4], ["^", C_OP, lambda: self.write("^"), 2,4], ["⌫", "#DC2626", lambda: self.borrar_caracter(), 5,4], [")", C_OP, lambda: self.write(")"), 4,4] 
        ]
        for b in btns: self.crear_btn_teclado(tec_inner, b[0], b[1], b[2], b[3], b[4])

        # Panel lateral mejorado
        pan = ctk.CTkFrame(bot, fg_color=C_CARD, corner_radius=18, border_width=2, border_color="#334155"); 
        pan.grid(row=0, column=1, sticky="nsew")
        pan_inner = ctk.CTkFrame(pan, fg_color="transparent")
        pan_inner.pack(fill="both", expand=True, padx=18, pady=18)
        
        ctk.CTkLabel(pan_inner, text="🌐 Sistema de Coordenadas", font=self.f_subtitle, text_color=C_TEXTO).pack(anchor="w", pady=(0,8))
        self.combo_sis = ctk.CTkComboBox(pan_inner, values=["Cartesianas", "Polares"], command=self.act_diff, 
                                         fg_color="#0F172A", button_color=C_ACENTO, button_hover_color="#00B8D4", 
                                         border_color=C_ACENTO, dropdown_fg_color="#1E293B", font=self.f_text)
        self.combo_sis.pack(pady=(0, 18), fill="x")

        # Card de resultados mejorado
        self.card_res = ctk.CTkFrame(pan_inner, fg_color="#0F172A", corner_radius=15, border_width=2, border_color=C_ACENTO); 
        self.card_res.pack(fill="x", pady=8)
        ctk.CTkLabel(self.card_res, text="📊 Resultados", font=self.f_subtitle, text_color=C_ACENTO).pack(pady=(12, 8))
        self.lbl_res_num = ctk.CTkLabel(self.card_res, text="---", font=("Segoe UI", 32, "bold"), text_color=C_ACENTO); 
        self.lbl_res_num.pack(pady=(5, 3))
        self.lbl_res_exact = ctk.CTkLabel(self.card_res, text="Exacto: ---", font=self.f_text2, text_color=C_VERDE_OK); 
        self.lbl_res_exact.pack(pady=2)
        self.lbl_error = ctk.CTkLabel(self.card_res, text="Error: ---", font=self.f_text2, text_color=C_ROJO_ERROR); 
        self.lbl_error.pack(pady=(2, 12))

        # Botones de acción mejorados
        self.btn_calc_big = ctk.CTkButton(pan_inner, text="🚀 CALCULAR", font=("Segoe UI", 18, "bold"), 
                                          fg_color=C_ACENTO, hover_color="#00B8D4", height=65, corner_radius=15, command=self.ejecutar)
        self.btn_calc_big.pack(side="bottom", fill="x", pady=(10, 0))
        ctk.CTkButton(pan_inner, text="🗑️ Limpiar Todo", fg_color="#334155", hover_color="#475569", height=40, 
                             corner_radius=12, command=self.limpiar_todo).pack(side="bottom", fill="x", pady=(0, 8))
        
        self.renderizar_limites(True); self.actualizar_renderizado()

    def renderizar_limites(self, doble=True):
        for w in self.frame_limites.winfo_children(): w.destroy()
        def set(w): self.entry_foco = w
        def add(p):
            f = ctk.CTkFrame(p, fg_color="transparent"); f.pack(side="left", padx=3)
            eb = ctk.CTkEntry(f, width=50, height=35, justify="center", fg_color="#0F172A", border_color=C_ACENTO, 
                            border_width=2, corner_radius=8, font=self.f_text)
            eb.pack(pady=3); eb.bind("<FocusIn>", lambda e: set(eb)); eb.bind("<Button-1>", lambda e: set(eb))
            ctk.CTkLabel(f, text="∫", font=("Times New Roman", 48), text_color=C_ACENTO).pack(pady=0)
            ea = ctk.CTkEntry(f, width=50, height=35, justify="center", fg_color="#0F172A", border_color=C_ACENTO, 
                            border_width=2, corner_radius=8, font=self.f_text)
            ea.pack(pady=3); ea.bind("<FocusIn>", lambda e: set(ea)); ea.bind("<Button-1>", lambda e: set(ea))
            return ea, eb
        self.inputs = []; self.inputs.extend(add(self.frame_limites)); self.inputs.extend(add(self.frame_limites))
        if not doble: self.inputs.extend(add(self.frame_limites))

    def cambiar_modo(self, v):
        doble = (v == "Integral Doble")
        self.combo_sis.configure(values=["Cartesianas", "Polares"] if doble else ["Cartesianas", "Cilíndricas", "Esféricas"])
        self.combo_sis.set("Cartesianas"); self.renderizar_limites(doble); self.act_diff(None)

    def act_diff(self, _):
        m, s = self.seg_modo.get(), self.combo_sis.get()
        txt = "dy dx" if m=="Integral Doble" and s=="Cartesianas" else "r dr dθ"
        if m=="Integral Triple": txt = "dz dy dx" if s=="Cartesianas" else ("r dz dr dθ" if s=="Cilíndricas" else "ρ²sen(φ) dρ dφ dθ")
        self.lbl_diff.configure(text=txt)

    def ejecutar(self):
        m, s, f = self.seg_modo.get(), self.combo_sis.get(), self.entry_funcion.get()
        try:
            vals = []
            for c in self.inputs:
                t = c.get()
                vals.append(sp.sympify(t) if t else sp.Integer(0))
            l1, l2 = [vals[0], vals[1]], [vals[2], vals[3]]
            l3 = [vals[4], vals[5]] if len(vals)>4 else None
        except: self.lbl_res_num.configure(text="Error Lím"); return

        self.lbl_res_num.configure(text="⏳"); self.btn_calc_big.configure(state="disabled"); self.update()
        def tarea():
            try:
                if m == "Integral Doble": res = self.motor_mate.integral_doble(f, l1, l2, s)
                else: res = self.motor_mate.integral_triple(f, l1, l2, l3, s)
                ex, num, err = res
                def show():
                    if isinstance(ex, str) and not isinstance(num, (int, float)):
                        self.lbl_res_num.configure(text="⚠️ Error"); self.lbl_res_exact.configure(text=str(ex)[:25])
                    else:
                        if isinstance(num, str): self.lbl_res_num.configure(text="---")
                        else: self.lbl_res_num.configure(text=f"{num:.5f}")
                        
                        val_ex_str = f"{ex:.5f}" if isinstance(ex, float) else "Simbólico"
                        self.lbl_res_exact.configure(text=f"✓ Exacto: {val_ex_str}")
                        
                        err_str = f"{err:.4f}%" if isinstance(err, float) else "---"
                        self.lbl_error.configure(text=f"📉 Error: {err_str}")

                    self.btn_calc_big.configure(state="normal")
                self.after(0, show)
            except Exception as e: self.after(0, lambda: [self.lbl_res_num.configure(text="❌ Fallo"), self.btn_calc_big.configure(state="normal")])
        threading.Thread(target=tarea, daemon=True).start()

    # PANTALLA HOME
    def setup_home(self):
        f = self.frames["home"]; f.grid_columnconfigure(0, weight=1); f.grid_rowconfigure(0, weight=1)
        
        # Scrollable frame para manejar contenido largo
        scroll_frame = ctk.CTkScrollableFrame(f, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # --- CORRECCIÓN HEADER (GRID + CARGA DE IMÁGENES) ---
        header = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header.pack(fill="x", pady=(10, 20))
        
        # Configurar Grid para centrado perfecto: Col 0 (Izq), Col 1 (Centro), Col 2 (Der)
        header.grid_columnconfigure(0, weight=1)
        header.grid_columnconfigure(1, weight=1)
        header.grid_columnconfigure(2, weight=1)

        # Ruta actual para cargar imágenes de forma segura
        current_path = os.path.dirname(os.path.realpath(__file__))
        
        # Escudo ESCOM (Columna 0, Alineado a la derecha de su celda)
        try:
            image_path = os.path.join(current_path, "escudo_escom.png")
            # IMPORTANTE: Asignar a self.img_escom para evitar que Python borre la imagen
            self.img_escom = ctk.CTkImage(Image.open(image_path), size=(100, 100))
            ctk.CTkLabel(header, image=self.img_escom, text="").grid(row=0, column=0, padx=20, sticky="e")
        except: 
            ctk.CTkLabel(header, text="🎓", font=ctk.CTkFont(size=80)).grid(row=0, column=0, padx=20, sticky="e")
        
        # Info central (Columna 1, Centrado)
        centro = ctk.CTkFrame(header, fg_color="transparent")
        centro.grid(row=0, column=1) # Sin sticky para que quede flotando en el centro exacto
        
        ctk.CTkLabel(centro, text="Instituto Politécnico Nacional", 
                    font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"), 
                    text_color=C_TEXTO).pack()
        ctk.CTkLabel(centro, text="Escuela Superior de Cómputo", 
                    font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), 
                    text_color=C_ACENTO).pack(pady=2)
        ctk.CTkLabel(centro, text="Ingeniería en Sistemas Computacionales", 
                    font=ctk.CTkFont(family="Segoe UI", size=13), 
                    text_color=C_TEXTO_GRIS).pack()
        
        # Escudo IPN (Columna 2, Alineado a la izquierda de su celda)
        try:
            image_path = os.path.join(current_path, "escudo_ipn.png")
            # IMPORTANTE: Asignar a self.img_ipn
            self.img_ipn = ctk.CTkImage(Image.open(image_path), size=(100, 100))
            ctk.CTkLabel(header, image=self.img_ipn, text="").grid(row=0, column=2, padx=20, sticky="w")
        except:
            ctk.CTkLabel(header, text="🏛️", font=ctk.CTkFont(size=80)).grid(row=0, column=2, padx=20, sticky="w")
        
        # --- FIN CORRECCIÓN HEADER ---

        # Separador con gradiente simulado
        sep1 = ctk.CTkFrame(scroll_frame, height=3, fg_color=C_ACENTO, corner_radius=2)
        sep1.pack(fill="x", padx=100, pady=15)
        
        # Título principal del proyecto
        titulo_proyecto = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        titulo_proyecto.pack(pady=(20, 10))
        
        ctk.CTkLabel(titulo_proyecto, text="⚡ CALCULADORA", 
                    font=ctk.CTkFont(family="Segoe UI", size=56, weight="bold"), 
                    text_color=C_ACENTO).pack(side="left")
        ctk.CTkLabel(titulo_proyecto, text="DE", 
                    font=ctk.CTkFont(family="Segoe UI", size=56, weight="bold"), 
                    text_color=C_ACENTO_2).pack(side="left", padx=(10,0))
        ctk.CTkLabel(titulo_proyecto, text="INTEGRALES", 
                    font=ctk.CTkFont(family="Segoe UI", size=56, weight="bold"), 
                    text_color="#F59E0B").pack(side="left", padx=(10,0))
        
        ctk.CTkLabel(scroll_frame, text="Calculadora Avanzada de Integrales Múltiples", 
                    font=ctk.CTkFont(family="Segoe UI", size=18), 
                    text_color=C_TEXTO_GRIS).pack(pady=(0, 10))
        
        ctk.CTkLabel(scroll_frame, text="Aproximación Numérica vs Solución Exacta", 
                    font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                    text_color=C_VERDE_OK).pack(pady=(0, 30))
        
        # Botón principal animado
        btn_inicio = ctk.CTkButton(scroll_frame, text="🚀 Iniciar Calculadora →", height=65, width=300, 
                                  font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"), 
                                  fg_color=C_ACENTO, hover_color="#00B8D4", corner_radius=16, 
                                  command=self.ir_calc, border_width=2, border_color=C_ACENTO_2)
        btn_inicio.pack(pady=20)
        
        # Features en cards
        features_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        features_container.pack(pady=30, padx=50, fill="x")
        
        features_data = [
            ("📊", "Integrales Dobles", "∬ f(x,y) dA", "Cartesianas y Polares"),
            ("📐", "Integrales Triples", "∭ f(x,y,z) dV", "Cartesianas, Cilíndricas y Esféricas"),
            ("🎨", "Visualización 3D", "Gráficos Interactivos", "Superficie, Contorno y Vectorial"),
            ("⚡", "Cálculo Exacto", "Con SymPy", "Solución simbólica matemática"),
            ("🔢", "Aproximación Numérica", "Sumas de Riemann", "Comparación con error relativo"),
            ("🎯", "Análisis de Error", "Precisión vs Exacto", "Evaluación de convergencia")
        ]
        
        for i in range(0, len(features_data), 3):
            row = ctk.CTkFrame(features_container, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            for j in range(3):
                if i+j < len(features_data):
                    emoji, titulo, subtitulo, desc = features_data[i+j]
                    
                    card = ctk.CTkFrame(row, fg_color=C_CARD, corner_radius=15, 
                                       border_width=2, border_color="#334155")
                    card.pack(side="left", expand=True, fill="both", padx=8)
                    
                    ctk.CTkLabel(card, text=emoji, font=ctk.CTkFont(size=40)).pack(pady=(15, 5))
                    ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                                text_color=C_ACENTO).pack(pady=2)
                    ctk.CTkLabel(card, text=subtitulo, font=ctk.CTkFont(family="Consolas", size=11), 
                                text_color=C_TEXTO_GRIS).pack(pady=2)
                    ctk.CTkLabel(card, text=desc, font=ctk.CTkFont(size=10), 
                                text_color=C_TEXTO_GRIS).pack(pady=(2, 15))
        
        # Separador
        sep2 = ctk.CTkFrame(scroll_frame, height=2, fg_color="#334155", corner_radius=2)
        sep2.pack(fill="x", padx=100, pady=25)
        
        # Equipo de desarrollo
        equipo_frame = ctk.CTkFrame(scroll_frame, fg_color=C_CARD, corner_radius=18, 
                                   border_width=2, border_color=C_ACENTO)
        equipo_frame.pack(padx=50, pady=20, fill="x")
        
        ctk.CTkLabel(equipo_frame, text="👥 Equipo de Desarrollo", 
                    font=ctk.CTkFont(family="Segoe UI", size=24, weight="bold"), 
                    text_color=C_ACENTO).pack(pady=(20, 15))
        
        integrantes = [
            "Bonilla Hernández Ximena Sofía",
            "Castillo Vidal Carmen Andrea", 
            "Cruz Rodríguez Bruno Aarón"
        ]
        
        for nombre in integrantes:
            nombre_frame = ctk.CTkFrame(equipo_frame, fg_color="#0F172A", corner_radius=10)
            nombre_frame.pack(pady=5, padx=30, fill="x")
            ctk.CTkLabel(nombre_frame, text=f"✨ {nombre}", 
                        font=ctk.CTkFont(family="Segoe UI", size=14), 
                        text_color=C_TEXTO).pack(pady=12, padx=20)
        
        # Info del curso
        ctk.CTkLabel(equipo_frame, text="Proyecto Terminal - Análisis Vectorial 26-1", 
                    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
                    text_color=C_ACENTO_2).pack(pady=(15, 5))
        ctk.CTkLabel(equipo_frame, text="Dr. David Correa Coyac", 
                    font=ctk.CTkFont(family="Segoe UI", size=13), 
                    text_color=C_VERDE_OK).pack(pady=2)
        ctk.CTkLabel(equipo_frame, text="Profesor de la asignatura", 
                    font=ctk.CTkFont(family="Segoe UI", size=11), 
                    text_color=C_TEXTO_GRIS).pack(pady=(0, 20))
        
        # Footer
        footer = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        footer.pack(pady=30)
        
        ctk.CTkLabel(footer, text="🔬 Desarrollado con Python, SymPy, NumPy y Matplotlib", 
                    font=ctk.CTkFont(size=11), text_color=C_TEXTO_GRIS).pack()
        ctk.CTkLabel(footer, text="2026 © ESCOM - IPN", 
                    font=ctk.CTkFont(size=10, weight="bold"), text_color=C_ACENTO).pack(pady=5)
        ctk.CTkLabel(footer, text="Hecho con <3 para el análisis matemático avanzado", 
                    font=ctk.CTkFont(size=11), text_color=C_TEXTO_GRIS).pack(pady=3)


    # PANTALLA GRAFICADORA
    def setup_graf(self):
        f = self.frames["graf"]; f.grid_columnconfigure(0, weight=1); f.grid_rowconfigure(1, weight=1)
        
        # Header
        h = ctk.CTkFrame(f, fg_color="transparent"); h.pack(fill="x", padx=35, pady=(20, 15))
        titulo_frame = ctk.CTkFrame(h, fg_color="transparent")
        titulo_frame.pack(side="left")
        ctk.CTkLabel(titulo_frame, text="📊 Graficadora 3D", font=self.f_hero, text_color=C_ACENTO).pack(anchor="w")
        ctk.CTkLabel(titulo_frame, text="Visualización de funciones en tres dimensiones", 
                    font=self.f_text2, text_color=C_TEXTO_GRIS).pack(anchor="w", pady=(2,0))
        
        # Controles
        controles = ctk.CTkFrame(f, fg_color=C_CARD, corner_radius=18, border_width=2, border_color="#334155")
        controles.pack(fill="x", padx=35, pady=(0, 15))
        ctrl_inner = ctk.CTkFrame(controles, fg_color="transparent")
        ctrl_inner.pack(fill="x", padx=20, pady=15)
        
        # Tipo de gráfico
        ctk.CTkLabel(ctrl_inner, text="Tipo de Gráfico:", font=self.f_subtitle, text_color=C_TEXTO).pack(anchor="w", pady=(0,5))
        self.tipo_grafico = ctk.CTkSegmentedButton(ctrl_inner, values=["Superficie", "Contorno", "Vectorial"], 
                                                 font=("Segoe UI",13,"bold"), selected_color=C_ACENTO)
        self.tipo_grafico.set("Superficie")
        self.tipo_grafico.pack(fill="x", pady=(0, 12))
        
        # Entrada de función para graficar
        func_frame = ctk.CTkFrame(ctrl_inner, fg_color="transparent")
        func_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(func_frame, text="Función z = f(x,y):", font=self.f_text, text_color=C_TEXTO_GRIS).pack(side="left", padx=(0, 10))
        self.entry_graf = ctk.CTkEntry(func_frame, placeholder_text="Ej: sin(sqrt(x^2 + y^2))", 
                                     font=("Consolas", 16), height=45, fg_color="#0F172A", 
                                     border_width=2, border_color=C_ACENTO, corner_radius=12)
        self.entry_graf.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry_graf.insert(0, "sin(sqrt(x^2 + y^2))")
        
        ctk.CTkButton(func_frame, text="🎨 Graficar", font=("Segoe UI", 14, "bold"), 
                      fg_color=C_ACENTO, hover_color="#00B8D4", height=45, width=120, 
                      corner_radius=12, command=self.graficar_3d).pack(side="right")
        
        # Rangos
        rango_frame = ctk.CTkFrame(ctrl_inner, fg_color="transparent")
        rango_frame.pack(fill="x")
        
        for i, var in enumerate(['x', 'y']):
            col_frame = ctk.CTkFrame(rango_frame, fg_color="transparent")
            col_frame.pack(side="left", expand=True, fill="x", padx=(0, 10 if i==0 else 0))
            ctk.CTkLabel(col_frame, text=f"Rango {var}:", font=self.f_text2, text_color=C_TEXTO_GRIS).pack(anchor="w")
            ent_frame = ctk.CTkFrame(col_frame, fg_color="transparent")
            ent_frame.pack(fill="x", pady=5)
            
            min_e = ctk.CTkEntry(ent_frame, width=80, height=35, justify="center", 
                               fg_color="#0F172A", border_color=C_ACENTO, placeholder_text="Min")
            min_e.pack(side="left", padx=(0, 5))
            min_e.insert(0, "-5")
            
            ctk.CTkLabel(ent_frame, text="a", text_color=C_TEXTO_GRIS).pack(side="left", padx=5)
            
            max_e = ctk.CTkEntry(ent_frame, width=80, height=35, justify="center", 
                               fg_color="#0F172A", border_color=C_ACENTO, placeholder_text="Max")
            max_e.pack(side="left", padx=(5, 0))
            max_e.insert(0, "5")
            
            if i == 0:
                self.x_min, self.x_max = min_e, max_e
            else:
                self.y_min, self.y_max = min_e, max_e
        
        # Canvas para gráfico
        self.graf_container = ctk.CTkFrame(f, fg_color=C_CARD, corner_radius=18, border_width=2, border_color="#334155")
        self.graf_container.pack(fill="both", expand=True, padx=35, pady=(0, 20))
        
        self.fig_3d = plt.figure(figsize=(10, 7), facecolor=C_CARD)
        self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
        self.ax_3d.set_facecolor(C_CARD)
        
        self.barra_color = None
        self.canvas_3d = FigureCanvasTkAgg(self.fig_3d, master=self.graf_container)
        self.canvas_3d.get_tk_widget().pack(fill="both", expand=True, padx=15, pady=15)
        
        # Mensaje inicial
        self.ax_3d.text(0, 0, 0, "Ingresa una función y presiona Graficar", 
                        fontsize=16, ha='center', color=C_TEXTO_GRIS)
        self.ax_3d.set_xlim(-1, 1)
        self.ax_3d.set_ylim(-1, 1)
        self.ax_3d.set_zlim(-1, 1)
        self.canvas_3d.draw()

    def graficar_3d(self):
        func_str = self.entry_graf.get()
        tipo = self.tipo_grafico.get()
        
        try:
            x_min, x_max = float(self.x_min.get()), float(self.x_max.get())
            y_min, y_max = float(self.y_min.get()), float(self.y_max.get())
        except:
            return
        
        def tarea():
            try:
                expr = self.motor_mate.parsear_funcion(func_str)
                if expr is None:
                    return
                
                f = sp.lambdify((self.motor_mate.x, self.motor_mate.y), expr, 'numpy')
                
                x = np.linspace(x_min, x_max, 60)
                y = np.linspace(y_min, y_max, 60)
                X, Y = np.meshgrid(x, y)
                Z = f(X, Y)
                
                def actualizar():
                    # 1. LIMPIEZA TOTAL (Opción Nuclear) ☢️
                    # Esto borra ejes, barras de color, títulos... TODO.
                    # Así evitamos que el gráfico se encoja.
                    self.fig_3d.clear()
                    
                    # 2. Re-creamos el eje 3D desde cero
                    self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
                    self.ax_3d.set_facecolor(C_CARD) # Restauramos el fondo oscuro
                    
                    # 3. Graficar
                    if tipo == "Superficie":
                        surf = self.ax_3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, 
                                                     edgecolor='none', antialiased=True)
                        # Agregamos la barra (ya no necesitamos guardarla en variable porque limpiamos todo arriba)
                        cbar = self.fig_3d.colorbar(surf, ax=self.ax_3d, shrink=0.5, aspect=10, pad=0.1)
                        
                        # Estilos de la barra
                        cbar.ax.yaxis.set_tick_params(color=C_TEXTO_GRIS)
                        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=C_TEXTO_GRIS)
                        
                    elif tipo == "Contorno":
                        self.ax_3d.contour3D(X, Y, Z, 60, cmap='plasma')
                        
                    else:  # Vectorial
                        U = np.gradient(Z, axis=1)
                        V = np.gradient(Z, axis=0)
                        self.ax_3d.quiver(X[::6, ::6], Y[::6, ::6], Z[::6, ::6], 
                                        U[::6, ::6], V[::6, ::6], np.zeros_like(Z[::6, ::6]),
                                        length=0.2, normalize=True, color=C_ACENTO)
                    
                    # 4. Re-aplicar estilos (porque al limpiar la figura se perdieron)
                    self.ax_3d.set_xlabel('X', color=C_TEXTO, fontsize=11)
                    self.ax_3d.set_ylabel('Y', color=C_TEXTO, fontsize=11)
                    self.ax_3d.set_zlabel('Z', color=C_TEXTO, fontsize=11)
                    self.ax_3d.set_title(f'z = {func_str}', color=C_ACENTO, fontsize=14, pad=10)
                    
                    # Quitar paneles de fondo
                    self.ax_3d.xaxis.pane.fill = False
                    self.ax_3d.yaxis.pane.fill = False
                    self.ax_3d.zaxis.pane.fill = False
                    
                    # Color de los ejes (ticks)
                    self.ax_3d.tick_params(axis='x', colors=C_TEXTO_GRIS)
                    self.ax_3d.tick_params(axis='y', colors=C_TEXTO_GRIS)
                    self.ax_3d.tick_params(axis='z', colors=C_TEXTO_GRIS)

                    self.ax_3d.grid(True, alpha=0.2)
                    self.canvas_3d.draw()
                
                self.after(0, actualizar)
            except Exception as e:
                def error():
                    # Si falla, limpiamos y mostramos error
                    self.fig_3d.clear()
                    self.ax_3d = self.fig_3d.add_subplot(111, projection='3d')
                    self.ax_3d.set_facecolor(C_CARD)
                    self.ax_3d.text(0, 0, 0, f"Error: {str(e)[:40]}...", 
                                  fontsize=12, ha='center', color=C_ROJO_ERROR)
                    self.canvas_3d.draw()
                self.after(0, error)
        
        threading.Thread(target=tarea, daemon=True).start()
    # PANTALLA ABOUT
    def setup_about(self):
        f = self.frames["about"]; f.grid_columnconfigure(0, weight=1); f.grid_rowconfigure(0, weight=1)
        
        scroll = ctk.CTkScrollableFrame(f, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(scroll, text="ℹ️ Acerca del Proyecto", 
                    font=ctk.CTkFont(family="Segoe UI", size=40, weight="bold"), 
                    text_color=C_ACENTO).pack(pady=(20, 10))
        
        ctk.CTkLabel(scroll, text="Sistema Avanzado de Cálculo Vectorial", 
                    font=ctk.CTkFont(size=16), text_color=C_TEXTO_GRIS).pack(pady=(0, 30))
        
        # Card principal de información
        info_card = ctk.CTkFrame(scroll, fg_color=C_CARD, corner_radius=20, border_width=2, border_color=C_ACENTO)
        info_card.pack(padx=80, pady=20, fill="x")
        
        info_inner = ctk.CTkFrame(info_card, fg_color="transparent")
        info_inner.pack(padx=40, pady=35)
        
        # Sección académica
        ctk.CTkLabel(info_inner, text="🎓 Información Académica", 
                    font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), 
                    text_color=C_ACENTO).pack(anchor="w", pady=(0, 20))
        
        info_academica = [
            ("🏛️", "Institución:", "Instituto Politécnico Nacional"),
            ("🎓", "Escuela:", "Escuela Superior de Cómputo (ESCOM)"),
            ("💼", "Carrera:", "Ingeniería en Sistemas Computacionales"),
            ("📚", "Asignatura:", "Análisis Vectorial 26-1"),
            ("👨‍🏫", "Profesor:", "Dr. David Correa Coyac"),
            ("📅", "Semestre:", "2026-1"),
            ("🎯", "Tipo:", "Proyecto Terminal")
        ]
        
        for emoji, label, value in info_academica:
            row = ctk.CTkFrame(info_inner, fg_color="#0F172A", corner_radius=12)
            row.pack(fill="x", pady=6)
            
            left = ctk.CTkFrame(row, fg_color="transparent")
            left.pack(side="left", fill="x", expand=True, padx=20, pady=15)
            
            header = ctk.CTkFrame(left, fg_color="transparent")
            header.pack(side="left", anchor="w")
            
            ctk.CTkLabel(header, text=emoji, font=ctk.CTkFont(size=24)).pack(side="left", padx=(0, 12))
            ctk.CTkLabel(header, text=label, 
                        font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), 
                        text_color=C_ACENTO, anchor="w").pack(side="left")
            
            ctk.CTkLabel(row, text=value, 
                        font=ctk.CTkFont(family="Segoe UI", size=14), 
                        text_color=C_TEXTO, anchor="e").pack(side="right", padx=20)
        
        # Separador
        ctk.CTkFrame(info_inner, height=3, fg_color=C_ACENTO_2, corner_radius=2).pack(fill="x", pady=30)
        
        # Equipo
        ctk.CTkLabel(info_inner, text="👥 Equipo de Desarrollo", 
                    font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), 
                    text_color=C_ACENTO).pack(anchor="w", pady=(0, 20))
        
        integrantes_info = [
            ("Bonilla Hernández Ximena Sofía", "💻 Desarrollo Backend", "Implementación de algoritmos numéricos"),
            ("Castillo Vidal Carmen Andrea", "🎨 Diseño UI/UX", "Interfaz gráfica y experiencia de usuario"),
            ("Cruz Rodríguez Bruno Aarón", "📊 Visualización 3D", "Gráficos y análisis matemático")
        ]
        
        for i, (nombre, rol, desc) in enumerate(integrantes_info, 1):
            member_card = ctk.CTkFrame(info_inner, fg_color="#1E293B", corner_radius=15, border_width=2, border_color=C_ACENTO_2)
            member_card.pack(fill="x", pady=8)
            
            member_inner = ctk.CTkFrame(member_card, fg_color="transparent")
            member_inner.pack(fill="x", padx=25, pady=20)
            
            # Número y nombre
            top = ctk.CTkFrame(member_inner, fg_color="transparent")
            top.pack(fill="x", pady=(0, 8))
            
            num_badge = ctk.CTkLabel(top, text=f"#{i}", 
                                   font=ctk.CTkFont(size=16, weight="bold"), 
                                   text_color=C_ACENTO, fg_color="#0F172A", 
                                   corner_radius=8, width=40, height=40)
            num_badge.pack(side="left", padx=(0, 15))
            
            ctk.CTkLabel(top, text=nombre, 
                        font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"), 
                        text_color=C_TEXTO).pack(side="left", anchor="w")
            
            # Rol y descripción
            ctk.CTkLabel(member_inner, text=rol, 
                        font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), 
                        text_color=C_VERDE_OK, anchor="w").pack(anchor="w", pady=2)
            ctk.CTkLabel(member_inner, text=desc, 
                        font=ctk.CTkFont(size=12), 
                        text_color=C_TEXTO_GRIS, anchor="w").pack(anchor="w")
        
        # Características técnicas
        sep = ctk.CTkFrame(scroll, height=2, fg_color="#334155")
        sep.pack(fill="x", padx=100, pady=30)
        
        ctk.CTkLabel(scroll, text="⚙️ Características Técnicas", 
                    font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), 
                    text_color=C_ACENTO_2).pack(pady=(0, 20))
        
        tech_container = ctk.CTkFrame(scroll, fg_color="transparent")
        tech_container.pack(padx=80, fill="x")
        
        tech_features = [
            ("🔢 Cálculo Simbólico", ["SymPy para soluciones exactas", "Integración analítica múltiple", "Soporte de funciones transcendentales"]),
            ("📐 Métodos Numéricos", ["Sumas de Riemann (malla, trapecio)", "Aproximación adaptativa", "Cálculo de error relativo"]),
            ("🎨 Visualización", ["Gráficos 3D interactivos", "Superficies y contornos", "Campos vectoriales"]),
            ("⚡ Performance", ["Cálculo multihilo (threading)", "Optimización NumPy", "Renderizado eficiente"]),
            ("🌐 Coordenadas", ["Cartesianas (x, y, z)", "Polares (r, θ)", "Cilíndricas y Esféricas"]),
            ("🎯 Precisión", ["Comparación numérica vs exacta", "Análisis de convergencia", "Validación de resultados"])
        ]
        
        for i in range(0, len(tech_features), 2):
            row = ctk.CTkFrame(tech_container, fg_color="transparent")
            row.pack(fill="x", pady=8)
            
            for j in range(2):
                if i+j < len(tech_features):
                    titulo, items = tech_features[i+j]
                    
                    card = ctk.CTkFrame(row, fg_color=C_CARD, corner_radius=15, border_width=2, border_color="#475569")
                    card.pack(side="left", expand=True, fill="both", padx=8)
                    
                    ctk.CTkLabel(card, text=titulo, 
                                font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"), 
                                text_color=C_ACENTO).pack(pady=(15, 10), padx=20, anchor="w")
                    
                    for item in items:
                        item_frame = ctk.CTkFrame(card, fg_color="transparent")
                        item_frame.pack(fill="x", padx=20, pady=3)
                        ctk.CTkLabel(item_frame, text="•", text_color=C_VERDE_OK, 
                                   font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 8))
                        ctk.CTkLabel(item_frame, text=item, 
                                   font=ctk.CTkFont(size=12), 
                                   text_color=C_TEXTO_GRIS, anchor="w").pack(side="left", anchor="w")
                    
                    ctk.CTkLabel(card, text="").pack(pady=8)  # Spacer
        
        # Footer final
        footer_card = ctk.CTkFrame(scroll, fg_color="#0F172A", corner_radius=15, border_width=2, border_color=C_VERDE_OK)
        footer_card.pack(padx=100, pady=30, fill="x")
        
        ctk.CTkLabel(footer_card, text="💡 Proyecto desarrollado como aplicación práctica", 
                    font=ctk.CTkFont(size=14, weight="bold"), text_color=C_TEXTO).pack(pady=(20, 5))
        ctk.CTkLabel(footer_card, text="de conceptos de Análisis Vectorial avanzado", 
                    font=ctk.CTkFont(size=13), text_color=C_TEXTO_GRIS).pack(pady=(0, 8))
        ctk.CTkLabel(footer_card, text="🔬 Python • SymPy • NumPy • Matplotlib • CustomTkinter", 
                    font=ctk.CTkFont(size=12, weight="bold"), text_color=C_ACENTO).pack(pady=(8, 20))

if __name__ == "__main__": 
    App().mainloop()