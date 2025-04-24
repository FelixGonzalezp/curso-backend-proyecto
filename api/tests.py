from django.test import TestCase
from .models import TipoMedida, Plan, OrganismoSectorial, Medida, PlanOrganismoSectorial, Reporte
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

username = 'usertest'
password = '123456'

class TipoMedidaModelTest(TestCase):
    def test_str_representation(self):
        """
        Prueba la representación en cadena del modelo TipoMedida.
        """
        tipo = TipoMedida.objects.create(nombre="Ambiental", descripcion="Medida ambiental")
        self.assertEqual(str(tipo), f"{tipo.id} - Ambiental")

class PlanModelTest(TestCase):
    def test_str_representation(self):
        """
        Prueba la representación en cadena del modelo Plan.
        """
        plan = Plan.objects.create(
            nombre="Plan Ambiental",
            descripcion="Control ambiental",
            fecha_inicio="2024-01-01",
            fecha_termino="2024-12-31",
            responsable="Juan Pérez",
            estado="sin_iniciar"
        )
        self.assertEqual(str(plan), f"{plan.id} - Plan Ambiental")

class OrganismoSectorialModelTest(TestCase):
    def test_str_representation(self):
        """
        Prueba la representación en cadena del modelo OrganismoSectorial.
        """
        org = OrganismoSectorial.objects.create(
            nombre="Ministerio del Medio Ambiente",
            tipo="Gobierno",
            contacto="contacto@mma.cl"
        )
        self.assertEqual(str(org), f"{org.id} - Ministerio del Medio Ambiente")

class TipoMedidaApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de TipoMedida.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username=username, password=password)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Agrega el permiso necesario para poder hacer POST
        content_type = ContentType.objects.get_for_model(TipoMedida)
        permission = Permission.objects.get(codename='add_tipomedida', content_type=content_type)
        
        self.admin_user.user_permissions.add(permission)
        
        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin_user.groups.add(grupo)

    def test_api_tipomedida_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de tipo medida.
        """
        response = self.client.get('/api/tipo-medida/')
        self.assertEqual(response.status_code, 401)

    def test_api_tipomedida_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de tipo medida.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/tipo-medida/')
        self.assertIn(response.status_code, [200, 204])
    
    def test_api_tipomedida_post(self):
        """
        Prueba la creación de un tipo medida a través del endpoint de tipo medida.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nombre": "Política pública test",
            "descripcion": "Medidas de política pública generales, normativas o de autorregulación."
        }
        response = self.client.post('/api/tipo-medida/', data)
        self.assertEqual(response.status_code, 201)

class MedidaApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Medida.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username=username, password=password)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Agrega el permiso necesario para poder hacer POST
        # content_type = ContentType.objects.get_for_model(TipoMedida)
        # permission = Permission.objects.get(codename='add_tipomedida', content_type=content_type)
        
        # self.admin_user.user_permissions.add(permission)
        
        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin_user.groups.add(grupo)

    def test_api_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de Medida.
        """
        response = self.client.get('/api/medida/')
        self.assertEqual(response.status_code, 401)

    def test_api_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de Medida.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/medida/')
        self.assertIn(response.status_code, [200, 204])
    
    def test_api_post(self):
        """
        Prueba la creación de un Medida a través del endpoint de Medida.
        """
        # Crear datos relacionados mínimos necesarios
        TipoMedida.objects.create(nombre="Medida Test", descripcion="Desc test")        
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "indicador": "Prueba",
            "forma_calculo": "Prueba",
            "id_tipo_medida": "1",
            "frecuencia_reporte": "Anual",
            "medios_verificacion": "Prueba",
            "nombre_corto": "Prueba",
            "tipo_regilatoria": "Prueba"
        }
        response = self.client.post('/api/medida/', data)
        self.assertEqual(response.status_code, 201)

class OrganismoSectorialApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Organizmo sectorial.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username=username, password=password)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Agrega el permiso necesario para poder hacer POST
        # content_type = ContentType.objects.get_for_model(TipoMedida)
        # permission = Permission.objects.get(codename='add_tipomedida', content_type=content_type)
        
        # self.admin_user.user_permissions.add(permission)
        
        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin_user.groups.add(grupo)

    def test_api_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de Organizmo sectorial.
        """
        response = self.client.get('/api/organismo-sectorial/')
        self.assertEqual(response.status_code, 401)

    def test_api_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de Organizmo sectorial.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/organismo-sectorial/')
        self.assertIn(response.status_code, [200, 204])
    
    def test_api_post(self):
        """
        Prueba la creación de un Organizmo sectorial a través del endpoint de Organizmo sectorial.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nombre": "CONAF",
            "tipo": "Público",
            "contacto": "consulta.oirs@conaf.cl"
        }
        response = self.client.post('/api/organismo-sectorial/', data)
        self.assertEqual(response.status_code, 201)

class PlanApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Plan.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username=username, password=password)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        content_type = ContentType.objects.get_for_model(Plan)
        permission = Permission.objects.get(codename='add_plan', content_type=content_type)
        self.admin_user.user_permissions.add(permission)

        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin_user.groups.add(grupo)

    def test_api_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de plan.
        """
        response = self.client.get('/api/plan/')
        self.assertEqual(response.status_code, 401)

    def test_api_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de plan.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/plan/')
        self.assertIn(response.status_code, [200, 204])

    def test_api_post(self):
        """
        Prueba la creación de un plan a través del endpoint de plan.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "nombre": "Plan de Prueba",
            "descripcion": "Prueba de creación desde test",
            "fecha_inicio": "2024-04-01",
            "fecha_termino": "2024-12-31",
            "responsable": "Test User",
            "estado": "sin_iniciar"
        }
        response = self.client.post('/api/plan/', data)
        self.assertEqual(response.status_code, 201)

class PlanOrganismoSectorialApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Plan Organismo Sectorial.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username=username, password=password)
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        content_type = ContentType.objects.get_for_model(Plan)
        permission = Permission.objects.get(codename='add_plan', content_type=content_type)
        self.admin_user.user_permissions.add(permission)

        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin_user.groups.add(grupo)

    def test_api_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de plan Organismo Sectorial.
        """
        response = self.client.get('/api/plan-organismo-sectorial/')
        self.assertEqual(response.status_code, 401)

    def test_api_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de plan Organismo Sectorial.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/plan-organismo-sectorial/')
        self.assertIn(response.status_code, [200, 204])

    def test_api_post_error_parametros(self):
        """
        Prueba la creación de un plan Organismo Sectorial a través del endpoint de plan Organismo Sectorial.
        """
        
        # Crear datos relacionados mínimos necesarios
        tipo = TipoMedida.objects.create(nombre="Medida Test", descripcion="Desc test")
        Medida.objects.create(
            id_tipo_medida=tipo,
            nombre_corto="Med Test",
            indicador="Ind 1",
            forma_calculo="Suma",
            frecuencia_reporte="Mensual",
            medios_verificacion="Doc",
            tipo_regulatoria="Norma"
        )
        OrganismoSectorial.objects.create(nombre="Org Test", tipo="Público", contacto="org@test.cl")
        Plan.objects.create(
            nombre="Plan Test",
            descripcion="Test",
            fecha_inicio="2024-01-01",
            fecha_termino="2024-12-31",
            responsable="Tester",
            estado="sin_iniciar"
        )
        
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "id_plan": 1,
            "id_organismo_sectorial": 1,
            "id_media": [1, 3]
        }
        response = self.client.post('/api/plan-organismo-sectorial/', data)
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.data)
        self.assertIn('id_media', response.data['detail'])

    def test_api_post(self):
        """
        Prueba la creación de un plan Organismo Sectorial a través del endpoint de plan Organismo Sectorial.
        """
        
        # Crear datos relacionados mínimos necesarios
        tipo = TipoMedida.objects.create(nombre="Medida Test", descripcion="Desc test")
        Medida.objects.create(
            id_tipo_medida=tipo,
            nombre_corto="Med Test",
            indicador="Ind 1",
            forma_calculo="Suma",
            frecuencia_reporte="Mensual",
            medios_verificacion="Doc",
            tipo_regulatoria="Norma"
        )
        OrganismoSectorial.objects.create(nombre="Org Test", tipo="Público", contacto="org@test.cl")
        Plan.objects.create(
            nombre="Plan Test",
            descripcion="Test",
            fecha_inicio="2024-01-01",
            fecha_termino="2024-12-31",
            responsable="Tester",
            estado="sin_iniciar"
        )
        
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "id_plan": 1,
            "id_organismo_sectorial": 1,
            "id_media": [1]
        }
        response = self.client.post('/api/plan-organismo-sectorial/', data)
        self.assertEqual(response.status_code, 201)

class ReporteApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Reporte.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username=username, password=password)
        self.user.is_staff = True
        self.user.save()

        content_type = ContentType.objects.get_for_model(Reporte)
        permiso = Permission.objects.get(codename='add_reporte', content_type=content_type)
        self.user.user_permissions.add(permiso)

        grupo, _ = Group.objects.get_or_create(name='OrganismoSectorial')
        self.user.groups.add(grupo)

        # Crear datos relacionados mínimos necesarios
        self.tipo = TipoMedida.objects.create(nombre="Medida Test", descripcion="Desc test")
        self.medida = Medida.objects.create(
            id_tipo_medida=self.tipo,
            nombre_corto="Med Test",
            indicador="Ind 1",
            forma_calculo="Suma",
            frecuencia_reporte="Mensual",
            medios_verificacion="Doc",
            tipo_regulatoria="Norma"
        )
        self.org = OrganismoSectorial.objects.create(nombre="Org Test", tipo="Público", contacto="org@test.cl")
        self.plan = Plan.objects.create(
            nombre="Plan Test",
            descripcion="Test",
            fecha_inicio="2024-01-01",
            fecha_termino="2024-12-31",
            responsable="Tester",
            estado="sin_iniciar"
        )
        self.relacion = PlanOrganismoSectorial.objects.create(
            id_plan=self.plan,
            id_organismo_sectorial=self.org,
            id_media=self.medida
        )

    def test_api_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de reporte.
        """
        response = self.client.get('/api/reporte/')
        self.assertEqual(response.status_code, 401)

    def test_api_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de reporte.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/reporte/')
        self.assertIn(response.status_code, [200, 204])

    def test_api_post(self):
        """
        Prueba la creación de un reporte a través del endpoint de reporte.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "id_plan_organismo_sectorial": self.relacion.id,
            "valor_reportado": 85.5,
            "evidencia": "url de evidencia",
            "fecha_reporte": "2024-04-15"
        }
        response = self.client.post('/api/reporte/', data)
        self.assertEqual(response.status_code, 201)
