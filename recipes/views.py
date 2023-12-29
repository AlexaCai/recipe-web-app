from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Recipe, RecipeComments, RecipeIngredients, RecipeAllergens, RecipeCookingInstructions, RecipeToolsNeeded, RecipeSimilarComplementary
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import SearchAllergensForm, UserSubmitRecipe, RecipeIngredientsForm, RecipeAllergensForm, RecipeCookingInstructionsForm, RecipeToolsForm, RecipeSimilarComplementaryForm
from django.forms import inlineformset_factory
import pandas as pd
from django.db.models import Q
from .utils import get_chart
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.mail import EmailMessage



# Functions used to return appropriate views/html template for the recipes app depending on
# the URL
def home(request):
    return render(request, "recipes/home.html")

def about(request):
    return render(request, "recipes/about.html")

class RecipeListViewUnsignedUsers(ListView):
    model = Recipe
    template_name = "recipes/unsigned_users_recipes.html"
    context_object_name = "recipes"

def make_recipe_name_clickable_unsigned_detail(row):
    recipe = Recipe.objects.get(pk=row['id'])
    recipe_url = recipe.get_absolute_url()
    difficulty = recipe.calculate_difficulty()
    return f'<a href="{recipe_url}">{row["recipe_name"]}</a> (Difficulty: {difficulty})'

def unsigned_user_redirect_recipes_list_page(request):
    form = SearchAllergensForm(request.POST or None)
    recipes_df = None
    chart = None

    if request.method == 'POST':
        if form.is_valid():
            allergens_input = request.POST.get('allergens')
            chart_type = request.POST.get('chart_type')
            print(allergens_input, chart_type)

            allergens_list = [allergen.strip() for allergen in allergens_input.split(',')]

            allergen_queries = Q()

            for allergen in allergens_list:
                allergen_query = Q(recipe_allergens__allergen__icontains=allergen)
                allergen_queries |= allergen_query

            qs = Recipe.objects.exclude(allergen_queries).values(
                'id', 'recipe_name', 'origin_country', 'cooking_time', 'recipe_category', 'recipe_estimated_cost')
            
            if qs:
                recipes_df = pd.DataFrame(qs)
                recipes_df['recipe_name'] = recipes_df.apply(make_recipe_name_clickable_unsigned_detail, axis=1)
                chart = get_chart(chart_type, recipes_df, labels=recipes_df['recipe_category'].values)
                recipes_df = recipes_df.to_html(escape=False)

    view = RecipeListViewUnsignedUsers()
    view.queryset = Recipe.objects.all()
    recipes = view.get_queryset()

    context = {
        'form': form,
        'object_list': recipes,
        'recipes_df': recipes_df,
        'chart': chart

    }
    return render(request, 'recipes/unsigned_users_recipes.html', context)

def make_recipe_name_clickable_signed_detail(row):
    recipe = Recipe.objects.get(pk=row['id'])
    recipe_url_signed_users = recipe.get_absolute_url_signed_users()
    difficulty = recipe.calculate_difficulty()
    return f'<a href="{recipe_url_signed_users}">{row["recipe_name"]}</a> (Difficulty: {difficulty})'

