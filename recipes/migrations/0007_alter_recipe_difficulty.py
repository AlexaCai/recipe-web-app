# Generated by Django 4.2.6 on 2023-10-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_recipe_difficulty_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(blank=True, editable=False, max_length=20, null=True),
        ),
    ]
