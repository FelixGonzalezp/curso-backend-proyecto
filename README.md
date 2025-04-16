# Documentación de la API

## Descripción
Esta API permite gestionar diferentes entidades relacionadas con medidas, organismos sectoriales y planes. Actualmente, solo el endpoint `tipo-medida` está implementado.

<a href="https://github.com/FelixGonzalezp/backend-python-course/blob/main/modulo_4/clase_4/PP2-M4-Clase%204.pdf" target="_blank">Referencia clase Clase4: Django Rest Framework</a>


## Modelos

### TipoMedida
Representa un tipo de medida con las siguientes propiedades:
- `id_tipo_medida` (int): Identificador único.
- `nombre` (str): Nombre de la medida.
- `descripcion` (str): Descripción de la medida.

### Medida
Define una medida específica y está relacionada con un `TipoMedida`.
- `id_media` (int): Identificador único.
- `medida` (str): Nombre de la medida.
- `indicador` (str): Indicador de la medida.
- `forma_calculo` (str): Forma de cálculo de la medida.
- `medida_verificador` (str): Método de verificación.
- `id_tipo_medida` (foreign key): Relación con `TipoMedida`.

### OrganismoSectorial
Representa un organismo sectorial.
- `id_organismo_sectorial` (int): Identificador único.
- `nombre` (str): Nombre del organismo.
- `tipo` (str): Tipo de organismo.
- `contacto` (str): Contacto del organismo.

### Plan
Define un plan con su estado y responsable.
- `id_plan` (int): Identificador único.
- `nombre` (str): Nombre del plan.
- `descripcion` (str): Descripción del plan.
- `fecha_inicio` (date): Fecha de inicio.
- `fecha_termino` (date): Fecha de término.
- `responsable` (str): Responsable del plan.
- `estado` (bool): Estado activo/inactivo.

## Endpoints

### Documentacion
- **URL:** `/api/docs`
- **Método:** `GET`
- **Descripción:** Documentación de la API.

### Home
- **URL:** `/`
- **Método:** `GET`
- **Descripción:** Devuelve una respuesta vacía.
- **Respuesta:**
  ```json
  {}
  ```


### Tipo Medida
- **URL:** `/tipo-medida`
- **Métodos:** `GET`, `POST`
- **Descripción:** Permite obtener todas las `TipoMedida` registradas y agregar nuevas.

#### Obtener lista de tipos de medida
- **Método:** `GET`
- **Respuesta:**
  ```json
  [
    {
      "id_tipo_medida": 1,
      "nombre": "Medida 1",
      "descripcion": "Descripción de la medida 1"
    }
  ]
  ```

#### Crear un nuevo tipo de medida
- **Método:** `POST`
- **Cuerpo de la solicitud:**
  ```json
  {
    "nombre": "Nueva Medida",
    "descripcion": "Descripción de la nueva medida"
  }
  ```
- **Respuesta (201 - Creado):**
  ```json
  {
    "id_tipo_medida": 2,
    "nombre": "Nueva Medida",
    "descripcion": "Descripción de la nueva medida"
  }
  ```
- **Respuesta (400 - Error de validación):**
  ```json
  {
    "nombre": ["Este campo es obligatorio"]
  }
  ```

## Instalación y Ejecución
Para instalar y ejecutar el proyecto, se debe ejecutar el siguiente comando:

```sh
source virtualenv.sh
```

