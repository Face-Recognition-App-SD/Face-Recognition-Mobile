# Generated by Django 3.2.15 on 2022-09-07 07:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_date_of_birth'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='stree_address',
            new_name='street_address',
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:'+999999999'. Upto 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
