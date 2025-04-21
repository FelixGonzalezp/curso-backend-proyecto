from django.test import TestCase
from .models import TipoMedida, Plan, OrganismoSectorial, Medida, PlanOrganismoSectorial, Reporte
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

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
        self.admin_user = User.objects.create_user(username='admin', password='123456')
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        # Agrega el permiso necesario para poder hacer POST
        content_type = ContentType.objects.get_for_model(TipoMedida)
        permission = Permission.objects.get(codename='add_tipomedida', content_type=content_type)
        self.admin_user.user_permissions.add(permission)

class ReporteApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Reporte.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='organismo', password='123456')
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

    def test_api_reporte_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de reporte.
        """
        response = self.client.get('/api/reporte/')
        self.assertEqual(response.status_code, 401)

    def test_api_reporte_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de reporte.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/reporte/')
        self.assertIn(response.status_code, [200, 204])

    def test_api_reporte_post(self):
        """
        Prueba la creación de un reporte a través del endpoint de reporte.
        """
        self.client.force_authenticate(user=self.user)
        data = {
            "id_plan_organismo_sectorial": self.relacion.id,
            "valor_reportado": 85.5,
            "fecha_reporte": "2024-04-15"
        }
        response = self.client.post('/api/reporte/', data)
        self.assertEqual(response.status_code, 201)

class PlanApiTest(TestCase):

    def setUp(self):
        """
        Configura el entorno de prueba para los tests de la API de Plan.
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_user(username='admin2', password='123456')
        self.admin_user.is_superuser = True
        self.admin_user.is_staff = True
        self.admin_user.save()

        content_type = ContentType.objects.get_for_model(Plan)
        permission = Permission.objects.get(codename='add_plan', content_type=content_type)
        self.admin_user.user_permissions.add(permission)

        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin_user.groups.add(grupo)

    def test_api_plan_get_sin_autenticacion(self):
        """
        Prueba el acceso no autenticado al endpoint de plan.
        """
        response = self.client.get('/api/plan/')
        self.assertEqual(response.status_code, 401)

    def test_api_plan_get_con_autenticacion(self):
        """
        Prueba el acceso autenticado al endpoint de plan.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/plan/')
        self.assertIn(response.status_code, [200, 204])

    def test_api_plan_post(self):
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


from django.contrib.auth.models import Permission

class ValidacionErrorTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(username='admin3', password='123456', is_staff=True, is_superuser=True)

        # ⚠️ Agregarlo al grupo correcto
        grupo, _ = Group.objects.get_or_create(name='Administrador')
        self.admin.groups.add(grupo)

        self.client.force_authenticate(user=self.admin)

    def test_tipo_medida_post_falla_por_falta_de_datos(self):
        data = {"descripcion": "Falta nombre"}
        response = self.client.post('/api/tipo-medida/', data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('nombre', str(response.data))


class PermisosDenegadosTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='usuario_normal', password='123456')

    def test_usuario_sin_grupo_no_puede_postear_plan(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "nombre": "Plan Invalido",
            "descripcion": "No debería poder crearse",
            "fecha_inicio": "2024-04-01",
            "fecha_termino": "2024-12-31",
            "responsable": "Alguien",
            "estado": True
        }
        response = self.client.post('/api/plan/', data)
        self.assertEqual(response.status_code, 403)
        self.assertIn('No tiene permisos', str(response.data))