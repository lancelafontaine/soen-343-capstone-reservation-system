(function() {
	$ = jQuery = require('jquery');
	require('fullCalendar');
	require('./library/bootstrap.min.js');
})();

$(document).ready(function(){
    setSideBarConcordia();  
<<<<<<< HEAD
    $('#calendar').fullCalendar({
        // put your options and callbacks here
    })
=======

   $('input').blur(function() {
    var $this = $(this);
    if ($this.val())
      $this.addClass('used');
    else
      $this.removeClass('used');
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
>>>>>>> master
});

function setSideBarConcordia(){
    $sidebar = $('.sidebar');
    image_src = $sidebar.data('image');
    if(image_src !== undefined){
        sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
        $sidebar.append(sidebar_container);
    }  
}
<<<<<<< HEAD
=======



>>>>>>> master
