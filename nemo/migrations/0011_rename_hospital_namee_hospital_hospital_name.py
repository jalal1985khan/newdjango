# Generated by Django 4.2 on 2023-05-13 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0010_rename_hospital_name_hospital_hospital_namee'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hospital',
            old_name='hospital_namee',
            new_name='hospital_name',
        ),
    ]
