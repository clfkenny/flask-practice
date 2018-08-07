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