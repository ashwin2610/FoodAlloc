/* Open when someone clicks on the span element */
function openNav() {
	document.getElementById("cont").style.zIndex="-1";
    document.getElementById("myNav").style.height = "100%";
    
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
	
	document.getElementById("myNav").style.height = "0%";
	
	setTimeout(function() {
	document.getElementById("cont").style.zIndex="1";
	}, 200);
    
}


