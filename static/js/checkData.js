$(function(){
	$('#logindata').click(function(){
		
		$.ajax({
			url: '/checkUser',
			data: $('form').serialize(),
			dataType: 'json',
			type: 'POST',
			success: function(data){
				window.location.href = data.redirect
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
