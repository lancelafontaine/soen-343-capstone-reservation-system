(function() {

/*
Dependencies
*/

$ = jQuery = require('jquery');
require('fullcalendar');
moment = require('moment');
require('./library/bootstrap.min.js');

/*
Init page
*/
var currentRoom;
var session;
var waitingList;
var reservedList;

$(document).ready(function(){
  getUserSessionInfo();
  //display latest user info
  displayUserInfo();
  //set sidebar backgoround
  setSideBarConcordia();
  //set login page animation
  loginPageAnimation();
  // binding login event on to login button
  $("#login-button").click(function(){
    authenticateUser();
  });
  // binding login event on to login button
  $("#logout-button").click(function(){
    logoutUser();
  });
  // binding event to user's reservations
  $("#reservation-list").click(function(event) {
    cancelReservation();
  });
  //select room
  $("#room-list").on('click','li',function (){
    if (currentRoom != $(this).attr('id')) {
      $(currentRoom).removeClass("active");
      currentRoom = "#" + $(this).attr('id');
      $(this).addClass("active");
      showBookingByRoom();
    }
  });
  //calendar code
  $('#calendar').fullCalendar({
    header: {
      left: "",
      center: "title",
      right: ""
    },
    firstDay: 1,
    contentHeight: "auto",
    defaultView: "agendaWeek",
    defaultTimedEventDuration: "01:00:00",
    //TODO: disable previous date in calendar view
    selectable: true,
    allDaySlot: false,
    minTime: "08:00:00",
    maxTime: "21:00:00",
    slotDuration: "01:00:00",
    slotEventOverlap: false,
    eventColor: "#FF4A55",
    editable: true,  
    droppable: true,
    events: [],
    select: function(start, end, jsEvent, view){
      var room = $(currentRoom).text();
      var startDate = moment(start).format("YYYY-MM-DD HH:mm:ss");
      makeReservation(room, startDate);
    },
    eventClick: function(calEvent, jsEvent, view) {
      eventUsername = calEvent.title
      if (eventUsername == session.username){
        window.alert("Already registered for timeslot.")
      } else {
        var room = $(currentRoom).text();
        var startDate = moment(calEvent.start).format("YYYY-MM-DD HH:mm:ss");
        makeReservation(room, startDate);
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
        //console.log(data);
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
    method: 'GET',
    url: 'http://localhost:8000/getRooms/',
    cache: false,
    success: function(res){
      for (var i=0; i < res.rooms.length; i++) {
        $("#room-list").append("<li id='room-"+i+"'><a><p>" + res.rooms[i] + "</p></a></li>");
        if (!currentRoom){
          currentRoom = "#room-" + i;
          $("#room-"+i).addClass("active");
          showBookingByRoom();
        } 
      }
    }
  });
}

function showBookingByRoom() {
  $('#calendar').fullCalendar('removeEvents');
  var currentRoomReservation = [];
  var beginOfWeek = $('#calendar').fullCalendar('getDate').startOf('week').format().split("T");
  console.log(beginOfWeek);
  $.ajax({
    method: 'GET',
    url: "http://localhost:8000/getReservations/?roomNumber=" 
    + $(currentRoom).text() 
    + "&startTimeslot=" 
    + beginOfWeek[0] 
    + "%20" 
    + beginOfWeek[1],
    cache: false,
    success: function(res){
      console.log(res);
      for (var i=0; i < res.reservations.length; i++) {
        var reservation = res.reservations[i][1].split(" ");
        var user = res.reservations[i][0];
        var date = reservation[0].split("-");
        var year = date[0];
        var month = date[1];
        var day = date[2];
        var time = reservation[1].split(":");
        var hours = time[0];
        var minutes = time[1];
        var seconds = time[2];
        var eventStart = new Date(year, month-1, day, hours, minutes, seconds);

        var backgroundColor = '#663399';

        for (var j=0; j < waitingList.length; j++){
          if (res.reservations[i][1] == waitingList[j][2]) {
        console.log(waitingList)
            var backgroundColor = '#f982e8';
          }
        }

        var slot = {
          title: user,
          start: eventStart,
          backgroundColor: backgroundColor
        };
      $('#calendar').fullCalendar("renderEvent", slot, true);
      }
    }
  });
}

function getUserSessionInfo() {
  $.ajax({
    method: 'GET',
    url: 'http://localhost:8000/getSessionInfo',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      session = res;
    }
  });
}

function displayUserInfo() {
  getReservationList();
  getWaitingList();
}

function clearUserInfo() {
  $("#reservation-list").remove("*");
  $("#waiting-list").remove("*");
}

function getReservationList() {
  $.ajax({
    url: 'http://localhost:8000/getReservedList',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      //console.log(res);
      reservedList = res.reservedList;
      appendBookingList(reservedList, "reservation-list");
    }
  });
}

function getWaitingList() {
  $.ajax({
    url: 'http://localhost:8000/getWaitingList',
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      waitingList = res.waitingList;
      console.log(waitingList)
      appendBookingList(waitingList, "waiting-list");

      //get all rooms available from back-end
      getRoomList();
    }
  });
}

function makeReservation(room, timeslot){
  //building the request
  var requestData = "roomNumber=" + room + "&" + "timeslot=" + timeslot;
  //ajax call
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/makeReservation/',
    data: requestData,
    dataType: "json",
    xhrFields: {
      withCredentials: true
    },
    success: function(data, status){
      if( data.madeReservation == false ){
        var reservationErrorMsg = data.reservationError;
        $("#reservation-error-msg").html("<font color='red'><b>ERROR: " + reservationErrorMsg + " </b></font>");
      } else {
        console.log(data);
        location.reload();
      }
    }
  });
}

function cancelReservation() {
  //Select the current reservation list
  var selectCurrent = $( event.target ).closest( "tr" ).text();
  var roomNumber = selectCurrent.substring(0,5);
  var timeslot = selectCurrent.substring(6,selectCurrent.length);
  var requestData = "roomNumber=" + roomNumber + "&timeslot=" + timeslot;
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/cancelReservation/',
    data: requestData,
    dataType : "json",
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
     // console.log(res);
    }
  });
  location.reload();
}

//This function will modify the reservation
function modifyReservation(oldRoomNumber,newRoomNumber,oldTimeslot,newTimeslot) {
  var requestData = "oldRoomNumber=" 
  + oldRoomNumber 
  + "&newRoomNumber=" 
  + newRoomNumber  
  + "&oldTimeslot=" 
  + oldTimeslot 
  + "&newTimeslot=" 
  + newTimeslot;
  $.ajax({
    method: 'POST',
    url: 'http://localhost:8000/modifyReservation/',
    data: requestData,
    dataType : "json",
    cache: false,
    xhrFields: {
      withCredentials: true
    },
    success: function(res){
      console.log(res);
    }
  });
  location.reload();
}

/*
Helpers
*/

function appendBookingList(booking, listType) {
	for (var i = 0; i < booking.length; i++) {
    $("#"+listType).append("<tr id='" + listType + "-" + i + "'><td>" + booking[i][1] + "@" + booking[i][2]
      + "</td><td class='td-actions text-right'><button type='button' rel='tooltip' title='Modify' class='btn modify-reserved'><i class='fa fa-pencil'></i></button>"
      + "<button type='button' rel='tooltip' title='Cancel' class='btn cancel-reserved'>"
      + "<i class='fa fa-times'></i></button></td></tr>"
    );
  }
}

})();

