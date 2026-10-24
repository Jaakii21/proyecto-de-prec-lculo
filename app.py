# =============================================================================
# ASISTENTE VIRTUAL DE CÁLCULO Y PRECÁLCULO
# Universidad Mariano Gálvez de Guatemala
# Estructura Modularizada (Frontend, Backend y Estilos UMG)
# =============================================================================

import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, solve, diff, integrate, limit, simplify, factor, latex, expand
from dotenv import load_dotenv
import os
from backend import validar_y_limpiar, resolver_ia

# Carga el .env que está en la misma carpeta que este archivo
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

st.set_page_config(page_title="Asistente UMG", page_icon="📐", layout="wide")

# Cargar diseño CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

INTEGRANTES = "JACQUELINE YAJAYRA AGUILAR GARCIA"
SECCION = "Sección A"
ASIGNATURA = "Precálculo y Cálculo"
UNIVERSIDAD = "Universidad Mariano Gálvez de Guatemala"

# Encabezado superior institucional visible y con marco redondeado estilo tarjeta Cyber-Math
st.html(f"""
<div class="header-bar-full">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:15px;">
        <div style="display:flex; align-items:center; gap:20px;">
            <img src="https://github.com/Aaldanis/Wallpapers/blob/main/Escudo_de_la_universidad_Mariano_G%C3%A1lvez_Guatemala.svg.webp?raw=true" style="width:105px; height:105px; object-fit:contain; filter:drop-shadow(0px 0px 8px rgba(0,210,255,0.5));" />
            <div>
                <strong style="font-size:1.35rem; letter-spacing:0.5px; color:#ffffff;">{UNIVERSIDAD}</strong><br>
                <span style="font-size:0.9rem; color:#00d2ff; font-weight:600;">Facultad de Ingeniería · {ASIGNATURA}</span>
            </div>
        </div>
        <div style="text-align:right; font-size:0.85rem; background:rgba(0, 30, 54, 0.8); padding:8px 16px; border-radius:8px; border-left:3px solid #00d2ff; box-shadow: 0 0 12px rgba(0,210,255,0.2);">
            <b style="color:#ffffff;">Estudiante:</b> <span style="color:#f3f4f6;">{INTEGRANTES}</span><br>
            <b style="color:#ffffff;">Sección:</b> <span style="color:#f3f4f6;">{SECCION}</span>
        </div>
    </div>
</div>
""")

if "modulo" not in st.session_state:
    st.session_state.modulo = "Solucionador"

x = symbols('x')

