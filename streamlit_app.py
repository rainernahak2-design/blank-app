import streamlit as st
import math
import numpy as np
import matplotlib.pyplot as plt

def f(x, expr):
    return eval(expr, {"x": x, "math": math})

def bisection(expr, a, b, eps):
    while abs(b - a) > eps:
        c = (a + b) / 2
        if f(a, expr) * f(c, expr) < 0:
            b = c
        else:
            a = c
    return c

st.title("Bisection Method + Grafik")

fungsi = st.text_input("Fungsi", "x**3 - x - 2")
a = st.number_input("a", value=1.0)
b = st.number_input("b", value=2.0)
eps = st.number_input("Toleransi", value=0.0001)

if st.button("Proses"):
    akar = bisection(fungsi, a, b, eps)

    x = np.linspace(a, b, 200)
    y = [f(i, fungsi) for i in x]

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(0)
    ax.scatter([akar], [f(akar, fungsi)])
    st.pyplot(fig)

    st.success(f"Akar ≈ {akar}")
