const FADE_DURATIONS = [3000, 5000, 7000];
const OPACITIES = [0.2, 0.6, 1];

$(document).ready(function () {
    showWords();
});


function showWords() {
    let words = $(".word");

    words.each(function (index, element) {
        fadeElement(element);
    })
}

function fadeElement(element) {
    let duration = randomElementInArray(FADE_DURATIONS); // Get random fading duration.
    let opacity = OPACITIES[element.getAttribute("popularity")]; // Get opacity by popularity attribute.

    $(element).fadeTo(duration, opacity);
}

function generateRandomNumber(min, max) {
    let random_number = Math.random() * (max - min) + min;
    return Math.floor(random_number);
}

function randomElementInArray(array) {
    return array[generateRandomNumber(0, array.length)];
}