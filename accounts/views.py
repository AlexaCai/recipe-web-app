from django.shortcuts import render, redirect, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserAdminCreationForm, UserCreatePrivateRecipe, RecipeIngredientsFormSet, RecipeAllergensFormSet, RecipeCookingInstructionsFormSet
from recipes.models import Recipe, RecipeIngredients

def signup_view(request):
    if request.method == 'POST':
        # Form taken from forms.py
        form = UserAdminCreationForm(request.POST) 

        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        
        else:
            print("User creation failed")
            print(form.errors)
            
    else:
        # Form taken from forms.py
        form = UserAdminCreationForm()  

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    error_message = None
    # Default Django form for handling user authentication
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("recipes:recipes_list_signed_users")
            
        else:
            error_message = "ooops.. something went wrong"

    # Prepare data to send from view.py to template.html
    context = {"form": form, "error_message": error_message}
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')


def delete_account(request):
    if not request.user.is_authenticated:
    # Redirect to the home page if user try to go back on the delete account page after moving from it
        return redirect('recipes:home')

    user = request.user
    logout(request)
    user.delete()
    return render(request, 'accounts/account-deleted.html')


# Function to display the user's profile page information
@login_required
def profile_view(request):
    favorite_recipes = favorite_list(request)
    created_recipes = created_recipe(request)
    form = UserCreatePrivateRecipe()
    formset = RecipeIngredientsFormSet(prefix='formset')
    allergens_formset = RecipeAllergensFormSet(prefix='allergens')
    cooking_instructions_formset = RecipeCookingInstructionsFormSet(prefix='cooking_instructions')

    return render(
        request,
        'accounts/profile.html',
        {
            'favorite_recipes': favorite_recipes,
            'created_recipes': created_recipes,
            'form': form,
            'formset': formset,
            'allergens_formset': allergens_formset,
            'cooking_instructions_formset': cooking_instructions_formset,
        }
    )


# Used to add or remove recipes from the user's favorites.
def favorite_add(request, id):
    recipe = get_object_or_404(Recipe, id=id)

    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
    else:
        recipe.favorites.add(request.user)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# Used to display recipes that are favorited by user.
def favorite_list(request):
    favorites = request.user.favorites.all()
    favorite_recipes = Recipe.objects.filter(favorites=request.user)
    return favorite_recipes


# Used to display recipes that are created by user.
def created_recipe(request):
    created_recipes = request.user.created_recipes.all()
    return created_recipes


def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    recipe.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def user_private_recipe_new(request):
    if request.method == "POST":
        form = UserCreatePrivateRecipe(request.POST, request.FILES)
        formset = RecipeIngredientsFormSet(request.POST, prefix='formset')
        allergens_formset = RecipeAllergensFormSet(request.POST, prefix='allergens')
        cooking_instructions_formset = RecipeCookingInstructionsFormSet(request.POST, prefix='cooking_instructions')

        if form.is_valid() and formset.is_valid() and allergens_formset.is_valid() and cooking_instructions_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            formset.instance = recipe
            formset.save()

            allergens_formset.instance = recipe
            allergens_formset.save()

            cooking_instructions_formset.instance = recipe
            cooking_instructions_formset.save()

            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        
        else:
            print(form.errors)
            print(formset.errors)
            print(allergens_formset.errors)
            print(cooking_instructions_formset.errors)

    else:
        form = UserCreatePrivateRecipe()
        formset = RecipeIngredientsFormSet(prefix='formset')
        allergens_formset = RecipeAllergensFormSet(prefix='allergens')
        cooking_instructions_formset = RecipeCookingInstructionsFormSet(prefix='cooking_instructions')

    return render(request, 'accounts/profile.html', {'form': form, 'formset': formset, 'allergens_formset': allergens_formset, 'cooking_instructions_formset': cooking_instructions_formset})