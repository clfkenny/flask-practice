result = document.querySelector('div strong');

function changeColor(result) {
    var color = "green";

    if (result.innerText == "negative") {
        color = "Red";
    } 

    result.style.color = color;
}

changeColor(result);