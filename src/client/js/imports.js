(function() {
	$ = jQuery = require('jquery');
	require('fullCalendar');
	require('./library/bootstrap.min.js');
})();

$(document).ready(function(){
    setSideBarConcordia();  
    $('#calendar').fullCalendar({
        // put your options and callbacks here
    })
});

function setSideBarConcordia(){
    $sidebar = $('.sidebar');
    image_src = $sidebar.data('image');
    if(image_src !== undefined){
        sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
        $sidebar.append(sidebar_container);
    }  
}
