# Sistema de Gestión de Supermercado

Este es un sistema de gestión de supermercado desarrollado con Flask y Cassandra. Permite la gestión de clientes, productos y facturas.

## Requisitos

Asegúrate de tener instalado Python 3.10.6 y las bibliotecas necesarias. Puedes instalarlas ejecutando:

```bash
pip install flask cassandra-driver
```

## Configuración

1. Asegúrate de tener un nodo de Cassandra ejecutándose en `127.0.0.1`.
2. Crea un keyspace llamado `supermarket` en tu base de datos Cassandra.
3. Ejecuta la aplicación Flask con el siguiente comando:

```bash
python app.py
```

## Configuración de la Base de Datos

Este proyecto utiliza DataStax DevCenter versión 1.6 como herramienta de gestión de Cassandra. Asegúrate de tener instalado DataStax DevCenter antes de ejecutar la aplicación.

## Creación de Tablas en Cassandra

A continuación se presentan las consultas para crear las tablas necesarias en Cassandra. Puedes utilizar estas consultas en DataStax DevCenter o cualquier otra herramienta de administración de Cassandra.

1. **Tabla de Clientes:**
    ```cql
    CREATE TABLE supermarket.clientes (
      ci int,
      id uuid,
      name text,
      last_name text,
      gender text,
      age int,
      PRIMARY KEY (ci, id)
    );
    ```

2. **Tabla de Usuarios:**
    ```cql
    CREATE TABLE supermarket.usuarios (
      id uuid,
      email varchar,
      password varchar,
      PRIMARY KEY (id)
    );
    ```

3. **Tabla de Facturas:**
    ```cql
    CREATE TABLE supermarket.facturas (
      id uuid,
      ci_cliente int,
      name_cliente text,
      last_name_cliente text,
      name_producto text,
      description_producto text,
      promotion_producto boolean,
      amount decimal,
      date text,
      payment_method text,
      id_producto uuid,
      PRIMARY KEY (id, ci_cliente, id_producto)
    );
    ```

4. **Tabla de Productos:**
    ```cql
    CREATE TABLE supermarket.productos (
      id uuid,
      name text,
      description text,
      stock int,
      promotion boolean,
      price decimal,
      PRIMARY KEY (id)
    );
    ```

Asegúrate de tener una instancia de Cassandra ejecutándose y configurada correctamente con las claves y el espacio de nombres mencionados en el código de la aplicación.

## Estructura del Código

La aplicación cuenta con las siguientes rutas para la gestión de usuarios:

- **Inicio (/):** Página de inicio que contiene el formulario de inicio de sesión.

- **Panel (/panel):** Panel principal que proporciona información detallada sobre clientes, productos y facturas.

- **Clientes (/clientes):** Lista de clientes registrados en la base de datos.

- **Productos (/productos):** Lista de productos disponibles en el supermercado.

- **Facturas (/facturas):** Lista de facturas generadas.

- **Crear Cliente (/crear_cliente):** Formulario para agregar un nuevo cliente a la base de datos.

- **Crear Producto (/crear_producto):** Formulario para agregar un nuevo producto al inventario.

- **Crear Factura (/crear_factura):** Formulario para generar una nueva factura.

Adicionalmente, se han implementado funcionalidades para:

- **Editar Cliente:** Permite actualizar la información de un cliente existente.

- **Eliminar Cliente:** Elimina un cliente de la base de datos.

- **Editar Producto:** Permite realizar cambios en la información de un producto.

- **Eliminar Producto:** Elimina un producto de la base de datos.

- **Buscar Cliente:** Realiza una búsqueda por cédula para encontrar información detallada de un cliente.

- **Buscar Producto:** Busca un producto por código para mostrar detalles.

- **Buscar Factura:** Busca una factura por código o cédula de cliente para mostrar detalles.

- **Producto Más Vendido:** Muestra el producto más vendido en base a las facturas generadas.

Todas estas funcionalidades están implementadas para proporcionar una experiencia completa de gestión de clientes, productos y facturas.

## Créditos

Desarrollado por Antonietta Palazzo y Kevin Herrera.
