# Generated by Django 4.1.3 on 2022-12-24 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_contactadmin_email_remove_contactadmin_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
