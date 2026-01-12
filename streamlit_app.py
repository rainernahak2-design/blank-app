import streamlit as st
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Bisection Solver",
    page_icon="⚡",
    layout="wide"
)

# ======================
# CUSTOM CSS (PREMIUM UI)
# ======================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top left, #0f172a, #020617);
    color: white;
}

.hero {
    text-align: center;
    padding: 2rem 1rem;
}

.hero h1 {
    font-size: 3rem;
    background: linear-gradient(to right, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #94a3b8;
    font-size: 1.1rem;
}

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1.5rem;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

.stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 14px;
    height: 50px;
    font-weight: 600;
    border: none;
}

.stButton button:hover {
    transform: scale(1.03);
    transition: 0.2s ease;
}
</style>
""", unsafe_allow_html=True)

# ======================
# MATH FUNCTIONS
# ======================
def f(x, expr):
    return eval(expr, {"x": x, "math": math})

def bisection(expr, a, b, eps, max_iter=100):
    data = []
    i = 1

    if f(a, expr) * f(b, expr) >= 0:
        raise ValueError("f(a) dan f(b) harus berbeda tanda")

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

# ======================
# HERO SECTION
# ======================
st.markdown("""
<div class="hero">
    <h1>⚡ Bisection Method Solver</h1>
    <p>Web app numerik modern untuk mencari akar persamaan non-linear</p>
</div>
""", unsafe_allow_html=True)

# ======================
# INPUT CARD
# ======================
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        fungsi = st.text_input("Fungsi f(x)", "x**3 - x - 2")
    with col2:
        a = st.number_input("Nilai a", value=1.0)
    with col3:
        b = st.number_input("Nilai b", value=2.0)
    with col4:
        eps = st.number_input("Toleransi", value=0.0001, format="%.6f")

    tengah = st.columns(3)
    with tengah[1]:
        proses = st.button("🚀 Jalankan Perhitungan", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ======================
# OUTPUT
# ======================
if proses:
    try:
        akar, tabel = bisection(fungsi, a, b, eps)
        df = pd.DataFrame(tabel, columns=["Iterasi", "a", "b", "c", "f(c)"])

        st.markdown("## 📊 Hasil Perhitungan")

        m1, m2, m3 = st.columns(3)
        m1.metric("Akar", f"{akar:.6f}")
        m2.metric("Iterasi", len(df))
        m3.metric("Toleransi", eps)

        # Grafik interaktif (Plotly)
        x = np.linspace(a, b, 400)
        y = [f(i, fungsi) for i in x]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="f(x)"))
        fig.add_trace(go.Scatter(
            x=[akar], 
            y=[f(akar, fungsi)], 
            mode="markers",
            marker=dict(size=12),
            name="Akar"
        ))

        fig.update_layout(
            template="plotly_dark",
            title="Grafik Fungsi",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📄 Lihat Tabel Iterasi"):
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# ======================
# FOOTER
# ======================
st.markdown("""
<p style='text-align:center; color:#64748b; margin-top:40px;'>
Built with ❤️ using Python & Streamlit — Numerical Method Project
</p>
""", unsafe_allow_html=True)
