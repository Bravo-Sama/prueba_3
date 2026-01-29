# Sistema de Gestión de Proyectos API - Evaluación 3

Este proyecto es una API RESTful desarrollada con **Django** y **Django Rest Framework** para la gestión de clientes, proyectos y tareas. Implementa seguridad avanzada mediante **JWT** y lógica de negocio automatizada para el control de progresos.

## 🚀 Características Principales

* **Autenticación Segura**: Implementación de JSON Web Tokens (JWT) para el acceso a endpoints.
* **Roles y Permisos**: Aislamiento de datos donde los clientes solo visualizan sus propios proyectos.
* **Lógica de Negocio**: Cálculo automático del progreso del proyecto basado en el avance de sus tareas.
* **Eliminación Lógica**: Los registros de clientes no se eliminan físicamente, sino que se desactivan para mantener la integridad histórica.
* **Persistencia**: Conexión robusta a base de datos MariaDB/MySQL a través de XAMPP.

## 🛠️ Requisitos previos

* Python 3.12+
* XAMPP (MySQL/MariaDB)
* Virtualenv

## 📦 Instalación y Configuración

1. **Clonar el repositorio**:
   ```bash
   git clone [https://github.com/Bravo-Sama/prueba_3.git](https://github.com/Bravo-Sama/prueba_3.git)
   cd prueba_3
Configurar el entorno virtual:

Bash
python -m venv venv
./venv/Scripts/activate
Instalar dependencias:

Bash
pip install -r requirements.txt
Variables de Entorno: Crea un archivo .env basado en .env.example con tus credenciales de base de datos local.

Migraciones y Superusuario:

Bash
python manage.py migrate
python manage.py createsuperuser
Ejecutar el servidor:

Bash
python manage.py runserver
📊 Estructura de Datos (Modelo Relacional)
La API sigue una estructura jerárquica de cuatro niveles:

Cliente: Entidad principal de la empresa.

Proyecto: Vinculado a un cliente específico.

Tarea: Unidad de trabajo dentro de un proyecto.

SubTarea: Nivel de detalle técnico final.

🧪 Pruebas de API
Se incluye una colección de Postman para probar los siguientes casos:

Obtención de Token (POST /api/token/)

Creación de Clientes y Proyectos (POST)

Validación de rangos de progreso (Error 400)

Eliminación lógica de clientes (DELETE)
