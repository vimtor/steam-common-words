$(document).ready(function () {
    resetSearchbar();
});

function resetSearchbar() {
    console.log("reset");
    let searchBar = $("#search-bar-error");
    let searchInput = $(".search-input-error");

    searchInput.click(function () {
        searchBar[0].id = "search-bar";
        searchInput[0].className = "search-input";
        searchInput[0].placeholder = "Search you favorite game...";
    });
}