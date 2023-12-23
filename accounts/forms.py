from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from recipes.models import Recipe, RecipeIngredients, RecipeAllergens, RecipeCookingInstructions
from django.contrib.auth.forms import PasswordResetForm

User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):

    # Form for creating new users. Includes all the required fields, plus a repeated password.
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'email']

    def clean(self):
        
        # Verify both passwords match.
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):

    # Form for updating users. Includes all the fields on the user, but replaces the password field
    # with admin's password hash display field.
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'is_active', 'admin']

    def clean_password(self):
        return self.initial["password"]
    
class RegisterForm(forms.ModelForm):
    
    # Form for creating new users. Includes all the required fields, plus a repeated password.
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['full_name', 'email']

    def clean(self):
        
        # Verify both passwords match.
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_active = False 
        if commit:
            user.save()
        return user
    
# Used to customize the fields that are required when users want to reset their passwords.
class MyPasswordResetForm(PasswordResetForm):
    
    new_password1 = forms.CharField(
        label="Enter new password",
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label="Enter new password confirmation",
        widget=forms.PasswordInput,
    )
    
unit_measure_choices = (
    ("ml - milliliter", "ml - Milliliter"),
    ("fl oz - fluid ounce", "fl oz - Fluid Ounce"),
    ("tbsp - tablespoon", "tbsp - Tablespoon"),
    ("tsp - teaspoon", "tsp - Teaspoon"),
    ("L - liter", "L - Liter"),
    ("pt - pint", "pt - Pint"),
    ("g - gram", "g - Gram"),
    ("oz - ounce", "oz - Ounce"),
    ("lb - pound", "lb - Pound"),
    ("kg - kilogram", "kg - Kilogram"),
    ("cup", "Cup"),
    ("unit", "Unit"),
    ("units", "Units"),
    ("to taste", "To Taste"),
)
    
