from django.db import migrations
from django.contrib.auth.hashers import make_password


def seed_admin_password(apps, schema_editor):
    AdminSettings = apps.get_model('admin_panel', 'AdminSettings')
    AdminSettings.objects.create(
        admin_password=make_password('admin1234')
    )


def reverse_seed(apps, schema_editor):
    AdminSettings = apps.get_model('admin_panel', 'AdminSettings')
    AdminSettings.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_admin_password, reverse_seed),
    ]