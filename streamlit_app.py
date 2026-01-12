import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# =============================
# Page Config
# =============================
st.set_page_config(
    page_title="Bisection Solver",
    page_icon="📈",
    layout="centered"
)

# =============================
# Custom Dark Style (CSS)
# =============================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}

.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
}

h1, h2, h3, label {
    color: #f8fafc !important;
}

div[data-baseweb="input"] > div {
    background-color: #1e293b;
}

div[data-baseweb="input"] input {
    color: white;
}

.stButton button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
    border: none;
}

.stButton button:hover {
    transform: scale(1.02);
    transition: 0.2s ease;
}

.block-container {
    padding-top: 2rem;
}

.css-1d391kg {
    background-color: #020617;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Fungsi matematika
# =============================
def f(x, expr):
    return eval(expr, {"x": x, "math": math})

def bisection(expr, a, b, eps, max_iter=100):
    data = []
    i = 1

    if f(a, expr) * f(b, expr) >= 0:
        raise ValueError("f(a) dan f(b) harus berbeda tanda!")

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

# =============================
# Header
# =============================
st.markdown("<h1 style='text-align:center;'>📈 Bisection Method Solver</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8;'>Aplikasi numerik untuk mencari akar persamaan non-linear</p>", unsafe_allow_html=True)

st.markdown("---")

# =============================
# Input Layout
# =============================
col1, col2 = st.columns(2)

with col1:
    fungsi = st.text_input("Fungsi f(x)", "x**3 - x - 2")
    a = st.number_input("Nilai a", value=1.0)

with col2:
    b = st.number_input("Nilai b", value=2.0)
    eps = st.number_input("Toleransi", value=0.0001, format="%.6f")

st.markdown("")

# Tombol tengah
center_btn = st.columns(3)
with center_btn[1]:
    proses = st.button("🚀 Proses Perhitungan", use_container_width=True)

# =============================
# Output
# =============================
if proses:
    try:
        akar, tabel = bisection(fungsi, a, b, eps)
        df = pd.DataFrame(tabel, columns=["Iterasi", "a", "b", "c", "f(c)"])

        st.markdown("### ✅ Hasil Perhitungan")
        st.success(f"Akar persamaan ≈ {akar:.6f}")
        st.info(f"Total iterasi: {len(df)}")

        st.markdown("### 📊 Tabel Iterasi")
        st.dataframe(df, use_container_width=True)

        st.markdown("### 📈 Grafik Fungsi")
        x = np.linspace(a, b, 300)
        y = [f(i, fungsi) for i in x]

        fig, ax = plt.subplots(facecolor="#0f172a")
        ax.set_facecolor("#020617")
        ax.plot(x, y, label="f(x)")
        ax.axhline(0, linestyle="--")
        ax.scatter([akar], [f(akar, fungsi)], label="Akar")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        ax.tick_params(colors="white")
        for spine in ax.spines.values():
            spine.set_color("white")

        st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ Error: {e}")

# =============================
# Footer
# =============================
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#64748b;'>Dibuat dengan Streamlit • Metode Numerik • Bisection</p>",
    unsafe_allow_html=True
)
