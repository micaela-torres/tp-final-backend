# IMPORTACION DE FS

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# CREAR APP
app = Flask(__name__)

CORS(app)

# CONFIGURACIÓN A LA BASE DE DATOS

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "mysql+pymysql://mica2111:12345678mica@mica2111.mysql.pythonanywhere-services.com/mica2111$default"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# CREAMOS EL OBJETO DB

db = SQLAlchemy(app)

# OBJETO MA "TRANSFORMA LOS METODOS EN DATOS"

ma = Marshmallow(app)

# DEFINICIÓN DE LA TABLA A PARTIR DE UNA CLASE


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # DEFINIMOS UN CODIGO UNICO
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(400))
    precio = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    imagen = db.Column(db.String(400))

    def __init__(self, id, nombre, descripcion, precio, stock, imagen):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen


# CREAMOS LA TABLA

with app.app_context():
    db.create_all()


class ProductoSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "descripcion", "precio", "stock", "imagen")


# CREAR DOS OBJETOS PARA TRANSFORMAR
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

# CREAR LAS RUTAS PARA: producto


# '/productos' SE VEN TODOS LOS PRODUCTOS
@app.route("/productos", methods=["GET"])
def get_productos():
    all_productos = Producto.query.all()
    return productos_schema.jsonify(all_productos)


@app.route("/productos", methods=["POST"])
def create_producto():
    id = request.json["id"]
    nombre = request.json["nombre"]
    descripcion = request.json["descripcion"]
    precio = request.json["precio"]
    stock = request.json["stock"]
    imagen = request.json["imagen"]

    new_producto = Producto(id, nombre, descripcion, precio, stock, imagen)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)


# '/productos/<id>' VEMOS EL PRODUCTO POR ID


@app.route("/productos/<id>", methods=["GET"])
def get_producto(id):
    producto = Producto.query.get(id)
    return producto_schema.jsonify(producto)


# '/productos/<id>' BORRAMOS UN PRODUCTO POR ID


@app.route("/productos/<id>", methods=["DELETE"])
def delete_producto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)


# '/productos/<id>' MODIFICAMONS UN PRODUCTO POR ID


@app.route("/productos/<id>", methods=["PUT"])
def update_producto(id):
    producto = Producto.query.get(id)
    nombre = request.json["nombre"]
    descripcion = request.json["descripcion"]
    precio = request.json["precio"]
    stock = request.json["stock"]
    imagen = request.json["imagen"]

    producto.id = id
    producto.nombre = nombre
    producto.descripcion = descripcion
    producto.precio = precio
    producto.stock = stock
    producto.imagen = imagen

    db.session.commit()
    return producto_schema.jsonify(producto)


# LEVANTAMOS LA APP

if __name__ == "__main__":
    app.run(debug=True)
