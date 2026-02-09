from flask import blueprints, render_template, request, redirect
from db import conectar

productos_bp = blueprints.Blueprint("productos_dp", __name__)

@productos_bp.route("/productos")
def productos():
    conn = conectar()
    producto = conn.execute("SELECT * FROM productos").fetchall()
    for p in producto:
        print(dict(p)) 
    conn.close()
    return render_template("productos.html", productos=producto, page = "productos")

@productos_bp.route("/agregar_productos", methods=["GET", "POST"])
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
    return render_template("agregar_productos.html", page= "agregar_productos")
@productos_bp.route("/editar_producto/<int:producto_id>", methods=["GET", "POST"])
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
@productos_bp.route("/eliminar_producto/<int:producto_id>")
def eliminar_producto(producto_id):
    conn = conectar()
    conn.execute("DELETE FROM productos WHERE id=?", (producto_id,))
    conn.commit()
    conn.close()

    return redirect("/productos")