country_choices = (
    ("afghan", "Afghan"),
    ("albanian", "Albanian "),
    ("algerian", "Algerian"),
    ("american", "American"),
    ("andorran", "Andorran"),
    ("angolan", "Angolan"),
    ("argentine", "Argentine"),
    ("armenian", "Armenian"),
    ("australian", "Australian"),
    ("austrian", "Austrian"),
    ("azerbaijani", "Azerbaijani"),
    ("bahamian", "Bahamian"),
    ("bahraini", "Bahraini"),
    ("bangladeshi", "Bangladeshi"),
    ("barbadian", "Barbadian"),
    ("belarusian", "Belarusian"),
    ("belgian", "Belgian"),
    ("belizean", "Belizean"),
    ("beninese", "Beninese"),
    ("bhutanese", "Bhutanese"),
    ("bolivian", "Bolivian"),
    ("bosnian", "Bosnian"),
    ("botswanan", "Botswanan"),
    ("brazilian", "Brazilian"),
    ("british", "British"),
    ("bruneian", "Bruneian"),
    ("bulgarian", "Bulgarian"),
    ("burkinabe", "Burkinabe"),
    ("burmese", "Burmese"),
    ("burundian", "Burundian"),
    ("cambodian", "Cambodian"),
    ("cameroonian", "Cameroonian"),
    ("canadian", "Canadian"),
    ("cape verdean", "Cape Verdean"),
    ("central african", "Central African"),
    ("chadian", "Chadian"),
    ("chilean", "Chilean"),
    ("chinese", "Chinese"),
    ("colombian", "Colombian"),
    ("comoran", "Comoran"),
    ("congolese", "Congolese"),
    ("costa rican", "Costa Rican"),
    ("croatian", "Croatian"),
    ("cuban", "Cuban"),
    ("cyprio", "Cyprio"),
    ("czech", "Czech"),
    ("danish", "Danish"),
    ("djiboutian", "Djiboutian"),
    ("dominican", "Dominican"),
    ("dominican rep.", "Dominican Rep."),
    ("dutch", "Dutch"),
    ("east timorese", "East Timorese"),
    ("ecuadorian", "Ecuadorian"),
    ("egyptian", "Egyptian"),
    ("emirati", "Emirati"),
    ("equ. guinean", "Equ. Guinean"),
    ("eritrean", "Eritrean"),
    ("estonian", "Estonian"),
    ("ethiopian", "Ethiopian"),
    ("fijian", "Fijian"),
    ("filipino", "Filipino"),
    ("finnish", "Finnish"),
    ("french", "French"),
    ("gabonese", "Gabonese"),
    ("gambian", "Gambian"),
    ("georgian", "Georgian"),
    ("german", "German"),
    ("ghanaian", "Ghanaian"),
    ("greek", "Greek"),
    ("grenadian", "Grenadian"),
    ("guatemalan", "Guatemalan"),
    ("guinean", "Guinean"),
    ("guinea-bi.", "Guinea-Bi."),
    ("guyanese", "Guyanese"),
    ("haitian", "Haitian"),
    ("honduran", "Honduran"),
    ("hungarian", "Hungarian"),
    ("icelandic", "Icelandic"),
    ("indian", "Indian"),
    ("indonesian", "Indonesian"),
    ("iranian", "Iranian"),
    ("iraqi", "Iraqi"),
    ("irish", "Irish"),
    ("israeli", "Israeli"),
    ("italian", "Italian"),
    ("ivorian", "Ivorian"),
    ("jamaican", "Jamaican"),
    ("japanese", "Japanese"),
    ("jordanian", "Jordanian"),
    ("kazakhstani", "Kazakhstani"),
    ("kenyan", "Kenyan"),
    ("kiribatian", "Kiribatian"),
    ("kuwaiti", "Kuwaiti"),
    ("kyrgyz", "Kyrgyz"),
    ("laotian", "Laotian"),
    ("latvian", "Latvian"),
    ("lebanese", "Lebanese"),
    ("lesotho", "Lesotho"),
    ("liberian", "Liberian"),
    ("libyan", "Libyan"),
    ("liechtensteiner", "Liechtensteiner"),
    ("lithuanian", "Lithuanian"),
    ("luxembourgish", "Luxembourgish"),
    ("macedonian", "Macedonian"),
    ("malagasy", "Malagasy"),
    ("malawian", "Malawian"),
    ("malaysian", "Malaysian"),
    ("maldivian", "Maldivian"),
    ("malian", "Malian"),
    ("maltese", "Maltese"),
    ("marshallese", "Marshallese"),
    ("mauritanian", "Mauritanian"),
    ("mauritian", "Mauritian"),
    ("mexican", "Mexican"),
    ("micronesian", "Micronesian"),
    ("moldovan", "Moldovan"),
    ("monegasque", "Monegasque"),
    ("mongolian", "Mongolian"),
    ("montenegrin", "Montenegrin"),
    ("moroccan", "Moroccan"),
    ("mozambican", "Mozambican"),
    ("namibian", "Namibian"),
    ("nauruan", "Nauruan"),
    ("nepalese", "Nepalese"),
    ("new zealand", "New Zealand"),
    ("nicaraguan", "Nicaraguan"),
    ("niger", "Niger"),
    ("nigerian", "Nigerian"),
    ("north korean", "North Korean"),
    ("norwegian", "Norwegian"),
    ("omani", "Omani"),
    ("pakistani", "Pakistani"),
    ("palauan", "Palauan"),
    ("palestinian", "Palestinian"),
    ("panamanian", "Panamanian"),
    ("papua new gui.", "Papua New Gui."),
    ("paraguayan", "Paraguayan"),
    ("peruvian", "Peruvian"),
    ("polish", "Polish"),
    ("portuguese", "Portuguese"),
    ("qatari", "Qatari"),
    ("romanian", "Romanian"),
    ("russian", "Russian"),
    ("rwandan", "Rwandan"),
    ("st kitts & nevis", "St Kitts & Nevis"),
    ("saint lucian", "Saint Lucian"),
    ("st vincent & grenadines", "St Vincent & Grenadines"),
    ("salvadoran", "Salvadoran"),
    ("sammarinese", "Sammarinese"),
    ("samoan", "Samoan"),
    ("sao tomean", "Sao Tomean"),
    ("saudi arabian", "Saudi Arabian"),
    ("senegalese", "Senegalese"),
    ("serbian", "Serbian"),
    ("seychellois", "Seychellois"),
    ("sierra leonean", "Sierra Leonean"),
    ("singaporean", "Singaporean"),
    ("slovak", "Slovak"),
    ("slovenian", "Slovenian"),
    ("solomon islands", "Solomon Islands"),
    ("somali", "Somali"),
    ("south african", "South African"),
    ("south korean", "South Korean"),
    ("south sudanese", "South Sudanese"),
    ("spanish", "Spanish"),
    ("sri lankan", "Sri Lankan"),
    ("sudanese", "Sudanese"),
    ("surinamese", "Surinamese"),
    ("swazi", "Swazi"),
    ("swedish", "Swedish"),
    ("swiss", "Swiss"),
    ("syrian", "Syrian"),
    ("taiwanese", "Taiwanese"),
    ("tajik", "Tajik"),
    ("tanzanian", "Tanzanian"),
    ("thai", "Thai"),
    ("togolese", "Togolese"),
    ("tongan", "Tongan"),
    ("trinidadian & tobagonian", "Trinidadian & Tobagonian"),
    ("tunisian", "Tunisian"),
    ("turkish", "Turkish"),
    ("turkmen", "Turkmen"),
    ("tuvaluan", "Tuvaluan"),
    ("ugandan", "Ugandan"),
    ("ukrainian", "Ukrainian"),
    ("uruguayan", "Uruguayan"),
    ("uzbek", "Uzbek"),
    ("vanuatuan", "Vanuatuan"),
    ("venezuelan", "Venezuelan"),
    ("vietnamese", "Vietnamese"),
    ("yemeni", "Yemeni"),
    ("zambian", "Zambian"),
    ("zimbabwean", "Zimbabwean"),
    ("no category", "No Category"),
    ("mixed", "Mixed"),
)

