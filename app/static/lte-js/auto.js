function refresh()
{
	setTimeout( function() {
	  $('#auto').load('index');
	  refresh();
	}, 2000000);
}