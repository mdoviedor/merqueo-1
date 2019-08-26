# Merqueo Test


## install
- Instalar python3
- Instalar pip3
- clonar el proyecto
  ``
    git clone ...
  ``
- Ubicarse en la carpeta del proyecto
``
  cd merqueo
``
- Install virtualenv
``
  pip3 install virtualenv
``
- Crear virtualenv
 ``
  virtualenv venv
 ``
 - Activar virtualenv
 ``
  source venv/bin/activate
 ``
 - Instalar requerimientos
 ``
  pip install -r requirements.txt
 ``
 - Iniciar el servicio
 ``
  python manage.py runserver 127.0.0.1:8000
 ``

# Cargar datos
- Ejecutar el comando
``
  python manage.py loaddatafromjson
``

# Testing
- Ejecutar el comando
``
  python manage.py test
``
# Documentacion

-- URL api [link](http://ec2-18-224-229-157.us-east-2.compute.amazonaws.com:8000/)
