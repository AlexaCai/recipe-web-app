from django import forms
from recipes.models import Recipe, RecipeIngredients, RecipeAllergens, RecipeCookingInstructions, RecipeToolsNeeded, RecipeSimilarComplementary
from django.forms import inlineformset_factory

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

class UserSubmitRecipe(forms.ModelForm):
    recipe_name = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)
    special_note = forms.CharField(widget=forms.Textarea, required=False)
    cooking_time = forms.IntegerField(required=True)
    number_of_portions = forms.IntegerField(required=True)
    recipe_estimated_cost = forms.DecimalField(required=True, max_digits=5, decimal_places=2)
    origin_country = forms.ChoiceField(choices=country_choices, required=True, widget=forms.Select(attrs={'id': 'id_origin_country_update'}))
    recipe_category = forms.ChoiceField(choices=category_choices, required=True, widget=forms.Select(attrs={'id': 'id_recipe_category_update'}))
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

class RecipeToolsForm(forms.ModelForm):
    class Meta:
        model = RecipeToolsNeeded
        fields = ['cooking_tool_name']

RecipeToolsFormSet = inlineformset_factory(Recipe, RecipeToolsNeeded, form=RecipeToolsForm, extra=1, can_delete=True)

class RecipeSimilarComplementaryForm(forms.ModelForm):
    class Meta:
        model = RecipeSimilarComplementary
        fields = ['complementary_recipe_name', 'complementary_recipe_link_unsigned_users']

RecipeSimilarComplementaryFormSet = inlineformset_factory(Recipe, RecipeSimilarComplementary, form=RecipeSimilarComplementaryForm, extra=1, can_delete=True)