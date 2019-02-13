$(document).ready(function () {
    resetSearchbar();
    autocomplete(2);
});

function resetSearchbar() {
    let searchBar = $(".search-bar");
    let searchInput = $(".search-input");

    // Reset the search bar when clicked.
    searchInput.click(function () {
        searchBar.removeAttr("id");

        $(this).removeClass("search-input-error");
        $(this).removeClass("search-input-warning");
        $(this).attr("placeholder", "");
    });

    // Rewrite placeholder when the input is deselected.
    searchInput.on('blur', function () {
        $(this).attr("placeholder", "Search you favorite game...");
    });
}

function autocomplete(minimumCharacters) {
    // Find required elements.
    let searchInput = $(".search-input");
    let searchBar = $(".search-bar");
    let predictions = $("#predictions");
    let linksContainer = $("#links");

    // Populate the names array with the contents of the JSON.
    let names = [];
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
            linksContainer.css('visibility', matches.length > 0 ? 'hidden' : 'visible');

            $.each(matches, function (index, value) {
                // Create a new prediction element.
                let prediction = $("<div></div>").attr("class", "prediction").text(value);

                // Add a click listener to the new element.
                $(prediction).click(function () {
                    // Update the input text and focus.
                    searchInput.val($(this).text());
                    searchBar.submit();
                });

                predictions.append(prediction);
            });
        }

        // If the input field is empty, make the links visible again.
        if (searchInput.val() === "") {
            linksContainer.css('visibility', 'visible')
        }
    });
}


function getMatches(inputName, names, max) {
    // For performance reasons, lower case the input one time.
    let nameToMatch = inputName.toLowerCase();

    // Iterate over names until number five of elements contain the name to match.
    let matches = names.filter(name => name.toLowerCase().includes(nameToMatch));

    return matches.slice(0, max);
}