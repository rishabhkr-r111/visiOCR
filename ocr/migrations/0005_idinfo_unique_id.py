# Generated by Django 5.1.2 on 2024-11-14 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0004_remove_idinfo_vaild_till_idinfo_valid_till'),
    ]

    operations = [
        migrations.AddField(
            model_name='idinfo',
            name='unique_id',
            field=models.CharField(default=1212, max_length=64, unique=True),
            preserve_default=False,
        ),
    ]
