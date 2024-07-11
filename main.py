from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:12345@localhost/Libreria_tarea"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

##### Models

class Libro(db.Model):
    idLibro = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(45), nullable = False)
    precio = db.Column(db.Float, nullable = False)
    cantidad = db.Column(db.Integer, nullable = False)
    autor = db.Column(db.String(45), nullable = False)
    genero = db.Column(db.String(45), nullable = False)


    def __repr__(self):
        return f'<Libro {self.titulo}>'
    
class Cliente(db.Model):
    idCliente = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(45), nullable = False)
    apellido = db.Column(db.String(45), nullable = False)


    def __repr__(self):
        return f'<Libro {self.Nombre}>'
    

###### Routes Get

@app.route('/libro', methods=['GET'])
def getLibros():
    libros = Libro.query.all()
    libro_list = []
    for libro in libros:
        libro_data = {
            "id": libro.idLibro,
            "Titulo": libro.titulo,
            "Precio": libro.precio,
            "Cantidad": libro.cantidad,
            "Autor": libro.autor,
            "Genero": libro.genero
        }
        libro_list.append(libro_data)
    return jsonify(libro_list), 200

@app.route('/cliente', methods=['GET'])
def getCliente():
    clientes = Cliente.query.all()
    cliente_list = []
    for cliente in clientes:
        cliente_data = {
            "id": cliente.idCliente,
            "Nombre": cliente.nombre,
            "Apellido": cliente.apellido,
        }
        cliente_list.append(cliente_data)
    return jsonify(cliente_list), 200

##### Routes Post

@app.route('/libro', methods=['POST'])
def createLibro():
    titulo = request.json['titulo']
    precio = request.json['precio']
    cantidad = request.json['cantidad']
    autor = request.json['autor']
    genero = request.json['genero']
    
    new_libro = Libro(titulo = titulo, precio = precio, cantidad = cantidad, autor = autor, genero = genero)
    db.session.add(new_libro)
    db.session.commit()
    return jsonify({'message':'libro creado', 'libro': new_libro.idLibro}), 201

@app.route('/cliente', methods=['POST'])
def createCliente():
    nombre = request.json['nombre']
    apellido = request.json['apellido']

    
    new_cliente = Cliente(nombre = nombre , apellido = apellido)
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify({'message':'cliente creado', 'cliente': new_cliente.idCliente}), 201


###### Routes get by ID

@app.route('/libro/<int:idLibro>', methods=['GET'])
def getLibroById(idLibro):
    libro = Libro.query.get(idLibro)
    if libro is None:
        return jsonify({'message': 'Libro not found!'}), 404
    libro_data = {
         "id": libro.idLibro,
         "Titulo": libro.titulo,
         "Precio": libro.precio,
         "Cantidad": libro.cantidad,
         "Autor": libro.autor,
         "Genero": libro.genero
    }
    return jsonify(libro_data), 200

@app.route('/cliente/<int:idCliente>', methods=['GET'])
def getClienteById(idCliente):
    cliente = Cliente.query.get(idCliente)
    if cliente is None:
        return jsonify({'message': 'Cliente not found!'}), 404
    cliente_data = {
         "id": cliente.idCliente,
         "Nombre": cliente.nombre,
         "Apellido": cliente.apellido,
    }
    return jsonify(cliente_data), 200


###### Routes Delete
    
@app.route('/libro/<int:idLibro>', methods=['DELETE'])
def deleteLibro(idLibro):
    libro = Libro.query.get(idLibro)
    if libro is None:
        return jsonify({'message': 'Libro not found!'}), 404
    
    db.session.delete(libro)
    db.session.commit()
    return jsonify({'message': 'Libro deleted!'}), 200

@app.route('/cliente/<int:idCliente>', methods=['DELETE'])
def deleteCliente(idCliente):
    cliente = Cliente.query.get(idCliente)
    if cliente is None:
        return jsonify({'message': 'Cliente not found!'}), 404
    
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente deleted!'}), 200



app.run()