class RecipeListViewSignedUsers(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = "recipes/signed_users_recipes.html"

@login_required
def signed_user_redirect_recipes_list_page(request):
    form = SearchAllergensForm(request.POST or None)
    recipes_df = None
    chart = None

    if request.method == 'POST':
        if form.is_valid():
            allergens_input = request.POST.get('allergens')
            chart_type = request.POST.get('chart_type')
            print(allergens_input, chart_type)

            allergens_list = [allergen.strip() for allergen in allergens_input.split(',')]

            allergen_queries = Q()

            for allergen in allergens_list:
                allergen_query = Q(recipe_allergens__allergen__icontains=allergen)
                allergen_queries |= allergen_query

            qs = Recipe.objects.exclude(allergen_queries).values(
                'id', 'recipe_name', 'origin_country', 'cooking_time', 'recipe_category', 'recipe_estimated_cost')
            
            if qs:
                recipes_df = pd.DataFrame(qs)
                recipes_df['recipe_name'] = recipes_df.apply(make_recipe_name_clickable_signed_detail, axis=1)
                chart = get_chart(chart_type, recipes_df, labels=recipes_df['recipe_category'].values)
                recipes_df = recipes_df.to_html(escape=False)


    view = RecipeListViewSignedUsers()
    view.queryset = Recipe.objects.all()
    recipes = view.get_queryset()

    context = {
        'form': form,
        'object_list': recipes,
        'recipes_df': recipes_df,
        'chart': chart

    }
    return render(request, 'recipes/signed_users_recipes.html', context)

class RecipeDetailViewUnsignedUsers(DetailView):
    model = Recipe
    template_name = "recipes/unsigned_users_recipes_details.html"

def unsigned_user_redirect_recipes_detailed_page(request, pk):
    view = RecipeDetailViewUnsignedUsers.as_view()
    return view(request, pk=pk)

class RecipeDetailViewSignedUsers(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "recipes/signed_users_recipes_details.html"

@login_required
def signed_user_redirect_recipes_detailed_page(request, pk):
    view = RecipeDetailViewSignedUsers.as_view()
    return view(request, pk=pk)



# Takes the request coming from the web app on recipes that are searched by name \
# and returns the JSON response containing the recipes that match the search query.
def search_recipes_by_name(request):
    search_query = request.GET.get("query")
    matching_recipes = Recipe.objects.filter(recipe_name__icontains=search_query)

    recipes_json = [
        {
            "recipe_name": recipe.recipe_name,
            "recipe_origin_country": recipe.origin_country,
            "recipe_difficulty": recipe.difficulty,
            "recipe_category": recipe.recipe_category,
            "recipe_url": recipe.get_absolute_url(),
            "recipe_url_signed_users": recipe.get_absolute_url_signed_users(),
            "pic": recipe.pic.url,
        }
        for recipe in matching_recipes
    ]

    print(recipes_json)
    return JsonResponse({"recipes": recipes_json})


# Takes the request coming from the web app on recipes that are searched by filters \
# and returns the JSON response containing the recipes that match the search query.
def search_recipes_by_filters(request):
    search_query1 = request.GET.get("query1")
    search_query2 = request.GET.get("query2")
    search_query3 = request.GET.get("query3")
    search_query4 = request.GET.get("query4")

    # Initialize the queryset with all recipes
    matching_recipes = Recipe.objects.all()

    if search_query1:
        matching_recipes = matching_recipes.filter(
            origin_country__icontains=search_query1
        )

    if search_query2:
        matching_recipes = matching_recipes.filter(
            recipe_category__icontains=search_query2
        )

    if search_query3:
        if search_query3 == "1":
            matching_recipes = matching_recipes.filter(cooking_time__lte=15)
        elif search_query3 == "2":
            matching_recipes = matching_recipes.filter(cooking_time__lte=30)
        elif search_query3 == "3":
            matching_recipes = matching_recipes.filter(cooking_time__lte=45)
        elif search_query3 == "4":
            matching_recipes = matching_recipes.filter(cooking_time__lte=60)
        elif search_query3 == "5":
            matching_recipes = matching_recipes.filter(cooking_time__gt=60)

    if search_query4:
        if search_query4 == "1":
            matching_recipes = matching_recipes.filter(recipe_estimated_cost__lte=5)
        elif search_query4 == "2":
            matching_recipes = matching_recipes.filter(recipe_estimated_cost__lte=10)
        elif search_query4 == "3":
            matching_recipes = matching_recipes.filter(recipe_estimated_cost__lte=20)
        elif search_query4 == "4":
            matching_recipes = matching_recipes.filter(recipe_estimated_cost__lte=30)
        elif search_query4 == "5":
            matching_recipes = matching_recipes.filter(recipe_estimated_cost__gt=30)

    recipes_json = [
        {
            "recipe_name": recipe.recipe_name,
            "recipe_origin_country": recipe.origin_country,
            "recipe_difficulty": recipe.difficulty,
            "recipe_category": recipe.recipe_category,
            "recipe_url": recipe.get_absolute_url(),
            "recipe_url_signed_users": recipe.get_absolute_url_signed_users(),
            "pic": recipe.pic.url,
        }
        for recipe in matching_recipes
    ]

    return JsonResponse({"recipes": recipes_json})


# Takes the request coming from the web app on recipes that are searched by ingredients
# and returns the JSON response containing the recipes that match the search query.
def search_recipes_by_ingredients(request):
    # Retrieves the 'query' parameter from the GET request
    search_query = request.GET.get("query")
    # Splits the search query (a comma-separated list of ingredients) into individual ingredients \
    # and stores them in a list called 'ingredients'. The strip() is used to remove \
    # any leading or trailing whitespaces from each ingredient.
    ingredients = [ingredient.strip() for ingredient in search_query.split(",")]

    # Retrieves all recipes that contain the first ingredient in the ingredients list.
    matching_recipes = Recipe.objects.filter(
        recipe_ingredients__ingredient_name__icontains=ingredients[0]
    )

    # Code iterates over the remaining ingredients of the list (if any) using a for loop.
    # 'for ingredient in ingredients[1:]:' iterates over each ingredient in the list, skipping the \
    # first one.
    for ingredient in ingredients[1:]:
        # For each ingredient in the loop, it further filters the recipes to find those containing \
        # the current ingredient.
        matching_recipes = matching_recipes.filter(
            recipe_ingredients__ingredient_name__icontains=ingredient
        )

    # distinct() method is used to remove duplicates recipes if one recipe contains more than one \
    # of the same ingredient in his list (e.g.: a recipe contains both 'granulated sugar' and \
    # 'powdered sugar' in its ingredients list, and the user searches for 'sugar'). With dinstinct() \
    # the recipe will only appear once in the search results instead of twice.
    matching_recipes = matching_recipes.distinct()

    recipes_json = [
        {
            "recipe_name": recipe.recipe_name,
            "recipe_origin_country": recipe.origin_country,
            "recipe_difficulty": recipe.difficulty,
            "recipe_category": recipe.recipe_category,
            "recipe_url": recipe.get_absolute_url(),
            "recipe_url_signed_users": recipe.get_absolute_url_signed_users(),
            "pic": recipe.pic.url,
        }
        for recipe in matching_recipes
    ]

    return JsonResponse({"recipes": recipes_json})

# Logic to allow users to add comments to recipes
def publish_comment(request, pk):
    if request.method == 'POST':
        comment_text = request.POST.get('comment') 
        recipe = Recipe.objects.get(pk=pk)
        recipe.comments.create(text=comment_text, user=request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def delete_comment(request, id):
    comment = get_object_or_404(RecipeComments, id=id)
    comment.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def update_comment(request, id):
    comment = get_object_or_404(RecipeComments, id=id)
    comment.text = request.POST.get('comment')
    comment.updated_at = timezone.now() 
    comment.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# Logic allowing users to submit a recipe by email via the web app (submit recipe page)
def user_submit_recipe(request):
    RecipeIngredientsFormSet = inlineformset_factory(Recipe, RecipeIngredients, form=RecipeIngredientsForm, extra=1, can_delete=True)
    RecipeAllergensFormSet = inlineformset_factory(Recipe, RecipeAllergens, form=RecipeAllergensForm, extra=1, can_delete=True)
    RecipeCookingInstructionsFormSet = inlineformset_factory(Recipe, RecipeCookingInstructions, form=RecipeCookingInstructionsForm, extra=1, can_delete=True)
    RecipeToolsFormSet = inlineformset_factory(Recipe, RecipeToolsNeeded, form=RecipeToolsForm, extra=1, can_delete=True)
    RecipeSimilarComplementaryFormSet = inlineformset_factory(Recipe, RecipeSimilarComplementary, form=RecipeSimilarComplementaryForm, extra=1, can_delete=True)

    if request.method == 'POST':
        form = UserSubmitRecipe(request.POST, request.FILES)
        formset = RecipeIngredientsFormSet(request.POST, request.FILES, prefix='ingredients')
        allergens_formset = RecipeAllergensFormSet(request.POST, request.FILES, prefix='allergens')
        cooking_instructions_formset = RecipeCookingInstructionsFormSet(request.POST, request.FILES, prefix='cooking_instructions')
        recipe_tools_formset = RecipeToolsFormSet(request.POST, request.FILES, prefix='recipe_tools')
        recipe_similar_complementary_formset = RecipeSimilarComplementaryFormSet(request.POST, request.FILES, prefix='recipe_similar_complementary')


        if form.is_valid() and formset.is_valid() and allergens_formset.is_valid() and cooking_instructions_formset.is_valid() and recipe_tools_formset.is_valid() and recipe_similar_complementary_formset.is_valid():
            recipe_name = form.cleaned_data['recipe_name']
            description = form.cleaned_data['description']
            special_note = form.cleaned_data['special_note']
            cooking_time = form.cleaned_data['cooking_time']
            number_of_portions = form.cleaned_data['number_of_portions']
            recipe_estimated_cost = form.cleaned_data['recipe_estimated_cost']
            origin_country = form.cleaned_data['origin_country']
            recipe_category = form.cleaned_data['recipe_category']
            pic = form.cleaned_data['pic']

            ingredients = [
                {
                    'ingredient_name': form.cleaned_data['ingredient_name'],
                    'quantity': form.cleaned_data['quantity'],
                    'unit_of_measurement': form.cleaned_data['unit_of_measurement'],
                    'possible_substitute': form.cleaned_data['possible_substitute'],
                    'substitute_special_note': form.cleaned_data['substitue_special_note']
                } for form in formset if form.cleaned_data
]
            
            allergens = [
                {
                    'allergen': form.cleaned_data['allergen']
                } for form in allergens_formset if form.cleaned_data
]
            
            cooking_instructions = [
                {
                    'step_name': form.cleaned_data['step_name'],
                    'step_instruction': form.cleaned_data['step_instruction']
                } for form in cooking_instructions_formset if form.cleaned_data
]
            
            recipe_tools = [
                {
                    'cooking_tool_name': form.cleaned_data['cooking_tool_name']
                } for form in recipe_tools_formset if form.cleaned_data
]
            
            recipe_similar_complementary = [
                {
                    'complementary_recipe_name': form.cleaned_data['complementary_recipe_name'],
                    'complementary_recipe_link_unsigned_users': form.cleaned_data['complementary_recipe_link_unsigned_users']
                } for form in recipe_similar_complementary_formset if form.cleaned_data
]
            
            html = render_to_string('recipes/user_submit_recipe_email.html', {
                'recipe_name': recipe_name, 
                'description': description, 
                'special_note': special_note, 
                'cooking_time': cooking_time, 
                'number_of_portions': number_of_portions, 
                'recipe_estimated_cost': recipe_estimated_cost,
                'origin_country': origin_country,
                'recipe_category': recipe_category,
                'pic': pic,
                'ingredients': ingredients,
                'allergens': allergens,
                'cooking_instructions': cooking_instructions,
                'recipe_tools': recipe_tools,
                'recipe_similar_complementary': recipe_similar_complementary
                })

            email = EmailMessage(
                f'New recipe submitted from {request.user.email if request.user.is_authenticated else "Unsigned user"}',
                html,
                'atablespoonofdiscovery@gmail.com',
                ['atablespoonofdiscovery@gmail.com'],
            )
            email.content_subtype = 'html'

            if 'pic' in request.FILES:
                email.attach(request.FILES['pic'].name, request.FILES['pic'].read())

            email.send()

            return redirect('recipes:user_submitted_recipe_success')
        else:
            return redirect('recipes:user_submitted_recipe_failed')
        
    else:
        form = UserSubmitRecipe()
        formset = RecipeIngredientsFormSet(prefix='ingredients')
        allergens_formset = RecipeAllergensFormSet(prefix='allergens')
        cooking_instructions_formset = RecipeCookingInstructionsFormSet(prefix='cooking_instructions')
        recipe_tools_formset = RecipeToolsFormSet(prefix='recipe_tools')
        recipe_similar_complementary_formset = RecipeSimilarComplementaryFormSet(prefix='recipe_similar_complementary')

    return render(request, "recipes/user_submit_recipe.html",{
        'form': form,
        'formset': formset,
        'allergens_formset': allergens_formset,
        'cooking_instructions_formset': cooking_instructions_formset,
        'recipe_tools_formset': recipe_tools_formset,
        'recipe_similar_complementary_formset': recipe_similar_complementary_formset
    })
