import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import seaborn as sns
import warnings

class CalculadoraIntegrales:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Gráfica de Integrales - EPISS UNAJ 2025")
        self.root.geometry("700x400")
        
        # Configurar estilo seaborn
        sns.set(style="darkgrid")
        
        # Variables
        self.funcion_var = tk.StringVar()
        self.funcion2_var = tk.StringVar()
        self.limite_inf_var = tk.StringVar()
        self.limite_sup_var = tk.StringVar()
        self.resultado_var = tk.StringVar()
        self.tipo_integral_var = tk.StringVar(value="indefinida")
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
        style.configure('TEntry', font=('Arial', 10), padding=5)
        style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 10))
        style.configure('TCombobox', font=('Arial', 10))
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(main_frame, text="Calculadora Gráfica de Integrales", 
                          font=('Arial', 14, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Selección de tipo de integral
        tipo_frame = ttk.Frame(main_frame)
        tipo_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Label(tipo_frame, text="Tipo de integral:").pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(tipo_frame, text="Indefinida", variable=self.tipo_integral_var,
                       value="indefinida", command=self.toggle_campos).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(tipo_frame, text="Definida (1 función)", variable=self.tipo_integral_var,
                       value="definida", command=self.toggle_campos).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(tipo_frame, text="Área entre 2 funciones", variable=self.tipo_integral_var,
                       value="area_entre_funciones", command=self.toggle_campos).pack(side=tk.LEFT, padx=5)
        
        # Entrada de función 1
        ttk.Label(main_frame, text="Función f(x):").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        funcion_entry = ttk.Entry(main_frame, textvariable=self.funcion_var, width=40)
        funcion_entry.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))
        
        # Entrada de función 2 (solo para área entre funciones)
        self.funcion2_frame = ttk.Frame(main_frame)
        self.funcion2_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10), sticky=tk.W)
        
        ttk.Label(self.funcion2_frame, text="Función g(x):").pack(side=tk.LEFT, padx=(0, 5))
        self.funcion2_entry = ttk.Entry(self.funcion2_frame, textvariable=self.funcion2_var, width=40)
        self.funcion2_entry.pack(side=tk.LEFT)
        
        # Ejemplos de funciones
        ejemplos = ttk.Label(main_frame, text="Ejemplos: x**2, sin(x), exp(x), ln(x), sqrt(x), 1/x, pi")
        ejemplos.grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Límites (para integral definida y área entre funciones)
        self.limites_frame = ttk.Frame(main_frame)
        self.limites_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Label(self.limites_frame, text="Límite inferior:").pack(side=tk.LEFT, padx=5)
        limite_inf_entry = ttk.Entry(self.limites_frame, textvariable=self.limite_inf_var, width=10)
        limite_inf_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.limites_frame, text="Límite superior:").pack(side=tk.LEFT, padx=5)
        limite_sup_entry = ttk.Entry(self.limites_frame, textvariable=self.limite_sup_var, width=10)
        limite_sup_entry.pack(side=tk.LEFT, padx=5)
        
        # Botones
        botones_frame = ttk.Frame(main_frame)
        botones_frame.grid(row=6, column=0, columnspan=3, pady=(20, 10))
        
        calcular_btn = ttk.Button(botones_frame, text="Calcular", command=self.calcular_integral)
        calcular_btn.pack(side=tk.LEFT, padx=10)
        
        limpiar_btn = ttk.Button(botones_frame, text="Limpiar", command=self.limpiar)
        limpiar_btn.pack(side=tk.LEFT, padx=10)
        
        # Resultado
        ttk.Label(main_frame, text="Resultado:").grid(row=7, column=0, sticky=tk.W, pady=(10, 0))
        resultado_entry = ttk.Entry(main_frame, textvariable=self.resultado_var, width=60, state='readonly')
        resultado_entry.grid(row=7, column=1, sticky=tk.W, pady=(10, 0))
        
        # Configurar grid para expansión
        main_frame.columnconfigure(1, weight=1)
        
        # Ocultar campos inicialmente
        self.toggle_campos()
    
    def toggle_campos(self):
        tipo = self.tipo_integral_var.get()
        
        if tipo == "indefinida":
            self.funcion2_frame.grid_remove()
            self.limites_frame.grid_remove()
        elif tipo == "definida":
            self.funcion2_frame.grid_remove()
            self.limites_frame.grid()
        else:  # area_entre_funciones
            self.funcion2_frame.grid()
            self.limites_frame.grid()
    
    def calcular_integral(self):
        try:
            # Obtener la función principal
            funcion_str = self.funcion_var.get().strip()
            if not funcion_str:
                messagebox.showerror("Error", "Por favor ingrese al menos la función f(x)")
                return
            
            # Definir símbolo x
            x = sp.Symbol('x')
            
            # Parsear la función principal
            try:
                f = sp.sympify(funcion_str)
            except (sp.SympifyError, SyntaxError) as e:
                messagebox.showerror("Error", f"Función f(x) no válida: {str(e)}")
                return
            
            tipo = self.tipo_integral_var.get()
            
            if tipo == "indefinida":
                # Calcular integral indefinida
                integral = sp.integrate(f, x)
                self.resultado_var.set(f"∫({funcion_str}) dx = {sp.pretty(integral)} + C")
                
                # Mostrar gráfico de integral indefinida
                self.mostrar_grafico_indefinida(f, integral, funcion_str, x)
                
            elif tipo == "definida":
                # Calcular integral definida de una función
                self.calcular_integral_definida(f, funcion_str, x)
                
            elif tipo == "area_entre_funciones":
                # Calcular área entre dos funciones
                self.calcular_area_entre_funciones(f, funcion_str, x)
        
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
    
    def mostrar_grafico_indefinida(self, f, integral, f_str, x):
        """Muestra el gráfico para integral indefinida con slider para C"""
        try:
            # Configurar figura
            fig, ax = plt.subplots(figsize=(7, 6), dpi=100)
            plt.subplots_adjust(bottom=0.25, top=0.85)
            
            # Configurar colores
            colores = sns.color_palette("Set2", n_colors=101)
            
            # Definir constante de integración
            C_sym = sp.Symbol('C')
            f_base = integral
            
            # Función para evaluar
            f_func = sp.lambdify((x, C_sym), f_base + C_sym, modules=['numpy'])
            
            # Rango de valores x
            x_vals = np.linspace(-10, 10, 500)
            
            # Configurar título con LaTeX
            f_latex = sp.latex(f)
            ax.set_title(fr"Integrales indefinidas de $f(x) = {f_latex}$", fontsize=14)
            
            # Función para generar fórmula LaTeX
            def generar_formula(c_val):
                f_con_valor = f_base + c_val
                return rf"$\int {f_latex}\,dx = {sp.latex(f_con_valor)}$"
            
            # Mostrar fórmula inicial
            c_inicial = 0
            formula_box = ax.text(0.05, 0.95, generar_formula(c_inicial),
                                transform=ax.transAxes, fontsize=13,
                                verticalalignment='top',
                                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Graficar función inicial
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                y_vals = f_func(x_vals, c_inicial)
                ax.plot(x_vals, y_vals, color=colores[50], alpha=1)
            
            # Configurar ejes
            ax.set_xlabel(r"$x$", fontsize=12)
            ax.set_ylabel(r"$F(x)$", fontsize=12)
            ax.grid(True)
            
            # Crear slider para C
            ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
            slider_c = Slider(ax_slider, "C", -20, 20, valinit=c_inicial, valstep=1)
            
            # Conjunto para rastrear valores de C ya graficados
            valores_graficados = {c_inicial}
            
            # Función de actualización del slider
            def actualizar(val):
                c_val = int(slider_c.val)
                
                if c_val not in valores_graficados:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        y_new = f_func(x_vals, c_val)
                    idx = c_val + 50
                    ax.plot(x_vals, y_new, color=colores[idx % 101], alpha=0.85)
                    valores_graficados.add(c_val)
                    
                    ax.relim()
                    ax.autoscale_view()
                    ax.margins(x=0.05, y=0.1)
                
                formula_box.set_text(generar_formula(c_val))
                fig.canvas.draw_idle()
            
            slider_c.on_changed(actualizar)
            
            # Mostrar la figura
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")
    
    def calcular_integral_definida(self, f, f_str, x):
        """Calcula la integral definida de una función y muestra el gráfico"""
        # Obtener límites
        limite_inf_str = self.limite_inf_var.get().strip()
        limite_sup_str = self.limite_sup_var.get().strip()
        
        if not limite_inf_str or not limite_sup_str:
            messagebox.showerror("Error", "Por favor ingrese ambos límites")
            return
        
        try:
            limite_inf = sp.sympify(limite_inf_str)
            limite_sup = sp.sympify(limite_sup_str)
        except (sp.SympifyError, SyntaxError) as e:
            messagebox.showerror("Error", f"Límites no válidos: {str(e)}")
            return
        
        # Calcular integral definida
        integral = sp.integrate(f, (x, limite_inf, limite_sup))
        self.resultado_var.set(f"∫_{limite_inf_str}^{limite_sup_str} ({f_str}) dx = {integral.evalf()}")
        
        # Mostrar gráfico
        self.mostrar_grafico_definida(f, f_str, x, limite_inf, limite_sup)
    
    def mostrar_grafico_definida(self, f, f_str, x, limite_inf, limite_sup):
        """Muestra el gráfico para integral definida con estilo similar a Indef.py"""
        try:
            # Configurar figura
            fig, ax = plt.subplots(figsize=(7, 6), dpi=100)
            plt.subplots_adjust(bottom=0.15, top=0.85)
            
            # Convertir la función sympy a numpy
            f_np = sp.lambdify(x, f, 'numpy')
            
            # Calcular dominio válido para la función
            try:
                # Intentar encontrar el dominio donde la función es real
                dominio_min = float(limite_inf.evalf())
                dominio_max = float(limite_sup.evalf())
                
                # Para funciones con raíces cuadradas, ajustar el dominio
                if 'sqrt' in f_str:
                    # Calcular puntos donde el argumento de la raíz es cero
                    arg_raiz = list(f.atoms(sp.Pow))[0].base if list(f.atoms(sp.Pow)) else None
                    if arg_raiz:
                        puntos_criticos = sp.solve(arg_raiz, x)
                        if puntos_criticos:
                            dominio_min = max(dominio_min, min(float(pc.evalf()) for pc in puntos_criticos if float(pc.evalf()) > dominio_min))
                            dominio_max = min(dominio_max, max(float(pc.evalf()) for pc in puntos_criticos if float(pc.evalf()) < dominio_max))
                
                # Rango de valores x
                x_min = min(dominio_min, -10)
                x_max = max(dominio_max, 10)
                x_vals = np.linspace(x_min - 0.1, x_max + 0.1, 500)
                
                # Evaluar la función solo en el dominio válido
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    y_vals = f_np(x_vals)
                
                # Graficar la función
                ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {f_str}')
                
                # Rellenar el área bajo la curva solo en el intervalo de integración
                x_fill = np.linspace(float(limite_inf.evalf()), float(limite_sup.evalf()), 100)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    y_fill = f_np(x_fill)
                ax.fill_between(x_fill, y_fill, color='skyblue', alpha=0.4)
                
            except Exception as e:
                # Si hay problemas con el dominio, usar solo el intervalo de integración
                x_vals = np.linspace(float(limite_inf.evalf()) - 0.1, float(limite_sup.evalf()) + 0.1, 100)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    y_vals = f_np(x_vals)
                ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {f_str}')
                ax.fill_between(x_vals, y_vals, color='skyblue', alpha=0.4)
            
            # Configurar título con LaTeX
            f_latex = sp.latex(f)
            
            # Simplificar la representación del resultado para evitar problemas con LaTeX
            resultado = sp.integrate(f, (x, limite_inf, limite_sup))
            resultado_str = f"{resultado.evalf(3)}"  # Usar solo el valor numérico
            
            formula_text = rf"$\int_{{{sp.latex(limite_inf)}}}^{{{sp.latex(limite_sup)}}} {f_latex}\,dx \approx {resultado_str}$"
            
            ax.text(0.05, 0.95, formula_text,
                   transform=ax.transAxes, fontsize=13,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Configurar ejes
            ax.set_xlabel(r"$x$", fontsize=12)
            ax.set_ylabel(r"$f(x)$", fontsize=12)
            ax.legend()
            ax.grid(True)
            
            # Mostrar la figura
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")
    
    def calcular_area_entre_funciones(self, f, f_str, x):
        """Calcula el área entre dos funciones y muestra el gráfico"""
        # Obtener segunda función
        funcion2_str = self.funcion2_var.get().strip()
        if not funcion2_str:
            messagebox.showerror("Error", "Por favor ingrese la función g(x)")
            return
        
        try:
            g = sp.sympify(funcion2_str)
        except (sp.SympifyError, SyntaxError) as e:
            messagebox.showerror("Error", f"Función g(x) no válida: {str(e)}")
            return
        
        # Obtener límites
        limite_inf_str = self.limite_inf_var.get().strip()
        limite_sup_str = self.limite_sup_var.get().strip()
        
        
        if not limite_inf_str or not limite_sup_str:
            # Si no hay límites, encontrar intersecciones
            try:
                intersecciones = sp.solve(f - g, x)
                if not intersecciones:
                    messagebox.showerror("Error", "No se encontraron puntos de intersección. Ingrese límites manualmente.")
                    return
                
                if len(intersecciones) == 1:
                    messagebox.showinfo("Información", 
                                      f"Solo hay un punto de intersección en x = {intersecciones[0]}. "
                                      "Ingrese límites manualmente para calcular el área.")
                    return
                
                puntos = sorted([float(i.evalf()) for i in intersecciones])
                limite_inf, limite_sup = puntos[0], puntos[-1]
                
                if len(intersecciones) > 2:
                    messagebox.showwarning("Advertencia", 
                                         f"Se encontraron múltiples intersecciones en x = {puntos}. "
                                         f"Calculando área entre x = {limite_inf} y x = {limite_sup}.")
                
            except Exception as e:
                messagebox.showerror("Error", 
                                   f"No se pudieron encontrar intersecciones automáticamente: {str(e)}\n"
                                   "Ingrese los límites manualmente.")
                return
        else:
            # Usar límites proporcionados por el usuario
            try:
                limite_inf = sp.sympify(limite_inf_str)
                limite_sup = sp.sympify(limite_sup_str)
            except (sp.SympifyError, SyntaxError) as e:
                messagebox.showerror("Error", f"Límites no válidos: {str(e)}")
                return
        
        # Calcular área entre las dos funciones
        area = sp.integrate(abs(f - g), (x, limite_inf, limite_sup))
        self.resultado_var.set(
            f"Área entre f(x)={f_str} y g(x)={funcion2_str} "
            f"desde LimInf={limite_inf} hasta LimSup={limite_sup} = {area.evalf(3)}"
        )
        
        # Mostrar gráfico
        self.mostrar_grafico_area_entre_funciones(f, g, f_str, funcion2_str, x, limite_inf, limite_sup)
    
    def mostrar_grafico_area_entre_funciones(self, f, g, f_str, g_str, x, limite_inf, limite_sup):
        """Muestra el gráfico para el área entre dos funciones con estilo similar"""
        try:
            # Configurar figura
            fig, ax = plt.subplots(figsize=(7, 6), dpi=100)
            plt.subplots_adjust(bottom=0.15, top=0.85)
            
            # Convertir funciones sympy a numpy
            f_np = sp.lambdify(x, f, 'numpy')
            g_np = sp.lambdify(x, g, 'numpy')
            
            # Rango de valores x
            x_min = min(float(limite_inf.evalf()), -10)
            x_max = max(float(limite_sup.evalf()), 10)
            x_vals = np.linspace(x_min - 1, x_max + 1, 500)
            
            # Evaluar funciones con manejo de advertencias
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                f_vals = f_np(x_vals)
                g_vals = g_np(x_vals)
            
            # Graficar las funciones
            ax.plot(x_vals, f_vals, 'b-', linewidth=2, label=f'f(x) = {f_str}')
            ax.plot(x_vals, g_vals, 'r-', linewidth=2, label=f'g(x) = {g_str}')
            
            # Rellenar el área entre las curvas
            x_fill = np.linspace(float(limite_inf.evalf()), float(limite_sup.evalf()), 100)
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                f_fill = f_np(x_fill)
                g_fill = g_np(x_fill)
            
            ax.fill_between(x_fill, f_fill, g_fill, where=(f_fill > g_fill), 
                           color='green', alpha=0.3, label='Área entre curvas')
            ax.fill_between(x_fill, g_fill, f_fill, where=(g_fill > f_fill), 
                           color='green', alpha=0.3)
            
            # Configurar título con LaTeX
            f_latex = sp.latex(f)
            g_latex = sp.latex(g)
            ax.set_title(fr"Área entre $f(x) = {f_latex}$ y $g(x) = {g_latex}$", fontsize=14)
            
            # Mostrar fórmula del resultado (simplificada para evitar problemas con LaTeX)
            area = sp.integrate(abs(f - g), (x, limite_inf, limite_sup))
            formula_text = rf"$\text{{Área}} = \int_{{{limite_inf}}}^{{{limite_sup}}} |{f_latex} - {g_latex}|\,dx \approx {area.evalf(3)}$"
            
            ax.text(0.05, 0.95, formula_text,
                   transform=ax.transAxes, fontsize=13,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            # Configurar ejes
            ax.set_xlabel(r"$x$", fontsize=12)
            ax.set_ylabel(r"$y$", fontsize=12)
            ax.legend()
            ax.grid(True)
            
            # Mostrar la figura
            plt.show()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el gráfico: {str(e)}")
    
    def limpiar(self):
        """Limpia todos los campos"""
        self.funcion_var.set("")
        self.funcion2_var.set("")
        self.limite_inf_var.set("")
        self.limite_sup_var.set("")
        self.resultado_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraIntegrales(root)
    root.mainloop()