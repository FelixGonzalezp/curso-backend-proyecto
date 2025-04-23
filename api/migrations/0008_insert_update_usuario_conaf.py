from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

def create_or_update_user(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    
    # Verifica si ya existe un superusuario con el nombre de usuario 'conaf'
    user, created = User.objects.get_or_create(username='conaf')
    user.email = 'conaf@backendpython.com'
    user.password = make_password('123456')
    
    # Si el usuario ya existe, actualiza su correo y contraseña
    user.save()

    # Obtener o crear el grupo 'OrganismoSectorial'
    user_group, _ = Group.objects.get_or_create(name='OrganismoSectorial')

    # Agregar el suario al grupo si no está ya
    if not user.groups.filter(name='OrganismoSectorial').exists():
        user.groups.add(user_group)

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_insert_update_superadmin'),
    ]

    operations = [
        migrations.RunPython(create_or_update_user),
    ]
