(function() {
	$ = jQuery = require('jquery');
	require('./library/bootstrap.min.js');
})();

$(document).ready(function(){
    setSideBarConcordia();  
});

function setSideBarConcordia(){
    $sidebar = $('.sidebar');
    image_src = $sidebar.data('image');
    if(image_src !== undefined){
        sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
        $sidebar.append(sidebar_container);
    }  
}

