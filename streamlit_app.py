import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import math

st.set_page_config(page_title="Bisection Solver", layout="wide")

# =========================
# Safe math environment
# =========================
safe_dict = {
    "x": 0,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "log": math.log,
    "sqrt": math.sqrt,
    "pi": math.pi,
    "e": math.e
}

def f(x, expr):
    safe_dict["x"] = x
    return eval(expr, {"__builtins__": {}}, safe_dict)

def bisection(expr, a, b, eps, max_iter=100):
    if f(a, expr) * f(b, expr) > 0:
        raise ValueError("f(a) dan f(b) harus berbeda tanda!")

    data = []
    i = 1

    while abs(b - a) > eps and i <= max_iter:
        c = (a + b) / 2
        fc = f(c, expr)

        data.append([i, a, b, c, fc])

        if f(a, expr) * fc < 0:
            b = c
        else:
            a = c

        i += 1

    return c, data

# =========================
# UI
# =========================

st.title("⚡ Bisection Method Solver")
st.caption("Aplikasi numerik modern berbasis Streamlit")

col1, col2, col3, col4 = st.columns(4)

with col1:
    fungsi = st.text_input("Fungsi f(x)", "x**3 - x - 2")
with col2:
    a = st.number_input("Nilai a", value=1.0)
with col3:
    b = st.number_input("Nilai b", value=2.0)
with col4:
    eps = st.number_input("Toleransi", value=0.0001, format="%.6f")

st.markdown("")
run = st.button("🚀 Jalankan Perhitungan", use_container_width=True)

if run:
    try:
        akar, tabel = bisection(fungsi, a, b, eps)
        df = pd.DataFrame(tabel, columns=["Iterasi", "a", "b", "c", "f(c)"])

        st.success(f"Akar ≈ {akar:.6f}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Akar", f"{akar:.6f}")
        c2.metric("Iterasi", len(df))
        c3.metric("Toleransi", eps)

        # Grafik
        x = np.linspace(a, b, 300)
        y = [f(i, fungsi) for i in x]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, name="f(x)"))
        fig.add_trace(go.Scatter(x=[akar], y=[f(akar, fungsi)],
                                 mode="markers", marker=dict(size=10),
                                 name="Akar"))

        fig.update_layout(template="plotly_dark", height=500)

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 Tabel Iterasi"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Terjadi error: {e}")
