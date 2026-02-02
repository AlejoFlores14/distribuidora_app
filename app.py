""""iniciando flask"""
from flask import Flask, render_template, request, redirect
from db import crear_tablas, conectar
app = Flask(__name__)
crear_tablas()
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/productos")
def productos():
    conn = conectar()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    for p in productos:
        print(dict(p))
    conn.close()
    return render_template("productos.html", productos=productos)

@app.route("/agregar_productos", methods=["GET", "POST"])
def agregar_productos():
    if request.method == "POST":
        nombre = request.form["nombre"]
        codigo = request.form["codigo"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        categoria = request.form["categoria"]
        conn = conectar()
        conn.execute(
            """INSERT INTO productos (nombre, codigo, precio, stock, categoria) 
            VALUES (?, ?, ?, ?, ?)""",(nombre, codigo, precio, stock, categoria)
        )
        conn.commit()
        conn.close()
        return redirect("/productos")
    return render_template("agregar_productos.html")


if __name__ == '__main__':
    app.run(debug=True)
