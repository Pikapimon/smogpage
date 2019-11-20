
function fun1(){
	$("#piweritem").hover(function(){
		$("#subtitles1").slideDown("fast");
		// $(".subtitle1").show();
		$("#piwer").css("background-color","rgb(128,128,128)");
	},function(){
	 	$("#subtitles1").slideUp("fast");
		 // $(".subtitle1").hide();
		setTimeout("restoreColor('piwer')",200);
		 })
	$("#introductionitem").hover(function(){
		$("#subtitles2").slideDown("fast");
		$("#introduction").css("background-color","rgb(128,128,128)");
	},function(){
		$("#subtitles2").slideUp("fast");
		setTimeout("restoreColor('introduction')",100);
	})

	$("#purchaseitem").hover(function(){
		$("#subtitles3").slideDown("fast");
		$("#purchase").css("background-color","rgb(128,128,128)");
	},function(){
		$("#subtitles3").slideUp("fast");
		setTimeout("restoreColor('purchase')",220);
	})

	$("#cooperation").hover(function(){
		$("#subtitles4").slideDown("fast");
		$("#cooperation").css("background-color","rgb(128,128,128)");
	},function(){
		$("#subtitles4").slideUp("fast");
		setTimeout("restoreColor('cooperation')",150);
	})

};


function restoreColor(a){
	console.log(a)
	$('#'+a).css('background-color','rgb(49,49,49)');
}


function fun2(){
	$("#theBotton").mouseenter(function(){
		$(this).hide();
	});
}