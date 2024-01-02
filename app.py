from flask import Flask, render_template, request, redirect, url_for 
from cassandra.cluster import Cluster  
  
app = Flask(__name__)  
 
# Conexión a Cassandra 
cluster = Cluster(['127.0.0.1'])  # IP de  nodo de Cassandra 
session = cluster.connect('supermarket')  # Reemplaza con tu keyspace 
 
@app.route('/') 
def index(): 
    return render_template('login.html') 
 
@app.route('/', methods=['GET', 'POST']) 
def login(): 
    if request.method == 'POST': 
        # Obtener datos del formulario 
        email = request.form['username'] 
        password = request.form['password'] 
 
        # Realizar consulta a la base de datos Cassandra 
        query = "SELECT * FROM usuarios WHERE email = %s AND password = %s ALLOW FILTERING" 
        rows = session.execute(query, (email, password)) 
 
        # Verificar si los datos coinciden en la base de datos 
        if rows: 
            # Si coincide, redirigir a la página de panel 
            return redirect(url_for('dashboard')) 
        else: 
            # Si no coincide, redirigir nuevamente a la página de login 
            return redirect(url_for('login')) 
 
    # Si el método es GET o si la validación falla, mostrar la página de login 
    return render_template('login') 
 
@app.route('/panel') 
def dashboard(): 
    # Lógica para la página del dashboard 
    return render_template('panel.html') 
 
 
 
if __name__ == '__main__': 
    app.run(debug=True)