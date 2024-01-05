from flask import Flask, render_template, request, redirect, url_for
from cassandra.cluster import Cluster 
from uuid import UUID
from decimal import Decimal
 
app = Flask(__name__) 

# Conexión a Cassandra
cluster = Cluster(['127.0.0.1'])  # IP de nodo de Cassandra
session = cluster.connect('supermarket')  # Mi keyspace


#----------------------------------------Rutas Estáticas
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
#----------------------------------------Rutas Estáticas


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


#----------------------------------------Lógica de Clientes/Create
@app.route('/formulario_cliente', methods=['GET', 'POST'])
def formulario_cliente():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        cedula = int(request.form['cedula'])
        edad = int(request.form['edad'])
        sexo = request.form['sexo']
        
        # Intentar insertar el cliente
        query_insertar = "INSERT INTO clientes (id, ci, name, last_name, gender, age) VALUES (uuid(), %s, %s, %s, %s, %s)"
        
        # Verificar si la cédula ya existe antes de la inserción
        query_verificar = "SELECT id FROM clientes WHERE ci = %s LIMIT 1"
        cedula_existente = session.execute(query_verificar, (cedula,)).one()
        
        if cedula_existente:
            return redirect(url_for('clientes_index'))  # Redirige a la página de clientes
        
        try:
            session.execute(query_insertar, (cedula, nombres, apellidos, sexo, edad))
        except Exception as e:
            return redirect(url_for('clientes_index'))  # Redirige a la página de clientes
    
    return redirect(url_for('clientes_index'))
#----------------------------------------Lógica de Clientes/Create


#----------------------------------------Lógica de Productos/Create
@app.route('/formulario_producto', methods=['GET', 'POST'])
def formulario_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        unidades = int(request.form['unidades'])
        promocion = request.form['promocion'] == "Sí"  # Convertir la cadena a booleano
        precio = float(request.form['precio'])
        
        # Intentar insertar el producto
        query_insertar = "INSERT INTO productos (id, name, description, stock, promotion, price) VALUES (uuid(), %s, %s, %s, %s, %s)"
        
        try:
            session.execute(query_insertar, (nombre, descripcion, unidades, promocion, precio))
        except Exception as e:
            return redirect(url_for('productos_index'))  # Redirige a la página de productos
        
        return redirect(url_for('productos_index'))  # Redirige a la página de productos
    
    return redirect(url_for('productos_index'))
#----------------------------------------Lógica de Productos/Create


#----------------------------------------Lógica de Eliminación

#--Cliente
@app.route('/eliminar_cliente/<int:ci>', methods=['GET'])
def eliminar_cliente(ci):
   
    # Lógica para eliminar al cliente de la base de datos
    query = "DELETE FROM clientes WHERE ci = %s"
    session.execute(query, (ci,))
    
    # Redirigir al panel una vez eliminado
    return redirect(url_for('panel'))

#--Producto 
@app.route('/eliminar_producto/<string:product_id>', methods=['GET'])
def eliminar_producto(product_id):
    # Convertir el string UUID a un objeto UUID
    product_uuid = UUID(product_id)

    # Realizar la eliminación del producto en la base de datos utilizando el UUID
    query = "DELETE FROM productos WHERE id = %s"
    session.execute(query, (product_uuid,))

    # Redirigir al panel una vez eliminado
    return redirect(url_for('panel'))
#----------------------------------------Lógica de Eliminación


#----------------------------------------Lógica de Clientes/Edit

#--Encontrar la información del cliente y enviarla al formulario edit.html
@app.route('/editar_cliente/<int:ci>', methods=['GET'])
def editar_cliente(ci):
    query_buscar_cliente = "SELECT * FROM clientes WHERE ci = %s LIMIT 1"
    cliente = session.execute(query_buscar_cliente, (ci,)).one()

    if cliente:
        # Si se encontró al cliente, enviar sus datos a la plantilla de edición
        datos_cliente = {
            'id': cliente.id,
            'nombres': cliente.name,
            'apellidos': cliente.last_name,
            'cedula': cliente.ci,
            'edad': cliente.age,
            'sexo': cliente.gender
        }
        return render_template('clientes/edit.html', cliente=datos_cliente)
    
    return redirect(url_for('panel'))

#--Editar la información del encontrado cliente y actulizar en la base de datos
@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    id = UUID(request.form['id'])
    cedula = int(request.form['cedula'])
    nuevo_nombre = request.form['nombres']
    nuevo_apellido = request.form['apellidos']
    nuevo_genero = request.form['sexo']
    nueva_edad = int(request.form['edad'])

    query = "UPDATE clientes SET name = %s, last_name = %s, gender = %s, age = %s WHERE ci = %s AND id = %s"
    session.execute(query, (nuevo_nombre, nuevo_apellido, nuevo_genero, nueva_edad, cedula, id))

    return redirect(url_for('panel'))
