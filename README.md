# Sistema de Gestión de Medidas y Planes - Backend API (Django)

## Descripción General
Este proyecto implementa una API RESTful para la gestión de planes, medidas y reportes de cumplimiento asociados a organismos sectoriales, en el marco de la **Resolución Exenta N°1379-2020**.
[Ver en Ley Chile](https://www.bcn.cl/leychile/navegar?idNorma=1148568)


El sistema permite:
- Registrar **planes de acción** y asignarlos a organismos.
- Definir **medidas** con indicadores, frecuencia y forma de cálculo.
- **Reportar avances** y cumplimiento de medidas.
- Gestionar usuarios por **roles (Administrador, OrganismoSectorial)**.
- Consumir la API desde interfaces HTML o clientes REST (como Postman).

---

## Tecnologías Utilizadas

- Python 3.11+
- Django 5.1
- Django REST Framework
- DRF Spectacular (Documentación Swagger/OpenAPI 3.0)
- Bootstrap 5 (Frontend HTML)
- SQLite (modo local)
- PostgreSQL (modo producción, vía **Neon**)
- Despliegue en la nube con **Render**

---

## Estructura del Proyecto

```
django_proyecto/
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py              # API REST (CRUD completo)
│   ├── views_html.py         # Vistas HTML protegidas
│   ├── urls.py               # Rutas de la API
│   ├── urls_html.py          # Rutas HTML
│   ├── templates/            # HTML con Bootstrap
├── django_proyecto/
│   ├── settings.py           # Config local o producción (Render)
│   ├── settings_dev.py
│   ├── urls.py
├── staticfiles/              # Archivos recolectados via collectstatic
├── .env                      # Variables de entorno
├── requirements.txt
├── render.yaml               # Configuración para Render
├── README.md
```

---

## Modelos y Relaciones

- **TipoMedida**: Categorías para medidas.
- **Medida**: Indicador, forma de cálculo, frecuencia, etc.
- **OrganismoSectorial**: Encargados por medida.
- **Plan**: Planes ambientales asignados.
- **PlanOrganismoSectorial**: Relación Plan - Organismo - Medida.
- **Reporte**: Avance en medidas específicas por fecha.

---

## Requisitos de la Entrega Final

Según lo solicitado por el docente, este proyecto incorpora los siguientes puntos clave para la evaluación final:

1. **Pruebas unitarias**: Se implementan tests básicos utilizando el módulo `unittest` y `TestCase` de Django (`tests.py`).
2. **Integración continua**: Configuración de GitHub Actions para ejecutar pruebas automáticamente en cada push.
3. **Despliegue continuo**: Implementación automática en ambiente productivo (`Render`) tras cada actualización en `main`.

> Todo esto se encuentra integrado al repositorio en GitHub.

---

## Autenticación y Roles

El sistema utiliza autenticación mediante:

- **JWT (JSON Web Tokens)** – usando `rest_framework_simplejwt`
- **SessionAuthentication** – útil para navegación desde la interfaz HTML

Además, todos los endpoints requieren autenticación gracias a la configuración global en `REST_FRAMEWORK`.

Se aplican permisos personalizados por tipo de usuario:

- `IsAdministrador`: Acceso total.
- `IsOrganismoSectorial`: Permite ver y reportar.

---

## Instalación y Ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/FelixGonzalezp/curso-backend-proyecto.git
cd curso-backend-proyecto
```

### 2. Crea un entorno virtual y actívalo

```bash
python -m venv env
env\Scripts\activate     # Windows
source env/bin/activate  # Linux/macOS
```

### 3. Instala los requisitos

```bash
pip install -r requirements.txt
```

### 4. Configura variables de entorno

Crea un archivo `.env` con contenido como:

```
DEBUG=True
SECRET_KEY=clave-secreta
PRODUCTION_HOST=curso-backend-proyecto-fgtv.onrender.com
```

### 5. Migraciones y superusuario

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Ejecuta el servidor

```bash
python manage.py runserver
```

---

## Documentación API

Visita:

- `http://localhost:8000/api/docs/` (Swagger UI)

Endpoints están agrupados por:
- Plan
- Medida
- Tipo de medida
- Organismo sectorial
- Reporte
- Relaciones (Plan - Organismo - Medida)

Cada grupo contiene métodos GET, POST, PUT, PATCH y DELETE (según permisos).

---

## Vistas HTML

Accesibles sólo con sesión iniciada:

| Página                 | Ruta               |
|------------------------|--------------------|
| Inicio                 | `/`                |
| Ver Planes             | `/plan/`           |
| Crear Plan             | `/plan/crear/`     |
| Ver Reportes           | `/reportes/`       |
| Crear Reporte          | `/reportes/crear/` |

---

## Despliegue en Render

Este proyecto está listo para producción con Render.

1. Configura `render.yaml` y entorno `.env`
2. Recolecta estáticos:

```bash
python manage.py collectstatic
```

3. Subir a GitHub
4. Render detectará los cambios automáticamente

---

## Estado del Proyecto

✅ CRUD completo  
✅ Swagger agrupado + ejemplos  
✅ Validaciones manuales y mensajes claros  
✅ Interfaz HTML funcional  
✅ Autenticación y roles  
✅ Recolector de estáticos funcionando  

---

## Roadmap Académico

| Fase           | Fecha                | Estado   |
|----------------|----------------------|----------|
| Avance 1       | 15 de febrero de 2025 | ✅ |
| Avance 2       | 9 de abril de 2025    | ✅ |
| **Entrega Final** | **24 de abril de 2025** | 🔜 |

---

## 🧾 Licencia

```
© 2025 Backend Python – Uso académico. Proyecto desarrollado con fines educativos.
```
```

---