from django.contrib import admin
from .models import Recipe, RecipeIngredients, RecipeAllergens, RecipeCookingInstructions, RecipeToolsNeeded, RecipeSimilarComplementary, RecipeComments

class RecipeIngredientsInline(admin.TabularInline):
    model = RecipeIngredients
    extra = 1

class RecipeAllergensInline(admin.TabularInline):
    model = RecipeAllergens
    extra = 1

class RecipeCookingInstructionsInline(admin.TabularInline):
    model = RecipeCookingInstructions
    extra = 1

class RecipeToolsNeededInline(admin.TabularInline):
    model = RecipeToolsNeeded
    extra = 1

class RecipeSimilarComplementaryInline(admin.TabularInline):
    model = RecipeSimilarComplementary
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientsInline, RecipeAllergensInline, RecipeCookingInstructionsInline, RecipeToolsNeededInline, RecipeSimilarComplementaryInline] 
    readonly_fields = ('difficulty', 'creation_date', 'recipe_url', 'recipe_url_signed_users')
    list_display = ('recipe_name', 'user', 'creation_date', 'is_public')  

    fieldsets = (
        ('Recipe basic information', {
            'fields': ('recipe_name', 'user', 'is_public', 'description','special_note', 'cooking_time', 'number_of_portions', 'origin_country', 'recipe_category', 'recipe_estimated_cost', 'pic'),
        }),
        ('Automatic fields (values generated automatically after recipe creation)', {
            'fields': ('difficulty', 'creation_date', 'recipe_url', 'recipe_url_signed_users')
        }),
    )

class RecipeCommentsAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'text', 'created_at')
    list_filter = ('recipe', 'user', 'created_at')
    search_fields = ('recipe__recipe_name', 'user__username', 'text')
    date_hierarchy = 'created_at'

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeComments, RecipeCommentsAdmin)
