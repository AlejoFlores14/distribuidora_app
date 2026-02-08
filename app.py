""""iniciando flask"""
from flask import Flask, render_template, request, redirect
from db import crear_tablas, conectar
app = Flask(__name__)
crear_tablas()
@app.route("/")
def index():
    return render_template("index.html")
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
@app.route("/editar_producto/<int:producto_id>", methods=["GET", "POST"])
def editar_producto(producto_id):
    conn = conectar()
    if request.method == "POST":
        nombre = request.form["nombre"]
        codigo = request.form["codigo"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        categoria = request.form["categoria"]
        conn.execute(
            """UPDATE productos SET 
            nombre=?, codigo=?, precio=?, stock=?, categoria=? WHERE id=?""",
            (nombre, codigo, precio, stock, categoria, producto_id)
        )
        conn.commit()
        conn.close()
        return redirect("/")
    producto = conn.execute("SELECT * FROM productos WHERE id=?", (producto_id,)).fetchone()
    conn.close()
    return render_template("editar_producto.html", producto=producto)
@app.route("/eliminar_producto/<int:producto_id>")
def eliminar_producto(producto_id):
    conn = conectar()
    conn.execute("DELETE FROM productos WHERE id=?", (producto_id,))
    conn.commit()
    conn.close()
    return redirect("/productos")

if __name__ == '__main__':
    app.run(debug=True)
