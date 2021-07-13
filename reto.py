from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/colegios'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'reto'

db = SQLAlchemy(app)

class Colegio(db.Model):
    nombre = db.Column(db.Text(), primary_key=True, nullable=False)
    direccion = db.Column(db.Text(), primary_key=True, nullable=False)
    tipo = db.Column(db.Text(), nullable=False)
    cursos = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, direccion, tipo, cursos, telefono):
        self.nombre = nombre
        self.direccion = direccion
        self.tipo = tipo
        self.cursos = cursos
        self.telefono = telefono

    def __repr__(self):
        return '<Colegio %r>' % self.nombre

class Queries(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    centro = db.Column(db.Text())
    ubicacion = db.Column(db.Text(), nullable=False)
    distancia = db.Column(db.Integer, nullable=False)

    def __init__(self, centro, ubicacion, distancia):
        self.centro = centro
        self.ubicacion = ubicacion
        self.distancia = distancia

    def __repr__(self):
        return '<Query %r>' % self.centro


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        details = request.form
        centro = details['centro']
        ubicacion = details['ubicacion']
        distancia = details['distancia']
        newQuery = Queries(centro, ubicacion, distancia)
        db.session.add(newQuery)
        db.session.commit()
        db.session.close()

        return render_template('index.html')

    return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)