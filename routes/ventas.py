from flask import blueprints, render_template

ventas_bp = blueprints.Blueprint("ventas_bp", __name__)
@ventas_bp.route("/ventas")
def ventas():
    return render_template("ventas.html", page = "ventas")
@ventas_bp.route("/agregar_venta", methods=["GET", "POST"])
def agregar_venta():
    return render_template("agregar_venta.html", page = "agregar_venta")