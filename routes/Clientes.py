"""
Docstring for routes.Clientes
"""
from flask import Blueprint, render_template, request, redirect
from db import conectar
clientes_bp = Blueprint("clientes_bp", __name__)

@clientes_bp.route("/clientes")
def clientes():
    conn = conectar()
    clientes = conn.execute("SELECT * FROM clientes").fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes, page="clientes")

@clientes_bp.route("/agregar_cliente", methods=["GET", "POST"])
def agregar_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        telefono = request.form["telefono"]
        direccion = request.form["direccion"]
        email = request.form["email"]

        conn = conectar()
        conn.execute("""
            INSERT INTO clientes (nombre, telefono, direccion, email)
            VALUES (?, ?, ?, ?)
        """, (nombre, telefono, direccion, email))

        conn.commit()
        conn.close()

        return redirect("/clientes")

    return render_template("agregar_clientes.html", page="agregar_cliente") 