# Generated by Django 4.2.20 on 2025-04-19 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_auto_20250419_1747"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="name",
            field=models.CharField(max_length=300),
        ),
    ]
