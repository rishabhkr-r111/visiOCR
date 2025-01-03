# Generated by Django 5.1.2 on 2024-10-28 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='idinfo',
            name='id_number',
            field=models.CharField(default=1, max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='idinfo',
            name='encrypted_id_number',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='idinfo',
            name='id_type',
            field=models.CharField(max_length=10),
        ),
    ]
