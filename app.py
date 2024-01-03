from flask import Flask, render_template, request, redirect, url_for
from cassandra.cluster import Cluster 
 
app = Flask(__name__) 

# Conexión a Cassandra
cluster = Cluster(['127.0.0.1'])  # IP de nodo de Cassandra
session = cluster.connect('supermarket')  # Mi keyspace


#----------------------------------------Rutas
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Lógica para cerrar sesión
    return redirect(url_for('index'))

@app.route('/crear_cliente')
def crear_cliente():
    return render_template('Clientes/create.html')

@app.route('/crear_factura')
def crear_factura():
    return render_template('Facturas/create.html')

@app.route('/crear_producto')
def crear_producto():
    return render_template('Productos/create.html')
#----------------------------------------Rutas


#-----------------------------------------Lógica de login
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
            return redirect(url_for('panel'))
        else:
            # Si no coincide, redirigir nuevamente a la página de login
            return redirect(url_for('login'))

    # Si el método es GET o si la validación falla, mostrar la página de login
    return render_template('login')
#----------------------------------------Lógica de login


#----------------------------------------Lógica de Panel Principal
@app.route('/panel')
def panel():
     
    # Realizar consulta a la base de datos Cassandra
    clients = session.execute("SELECT * FROM clientes")
    products = session.execute("SELECT * FROM productos")

    # Mostrar resultados en una plantilla HTML
    return render_template('panel.html', clients=clients, products=products)

#----------------------------------------Lógica de Panel Principal


#----------------------------------------Lógica de Clientes/Index
@app.route('/clientes')
def clientes_index():

    # Realizar consulta a la base de datos Cassandra
    clients = session.execute("SELECT * FROM clientes")
    
    # Mostrar resultados en una plantilla HTML
    return render_template('clientes/index.html', clients=clients)
#----------------------------------------Lógica de Clientes/Index


#----------------------------------------Lógica de Productos/Index
@app.route('/productos')
def productos_index():

    products = session.execute("SELECT * FROM productos")

    # Mostrar resultados en una plantilla HTML
    return render_template('productos/index.html', products=products)
#----------------------------------------Lógica de Productos/Index


#----------------------------------------Lógica de Facturas/Index
@app.route('/facturas')
def facturas_index():

    bills = session.execute("SELECT * FROM factura")

    # Lógica para la página de facturas
    return render_template('facturas/index.html', bills=bills)
#----------------------------------------Lógica de Facturas/Index


if __name__ == '__main__':
    app.run(debug=True)