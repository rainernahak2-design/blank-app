from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def f(x, expr):
    return eval(expr, {"x": x, "math": math})

def bisection(expr, a, b, eps=0.0001, max_iter=100):
    hasil_iterasi = []
    iterasi = 0

    while abs(b - a) > eps and iterasi < max_iter:
        c = (a + b) / 2
        fa = f(a, expr)
        fc = f(c, expr)

        hasil_iterasi.append((iterasi+1, a, b, c, fc))

        if fa * fc < 0:
            b = c
        else:
            a = c

        iterasi += 1

    return c, hasil_iterasi

def buat_grafik(expr, akar, a, b):
    x_vals = [a + i*(b-a)/200 for i in range(201)]
    y_vals = [f(x, expr) for x in x_vals]

    plt.figure()
    plt.plot(x_vals, y_vals)
    plt.axhline(0)
    plt.scatter([akar], [f(akar, expr)])
    plt.title("Grafik f(x) dan Akar")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)

    # Simpan ke memory sebagai base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

@app.route("/", methods=["GET", "POST"])
def index():
    hasil = None
    tabel = []
    grafik = None

    if request.method == "POST":
        fungsi = request.form["fungsi"]
        a = float(request.form["a"])
        b = float(request.form["b"])
        eps = float(request.form["eps"])

        hasil, tabel = bisection(fungsi, a, b, eps)
        grafik = buat_grafik(fungsi, hasil, a, b)

    return render_template("index.html", hasil=hasil, tabel=tabel, grafik=grafik)

if __name__ == "__main__":
    app.run(debug=True)
