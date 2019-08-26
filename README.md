# Merqueo Test


## install
- Instalar python3 y pip
- clonar el proyecto y ubicarse en la carpeta

  ```console
    git clone ...
    cd merqueo
  ```
- Install virtualenv y crear entorno virtual

   ```console
    python3 -m pip install virtualenv
    virtualenv venv
   ```
 - Activar virtualenv
 
     ```console
      source venv/bin/activate
     ```
 - Instalar requerimientos
 
     ```console
      pip install -r requirements.txt
     ```
 - Iniciar el servicio
   
     ```console
      python manage.py runserver 127.0.0.1:8000
     ```

# Cargar datos
Para cargar los datos de los json a la base de datos ejecute el sigiente comando.
```console
    python manage.py loaddatafromjson
```

# Testing
Para ejecutar las pruebas de los servicios ejecute.

```console
  python manage.py test
```

# Documentacion

Documentación y test del API [link](http://ec2-18-224-229-157.us-east-2.compute.amazonaws.com:8000/)

El API cuenta con los servicios CRUD de las entidades Products, Providers, Users, Orders, inventory.
## Otros servicios
| Endpoint                 | Descripción |
| ------------------------ | ----------- |
| /inventory/after         | Lista el Inventartio del dia | 
| /orders/in_inventory/    | productos que puedes ser alistados desde el inventario |
| /orders/{id}/provider/   | Orden con la lista de los productos que pueden ser tomados de inventario y los que deben ser alistados por proveedores |
| /products/best_sellers/  | Productos mas vendidos el dia  |
| /products/less_sold/     | Productos menos vendidos el dia |

## Breve descripcion de la implementacion
El API fue desarrollada con python, usando Django rest framework, Se hizo uso de MySQL como motor de base de datos.
Fue desplegada en Amazon Web Serives, haciendo uso de E2C, la base en el servicio RDC de AWS.
 
## Modelo de capas
![alt Modelo de capas](https://firebasestorage.googleapis.com/v0/b/spartan-concord-243720.appspot.com/o/layerModel.png?alt=media&token=a29d453f-87db-4334-aeee-fffa6c2fb1f8)
### Modelo(ORM)
 Entidades encargadas de gestionar la conexion, peristencia y consulta de informacion de la base de datos.
### Views(ViewSet)
Se encarga de recibir la peticion, ejecutar la logica requerida y serializar los datos para poder dar respuesta.

> **Serializer:**
Se encarga de validar y trasformar los modelos o queryset en listas o dicionarios para poder ser retorn en formato JSON.

>**Logica de negocio:**
Encargada de ejecutar la logica solicitada  en la aplicacion
