/* ------------------------------------------------
# ALL SCRIPTS HERE IT WILL EXTENDS TO ALL THE PAGES
------------------------------------------------- */

// 1) Character remaining counter
$(document).ready(function() {
	var start = 0;
	var limit = 1000;

	$("#message").keyup(function() {
		start = this.value.length
		if (start > limit) {
			return false;
		}
		else if (start == 1000){
			$('#remaining').html('Characters remaining: ' + (limit - start)).css('color', 'red');
			swal('Opsss !', 'Characters limit exceeded !', 'info');
		}
		else if (start > 984){
			$('#remaining').html('Characters remaining: ' + (limit - start)).css('color', 'red');
		}
		else if (start < 1000){
			$('#remaining').html('Characters remaining: ' + (limit - start)).css('color', 'black');
		}
		else{
			$('#remaining').html('Characters remaining: ' + (limit)).css('color', 'black');
		}
	})
});

// 2) Input mask (PHONE)
$(document).ready(function() {
	$('.phone').inputmask('(999) 999-9999', {'onincomplete': function(){
		swal("Opsss !", "Incomplete phone. Please review !", 'info');
		$(".phone").val("");
		return false;
	}});
});

// 3) Function to get the the Time running at realtime
setInterval(function(){
	var date = new Date();
	$('#clock, #mini-clock').html(
		(date.getHours() < 10 ? '0' : '') + date.getHours() + ":" + (date.getMinutes() < 10 ? "0" : '') + date.getMinutes() + ":" + (date.getSeconds() < 10 ? "0" : '') + date.getSeconds()
	);
}, 500);

// 4) Script to update the page always at (00:00)
function autoRefresh(hours, minutes, seconds){
	var now = new Date(), then = new Date();
	then.setHours(hours, minutes, seconds, 0);
	if (then.getTime() < now.getTime()){
		then.setDate(now.getDate() + 1);
	}
	var timeout = (then.getTime() - now.getTime());
	setTimeout(function(){
		window.location.reload(true);
	}, timeout);
}
autoRefresh(0,0,0)

// 5) Script If no messages, hide all content
$(document).ready(function(){
	var verify = $('#chk_td').length;
	if (verify == 0) {
		$('.hide').css('display', 'none');
		$('#msg').text('No Message found');
		$('#refresh').html('<i class="fas fa-sync-alt fa-3x">')
	}
});

// 6) Script to make email lowercase only
$(document).ready(function(){
	$('#email').keyup(function(){
		this.value = this.value.toLowerCase();
	});
});

// 7) Script to advice the user about auto logout at 5 min (after 25 min you don't do anything)
setTimeout(function(){
	var notice = document.querySelector('#warning');
	if (notice) {
		notice.click();
	}
}, 25 * 60000); // 25 minutes

// 8) Script to auto logout (after 5 min passed) 
setTimeout(function(){
	var action = document.querySelector('#info');
	if (action) {
		action.click();
	}
}, 30 * 60000); // 30 minutes

// 9) Script (Name field) only latter is allowed
$(document).ready(function(){
	// in order to type only letters inside the name field
	jQuery('input[name="name"]').keyup(function(){
		var letter = jQuery(this).val();
		var allow = allow = letter.replace(/[^a-zA-Z _]/g, '');
		jQuery(this).val(allow);
	});
	// Prevent starting with space for every field
	$("input").on("keypress", function(e){
		if (e.which === 32 && ! this.value.length)
		e.preventDefault();
	});
});

// 10) Script to make the first letter always capitalized
$("#name").keyup(function(){
	var txt = $(this).val();
	$(this).val(txt.replace(/^(.)|\s(.)/g, function($1){
		return $1.toUpperCase();
	}));
});

// 9) Allow to put only First and Surname
$(document).ready(function() {
	$('#name').keyup(function() {
		var name = $('#name').val();
		if (name.split(' ').length == 3) {
			swal('Opss !', 'First and Last name only.', 'info');
			$('#name').val('');
			return false;
		}
	});
});

// 10) Function to pulse the text in the login page
(function pulse(){
	$('.text-pulse').fadeOut(1000).fadeIn(1000, pulse);
})();

// 11) <!-- Function to hide/show password -->
function myFunction() {
	var p = document.getElementById("password");
	if (p.type === "password") {
		p.type = "text";
	}else{
		p.type = "password";
	}
}

// 12) Function to close offcanvas when the button is clicked
jQuery("#offcanvasRight, .offcanvas-body a").click(function(){
	console.log($(this).attr('href'));
	jQuery('.offcanvas').offcanvas('hide');
});

// 13) Script to accept only until 2mb upload file
var upload = document.getElementById('file');
upload.onchange = function() {
	if (this.files[0].size > 2 * 1048576){
		swal('Attention !', 'Maximum allowed size is 2 mb.', 'info');
		this.vulue = "";
	};
};

// 14) Ajax backend Spinner
jQuery(function($) {
	$(document).ajaxSend(function() {
		$('#bg-spinner').fadeIn(500);
	});

	$('.send-email').click(function() {
		$.ajax({
		type: 'GET',
		success:function (data) {
			var d = $.parseJSON(data);
			alert(d.Test);
		}
		}).done(function() {
		setTimeout(function() {
			$('#bg-spinner').fadeOut(500);
		}, 700);
		});
	});
});
// Close modal (after 'send button is clicked')
$(".send-email").click(function(){
	var msg = $('#email-msg').val();
	var subject = $('#email-subject').val();

	if ((msg != '') && (subject != '')) {
		$('.close-modal').modal('hide');
	}
});