$(document).ready(function () {
    resetSearchbar();
    autocomplete(2);
});

function resetSearchbar() {
    let searchBar = $("#search-bar-error");
    let searchInput = $(".search-input-error");

    if (searchInput.length === 0) {
        searchInput = $(".search-input-warning");
    }

    if (searchBar.length === 0) {
        searchBar = $("#search-bar-warning");
    }

    if (searchInput.length === 0) {
        searchInput = $(".search-input");
    }

    if (searchBar.length === 0) {
        searchBar = $("#search-bar");
    }

    // Reset the search bar when clicked.
    searchInput.click(function () {
        searchBar[0].id = "search-bar";
        searchInput[0].className = "search-input";
        searchInput[0].placeholder = "";
    });

    // Rewrite placeholder when the input is deselected.
    searchInput.on('blur', function () {
        searchInput[0].placeholder = "Search you favorite game...";
    });
}

function autocomplete(minimumCharacters) {

    let searchInput = $(".search-input");
    let formContainer = $("#form-container");
    let linksContainer = $("#links");

    let names = [];

    // Populate the names array with the contents of the JSON.
    $.getJSON("static/data/game_names.json", function (data) {
        $.each(data, function (key, value) {
            names.push(value.toString());
        })
    });

    searchInput.on("change keyup paste focus", function () {
        // Clear list each time the user changes the input.
        $(".prediction").remove();

        if (searchInput.val().length >= minimumCharacters) {
            let matches = getMatches(searchInput.val(), names, 5);

            // Hide and show the links container if there are matches.
            if (matches.length > 0) {
                linksContainer.css('visibility', 'hidden')
            } else {
                linksContainer.css('visibility', 'visible')
            }

            $.each(matches, function (index, value) {
                // Create a new prediction element.
                // TODO: Make the new element using JQuery.
                let prediction = document.createElement("DIV");
                prediction.setAttribute("class", "prediction");
                prediction.innerText = value;

                // Add a click listener to the new element.
                $(prediction).click(function () {
                    // Update the input text.
                    searchInput.val($(this)[0].innerText);

                    // Update the prediction list again.
                    searchInput.focus();
                });

                formContainer.append(prediction);
            });
        }

        if (searchInput.val() === "") {
            linksContainer.css('visibility', 'visible')
        }
    });
}


function getMatches(inputName, names, number) {
    // For performance reasons, lower case the input one time.
    let nameToMatch = inputName.toLowerCase();

    let matches = [];
    let counter = 0;

    // Iterate over names until number five of elements contain the name to match.
    $.each(names, function (index, value) {
        if (value.toLowerCase().includes(nameToMatch)) {
            matches.push(value);
            counter++;
        }

        // Exit the foreach loop.
        if (counter === number) {
            return false;
        }
    });

    // Check if there is only one match and is exactly the one inputted.
    if (matches.length === 1 && matches[0].toLowerCase() === nameToMatch) {
        return [];
    }

    return matches;
}