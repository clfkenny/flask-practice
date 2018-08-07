result = document.querySelector('div strong');

function changeColor(result) {
    var color = "green";

    if (result.innerText == "negative") {
        color = "Red";
    } 

    result.style.color = color;
}

changeColor(result);

function showPred(){
	var pred = document.querySelector("div.pred_hide");
	var input = document.querySelector("div.input_text");
	if(input.innerText !=""){
		pred.style.display = "block";
	}
	else{
		pred.style.display = "none";
	}
}

function hidePred(){
	var pred = document.querySelector("div.pred_hide");
	var input = document.querySelector("div.input_text");
	if(input.innerText == ""){
		pred.style.display = "none";
	}
}

hidePred()

function clearInput(){
	var text_box = document.querySelector('#text_review');
	text_box.value = "";
}