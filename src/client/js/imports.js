(function() {

/*
Dependencies
*/

$ = jQuery = require('jquery');
require('fullcalendar');
require('moment');
require('./library/bootstrap.min.js');

/*
Init page 
*/

$(document).ready(function(){
  //get all rooms available from back-end
  getRoomList();
  //set sidebar backgoround
  setSideBarConcordia();
  //set login page animation
  loginPageAnimation();
  //refresh user data
  getUserInfo();
  //get user reservation
  getReservationList();
  // binding login event on to login button
  $("#login-button").click(function(){
    authenticateUser();
  });
  // binding login event on to login button
  $("#logout-button").click(function(){
    logoutUser();
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
    events: [], //mock bookings, we need more investigation on events implementation
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
				true);
			}
		}
  });
});

/*
Free functions
*/

function setSideBarConcordia(){
  $sidebar = $('.sidebar');
  image_src = $sidebar.data('image');
  if(image_src !== undefined){
    sidebar_container = '<div class="sidebar-background" style="background-image: url(' + image_src + ') "/>'
    $sidebar.append(sidebar_container);
  }
}

function loginPageAnimation(){
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
}

function authenticateUser(){
  // Retrieving username and password from login page
  var username = $("#username").val();
  var password = $("#password").val();
  // Logging on console for debugging purpose
  //console.log("Username: " + username);
  //console.log("Password: " + password);
  if( username.length == 0 || password.length == 0 ){
    $("#login-error-msg").html("<font color='red'><b> ERROR: One of the fields above is empty. </b></font>");
  } 
  var requestData = "username=" + username + "&password=" + password; 
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/login/',
    data: requestData,
    dataType: "json",
    xhrFields: {
      withCredentials: true
    },
    success: function(data, status){
      if(data.loggedIn == true){
        console.log(data);
        window.top.location = '/home.html';
      } else {
        var errorMsg = data.loginError;
        $("#login-error-msg").html("<font color='red'><b> ERROR: " + errorMsg + "</b></font>");
      }
    }
  });
}

function logoutUser(){
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/logout/',
    data: '',
    xhrFields: {
      withCredentials: true
    },
    success: function(data){
      window.top.location = '/';
    }
  });
}

function getRoomList() {
	$.ajax({
    url: 'http://localhost:8000/getRooms/',
    cache: false,
    success: function(res){
      for (var i=0; i < res.rooms.length; i++) {
        $("#room-list").append("<li><a><p>" + res.rooms[i] + "</p></a></li>");
      }
    }
  });
}

function getUserInfo() {
	$.ajax({
    url: 'http://localhost:8000/getSessionInfo',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      console.log(res);
      if (res.username) {
        console.log(res.username);
      }
    }
  });
}

function getReservationList() {
  $.ajax({
    url: 'http://localhost:8000/getReservedList',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      console.log(res);
      var booking = res.reservedList;
      appendBookingList(booking, "reservation-list");
    }
  });
}

function updateBooking() {
  //TODO: implementatuon
}

function createBooking() {
  //TODO: implementatuon
}

function deleteBooking() {
  //TODO: implementatuon
}

/*
Helpers
*/

function appendBookingList(booking, listType) {
	for (var i = 0; i < booking.length; i++) {
    $("#"+listType).append("<tr><td>" + booking[i]
      + "</td><td class='td-actions text-right'><button type='button' rel='tooltip' title='Remove' class='btn'>"
      + "<i class='fa fa-times'></i></button></td></tr>"
    );
  }
}

})();

//////////////////////////////////
// EXAMPLE AJAX CALLS TO SERVER //
//////////////////////////////////

/*
window.alert('Check the console for example AJAX requests to all backend API endpoints.');
$.ajax({
  url: 'http://localhost:8000/getReservations/?roomNumber=H-905&startTimeslot=2016-10-27%2014:54:20',
  cache: false,
  success: function(res){
    console.log(res);
  }
}); */

/*
$.ajax({
  url: 'http://localhost:8000/getRooms/',
  cache: false,
  success: function(res){
    console.log(res);
  }
}); */

/*$.ajax({
  url: 'http://localhost:8000/getReservedList',
  cache: false,
  xhrFields: {
    withCredentials: true
  },
  success: function(res){
    console.log(res);
  }
});*/