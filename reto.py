from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver import Firefox
import time
import requests

from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

driver = webdriver.Firefox(firefox_options=options, executable_path = 'C:/Users/Javier/Downloads/geckodriver.exe')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/colegios'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'reto'


db = SQLAlchemy(app)

class Schools(db.Model):
    nombre = db.Column(db.Text(), primary_key=True, nullable=False)
    calle = db.Column(db.Text(), nullable=False)
    codigo_postal = db.Column(db.Integer, primary_key=True, nullable=False)
    municipio = db.Column(db.Text(), nullable=False)
    provincia = db.Column(db.Text(), nullable=False)
    tipo = db.Column(db.Text(), nullable=False)
    cursos = db.Column(db.Text(), nullable=False)
    telefono = db.Column(db.Text(), nullable=False)
    link_web = db.Column(db.Text(), nullable=False)

    def __init__(self, nombre, calle, codigo_postal, municipio, provincia, tipo, cursos, telefono, link_web):
        self.nombre = nombre
        self.calle = calle
        self.codigo_postal = codigo_postal
        self.municipio = municipio
        self.provincia = provincia
        self.tipo = tipo
        self.cursos = cursos
        self.telefono = telefono
        self.link_web = link_web

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

    queries = Queries.query.all()

    if request.method == 'POST':
        details = request.form
        centro = details['centro']
        ubicacion = details['ubicacion']
        distancia = details['distancia']
        newQuery = Queries(centro, ubicacion, distancia)
        db.session.add(newQuery)
        db.session.commit()

        return render_template('index.html', queries=queries)

    return render_template('index.html', queries=queries)


@app.route('/scraper', methods=['GET', 'POST'])
def scraper():
    
    current = Queries.query.first()
    centro = current.centro
    ubicacion = current.ubicacion
    distancia = str(current.distancia)
    resultado = []

    geolocator = Nominatim(user_agent="find_coords")
    location = geolocator.geocode(ubicacion)
    dir = location.address
    localidad = dir.split(", ")[0]
    latitud = str(location.latitude)
    longitud = str(location.longitude)
    web = 'https://www.scholarum.es/es/buscador-centros/' + localidad + '/' + centro + '%7C' + centro + '/' + latitud + '/' + longitud + '/' + distancia

    # get web page
    driver.get(web)
    # execute script to scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep for 5s
    time.sleep(5)
    # driver.quit()

    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML') 

    #source = requests.get(web).text
    soup = BeautifulSoup(source, 'html.parser')
    a = soup.find_all("div", {"class": "contenido_registro_colegio_descripcion"})
    for tag in a:
        nombre = tag.find("a", {"class": "titulo_colegios_enlace async"}).text.strip()
        link = tag.find("a", {"class": "titulo_colegios_enlace async"})['href']
        calle = tag.find_all("p")[0].text
        cp = int(calle.split("CP ")[1])
        calle_split = calle.split(", ")[0]
        ciudad = tag.find_all("p")[1].text
        municipio = ciudad.split(", ")[0]
        provincia = ciudad.split(", ")[1]
        provincia_split = provincia.lstrip("(").rstrip(")")
        details = requests.get('https://www.scholarum.es'+ link).text
        soup = BeautifulSoup(details, 'html.parser')
        span = soup.find_all("span", {"class": "txt_nor"})
        for data in span:
            if "Enseñanzas" in data.text:
                cursos = data.text.split(": ")[1]
            if "Tipo" in data.text:
                tipo = data.text.split(": ")[1]
            if data.text.startswith("9"):
                telefono = data.text.split("- ")[0]

        link_colegio = soup.find_all("a", {"class": "enlace_web"})[0]['href']

        colegio = Schools(nombre, calle_split, cp, municipio, provincia_split, tipo, cursos, telefono, link_colegio)
        #colegio.calle = calle_split
        existente = Schools.query.filter_by(nombre=nombre, codigo_postal=cp)
        if existente.count() == 0:
            db.session.add(colegio)
            db.session.commit()
        resultado.append(colegio)
        #for res in resultado:
            #res.calle = calle_split 
        
    db.session.delete(current)
    db.session.commit()

    return render_template('resultados.html', colegios=resultado)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)