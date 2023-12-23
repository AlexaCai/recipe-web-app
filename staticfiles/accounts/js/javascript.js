// When the document is fully loaded, it calls the handleFormsets function for three different formsets
document.addEventListener('DOMContentLoaded', function () {
    handleFormsets('ingredients-formset-container', 'add-ingredient-form', 'remove-ingredient-form', 'ingredients_formset');
    handleFormsets('allergens-formset-container', 'add-allergen-form', 'remove-allergen-form', 'allergen_formset');
    handleFormsets('cooking-instructions-formset-container', 'add-cooking-instruction-form', 'remove-cooking-instruction-form', 'cooking_instructions_formset');
});

// handleFormsets function takes four arguments: the IDs of the formset container, the add button, etc... 
// It gets these elements from the DOM and sets up event listeners for the add and remove buttons.
function handleFormsets(containerId, addBtnId, removeBtnId, formsetClass) {
    var formsetContainer = document.getElementById(containerId);
    var addFormButton = document.getElementById(addBtnId);
    var removeFormButton = document.getElementById(removeBtnId);

        // Hide the remove button if there's only one formset (default when modal open)
        var formsets = formsetContainer.getElementsByClassName(formsetClass);
        if (formsets.length <= 1) {
            removeFormButton.style.display = 'none';
        }

        // Adds a new formset to the formset container when the add button is clicked, 
        // and updates the formset management form to reflect the new total forms count. 
        // also makes the remove button visible.
    addFormButton.addEventListener('click', function () {
        var formsets = formsetContainer.getElementsByClassName(formsetClass);
        var lastFormset = formsets[formsets.length - 1];
        var newFormset = lastFormset.cloneNode(true);

        // Clear the values of the inputs in the new formset
        var inputs = newFormset.querySelectorAll('input[type="text"], input[type="number"]');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].value = '';
        }

        // Clear the value of the textarea in the new formset
        var textarea = newFormset.querySelector('textarea');
        if (textarea) {
            textarea.value = '';
        }

        var formsetContainerCount = formsets.length;
        updateFormInputNames(newFormset, formsetContainerCount);

        formsetContainer.appendChild(newFormset);

        updateFormsetManagementForm(formsetContainer, formsetContainerCount + 1);

        // Show the remove button when a new formset is added
        removeFormButton.style.display = 'block';
    });

    // Removes the last formset from the formset container when the remove button is clicked, 
    // updates the names of the input fields in the remaining formsets, updates the formset management 
    // form to reflect the new total forms count, and hides the remove button if there's only one 
    // formset left.
    removeFormButton.addEventListener('click', function () {
        var formsets = Array.from(formsetContainer.getElementsByClassName(formsetClass));
        if (formsets.length > 1) {
            var lastFormset = formsets[formsets.length - 1];
            formsetContainer.removeChild(lastFormset);
    
            for (var i = 0; i < formsets.length - 1; i++) {
                updateFormInputNames(formsets[i], i);
            }
    
            updateFormsetManagementForm(formsetContainer, formsets.length - 1);
    
            // Get the updated list of formsets
            formsets = Array.from(formsetContainer.getElementsByClassName(formsetClass));
    
            // Hide the remove button if there's only one formset left
            if (formsets.length <= 1) {
                removeFormButton.style.display = 'none';
            }
        }
    });
}

// Selects all elements in the form that have a name attribute, and for each input, it replaces
// the index in the name with the new index. This is done using a regular expression that matches 
// -<number>- and replaces it with -<newIndex>-
function updateFormInputNames(form, formIndex) {
    var inputs = form.querySelectorAll('[name]');
    inputs.forEach(function (input) {
        var name = input.getAttribute('name').replace(/-\d+-/g, '-' + formIndex + '-');
        input.setAttribute('name', name);
    });
}

// Used to let the code know how many forms there are / are submitted
function updateFormsetManagementForm(formsetContainer, formCount) {
    var totalFormsInput = formsetContainer.querySelector('input[name$="TOTAL_FORMS"]');
    
    if (totalFormsInput) {
        totalFormsInput.value = formCount;
    }
}



