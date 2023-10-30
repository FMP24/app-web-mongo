from flask import Flask, render_template, request, abort, url_for, redirect, session, flash
app = Flask(__name__)	

from pymongo import MongoClient
from pymongo_get_database import get_database
from functools import wraps
app.secret_key = "my precious"
app.db = "datos"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Acceso no autorizado.')
            return redirect(url_for('login'))
    return wrap

@app.route('/login', methods=['GET','POST'])
def login():
    error=None
    if request.method == 'POST':
        if request.form['username'] != "admin" or request.form['password'] != "admin":
            error="Credenciales Incorrectas."
        else:
            session['logged_in']=True
            flash('Credenciales correctas.')
            return redirect(url_for('tablas'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tablas')
@login_required
def tablas():
    db = get_database('admin', 'admin')
    collections=db.list_collections()
    tablelist=[]
    for collection in collections:
        tablelist.append(collection['name'])
    return render_template('tablas.html', tablelist=tablelist)

@app.route('/tablas/<nombre_tabla>')
@login_required
def coleccion(nombre_tabla):
    db = get_database('admin', 'admin')
    collection = db[nombre_tabla]
    query = collection.find({})
    results = []
    for document in query:
        f_document = {}
        for key, value in document.items():
            f_document[key] = f'{key}: {value}'
        results.append(f_document)
    return render_template('colecciones.html', results=results, nombre_tabla=nombre_tabla)

if __name__ == '__main__':
    app.run("0.0.0.0",5000,debug=True)
