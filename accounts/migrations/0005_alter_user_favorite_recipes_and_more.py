# Generated by Django 4.2.6 on 2023-11-14 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0051_remove_recipe_allergens_recipeallergens'),
        ('accounts', '0004_user_favorite_recipes_user_user_created_recipes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorite_recipes',
            field=models.ManyToManyField(blank=True, default=[], related_name='favorited_by', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_created_recipes',
            field=models.ManyToManyField(blank=True, default=[], related_name='created_by', to='recipes.recipe'),
        ),
    ]
