# Generated by Django 4.2.6 on 2023-12-17 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_user_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='_is_active',
            new_name='is_active',
        ),
    ]
