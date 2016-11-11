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
        	right: "agendaWeek, agendaDay"
        },
        defaultView: "agendaWeek",
        selectable: true,
		selectHelper: true,
        allDaySlot: false,
        minTime: "08:00:00",
        maxTime: "23:00:00",
        slotEventOverlap: false,
        eventColor: "#FF4A55",
        editable: true,
        events: [], //mock bookings
        //select code: start time, end time
        select: function(start, end) {
			var title = prompt('Event Title:');
			if (title) {
				calendar.fullCalendar('renderEvent',
				{
					title: title,
					start: start,
					end: end
				},
				true // make the event "stick"
				);
			}
		}
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

/*
AJAX function
*/

function updateBooking() {
	//TODO: implementatuon
}

function createBooking() {
	//TODO: implementatuon
}

function deleteBooking() {
	//TODO: implementatuon
}

function getRoomList() {
	//TODO: implementatuon
	//This is to get a list of room
}

/*
Helpers
*/

function showRoom() {
	//TODO: implementation
	//This is to append room to sidebar 
}

function getUserInfo() {
	//TODO: implementation
	//This is to get the waiting list and reservation list
}

function appendToList() {
	//TODO: implementation
	//This is a helper to append an item to a list
}