category_choices = (
    ("appetizer", "Appetizer"),
    ("baked", "Baked"),
    ("breakfast", "Breakfast"),
    ("brunch", "Brunch"),
    ("cafe/tea", "Cafe/Tea"),
    ("condiment", "Condiment"),
    ("dinner", "Dinner"),
    ("dessert", "Dessert"),
    ("drink/cocktail", "Drink/Cocktail"),
    ("fish", "Fish"),
    ("fruit", "Fruit"),
    ("holiday", "Holiday"),
    ("hot beverage", "Hot beverages"),
    ("juice", "Juice"),
    ("lunch", "Lunch"),
    ("meat", "Meat"),
    ("pasta", "Pasta"),
    ("salad", "Salad"),
    ("sandwhich", "Sandwhich"),
    ("sauce", "Sauce"),
    ("seafood", "Seafood"),
    ("side", "Side"),
    ("smoothie/shake", "Smoothie/Shake"),
    ("snack", "Snack"),
    ("soup", "Soup"),
    ("vegan", "Vegan"),
    ("vegetable", "Vegetable"),
    ("vegetarian", "Vegetarian"),
)

class UserCreatePrivateRecipe(forms.ModelForm):
    recipe_name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    special_note = forms.CharField(widget=forms.Textarea, required=False)
    cooking_time = forms.IntegerField(required=True)
    number_of_portions = forms.IntegerField(required=True)
    recipe_estimated_cost = forms.DecimalField(required=True, max_digits=5, decimal_places=2)
    origin_country = forms.ChoiceField(choices=country_choices, required=False, widget=forms.Select(attrs={'id': 'id_origin_country_update'}))
    recipe_category = forms.ChoiceField(choices=category_choices, required=False, widget=forms.Select(attrs={'id': 'id_recipe_category_update'}))
    pic = forms.ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ['recipe_name', 'cooking_time', 'description', 'special_note', 'number_of_portions', 'recipe_estimated_cost', 'origin_country', 'recipe_category', 'pic']

class RecipeIngredientsForm(forms.ModelForm):

    unit_of_measurement = forms.ChoiceField(choices=unit_measure_choices, required=False, widget=forms.Select(attrs={'id': 'id_unit_of_measurement_update'}))

    class Meta:
        model = RecipeIngredients
        fields = ['ingredient_name', 'quantity', 'unit_of_measurement', 'possible_substitute', 'substitue_special_note']

RecipeIngredientsFormSet = inlineformset_factory(Recipe, RecipeIngredients, form=RecipeIngredientsForm, extra=1, can_delete=True)

class RecipeAllergensForm(forms.ModelForm):
    class Meta:
        model = RecipeAllergens
        fields = ['allergen']

RecipeAllergensFormSet = inlineformset_factory(Recipe, RecipeAllergens, form=RecipeAllergensForm, extra=1, can_delete=True)

class RecipeCookingInstructionsForm(forms.ModelForm):
    class Meta:
        model = RecipeCookingInstructions
        fields = ['step_name', 'step_instruction']

RecipeCookingInstructionsFormSet = inlineformset_factory(Recipe, RecipeCookingInstructions, form=RecipeCookingInstructionsForm, extra=1, can_delete=True)