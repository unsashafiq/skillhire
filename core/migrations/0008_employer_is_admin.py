# Generated by Django 5.2.1 on 2025-05-23 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_supportmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
