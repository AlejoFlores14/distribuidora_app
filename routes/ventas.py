"""
Rutas de ventas
"""
from flask import Blueprint, render_template, request, redirect
from db import conectar

ventas_bp = Blueprint("ventas_bp", __name__)


@ventas_bp.route("/ventas")
def ventas():
    conn = conectar()
    ventas = conn.execute("""
        SELECT 
            v.id AS venta_id,
            v.fecha,
            c.nombre AS cliente_nombre,
            p.codigo AS codigo,
            p.nombre AS nombre,
            vp.cantidad AS cantidad,
            vp.precio_unitario AS precio_unitario,
            (vp.cantidad * vp.precio_unitario) AS subtotal,
            v.total AS total
        FROM ventas v
        LEFT JOIN clientes c ON v.cliente_id = c.id
        INNER JOIN venta_productos vp ON v.id = vp.venta_id
        INNER JOIN productos p ON vp.producto_id = p.id
        ORDER BY v.fecha DESC
    """).fetchall()
    conn.close()

    return render_template("ventas.html", ventas=ventas, page="ventas")


@ventas_bp.route("/agregar_venta", methods=["GET", "POST"])
def agregar_venta():
    conn = conectar()
    productos = conn.execute("SELECT * FROM productos").fetchall()
    clientes = conn.execute("SELECT * FROM clientes").fetchall()

    if request.method == "POST":
        producto_id = int(request.form["producto_id"])
        cantidad = int(request.form["cantidad"])
        cliente_id = int(request.form["cliente_id"]) 
        producto = conn.execute(
            "SELECT * FROM productos WHERE id=?",
            (producto_id,)
        ).fetchone()

        if not producto:
            conn.close()
            return "Producto no existe", 400

        if producto["stock"] < cantidad:
            conn.close()
            return "Stock insuficiente", 400

        total_venta = producto["precio"] * cantidad

        # Crear venta
        conn.execute(
            "INSERT INTO ventas (total, cliente_id) VALUES (?, ?)",
            (total_venta, cliente_id)
        )

        venta_id = conn.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]

        # Insertar detalle
        conn.execute("""
            INSERT INTO venta_productos 
            (venta_id, producto_id, cantidad, precio_unitario)
            VALUES (?, ?, ?, ?)
        """, (venta_id, producto_id, cantidad, producto["precio"]))

        # Actualizar stock
        conn.execute("""
            UPDATE productos 
            SET stock = stock - ?
            WHERE id = ?
        """, (cantidad, producto_id))

        conn.commit()
        conn.close()

        return redirect("/ventas")

    conn.close()
    return render_template("agregar_ventas.html", productos=productos, clientes=clientes, page="agregar_venta")
