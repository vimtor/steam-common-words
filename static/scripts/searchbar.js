$(document).ready(function () {
    resetSearchbar();
});

function resetSearchbar() {
    // TODO: Research a more efficient way of doing this.
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

    console.log(searchInput);

    searchInput.click(function () {
        searchBar[0].id = "search-bar";
        searchInput[0].className = "search-input";
        searchInput[0].placeholder = "";
    });

    searchInput.on('blur', function () {
        searchInput[0].placeholder = "Search you favorite game...";
    });
}