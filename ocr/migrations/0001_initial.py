# Generated by Django 5.1.2 on 2024-10-28 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IDInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_type', models.CharField(max_length=12)),
                ('name', models.CharField(max_length=100)),
                ('dob', models.CharField(max_length=10)),
                ('encrypted_id_number', models.CharField(max_length=512)),
            ],
        ),
    ]
