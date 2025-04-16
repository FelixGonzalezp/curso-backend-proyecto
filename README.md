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

La API facilita la coordinación entre **organismos sectoriales** y la **autoridad ambiental**, permitiendo:

- Gestión de planes de acción y medidas.
- Asignación de medidas a organismos responsables.
- Reporte de avances e indicadores.
- Acceso restringido según roles (Administrador, OrganismoSectorial).
- Documentación Swagger de todos los endpoints.

---

## Tecnologías Utilizadas

- Python 3.11+
- Django 5.1
- Django REST Framework
- DRF Spectacular (Documentación OpenAPI)
- SQLite (base de datos por defecto)

---

## Estructura del Proyecto

```
django_proyecto/
├── api/                   # App principal con lógica del negocio
│   ├── models.py          # Modelos: Plan, Medida, TipoMedida, etc.
│   ├── views.py           # Vistas de API
│   ├── views_html.py      # Vistas HTML (con autenticación básica)
│   ├── serializers.py     # Serializadores DRF
│   ├── urls.py            # Rutas de la API
│   ├── urls_html.py       # Rutas HTML protegidas
│   ├── templates/         # HTML renderizado con Bootstrap
├── django_proyecto/       # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
├── manage.py              # Comando base de Django
├── requirements.txt       # Paquete y dependencias
├── README.md              # Este archivo
```

---

## Modelos Principales

### `TipoMedida`
- `nombre`, `descripcion`

### `Medida`
- `id_tipo_medida` (FK)
- `indicador`, `forma_calculo`, `frecuencia_reporte`, etc.

### `OrganismoSectorial`
- `nombre`, `tipo`, `contacto`

### `Plan`
- `nombre`, `descripcion`, fechas, `estado`, `responsable`

### `PlanOrganismoSectorial`
- Relaciona un `Plan`, un `OrganismoSectorial` y una `Medida`

### `Reporte`
- `id_plan_organismo_sectorial`, `valor_reportado`, `fecha_reporte`

---

## Roles de Usuario

El sistema distingue entre:

- **Administrador**: Puede crear, editar y ver todos los registros.
- **OrganismoSectorial**: Puede visualizar y reportar medidas asignadas.

---

## Instalación y Ejecución

### 1. Clona el repositorio

```bash
git clone <URL-del-repositorio>
cd django_proyecto
```

### 2. Crea y activa un entorno virtual

```bash
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows
```

### 3. Instala dependencias

```bash
pip install -r requirements.txt
```

### 4. Migraciones y usuario admin

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Ejecuta el servidor

```bash
python manage.py runserver
```

Accede en tu navegador a:
- `http://localhost:8000/` (inicio HTML)
- `http://localhost:8000/admin/` (admin)
- `http://localhost:8000/api/docs/` (Swagger UI)

---

## Endpoints REST Principales

| Recurso                     | Ruta                         | Métodos | Requiere login |
|----------------------------|------------------------------|---------|----------------|
| TipoMedida                 | `/api/tipo-medida/`          | GET, POST | ✅ |
| Medida                     | `/api/medida/`               | GET, POST | ✅ |
| Plan                       | `/api/plan/`                 | GET, POST | ✅ |
| Organismo Sectorial        | `/api/organismo-sectorial/`  | GET, POST | ✅ |
| PlanOrganismoSectorial     | `/api/plan-organismo-sectorial/` | GET, POST | ✅ |
| Reporte                    | `/api/reporte/`              | GET, POST | ✅ |
| Swagger UI                 | `/api/docs/`                 | GET      | ❌ |

---

## Autenticación

La API está protegida mediante:

- **BasicAuthentication** (usuario/contraseña base64)
- **SessionAuthentication** (vía login en Django admin)

**Permisos personalizados por rol** en las vistas:

```python
IsAdministrador
IsOrganismoSectorial
```

---

## Referencias

- [DRF Official Docs](https://www.django-rest-framework.org/)
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/)
- [Bootstrap](https://getbootstrap.com/)
- Resolución Exenta N°1379-2020 (MMA Chile)

---

## Contacto y Créditos

Este proyecto fue desarrollado en el contexto del curso **Backend Python** como parte del avance 3 del proyecto grupal.
Para dudas técnicas o revisión del código, utilizar los canales oficiales del curso o dejar comentarios en la entrega.

---

## Roadmap Académico (Fases)

1. **Avance 1**: Entregado el **15 de febrero de 2025**  
2. **Avance 2**: **9 de abril de 2025** (hasta las 23:55)  
3. **Avance 3**: Entrega programada para **21 de abril de 2025**  
4. **Entrega Final**: **28 de abril de 2025** (antes del inicio de clases)  

> Este roadmap sigue la planificación del curso **Backend Python – Proyecto Grupal (Grupo 4)**.

---

## 🧾 Licencia

```
© 2025 Backend Python – Uso académico. Proyecto desarrollado con fines educativos.
```