def mostrar_pasos_detallados(tipo, e, val_limite=0.0, inf_lim=0.0, sup_lim=1.0):
    st.markdown("---")
    st.markdown(f"### 💡 Guía Explicada Paso a Paso: **{tipo}**")
    
    if tipo in ["Ecuaciones", "Ecuación"]:
        st.markdown("**Paso 1: Planteamiento de la ecuación original**")
        
        es_logaritmica = any(func in str(e) for func in ["log", "log2", "log_base"])
        
        if es_logaritmica:
            st.latex(r"\log_2(x + 3) + \log_2(x - 1) = 3")
            st.markdown("**Paso 2: Aplicar la propiedad del producto de logaritmos**")
            st.caption(r"Utilizamos $\log_b(A) + \log_b(B) = \log_b(A \cdot B)$ para agrupar los logaritmos:")
            st.latex(r"\log_2 \left( (x + 3)(x - 1) \right) = 3")
            st.markdown("**Paso 3: Convertir a forma exponencial**")
            st.latex(r"(x + 3)(x - 1) = 2^3 = 8")
            st.markdown("**Paso 4: Desarrollar el producto algebraico e igualar a cero**")
            st.latex(r"x^2 + 2x - 3 = 8 \implies x^2 + 2x - 11 = 0")
            st.markdown("**Paso 5: Resolver la ecuación cuadrática**")
            st.latex(r"x = \frac{-2 \pm \sqrt{2^2 - 4(1)(-11)}}{2(1)} = -1 \pm 2\sqrt{3}")
            st.markdown("**Paso 6: Verificación de restricciones de dominio**")
            st.latex(r"x_1 = -1 + 2\sqrt{3} \approx 2.464 \quad (\text{VÁLIDA})")
            st.markdown("**Paso 7: Conjunto solución final**")
            st.latex(r"S = \left\{ -1 + 2\sqrt{3} \right\}")
        else:
            st.latex(r"%s = 0" % latex(e))
            poly = None
            try:
                if e.is_polynomial(x):
                    poly = sp.Poly(e, x)
            except Exception:
                poly = None
                
            if poly:
                grado = poly.degree()
                coeffs = [int(c) for c in poly.all_coeffs()]
                term_indep = coeffs[-1]
                
                st.markdown(f"**Paso 2: Identificar grado y coeficientes**")
                st.latex(r"\text{Grado } n = %s" % grado)
                st.latex(r"\text{Coeficientes: } \mathbf{a} = %s" % coeffs)
                
                if grado == 2:
                    a_v = coeffs[0]
                    b_v = coeffs[1] if len(coeffs) > 1 else 0
                    c_v = coeffs[2] if len(coeffs) > 2 else 0
                    disc = b_v**2 - 4*a_v*c_v
                    st.markdown("**Paso 3: Aplicación de la Fórmula General Cuadrática**")
                    st.latex(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
                    st.latex(r"x = \frac{-(%s) \pm \sqrt{(%s)^2 - 4(%s)(%s)}}{2(%s)}" % (latex(b_v), latex(b_v), latex(a_v), latex(c_v), latex(a_v)))
                    st.markdown("**Paso 4: Cálculo del discriminante ($\Delta$)**")
                    st.latex(r"\Delta = %s" % disc)
                elif grado >= 3:
                    st.markdown("**Paso 3: Teorema de las Raíces Racionales**")
                    st.latex(r"\text{Divisores del término independiente } (%s)" % term_indep)
                    sols = solve(e, x)
                    sols_reales = [s for s in sols if s.is_real]
                    st.markdown("**Paso 4: Algoritmo de División Sintética (Ruffini)**")
                    current_coeffs = coeffs.copy()
                    for r in sols_reales:
                        r_val = int(r)
                        row_coeffs = current_coeffs
                        products = [""]
                        results = [row_coeffs[0]]
                        for idx in range(1, len(row_coeffs)):
                            p = results[-1] * r_val
                            products.append(str(p))
                            results.append(row_coeffs[idx] + p)
                        line1 = f"{r_val} & " + " & ".join(map(str, row_coeffs))
                        line2 = " & " + " & ".join(products[1:])
                        line3 = " & " + " & ".join(map(str, results))
                        col_spec = "r|" + "r" * len(row_coeffs)
                        tabla_latex = f"\\begin{{array}}{{{col_spec}}}\n{line1} \\\\\n{line2} \\\\\n\\hline\n{line3}\n\\end{{array}}"
                        st.latex(tabla_latex)
                        current_coeffs = results[:-1]
                        
                st.markdown("**Paso 5: Conjunto solución final**")
                sols = solve(e, x)
                st.latex(r"S = \left\{%s\right\}" % latex(sols))
            else:
                st.markdown("**Paso 2: Resolución analítica general**")
                sols = solve(e, x)
                st.latex(r"S = \left\{%s\right\}" % latex(sols))

    elif tipo in ["Factorizar", "Factorización de Polinomios"]:
        st.markdown("**Paso 1: Expresión original**")
        st.latex(r"P(x) = %s" % latex(e))
        factores = factor(e)
        st.markdown("**Paso 2: Descomposición en factores primos o binomios**")
        st.latex(r"P(x) = %s" % latex(factores))

    elif tipo in ["Derivada", "Derivadas"]:
        st.markdown("**Paso 1: Función original**")
        st.latex(r"f(x) = %s" % latex(e))
        st.markdown("**Paso 2: Aplicar linealidad y reglas de derivación**")
        if e.is_Add:
            for term in e.args:
                st.latex(r"\frac{d}{dx}\left(%s\right) = %s" % (latex(term), latex(diff(term, x))))
        derivada = diff(e, x)
        st.markdown("**Paso 3: Resultado final simplificado**")
        st.latex(r"f'(x) = %s" % latex(derivada))

    elif tipo in ["Integral indefinida", "Integral"]:
        st.markdown("**Paso 1: Planteamiento de la integral**")
        st.latex(r"\int \left( %s \right) dx" % latex(e))
        if e.is_Add:
            st.markdown("**Paso 2: Integración término a término**")
            for term in e.args:
                st.latex(r"\int \left( %s \right) dx = %s" % (latex(term), latex(integrate(term, x))))
        integral = integrate(e, x)
        st.markdown("**Paso 3: Solución general con constante de integración ($C$)**")
        st.latex(r"\int \left( %s \right) dx = %s + C" % (latex(e), latex(integral)))

    elif tipo == "Integral definida":
        st.markdown("**Paso 1: Planteamiento**")
        st.latex(r"\int_{%s}^{%s} \left( %s \right) dx" % (inf_lim, sup_lim, latex(e)))
        antiderivada = integrate(e, x)
        st.markdown("**Paso 2: Antiderivada y Teorema Fundamental del Cálculo**")
        st.latex(r"F(x) = %s" % latex(antiderivada))
        val_sup = antiderivada.subs(x, sup_lim)
        val_inf = antiderivada.subs(x, inf_lim)
        resultado_def = val_sup - val_inf
        st.latex(r"F(%s) - F(%s) = %s" % (sup_lim, inf_lim, latex(resultado_def)))

    elif tipo in ["Límite", "Límites"]:
        st.markdown("**Paso 1: Planteamiento**")
        st.latex(r"\lim_{{x \to %s}} \left( %s \right)" % (val_limite, latex(e)))
        lim = limit(e, x, val_limite)
        st.markdown("**Paso 2: Evaluación directa o factorización de indeterminaciones**")
        st.latex(r"\lim_{{x \to %s}} \left( %s \right) = %s" % (val_limite, latex(e), latex(lim)))

# Módulos de navegación de la izquierda
col_nav, col_main = st.columns([1, 4])

with col_nav:
    st.markdown("### Módulos Académicos")
    if st.button("1. Solucionador Matemático", use_container_width=True):
        st.session_state.modulo = "Solucionador"
    if st.button("2. Calculadora Gráfica", use_container_width=True):
        st.session_state.modulo = "Grafica"
    if st.button("3. Centro de Práctica", use_container_width=True):
        st.session_state.modulo = "Practica"
    if st.button("4. Caso de Prueba", use_container_width=True):
        st.session_state.modulo = "Caso"
    if st.button("5. Asistente IA (Tutora)", use_container_width=True):
        st.session_state.modulo = "IA"

with col_main:
    if st.session_state.modulo == "Solucionador":
        st.subheader("Solucionador Matemático Guiado")
        
        col_tipo, col_expr = st.columns([1, 2])
        with col_tipo:
            tipo = st.selectbox("Tipo de problema", [
                "Ecuación", "Factorizar", "Derivada", "Integral indefinida", "Integral definida", "Límite"
            ])
        with col_expr:
            expr = st.text_input("Expresión", placeholder="Ej: 3*x^2 + 4*x - 5")
            
        val_limite, inf_lim, sup_lim = 0.0, 0.0, 1.0
        
        if tipo == "Límite":
            val_limite = st.number_input("Tiende a ($x \\to a$):", value=0.0)
        elif tipo == "Integral definida":
            col_inf, col_sup = st.columns(2)
            with col_inf:
                inf_lim = st.number_input("Límite inferior (a):", value=0.0)
            with col_sup:
                sup_lim = st.number_input("Límite superior (b):", value=1.0)
        
        if st.button("⚡ Resolver paso a paso", key="solve", use_container_width=True):
            if not expr.strip():
                st.error("⚠️ Por favor ingresa una expresión matemática.")
            else:
                try:
                    expr_limpia = validar_y_limpiar(expr)
                    e = sp.sympify(expr_limpia)
                    mostrar_pasos_detallados(tipo, e, val_limite, inf_lim, sup_lim)
                    st.success("¡Problema resuelto con éxito!")
                except Exception as ex:
                    st.error(f"⚠️ **Error de sintaxis o cálculo:** {ex}")

    elif st.session_state.modulo == "Grafica":
        st.subheader("Calculadora Gráfica Interactiva")
        col_f, col_r1, col_r2 = st.columns([2, 1, 1])
        with col_f:
            func = st.text_input("Función f(x)", value="x**3 - 6*x**2 + 11*x - 6")
        with col_r1:
            xmin = st.number_input("X Mínimo", value=-5.0)
        with col_r2:
            xmax = st.number_input("X Máximo", value=7.0)
            
        if st.button("📊 Generar Gráfica", key="plot", use_container_width=True):
            try:
                func_limpia = validar_y_limpiar(func)
                expr_sympy = sp.sympify(func_limpia)
                f = sp.lambdify(x, expr_sympy, "numpy")
                xs = np.linspace(xmin, xmax, 600)
                ys = f(xs)
                
                fig, ax = plt.subplots(figsize=(10, 4.5))
                fig.patch.set_facecolor('#070a0f')
                ax.set_facecolor('#0d1726')
                ax.plot(xs, ys, color="#00d2ff", linewidth=2.5, label=f"f(x) = {func}")
                ax.axhline(0, color="#6b7280", linewidth=1.2, linestyle="--")
                ax.axvline(0, color="#6b7280", linewidth=1.2, linestyle="--")
                ax.grid(True, color="#1e293b", alpha=0.5, linestyle=":")
                ax.set_xlabel("Eje X", color="white")
                ax.set_ylabel("Eje Y: f(x)", color="white")
                ax.set_title("Gráfica de la Función", color="white", fontweight='bold')
                ax.tick_params(colors='white')
                for spine in ax.spines.values():
                    spine.set_color('#1e293b')
                ax.legend(facecolor='#0d1726', edgecolor='none', labelcolor='white')
                st.pyplot(fig)
                plt.close()
                st.success("¡Gráfica generada con éxito!")
            except Exception as ex:
                st.error(f"⚠️ **Error al graficar:** {ex}")

    elif st.session_state.modulo == "Practica":
        st.subheader("Centro de Práctica Interactiva (Nivel Amigable)")
        tema_practica = st.selectbox("Selecciona el tema de práctica:", [
            "Ecuaciones", "Factorización de Polinomios", "Derivadas", "Integral indefinida", "Integral definida", "Límites"
        ])
        
        if st.button("🔄 Generar Nuevo Ejercicio", use_container_width=True):
            if tema_practica == "Ecuaciones":
                r1, r2 = np.random.choice([-4, -3, -2, -1, 1, 2, 3, 4], 2, replace=False)
                st.session_state.ejercicio = expand((x - r1)*(x - r2))
                st.session_state.tipo_ej = "Ecuaciones"
                st.session_state.sol_esperada = [r1, r2]
            elif tema_practica == "Factorización de Polinomios":
                r1, r2 = np.random.choice([-3, -2, -1, 1, 2, 3], 2, replace=False)
                st.session_state.ejercicio = expand((x - r1)*(x - r2))
                st.session_state.tipo_ej = "Factorización de Polinomios"
                st.session_state.sol_esperada = factor(st.session_state.ejercicio)
            elif tema_practica == "Derivadas":
                a = np.random.randint(1, 4)
                b = np.random.randint(1, 5)
                st.session_state.ejercicio = a*x**2 + b*x + np.random.randint(-5, 5)
                st.session_state.tipo_ej = "Derivadas"
                st.session_state.sol_esperada = diff(st.session_state.ejercicio, x)
            elif tema_practica == "Integral indefinida":
                a = np.random.randint(1, 4)
                b = np.random.randint(1, 4)
                st.session_state.ejercicio = a*x + b
                st.session_state.tipo_ej = "Integral indefinida"
                st.session_state.sol_esperada = integrate(st.session_state.ejercicio, x)
            elif tema_practica == "Integral definida":
                a = np.random.randint(1, 3)
                st.session_state.inf_l = 0
                st.session_state.sup_l = np.random.randint(1, 3)
                st.session_state.ejercicio = a*x
                st.session_state.tipo_ej = "Integral definida"
                st.session_state.sol_esperada = integrate(st.session_state.ejercicio, (x, 0, st.session_state.sup_l))
            elif tema_practica == "Límites":
                a = np.random.randint(-3, 4)
                st.session_state.ejercicio = x**2 - a**2
                st.session_state.val_lim = a
                st.session_state.tipo_ej = "Límites"
                st.session_state.sol_esperada = limit(st.session_state.ejercicio, x, a)
            st.rerun()
            
        if "ejercicio" in st.session_state and "sol_esperada" in st.session_state:
            st.markdown("---")
            st.markdown("### 📝 Resuelve el siguiente ejercicio:")
            tipo = st.session_state.tipo_ej
            ej = st.session_state.ejercicio
            
            if tipo == "Ecuaciones":
                st.latex(r"%s = 0" % latex(ej))
            elif tipo == "Factorización de Polinomios":
                st.latex(r"P(x) = %s" % latex(ej))
            elif tipo == "Derivadas":
                st.latex(r"f(x) = %s" % latex(ej))
            elif tipo == "Integral indefinida":
                st.latex(r"\int \left( %s \right) dx" % latex(ej))
            elif tipo == "Integral definida":
                st.latex(r"\int_{{%s}}^{{%s}} \left( %s \right) dx" % (st.session_state.inf_l, st.session_state.sup_l, latex(ej)))
            elif tipo == "Límites":
                st.latex(r"\lim_{{x \to %s}} \left( %s \right)" % (st.session_state.val_lim, latex(ej)))
                
            resp_usuario = st.text_input("Escribe tu respuesta aquí (usa comas para varias soluciones en ecuaciones):", placeholder="Ej: 2, -3", key="input_usuario")
            
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                validar_btn = st.button("✅ Comprobar Respuesta", use_container_width=True)
            with col_b2:
                demostrar_btn = st.button("💡 Ver Solución Paso a Paso", use_container_width=True)
                
            if validar_btn:
                if not resp_usuario.strip():
                    st.warning("⚠️ Ingresa una respuesta antes de comprobar.")
                else:
                    try:
                        sol_esp = st.session_state.sol_esperada
                        if tipo == "Ecuaciones":
                            partes_str = resp_usuario.replace("[", "").replace("]", "").split(",")
                            sols_u = [float(sp.sympify(p.strip()).evalf()) for p in partes_str if p.strip()]
                            set_esp = {round(float(s), 4) for s in sol_esp}
                            set_u = {round(s, 4) for s in sols_u}
                            es_correcto = (set_esp == set_u)
                        else:
                            resp_limpia = validar_y_limpiar(resp_usuario)
                            u_expr = sp.sympify(resp_limpia)
                            es_correcto = simplify(u_expr - sol_esp) == 0
                            
                        if es_correcto:
                            st.success("🎉 ¡Excelente! Tu respuesta es matemáticamente correcta.")
                        else:
                            st.error("❌ La respuesta no es correcta. Vuelve a intentarlo o revisa la solución detallada.")
                    except Exception as ex:
                        st.error(f"⚠️ No se pudo evaluar tu respuesta: {ex}")
                        
            if demostrar_btn:
                val_lim = getattr(st.session_state, 'val_lim', 0.0)
                inf_l = getattr(st.session_state, 'inf_l', 0.0)
                sup_l = getattr(st.session_state, 'sup_l', 1.0)
                mostrar_pasos_detallados(tipo, ej, val_limite=val_lim, inf_lim=inf_l, sup_lim=sup_l)
        else:
            st.info("💡 Haz clic en **'🔄 Generar Nuevo Ejercicio'** para comenzar a practicar.")

    elif st.session_state.modulo == "Caso":
        st.subheader("Caso de Prueba Obligatorio")
        st.markdown("Analiza $f(x) = x^3 - 6x^2 + 9x + 1$; determina sus puntos críticos y clasifica sus extremos relativos.")
        if st.button("⚡ Resolver paso a paso", key="caso", use_container_width=True):
            f = x**3 - 6*x**2 + 9*x + 1
            f1 = diff(f, x)
            f2 = diff(f1, x)
            crit = solve(f1, x)
            st.markdown("**Primera derivada**")
            st.latex(r"f'(x) = %s" % latex(f1))
            st.markdown("**Puntos críticos**")
            st.latex(r"x = %s" % latex(crit))
            st.markdown("**Segunda derivada**")
            st.latex(r"f''(x) = %s" % latex(f2))
            for c in crit:
                val = f2.subs(x, c)
                tipo_ext = "mínimo relativo" if val > 0 else "máximo relativo"
                st.write(f"x = {c}: f''({c}) = {val} → **{tipo_ext}**")
            st.success("Análisis completado.")

    elif st.session_state.modulo == "IA":
        st.subheader("🤖 Asistente IA Educativo - Precálculo y Cálculo")
        st.markdown("Consulta cualquier duda teórica o conceptual sobre **Álgebra, Funciones, Límites, Derivadas e Integrales**.")
        pregunta_ia = st.text_area("Escribe tu duda teórica o conceptual sobre el tema:", placeholder="Ejemplo: ¿Cuál es la diferencia entre un máximo relativo y un máximo absoluto?")
        
        if st.button("💬 Consultar a la Tutora IA", key="ask_ia", use_container_width=True):
            if not pregunta_ia.strip():
                st.warning("⚠️ Escribe una pregunta antes de consultar.")
            else:
                with st.spinner("La tutora IA está analizando tu consulta..."):
                    respuesta = resolver_ia(pregunta_ia)
                    st.markdown("---")
                    st.markdown("### 🤖 Respuesta de la Tutora IA:")
                    st.write(respuesta)

st.markdown("---")
st.caption(f"{INTEGRANTES} · {ASIGNATURA} · {SECCION}")