// Function for the 'show more' and 'reduce' buttons on the created recipes section of 
// profile page
document.addEventListener("DOMContentLoaded", function () {
    // Initialize visible card count
    var visibleCardCount = 6;

    function showMoreCards() {
        // Initialize hidden cards
        var hiddenCards = document.querySelectorAll('.created-recipe-card-hidden');
        for (var i = 0; i < hiddenCards.length && i < 6; i++) {
            hiddenCards[i].classList.remove('created-recipe-card-hidden');
            visibleCardCount++;
        }

        // Hide the "Show More" button if the number of cards shown is not 6
        if (i < 6) {
            document.getElementById('showMoreButtonCreatedRecipe').style.display = 'none';
            document.getElementById('hideExtraCardButtonCreatedRecipe').style.display = 'block';
        }
    }

    function hideExtraCards() {
        var cards = document.querySelectorAll('.created-recipe-card');
        for (var i = 7; i < cards.length; i++) {
            cards[i].classList.add('created-recipe-card-hidden');
        }

        visibleCardCount = 6;

        document.getElementById('hideExtraCardButtonCreatedRecipe').style.display = 'none';
        document.getElementById('showMoreButtonCreatedRecipe').style.display = 'block';
    }

    document.getElementById('showMoreButtonCreatedRecipe').addEventListener('click', showMoreCards);
    document.getElementById('hideExtraCardButtonCreatedRecipe').addEventListener('click', hideExtraCards);

        // Hide the "Show More" button if the number of cards is less than or equal to 6
        var cards = document.querySelectorAll('.created-recipe-card');
        if (cards.length <= 7) {
            document.getElementById('showMoreButtonCreatedRecipe').style.display = 'none';
        }
});



// Function for the 'show more' and 'reduce' buttons on the favorite recipes section of 
// profile page
document.addEventListener("DOMContentLoaded", function () {

    var visibleCardCount = 6;

    function showMoreCards() {
        var hiddenCards = document.querySelectorAll('.favorite-recipe-card-hidden');
        for (var i = 0; i < hiddenCards.length && i < 6; i++) {
            hiddenCards[i].classList.remove('favorite-recipe-card-hidden');
            visibleCardCount++;
        }

        if (i < 6) {
            document.getElementById('showMoreButtonFavoriteRecipe').style.display = 'none';
            document.getElementById('hideExtraCardButtonFavoriteRecipe').style.display = 'block';
        }
    }

    function hideExtraCards() {
        var cards = document.querySelectorAll('.favorite-recipe-card');
        for (var i = 7; i < cards.length; i++) {
            cards[i].classList.add('favorite-recipe-card-hidden');
        }

        visibleCardCount = 6;

        document.getElementById('hideExtraCardButtonFavoriteRecipe').style.display = 'none';
        document.getElementById('showMoreButtonFavoriteRecipe').style.display = 'block';
    }

    document.getElementById('showMoreButtonFavoriteRecipe').addEventListener('click', showMoreCards);
    document.getElementById('hideExtraCardButtonFavoriteRecipe').addEventListener('click', hideExtraCards);

    var cards = document.querySelectorAll('.favorite-recipe-card');
    if (cards.length <= 7) {
        document.getElementById('showMoreButtonFavoriteRecipe').style.display = 'none';
    }
});



// Function to bring back smoothly users to the top of a section when clicking on a link or
// button
function scrollToSection(event, targetSectionId) {
    event.preventDefault();
    var targetSection = document.querySelector(targetSectionId);
    var offset = targetSection.getBoundingClientRect().top + window.scrollY;
    window.scrollTo({
        top: offset,
        behavior: 'smooth'
    });
}

    var backToTopLink1 = document.querySelector('.back-to-top a');
    var backToCreatedRecipes = document.querySelector('#hideExtraCardButtonCreatedRecipe');
    var backToFavoriteRecipes = document.querySelector('#hideExtraCardButtonFavoriteRecipe');

    backToTopLink1.addEventListener('click', function (event) {
        scrollToSection(event, '#topsection');
    });

    backToCreatedRecipes.addEventListener('click', function (event) {
        scrollToSection(event, '#createdRecipes');
    });

    backToFavoriteRecipes.addEventListener('click', function (event) {
        scrollToSection(event, '#favoriteRecipes');
    });
