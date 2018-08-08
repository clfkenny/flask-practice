result = document.querySelector('div strong');


$( "#text_review" ).keyup(function() {
  getPred();
});

function clearInput(){
	var text_box = document.querySelector('#text_review');
	text_box.value = "";
	myChart.data.datasets[0].data = [0.5, 0.5];
	myChart.update();
}



var happy= document.getElementById('happy');
var mad= document.getElementById('mad');
var neutral= document.getElementById('neutral');



function showHappy() {
    happy.style.visibility = 'visible';
    mad.style.visibility = 'hidden';
    neutral.style.visibility = 'hidden';
}

function showMad() {
    happy.style.visibility = 'hidden';
    mad.style.visibility = 'visible';
    neutral.style.visibility = 'hidden';
}

function showNeutral() {
    happy.style.visibility = 'hidden';
    mad.style.visibility = 'hidden';
    neutral.style.visibility = 'visible';
}


window.onload = showNeutral();