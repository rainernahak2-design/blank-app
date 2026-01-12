# Grafik dengan matplotlib (tanpa plotly)
fig, ax = plt.subplots()
ax.plot(x, y, label="f(x)")
ax.axhline(0, linestyle="--")
ax.scatter([akar], [f(akar, fungsi)], label="Akar")
ax.set_title("Grafik Fungsi")
ax.legend()

st.pyplot(fig)
