(function()
{
	var canvas = document.querySelector( "#canvas" );
	var canvasPred = document.getElementById("canvas_preds");
	var context = canvas.getContext( "2d" );
	var contextPred = canvasPred.getContext( "2d" );

	canvas.width = 1500;
	canvas.height = 1500;

	var Mouse = { x: 0, y: 0 };
	var lastMouse = { x: 0, y: 0 };


	context.color = "black";
	context.lineWidth = 15;
	context.fillStyle="white";
	context.fillRect(0,0,canvas.width,canvas.height);



	contextPred.color = "black";
	contextPred.lineWidth = 15;
	contextPred.fillStyle="white";
	contextPred.fillRect(0,0,canvas.width,canvas.height);




    context.lineJoin = context.lineCap = 'round';
    contextPred.lineJoin = context.lineCap = 'round';
	
	debug();

	canvas.addEventListener( "mousemove", function( e )
	{
		lastMouse.x = Mouse.x;
		lastMouse.y = Mouse.y;

		Mouse.x = e.pageX - this.offsetLeft;
		Mouse.y = e.pageY - this.offsetTop;

	}, false );

	canvas.addEventListener( "mousedown", function( e )
	{
		canvas.addEventListener( "mousemove", onPaint, false );

	}, false );

	canvas.addEventListener( "mouseup", function()
	{
		canvas.removeEventListener( "mousemove", onPaint, false );
	}, false );






	var onPaint = function()
	{	
		context.lineWidth = context.lineWidth;
		context.lineJoin = "round";
		context.lineCap = "round";
		context.strokeStyle = context.color;
	
		context.beginPath();
		context.moveTo( lastMouse.x, lastMouse.y );
		context.lineTo( Mouse.x, Mouse.y );
		context.closePath();
		context.stroke();


		contextPred.lineWidth = context.lineWidth;
		contextPred.lineJoin = "round";
		contextPred.lineCap = "round";
		contextPred.strokeStyle = context.color;
	
		contextPred.beginPath();
		contextPred.moveTo( lastMouse.x, lastMouse.y );
		contextPred.lineTo( Mouse.x, Mouse.y );
		contextPred.closePath();
		contextPred.stroke();
	};



	function debug()
	{
		/* CLEAR BUTTON */
		var clearButton = $( "#clearButton" );
		
		clearButton.on( "click", function()
		{
			
				context.clearRect( 0, 0, 1500, 1500 );
				context.fillStyle="white";
				context.fillRect(0,0,canvas.width,canvas.height);

				contextPred.clearRect( 0, 0, 1500, 1500 );
				contextPred.fillStyle="white";
				contextPred.fillRect(0,0,canvas.width,canvas.height);

			
		});

		/* COLOR SELECTOR */

		$( "#colors" ).change(function()
		{
			var color = $( "#colors" ).val();
			context.color = color;
		});
		
		/* LINE WIDTH */
		
		$( "#lineWidth" ).change(function()
		{
			context.lineWidth = $( this ).val();
		});
	}
}());