#----------------------------------------Lógica de Clientes/Edit


#----------------------------------------Lógica de Productos/Edit

#--Encontrar la información del producto y enviarla al formulario edit.html
@app.route('/editar_producto/<string:product_id>', methods=['GET'])
def editar_producto(product_id):
    id = UUID(product_id)

    query_buscar_producto = "SELECT * FROM productos WHERE id = %s LIMIT 1"
    producto = session.execute(query_buscar_producto, (id,)).one()

    if producto:
        # Si se encontró al cliente, enviar sus datos a la plantilla de edición
        datos_producto = {
            'id': producto.id,
            'nombre': producto.name,
            'descripcion': producto.description,
            'unidades': producto.stock,
            'promocion': producto.promotion,
            'precio': producto.price
        }
        return render_template('productos/edit.html', producto=datos_producto)
    
    return redirect(url_for('panel'))

#--Editar la información del encontrado producto y actulizar en la base de datos
@app.route('/actualizar_producto', methods=['POST'])
def actualizar_producto():
    id = UUID(request.form['id'])
    nuevo_nombre = request.form['nombre']
    nuevo_descripcion = request.form['descripcion']
    nuevo_unidades = int(request.form['unidades'])
    nuevo_promocion = request.form['promocion'] == "Sí"  # Convertir la cadena a booleano
    nueva_precio = Decimal(request.form['precio'])

    # Actualizar la información del producto en la tabla
    query = "UPDATE productos SET name = %s, description = %s, stock = %s, promotion = %s, price = %s WHERE id = %s"
    session.execute(query, (nuevo_nombre, nuevo_descripcion, nuevo_unidades, nuevo_promocion, nueva_precio, id))

    return redirect(url_for('panel'))
#----------------------------------------Lógica de Productos/Edit

#----------------------------------------Lógica de Clientes/Botón Busqueda por Cédula
@app.route('/buscar_cliente', methods=['GET']) 
def buscar_cliente(): 
    cedula = request.args.get('id')  # Obtener la cédula del parámetro GET 
 
    # Realizar la consulta para buscar el cliente por cédula en la base de datos 
    query = "SELECT * FROM clientes WHERE ci = %s" 
    cliente_encontrado = session.execute(query, (int(cedula),)).one() 
 
    if cliente_encontrado: 
        # Si se encuentra el cliente, enviar los datos a la plantilla 
        cliente = { 
            'id': cliente_encontrado.id, 
            'ci': cliente_encontrado.ci, 
            'name': cliente_encontrado.name, 
            'last_name': cliente_encontrado.last_name, 
            'gender': cliente_encontrado.gender, 
            'age': cliente_encontrado.age 
        } 
        return render_template('clientes/index.html', cliente_encontrado=cliente) 
    else: 
        # Si no se encuentra, redirigir a una página de cliente no encontrado y mostrar un mensaje 
        return render_template('clientes/index.html', cliente_encontrado=None) 
#----------------------------------------Lógica de Clientes/Botón Busqueda por Cédula


#----------------------------------------Lógica de Productos/Botón Busqueda por Código
@app.route('/buscar_producto', methods=['GET']) 
def buscar_producto(): 
    codigo_producto = request.args.get('id')  # Obtener el id del parámetro GET

    try:
        id_producto = UUID(codigo_producto)
    except ValueError:
        # Manejar el caso en el que el UUID no sea válido
        return redirect(url_for('productos_index'))

    query = "SELECT * FROM productos WHERE id = %s" 
    producto_encontrado = session.execute(query, (id_producto,)).one()

    if producto_encontrado: 
        # Si se encuentra el producto, enviar los datos a la plantilla 
        producto = { 
            'id': producto_encontrado.id,
            'name': producto_encontrado.name,
            'description': producto_encontrado.description,
            'stock': producto_encontrado.stock,
            'promotion': producto_encontrado.promotion,
            'price': producto_encontrado.price
        } 
        return render_template('productos/index.html', producto_encontrado=producto) 
    else: 
        # Si no se encuentra, redirigir a una página de producto no encontrado y mostrar un mensaje 
        return render_template('productos/index.html', producto_encontrado=None)
#----------------------------------------Lógica de Productos/Botón Busqueda por Código


if __name__ == '__main__':
    app.run(debug=True)