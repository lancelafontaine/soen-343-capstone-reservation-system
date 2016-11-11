(function() {
	$ = jQuery = require('jquery');
	require('fullCalendar');
	require('moment');
	require('./library/bootstrap.min.js');
})();

$(document).ready(function(){

	//set sidebar backgoround
    setSideBarConcordia(); 
    //these codes need to be organized 
    $('input').blur(function() {
    	var $this = $(this);
    	if ($this.val()) $this.addClass('used');
    	else $this.removeClass('used');
  	});
  	var $ripples = $('.ripples');
  	$ripples.on('click.Ripples', function(e) {
    	var $this = $(this);
    	var $offset = $this.parent().offset();
    	var $circle = $this.find('.ripplesCircle');	
    	var x = e.pageX - $offset.left;
    	var y = e.pageY - $offset.top;
    	$circle.css({
      		top: y + 'px',
      		left: x + 'px'
    	});
    	$this.addClass('is-active');
  	});	
  	$ripples.on('animationend webkitAnimationEnd mozAnimationEnd oanimationend MSAnimationEnd', function(e) {
  		$(this).removeClass('is-active');
  	});

  	//calendar code
  	var date = new Date();
  	var currentDay = date.getDate();
  	var currentMo = date.getMonth();
  	var currentYr = date.getYear();
  	$('#calendar').fullCalendar({
        header: {
        	left: "prev, next today",
        	center: "title",
        	right: "month, agendaWeek, agendaDay"
        },
        defaultViews: "basicWeek",
        selectable: true,
        selectHelper: true
    });

});

function setSideBarConcordia(){
    $sidebar = $('.sidebar');
    image_src = $sidebar.data('image');
    if(image_src !== undefined){
        sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
        $sidebar.append(sidebar_container);
    }  
}