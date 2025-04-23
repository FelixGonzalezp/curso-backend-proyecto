from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

def create_or_update_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    
    # Verifica si ya existe un superusuario con el nombre de usuario 'admin'
    superuser, created = User.objects.get_or_create(username='admin')
    superuser.email = 'admingrupo4@backendpython.com'
    superuser.password = make_password('123456')
    
    # Si el superusuario ya existe, actualiza su correo y contraseña
    if not created:
        superuser.save()
    else:
        # Si el superusuario no existía, lo crea
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

    # Obtener o crear el grupo 'Administrador'
    administrador_group, _ = Group.objects.get_or_create(name='Administrador')

    # Agregar el superusuario al grupo si no está ya
    if not superuser.groups.filter(name='Administrador').exists():
        superuser.groups.add(administrador_group)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_plan_estado'),
    ]

    operations = [
        migrations.RunPython(create_or_update_superuser),
    ]