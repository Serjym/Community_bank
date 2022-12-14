# Generated by Django 4.1.4 on 2022-12-19 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_contactadmin_email_remove_contactadmin_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmmaryDataBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='Subject name')),
                ('file', models.FileField(upload_to='', verbose_name='summary files')),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
