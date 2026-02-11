""""iniciando flask"""
from flask import Flask,render_template
from db import crear_tablas
from routes.products import productos_bp
from routes.ventas import ventas_bp
from routes.Clientes import clientes_bp
app = Flask(__name__)
crear_tablas()

app.register_blueprint(productos_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(clientes_bp)

@app.route("/")
def index():
    """
    index
    """
    return render_template("index.html", page = "inicio")



if __name__ == '__main__':
    app.run(debug=True)
