# Generated by Django 3.2.15 on 2022-09-10 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_patient_patient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='emergency_contact_email',
            field=models.EmailField(max_length=255),
        ),
    ]
